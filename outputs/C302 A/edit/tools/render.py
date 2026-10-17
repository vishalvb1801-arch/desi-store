#!/usr/bin/env python3
"""Render edit-plan.json outside the app (ffmpeg + Pillow pill captions).

    python3 tools/render.py edit-plan.json [--variation V1] [--config tools/render-config.json]

Run from the project's edit/ folder. Output: ../renders/<project>-<variation>.mp4
- every shot is rendered at exactly its frame count on a 30 fps grid; short clips freeze their
  last frame (tpad clone), so there is never a black frame
- audio = the vo ranges of every segment joined (8 ms fades at song skips), loudnorm two-pass
- captions / text / logo are drawn with Pillow (rounded pills) and overlaid as an RGBA pipe
"""
import argparse, json, os, subprocess, sys, tempfile, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pills
from PIL import Image

FPS, W, H = 30, 1080, 1920
SCALE = f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},setsar=1"


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode:
        sys.exit(f"command failed: {' '.join(cmd)}\n{r.stderr[-3000:]}")
    return r


def probe_dur(path):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]).stdout)


def timeline(plan, clip_map):
    """Flatten segments into shots with absolute frame ranges."""
    shots, segs, t = [], {}, 0.0
    for s in plan["segments"]:
        d = round(s["vo"]["out"] - s["vo"]["in"], 3)
        segs[s["id"]] = {"start": t, "dur": d, "vo": s["vo"], "role": s["role"]}
        fixed = sum(sh.get("duration", 0) for sh in s["shots"])
        free = [sh for sh in s["shots"] if "duration" not in sh]
        share = (d - fixed) / len(free) if free else 0
        st = t
        for sh in s["shots"]:
            sd = sh.get("duration", share)
            f0, f1 = round(st * FPS), round((st + sd) * FPS)
            shots.append({"seg": s["id"], "clip": sh["clip"], "fit": sh["fit"], "f0": f0, "f1": f1,
                          "src": clip_map[sh["clip"]]["file"], "srcdur": float(clip_map[sh["clip"]]["duration"])})
            st += sd
        t += d
    total_frames = round(t * FPS)
    shots[-1]["f1"] = total_frames
    return shots, segs, t, total_frames


def render_shot(sh, out):
    n = sh["f1"] - sh["f0"]
    dur = n / FPS
    pre = ["-stream_loop", "-1"] if sh["fit"] == "loop" else []
    if sh["fit"] == "slow":
        vf = f"setpts=(PTS-STARTPTS)*{dur / sh['srcdur']:.6f},fps={FPS},{SCALE},tpad=stop_mode=clone:stop=-1"
    else:  # hold / trim / loop: normal speed, freeze the last frame if the shot outlasts the clip
        vf = f"setpts=PTS-STARTPTS,fps={FPS},{SCALE},tpad=stop_mode=clone:stop=-1"
    run(["ffmpeg", "-v", "error", "-y", *pre, "-i", sh["src"], "-an", "-vf", vf, "-frames:v", str(n),
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "10", "-pix_fmt", "yuv420p", "-r", str(FPS), out])


