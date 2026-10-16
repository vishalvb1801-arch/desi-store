#!/usr/bin/env python3
"""C300-W: build edit-plan.json, captions/overlays (.ass) and render C300-W-final.mp4.

Run from outputs/C300-W/edit:  python3 handoff/build_c300w.py [plan|render|all]
"""
import json, os, subprocess, sys

FPS = 30
SRC = 5.0417                      # every clip is 5.0417 s
AUDIO_END = 229.0417              # B.mp3 duration
XF = 0.4                          # the one crossfade (into clip_36)

# (start, end, clip, fit[, opts])   fit: trim | slow | freeze(first N s then hold)
SHOTS = [
    (0.00, 5.76, 1, "slow"),     (5.76, 11.00, 2, "slow"),
    (11.00, 15.70, 3, "trim"),   (15.70, 20.30, 4, "trim"),
    (20.30, 23.00, 5, "trim"),   (23.00, 26.80, 6, "trim"),
    (26.80, 30.45, 7, "trim"),   (30.45, 33.50, 8, "trim"),
    (33.50, 36.90, 9, "trim"),   (36.90, 40.10, 10, "trim"),
    (40.10, 43.45, 11, "trim"),  (43.45, 48.00, 12, "trim"),
    (48.00, 51.70, 13, "trim"),  (51.70, 55.20, 14, "trim"),
    (55.20, 59.60, 15, "trim"),  (59.60, 61.40, 16, "trim"),
    (61.40, 64.85, 17, "trim"),
    (64.85, 68.65, 18, "trim"),  (68.65, 72.46, 19, "trim"),
    (72.46, 75.40, 20, "trim"),  (75.40, 78.60, 21, "trim"),
    (78.60, 82.04, 22, "trim"),  (82.04, 85.84, 23, "trim"),
    (85.84, 88.54, 24, "trim"),  (88.54, 91.00, 25, "trim"),
    (91.00, 94.20, 26, "trim"),  (94.20, 96.70, 27, "trim"),
    (96.70, 98.90, 28, "trim"),  (98.90, 100.85, 29, "trim"),
    (100.85, 102.00, 30, "trim"),  (102.00, 107.05, 31, "slow"),
    (107.05, 113.75, 32, "slow"),  (113.75, 120.22, 33, "slow"),
    (120.22, 123.67, 34, "trim"),  (123.67, 128.50, 35, "slow"),
    (128.50, 132.30, 36, "trim"),  (132.30, 137.10, 37, "trim"),
    (137.10, 142.62, 56, "slow"),  (142.62, 147.78, 40, "slow"),
    (147.78, 151.96, 41, "slow"),  (151.96, 155.45, 42, "trim"),
    (155.45, 158.60, 43, "freeze", 1.2),
    (158.60, 161.86, 44, "trim"),  (161.86, 166.50, 45, "trim"),
    (166.50, 169.27, 46, "trim"),  (169.27, 177.10, 47, "slow"),
    (177.10, 181.20, 48, "trim"),  (181.20, 185.33, 49, "slow"),
    (185.33, 188.63, 50, "trim"),  (188.63, 191.82, 51, "trim"),
    (191.82, 197.90, 52, "slow"),  (197.90, 201.62, 53, "trim"),
    (201.62, 208.43, 54, "slow"),  (208.43, 211.82, 51, "trim"),
    (211.82, 215.28, 49, "trim"),  (215.28, 222.03, 55, "slow"),
    (222.03, AUDIO_END, 56, "slow"),
]
XFADE_INTO = 36   # clip whose shot gets the crossfade in

# Sung phrases (start = word onset) — captions follow B.mp3 as sung
PHRASES = [
    (5.76, "I kept this close, so close to my *heart*"),
    (20.30, "Every evening I come home *smiling*"),
    (23.00, "And I set my face like *nothing's wrong*"),
    (26.80, "You ask me, how was your day, *ji*?"),
    (30.45, "And I say *fine*, though I know it's not"),
    (33.50, "There is a *room* inside my chest"),
    (36.90, "Where I keep the words I *never said*"),
    (40.10, "I wanted *peace*, I wanted time"),
    (43.45, "I thought the *truth* could wait a while"),
    (48.00, "But the *silence* has a way tonight"),
    (51.70, "And it follows me from *room to room*"),
    (55.20, "I stand at the *edge* of my own reply"),
    (59.60, "*Afraid* of what comes into view"),
    (64.85, "I'm just *tired*, ji"),
    (68.65, "Tired of holding what I *can't undo*"),
    (72.46, "I'm just *tired*, ji"),
    (75.40, "Tired of *pretending* I can choose"),
    (78.60, "As you hear my voice *shake* a little"),
    (82.04, "It's because I'm *finally* letting through"),
    (85.84, "I'm just *tired*, ji"),
    (88.54, "And I need you to *see me true*"),
    (100.85, "You found a *letter* on the table"),
    (103.83, "And the *colour* left your face"),
    (107.05, "I saw the *hurt* before the question"),
    (110.50, "It was standing in the *space*"),
    (113.75, "I meant to *tell you* in the morning"),
    (117.10, "But my *courage* failed again"),
    (120.22, "Now the *truth* is in the light"),
    (123.67, "And I cannot *hide* from it, my friend"),
    (132.30, "I never meant to break your *trust*"),
    (137.10, "I never meant to *turn away*"),
    (140.35, "But carrying this *alone*"),
    (142.62, "has worn my *voice* away"),
    (147.78, "I'm just *tired*, ji"),
    (151.96, "Tired of living *half a life*"),
    (155.45, "I'm just *tired*, ji"),
    (158.60, "Tired of cutting truth to *size*"),
    (161.86, "If my eyes look like they are *begging*"),
    (165.40, "It's because I don't know how to *lie*"),
    (169.27, "I'm just *tired*, ji"),
    (172.00, "Please *hear me* before we say goodbye"),
    (181.20, "Maybe *love* can hold the fracture"),
    (185.33, "Maybe *truth* can let us stay"),
    (188.63, "If we walk through this *together*"),
    (191.82, "We may find a *kinder* way"),
    (197.90, "I'm just *tired*, ji"),
    (201.62, "But I am still here by *your side*"),
    (205.80, "I'm just *tired*, ji"),
    (208.43, "And I wanna *make this right*"),
    (211.82, "If you can *hold my hand* for one more moment"),
    (215.28, "We can learn to *breathe* again tonight"),
    (219.22, "I'm just *tired*, ji"),
    (222.03, "Stay with me now, let us *begin again*"),
]
HOOK_END = 7.0
SING_END = 226.6   # last sung word ends ~226.3

# Text overlays (absolute times): id, start, end, text, ass-style, x, y(px)
OVERLAYS = [
    ("hook1", 0.0, HOOK_END, "SHE WAS HIDING\\NSOMETHING", "Hook", 540, 300),
    ("product1", 137.30, 142.62, "EIS AYURVEDIC\\NPAIN RELIEF OIL", "Title", 540, 215),
    ("product2", 137.80, 142.62, "15+ Ayurvedic herbs", "Gold", 540, 1625),
    ("mech1", 142.80, 151.96, "Tablets mask it.\\NSprays sit on the skin.", "Title", 540, 230),
    ("massage1", 152.10, 158.60, "10 minutes of warm\\Nmassage before bed", "Title", 540, 230),
    ("cta1", 222.20, AUDIO_END, "50% OFF TODAY", "Offer", 540, 335),
    ("cta2", 222.40, AUDIO_END, "CASH ON DELIVERY · 30-day guarantee", "Sub", 540, 1640),
]
LOGO = ("logo", 222.20, AUDIO_END, 190, 52)   # id, start, end, size px, top y px


def words():
    return json.load(open("handoff/transcript.json"))["words"]