def build_audio(plan, segs, tmp, sfx):
    parts, labels, prev_out = [], [], None
    for i, s in enumerate(plan["segments"]):
        vin, vout = s["vo"]["in"], s["vo"]["out"]
        f = f"[0:a]atrim=start={vin}:end={vout},asetpts=PTS-STARTPTS"
        skip_in = prev_out is not None and abs(prev_out - vin) > 0.005
        nxt = plan["segments"][i + 1]["vo"]["in"] if i + 1 < len(plan["segments"]) else None
        skip_out = nxt is not None and abs(nxt - vout) > 0.005
        if skip_in:
            f += ",afade=t=in:d=0.008"
        if skip_out:
            f += f",afade=t=out:st={vout - vin - 0.008:.3f}:d=0.008"
        parts.append(f + f"[a{i}]"); labels.append(f"[a{i}]"); prev_out = vout
    total = sum(s["vo"]["out"] - s["vo"]["in"] for s in plan["segments"])
    fc = ";".join(parts) + ";" + "".join(labels) + f"concat=n={len(labels)}:v=0:a=1,afade=t=out:st={total - 0.3:.3f}:d=0.3[song]"
    inputs = ["-i", os.path.join("media", plan["segments"][0]["vo"]["file"])]
    if sfx:
        mix = ["[song]"]
        for k, x in enumerate(sfx):
            inputs += ["-i", os.path.join("media", x["file"])]
            ms = int(round((segs[x["segment"]]["start"] + x.get("at", 0)) * 1000))
            fc += f";[{k + 1}:a]volume={x.get('gainDb', -6)}dB,adelay={ms}|{ms}[s{k}]"; mix.append(f"[s{k}]")
        fc += f";{''.join(mix)}amix=inputs={len(mix)}:normalize=0:duration=first[mixed]"; out = "[mixed]"
    else:
        out = "[song]"
    raw = os.path.join(tmp, "song_raw.wav")
    run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", fc, "-map", out, "-ar", "48000", "-ac", "2", raw])
    lufs = plan["output"].get("loudnessLUFS", -14)
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", raw, "-af", f"loudnorm=I={lufs}:TP=-1:LRA=11:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True)
    m = json.loads(r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}") + 1])
    final = os.path.join(tmp, "song.wav")
    run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af",
         f"loudnorm=I={lufs}:TP=-1:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
         f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true",
         "-ar", "48000", "-ac", "2", final])
    return final