def wrap(text, limit=22):
    """Two lines at the space nearest the middle (only when > limit chars)."""
    plain = text.replace("*", "")
    if len(plain) <= limit:
        return text
    best = None
    inhl = False
    for i, ch in enumerate(text):
        if ch == "*":
            inhl = not inhl
        if ch == " " and not inhl:
            left = text[:i].replace("*", "")
            d = abs(len(left) - len(plain) / 2)
            if best is None or d < best[0]:
                best = (d, i)
    i = best[1]
    return text[:i] + "\n" + text[i + 1:]


def caption_items():
    ws = words()
    items = []
    for k, (st, text) in enumerate(PHRASES):
        nxt = PHRASES[k + 1][0] if k + 1 < len(PHRASES) else SING_END + 0.6
        nwords = len(text.replace("*", "").split())
        inside = [w for w in ws if st - 0.4 <= w["start"] < nxt - 0.05][:nwords]
        if inside:
            last = inside[-1]
            end = min(nxt, max(last["start"] + 1.0, min(last["end"], last["start"] + 1.6) + 0.4))
        else:
            end = min(nxt, st + 2.5)
        if k + 1 == len(PHRASES):
            end = min(SING_END + 0.6, AUDIO_END)
        start = max(st, HOOK_END)
        if end - start < 1.2:
            end = min(nxt, start + 1.2)
        items.append([round(start, 2), round(end, 2), wrap(text)])
    return items


def frame(t):
    return int(round(t * FPS))


def build_plan():
    segs = []
    # seg01 = hook: shots 1+2
    spans = [(p[0], c[1], p[1].replace("*", "")) for p, c in zip(PHRASES, caption_items())]

    def seg_line(s, e):
        hit = [t for a, b, t in spans if a < e - 0.05 and b > s + 0.3]
        return " / ".join(hit) or ("(intro)" if s < 1 else "(instrumental)")
    groups = [[0, 1]] + [[i] for i in range(2, len(SHOTS))]
    seg_of_shot = {}
    for gi, g in enumerate(groups):
        s, e = SHOTS[g[0]][0], SHOTS[g[-1]][1]
        sid = f"seg{gi + 1:02d}"
        shots = []
        for i in g:
            st, en, clip, fit = SHOTS[i][:4]
            sh = {"clip": f"clip_{clip}", "fit": "trim" if fit == "freeze" else fit}
            if len(g) > 1:
                sh["duration"] = round(en - st, 2)
            shots.append(sh)
            seg_of_shot[i] = sid
        tr = {"type": "crossfade", "durationSec": XF} if SHOTS[g[0]][2] == XFADE_INTO else {"type": "cut"}
        role = "hook" if gi == 0 else ("cta" if gi == len(groups) - 1 else "body")
        segs.append({"id": sid, "role": role, "line": seg_line(s, e),
                     "vo": {"file": "vo.mp3", "in": round(s, 2), "out": round(e, 2)},
                     "shots": shots, "transitionIn": tr})

    def locate(t, end=False):
        for sg in segs:
            if sg["vo"]["in"] - 1e-6 <= t < sg["vo"]["out"] - 1e-6 or (end and abs(t - sg["vo"]["out"]) < 1e-6):
                return sg
        return segs[-1]

    cap_items = []
    for st, en, text in caption_items():
        # split a caption across segment boundaries so times stay segment-relative
        t = st
        while t < en - 1e-6:
            sg = locate(t)
            s0, s1 = sg["vo"]["in"], sg["vo"]["out"]
            e = min(en, s1)
            cap_items.append({"segment": sg["id"], "start": round(t - s0, 2), "end": round(e - s0, 2), "text": text})
            t = e
    ovs = []
    for oid, st, en, text, style, x, y in OVERLAYS:
        pstyle = {"Hook": "headline", "Title": "headline", "Gold": "sub", "Offer": "price", "Sub": "sub"}[style]
        t, part = st, 0
        en = min(en, segs[-1]["vo"]["out"])
        while t < en - 1e-6:   # split an overlay across segment cuts (ids get a/b suffixes)
            sg = locate(t)
            s0, s1 = sg["vo"]["in"], sg["vo"]["out"]
            e = min(en, s1)
            ovs.append({"id": oid if part == 0 else f"{oid}{chr(97 + part)}", "type": "text", "segment": sg["id"],
                        "start": round(t - s0, 2), "end": round(e - s0, 2), "text": text.replace("\\N", "\n"),
                        "style": pstyle, "x": 0.5, "y": round(y / 1920, 2)})
            t, part = e, part + 1
    sg = segs[-1]
    ovs.append({"id": "logo", "type": "image", "file": "logo.png", "segment": sg["id"],
                "start": round(LOGO[1] - sg["vo"]["in"], 2), "end": round(sg["vo"]["out"] - sg["vo"]["in"], 2),
                "x": 0.5, "y": 0.08, "scale": 0.18})
    plan = {
        "project": "C300-W", "brand": "EIS", "version": 1,
        "output": {"width": 1080, "height": 1920, "fps": 30, "crf": 20, "loudnessLUFS": -14},
        "segments": segs,
        "captions": {"enabled": True, "style": {
            "font": "Poppins-Bold", "fallbackFont": "NotoSansDevanagari-Bold", "size": 58,
            "color": "#FFF4E0", "strokeColor": "#770A08", "strokeWidth": 14, "y": 0.72,
            "maxCharsPerLine": 44, "highlightColor": "#D4A23A"}, "items": cap_items},
        "overlays": ovs,
        "music": {"file": "music.mp3", "gainDb": -18, "duckUnderVO": True, "fadeInSec": 0.5, "fadeOutSec": 1.0, "enabled": False},
        "sfx": [],
        "variations": [{"name": "V1", "layers": {"music": False, "overlays": "all"}}],
    }
    json.dump(plan, open("edit-plan.json", "w"), indent=1, ensure_ascii=False)
    return plan


def ass_time(t):
    cs = int(round(t * 100))
    return f"{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}"


def build_ass(path):
    gold = r"{\c&H3AA2D4&}"
    cream = r"{\c&HE0F4FF&}"
    hdr = r"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Poppins,58,&H00E0F4FF,&H00E0F4FF,&H00080A77,&H00080A77,-1,0,0,0,100,100,0,0,3,14,0,5,40,40,0,1
Style: Hook,Poppins,82,&H00E0F4FF,&H00E0F4FF,&H00080A77,&H00080A77,-1,0,0,0,100,100,1,0,3,18,0,5,40,40,0,1
Style: Title,Poppins,62,&H00E0F4FF,&H00E0F4FF,&H00080A77,&H00080A77,-1,0,0,0,100,100,0,0,3,16,0,5,40,40,0,1
Style: Gold,Poppins,56,&H003AA2D4,&H003AA2D4,&H00080A77,&H00080A77,-1,0,0,0,100,100,0,0,3,14,0,5,40,40,0,1
Style: Offer,Poppins,80,&H003AA2D4,&H003AA2D4,&H00080A77,&H00080A77,-1,0,0,0,100,100,1,0,3,18,0,5,40,40,0,1
Style: Sub,Poppins,46,&H00E0F4FF,&H00E0F4FF,&H00080A77,&H00080A77,-1,0,0,0,100,100,0,0,3,14,0,5,30,30,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = []
    for st, en, text in caption_items():
        t = text.replace("\n", r"\N")
        out, on = "", False
        for ch in t:
            if ch == "*":
                out += cream if on else gold
                on = not on
            else:
                out += ch
        lines.append(f"Dialogue: 0,{ass_time(st)},{ass_time(en)},Cap,,0,0,0,,{{\\pos(540,1382)}}{out}")
    for oid, st, en, text, style, x, y in OVERLAYS:
        fade = r"\fad(200,0)" if en >= AUDIO_END - 0.01 else r"\fad(200,150)"
        lines.append(f"Dialogue: 1,{ass_time(st)},{ass_time(en)},{style},,0,0,0,,{{\\pos({x},{y}){fade}}}{text}")
    open(path, "w").write(hdr + "\n".join(lines) + "\n")


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-3000:])
        raise SystemExit(f"failed: {' '.join(cmd[:6])}")