class Layers:
    """Pre-renders every caption/overlay and answers 'what is on screen at frame f'."""
    def __init__(self, plan, segs, shots, variation, cfg):
        self.items = []
        cap = plan["captions"]; st = cap["style"]; box = st.get("box", {})
        y_over = cfg.get("captionY", {})
        if cap.get("enabled", True):
            for it in cap["items"]:
                a = segs[it["segment"]]["start"] + it["start"]; b = segs[it["segment"]]["start"] + it["end"]
                f0, f1 = round(a * FPS), round(b * FPS)
                ys = [y_over[s["clip"]] for s in shots if s["f0"] < f1 and s["f1"] > f0 and s["clip"] in y_over]
                y = ys[0] if ys else st.get("y", 0.70)
                im = pills.pill(it["text"], size=st.get("size", 60), color=st.get("color", "#FFF8EE"),
                                hl=st.get("highlightColor", "#E8B54A"), box=box.get("color", "#770A08"),
                                opacity=box.get("opacity", 0.88), padx=box.get("padX", 28), pady=box.get("padY", 14),
                                shadow=box.get("shadow", True))
                self.items.append((f0, f1, im, y, 0.12, True, None))
        allowed = variation.get("layers", {}).get("overlays", "all")
        for o in plan["overlays"]:
            if allowed != "all" and o["id"] not in allowed:
                continue
            a = segs[o["segment"]]["start"] + o["start"]; b = segs[o["segment"]]["start"] + o["end"]
            if o["type"] == "text":
                text = variation.get("overlayText", {}).get(o["id"], o["text"])
                style = o.get("style", "headline")
                if style == "headline":
                    im = pills.headline(text.split("\n"), size=cfg.get("headlineSize", 84))
                elif style == "price":
                    im = pills.headline(text.split("\n"), size=cfg.get("priceSize", 112), color="#E8B54A")
                else:  # cta / sub: gold pill with crimson type
                    im = pills.pill(text, size=cfg.get("ctaSize", 50), color="#770A08", hl="#770A08",
                                    box="#E8B54A", opacity=0.95, weight="ExtraBold")
            elif o["type"] == "image":
                im = Image.open(os.path.join("media", o["file"])).convert("RGBA")
                w = int(W * o.get("scale", 0.18)); im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
            else:
                continue
            f0, f1 = round(a * FPS), round(b * FPS)
            key = (o["type"], o.get("text") if o["type"] == "text" else o.get("file"), o.get("y", 0.5))
            # the same overlay on back-to-back segments stays on screen as one item (no re-fade at the cut)
            prev = next((k for k, it in enumerate(self.items) if it[6:] == (key,) and it[1] == f0), None)
            if prev is not None:
                it = self.items[prev]; self.items[prev] = (it[0], f1) + it[2:]
            else:
                self.items.append((f0, f1, im, o.get("y", 0.5), 0.2, False, key))

    def frame(self, f):
        """Return a hashable description of the overlay state at frame f."""
        st = []
        for k, (f0, f1, im, y, ramp, pop, _) in enumerate(self.items):
            if f0 <= f < f1:
                p = min(1.0, (f - f0 + 1) / (ramp * FPS))
                st.append((k, round(p, 3)))
        return tuple(st)

    def draw(self, state):
        canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        for k, p in state:
            f0, f1, im, y, ramp, pop, _ = self.items[k]
            if p < 1:
                sc = 0.94 + 0.06 * p if pop else 1.0
                if sc != 1.0:
                    im = im.resize((max(1, round(im.width * sc)), max(1, round(im.height * sc))), Image.BILINEAR)
                im = im.copy(); im.putalpha(im.getchannel("A").point(lambda v: int(v * p)))
            canvas.alpha_composite(im, ((W - im.width) // 2, int(round(y * H - im.height / 2))))
        return canvas.tobytes()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plan"); ap.add_argument("--variation", default="V1")
    ap.add_argument("--config", default="tools/render-config.json"); ap.add_argument("--keep", action="store_true")
    ap.add_argument("--out"); ap.add_argument("--only", help="comma-separated segment ids (test renders)")
    a = ap.parse_args()
    plan = json.load(open(a.plan))
    cm = json.load(open("handoff/clip-map.json")); clip_map = {c["id"]: c for c in cm} if isinstance(cm, list) else cm
    cfg = json.load(open(a.config)) if os.path.exists(a.config) else {}
    var = next(v for v in plan["variations"] if v["name"] == a.variation)
    if a.only:
        keep = set(a.only.split(","))
        plan["segments"] = [s for s in plan["segments"] if s["id"] in keep]
        plan["captions"]["items"] = [i for i in plan["captions"]["items"] if i["segment"] in keep]
        plan["overlays"] = [o for o in plan["overlays"] if o["segment"] in keep]
    shots, segs, total, nframes = timeline(plan, clip_map)
    tmp = tempfile.mkdtemp(prefix="render-", dir=cfg.get("tmpDir"))
    print(f"{len(shots)} shots, {total:.2f}s, {nframes} frames; tmp {tmp}", flush=True)
    listf = os.path.join(tmp, "list.txt")
    with open(listf, "w") as L:
        for i, sh in enumerate(shots):
            out = os.path.join(tmp, f"shot{i:03d}.mp4"); render_shot(sh, out); L.write(f"file '{out}'\n")
    base = os.path.join(tmp, "base.mp4")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", listf, "-c", "copy", base])
    sfx = [x for x in plan.get("sfx", []) if os.path.exists(os.path.join("media", x["file"]))]
    audio = build_audio(plan, segs, tmp, sfx)
    print(f"audio {probe_dur(audio):.3f}s  video {nframes / FPS:.3f}s", flush=True)
    layers = Layers(plan, segs, shots, var, cfg)
    os.makedirs("../renders", exist_ok=True)
    out = a.out or f"../renders/{plan['project'].replace(' ', '-')}-{a.variation}.mp4"
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-i", base, "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-i", audio, "-filter_complex",
                            "[0:v][1:v]overlay=0:0:format=auto,format=yuv420p[v]", "-map", "[v]", "-map", "2:a",
                            "-c:v", "libx264", "-profile:v", "high", "-preset", "slow", "-crf", str(plan["output"].get("crf", 18)),
                            "-pix_fmt", "yuv420p", "-r", str(FPS), "-frames:v", str(nframes),
                            "-c:a", "aac", "-ar", "48000", "-b:a", "192k", "-movflags", "+faststart", out],
                           stdin=subprocess.PIPE)
    last, buf = None, None
    for f in range(nframes):
        s = layers.frame(f)
        if s != last:
            buf = layers.draw(s); last = s
        enc.stdin.write(buf)
        if f % 900 == 0:
            print(f"  frame {f}/{nframes}", flush=True)
    enc.stdin.close()
    if enc.wait():
        sys.exit("final encode failed")
    if not a.keep:
        shutil.rmtree(tmp)
    print("wrote", out)


if __name__ == "__main__":
    main()