def render(work):
    os.makedirs(work, exist_ok=True)
    vf_tail = ("scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,"
               "crop=1080:1920,setsar=1,tpad=stop_mode=clone:stop_duration=12")
    files_a, files_b = [], []
    xf_idx = next(i for i, s in enumerate(SHOTS) if s[2] == XFADE_INTO)
    for i, sh in enumerate(SHOTS):
        st, en, clip, fit = sh[:4]
        n = frame(en) - frame(st)
        if i == xf_idx - 1:
            n += frame(XF)          # tail that the crossfade eats
        dur = (frame(en) - frame(st)) / FPS
        if fit == "slow":
            f = dur / SRC
            assert 0.8 - 1e-3 <= f <= 1.6 + 1e-3, (clip, f)
            pre = f"setpts={f:.6f}*(PTS-STARTPTS),fps={FPS}"
        elif fit == "freeze":
            pre = f"trim=end={sh[4]},setpts=PTS-STARTPTS,fps={FPS}"
        else:
            assert dur <= SRC + 1e-6 or clip == 0, (clip, dur)
            pre = f"setpts=PTS-STARTPTS,fps={FPS}"
        out = f"{work}/s{i:02d}.mp4"
        (files_a if i < xf_idx else files_b).append(out)
        if os.path.exists(out):          # shot cache: delete a file to re-render it
            continue
        run(["ffmpeg", "-v", "error", "-y", "-i", f"clips/clip_{clip}.mp4", "-an",
             "-vf", f"{pre},{vf_tail},trim=end_frame={n},setpts=PTS-STARTPTS",
             "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-pix_fmt", "yuv420p", "-r", str(FPS), out])
    for name, fl in (("a", files_a), ("b", files_b)):
        open(f"{work}/{name}.txt", "w").write("".join(f"file '{os.path.abspath(f)}'\n" for f in fl))
        run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{work}/{name}.txt", "-c", "copy", f"{work}/{name}.mp4"])
    len_a = (frame(SHOTS[xf_idx][0]) + frame(XF)) / FPS
    build_ass(f"{work}/c300w.ass")
    lid, ls, le, lsize, ly = LOGO
    fc = (f"[0:v][1:v]xfade=transition=fade:duration={XF}:offset={len_a - XF:.4f},setpts=PTS-STARTPTS[v0];"
          f"[v0]ass={work}/c300w.ass:fontsdir=media/fonts[v1];"
          f"[2:v]scale={lsize}:-1,format=rgba,fade=t=in:st=0:d=0.2:alpha=1,setpts=PTS+{ls}/TB[lg];"
          f"[v1][lg]overlay=x=(W-w)/2:y={ly}:enable='gte(t,{ls})':eof_action=repeat[v]")
    total = frame(AUDIO_END)
    run(["ffmpeg", "-v", "error", "-y", "-i", f"{work}/a.mp4", "-i", f"{work}/b.mp4",
         "-loop", "1", "-t", str(AUDIO_END - ls + 0.5), "-i", "media/logo.png", "-i", "media/vo.mp3",
         "-filter_complex", fc, "-map", "[v]", "-map", "3:a", "-frames:v", str(total),
         "-c:v", "libx264", "-crf", "20", "-preset", "slow", "-pix_fmt", "yuv420p", "-r", str(FPS),
         "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "renders/C300-W-final.mp4"])


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    os.makedirs("renders", exist_ok=True)
    if mode in ("plan", "all"):
        build_plan()
        build_ass("handoff/c300w.ass")
    if mode in ("render", "all"):
        render(sys.argv[2] if len(sys.argv) > 2 else "/tmp/c300w_work")
