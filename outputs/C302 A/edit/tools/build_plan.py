#!/usr/bin/env python3
"""Build edit-plan.json for C302 A from handoff/transcript.json + tools/chunks.txt + the shot table below.

Run from edit/:  python3 tools/build_plan.py [--durations]
"""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from align import toks

PRE, POST, SKIP, LAST_POST = 0.25, 0.35, 0.8, 0.5
MIN_CAP = 0.85

# re-aligned first words (isolated-window whisper + vocal-band energy); see delivery.md
START_FIX = {(2, 0): 14.30, (5, 0): 33.00, (10, 0): 77.74, (41, 0): 234.46}
# words whisper misheard or placed in the wrong window: (line, word) -> (start, end)
WORD_SET = {(39, 0): (221.30, 222.04), (39, 1): (222.16, 222.84), (39, 2): (222.84, 223.82),
            (44, 4): (258.05, 258.42), (59, 13): (290.90, 291.60), (59, 14): (291.60, 291.66), (59, 15): (291.66, 292.06), (59, 16): (292.06, 292.30)}
END_FIX = {(38, 6): 220.05, (60, 8): 296.95}

# which lyric words each segment sings: (line, first_word_idx, last_word_idx_exclusive or None)
SEGMENTS = [(1, [(1, 0, None)])]
SEGMENTS += [(2, [(2, 0, None), (3, 0, 2)])]          # "And me?" closes seg02 (3.8 s instrumental before "I couldn't")
SEGMENTS += [(3, [(3, 2, None)])]
SEGMENTS += [(n, [(n, 0, None)]) for n in range(4, 39)]
SEGMENTS += [(39, [(39, 0, 3)])]                        # "in a warm til oil" is not sung
SEGMENTS += [(n, [(n, 0, None)]) for n in range(40, 43)]
SEGMENTS += [(43, [(43, 0, None), (44, 0, 4)])]         # "Not the old me." closes seg43 (2.9 s instrumental after it)
SEGMENTS += [(44, [(44, 4, None)])]
SEGMENTS += [(n, [(n, 0, None)]) for n in range(45, 49)]
SEGMENTS += [(49, [(49, 0, 3)])]                        # "she couldn't move" is not sung
SEGMENTS += [(59, [(59, 13, None)])]                    # only "that's a bonus, see," is sung
SEGMENTS += [(60, [(60, 0, None)])]

# caption chunks that differ from chunks.txt because the song sings less / regroups
CHUNK_FIX = {2: None, 3: ["I couldn't", "even *bend* to touch", "my nani's *feet*"],
             39: ["*Mahanarayan*", "*Nirgundi*", "*Ashwagandha*"], 49: ["Priya's face *changed*"],
             44: ["The me I was", "*supposed* to be"], 59: ["that's a *bonus*, see"]}
EXTRA_CHUNKS = {2: ["And *me*?"], 43: ["Not the *old* me"]}

ROLE = lambda n: "hook" if n <= 5 else ("cta" if n >= 56 else "body")
PRODUCT = {25, 26, 28, 31, 38, 39, 56, 58, 60}

# shots per segment: list of (clip, fit[, duration]); filled from the durations table
SHOTS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "shots.json"))) \
    if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "shots.json")) else {}


def plain_len(c):
    return len(c.replace("*", ""))


def merge_text(a, b):
    if "*" in a and "*" in b:
        b = b.replace("*", "")
    return a + " " + b


def fit_chunks(cs, ideal, dur):
    """Merge neighbouring chunks (<=22 chars) only while the segment can't give every chunk MIN_CAP."""
    cs, ideal = list(cs), list(ideal)
    while len(cs) * MIN_CAP > dur + 1e-6:
        best = None
        for j in range(len(cs) - 1):
            if plain_len(cs[j]) + 1 + plain_len(cs[j + 1]) <= 22:
                span = (ideal[j + 2] if j + 2 < len(cs) else dur) - ideal[j]
                if best is None or span < best[0]:
                    best = (span, j)
        if best is None:
            break  # no legal merge left: keep the chunks, they share the time evenly
        j = best[1]
        cs[j:j + 2] = [merge_text(cs[j], cs[j + 1])]; ideal[j:j + 2] = [ideal[j]]
    return cs, ideal


def solve_starts(ideal, dur):
    """Chunk starts as close to the sung words as possible with every chunk >= MIN_CAP (first at 0.0)."""
    n = len(ideal)
    if n * MIN_CAP > dur:
        return [dur * j / n for j in range(n)]
    st = [0.0] + [max(0.0, x) for x in ideal[1:]]
    for j in range(1, n):
        st[j] = max(st[j], st[j - 1] + MIN_CAP)
    if dur - st[-1] < MIN_CAP:
        st[-1] = dur - MIN_CAP
    for j in range(n - 2, 0, -1):
        st[j] = min(st[j], st[j + 1] - MIN_CAP)
    return st


def words_by_line():
    T = json.load(open("handoff/transcript.json"))
    out = {}
    for r in T:
        ws = [dict(w) for w in r["words"]]
        for k, w in enumerate(ws):
            if (r["line"], k) in START_FIX:
                w["s"] = START_FIX[(r["line"], k)]
                if w["e"] is None or w["e"] <= w["s"]:
                    w["e"] = w["s"] + 0.3
            if (r["line"], k) in END_FIX:
                w["e"] = END_FIX[(r["line"], k)]
            if (r["line"], k) in WORD_SET:
                w["s"], w["e"] = WORD_SET[(r["line"], k)]
        out[r["line"]] = ws
    return out


def interpolate(ws):
    """Fill unmatched words evenly between their matched neighbours."""
    if all(w["s"] is None for w in ws):
        return ws  # line not sung at all
    k = 0
    while k < len(ws):
        if ws[k]["s"] is None:
            j = k
            while j < len(ws) and ws[j]["s"] is None:
                j += 1
            lo = ws[k - 1]["e"] if k > 0 else (ws[j]["s"] - 0.3 * (j - k))
            hi = ws[j]["s"] if j < len(ws) else lo + 0.3 * (j - k)
            step = (hi - lo) / (j - k)
            for i in range(k, j):
                ws[i]["s"], ws[i]["e"] = lo + step * (i - k), lo + step * (i - k + 1)
            k = j
        k += 1
    return ws


def main():
    lines = open("tools/lyrics.txt").read().strip().split("\n")
    chunks = [[c.strip() for c in l.split("|")] for l in open("tools/chunks.txt").read().strip().split("\n")]
    W = words_by_line()
    for n in W:
        W[n] = interpolate(W[n])
    segs = []
    for n, parts in SEGMENTS:
        ws = []
        for (ln, a, b) in parts:
            ws += W[ln][a:b]
        segs.append({"line_no": n, "words": ws})
    # boundaries
    for i, s in enumerate(segs):
        s0, e0 = s["words"][0]["s"], s["words"][-1]["e"]
        if i == 0:
            s["in"] = s0 - PRE
        if i + 1 < len(segs):
            nxt = segs[i + 1]["words"][0]["s"]
            if nxt - e0 > SKIP:
                s["out"] = e0 + POST; segs[i + 1]["in"] = nxt - PRE
            else:
                b = max((e0 + nxt) / 2, nxt - PRE); s["out"] = b; segs[i + 1]["in"] = b
        else:
            s["out"] = e0 + LAST_POST
    for s in segs:
        s["in"], s["out"] = round(s["in"], 2), round(s["out"], 2)
    if "--durations" in sys.argv:
        t = 0
        for i, s in enumerate(segs, 1):
            d = s["out"] - s["in"]
            print(f"seg{i:02d} line {s['line_no']:2d} {s['in']:7.2f}-{s['out']:7.2f} dur {d:5.2f} at {t:6.2f}  {lines[s['line_no'] - 1][:60]}")
            t += d
        print("total", round(t, 2))
        return
    # ---- captions ----
    items = []
    for i, s in enumerate(segs, 1):
        n = s["line_no"]; sid = f"seg{i:02d}"
        cs = CHUNK_FIX.get(n, chunks[n - 1]) if n in CHUNK_FIX else chunks[n - 1]
        if cs is None:
            cs = chunks[n - 1]
        cs = list(cs) + EXTRA_CHUNKS.get(n, [])
        # map chunk -> words by token count
        tk = [toks(c.replace("*", "")) for c in cs]
        flat = [w for w in s["words"]]
        assert sum(len(t) for t in tk) == len(flat), (n, cs, [w["w"] for w in flat])
        ideal, k = [], 0
        for t in tk:
            ideal.append(flat[k]["s"] - s["in"] - 0.1); k += len(t)
        dur = s["out"] - s["in"]
        cs, ideal = fit_chunks(cs, ideal, dur)
        starts = solve_starts(ideal, dur)
        ends = starts[1:] + [dur]
        for j, c in enumerate(cs):
            items.append({"segment": sid, "start": round(starts[j], 2), "end": round(ends[j], 2), "text": c})
    # ---- segments ----
    out_segs = []
    for i, s in enumerate(segs, 1):
        n = s["line_no"]; sid = f"seg{i:02d}"
        shots = [dict(zip(("clip", "fit", "duration"), sh)) for sh in SHOTS.get(str(n), [[f"clip_{n}", "hold" if n in PRODUCT else "slow"]])]
        text = lines[n - 1]
        if n == 2: text += " And me?"
        if n == 3: text = text.replace("And me? ", "")
        if n == 43: text += " Not the old me."
        if n == 44: text = "The me I was supposed to be."
        if n == 39: text = "Mahanarayan, Nirgundi, Ashwagandha,"
        if n == 49: text = "Priya's face changed,"
        if n == 59: text = "that's a bonus, see,"
        out_segs.append({"id": sid, "role": ROLE(n), "line": text, "vo": {"file": "vo.mp3", "in": s["in"], "out": s["out"]},
                         "shots": shots, "transitionIn": {"type": "cut"}})
    sid_of = {s["line_no"]: f"seg{i:02d}" for i, s in enumerate(segs, 1)}
    dur_of = {f"seg{i:02d}": round(s["out"] - s["in"], 2) for i, s in enumerate(segs, 1)}
    overlays = []
    for n in range(1, 6):
        sid = sid_of[n]
        overlays.append({"id": "hook1" if n == 1 else f"hook1_{sid}", "type": "text", "segment": sid, "start": 0.0,
                         "end": dur_of[sid], "text": "SHE CHOSE MY\n*BEST FRIEND*", "style": "headline", "x": 0.5, "y": 0.16})
    for n in (59, 60):
        sid = sid_of[n]
        overlays.append({"id": f"cta_{sid}", "type": "text", "segment": sid, "start": 0.0, "end": dur_of[sid],
                         "text": "50% OFF · CASH ON DELIVERY", "style": "cta", "x": 0.5, "y": 0.10})
        overlays.append({"id": f"price_{sid}", "type": "text", "segment": sid, "start": 0.0, "end": dur_of[sid],
                         "text": "₹999", "style": "price", "x": 0.5, "y": 0.80})
        overlays.append({"id": f"logo_{sid}", "type": "image", "file": "logo.png", "segment": sid, "start": 0.0,
                         "end": dur_of[sid], "x": 0.5, "y": 0.88, "scale": 0.18})
    plan = {
        "project": "C302 A", "brand": "EIS", "version": 1,
        "output": {"width": 1080, "height": 1920, "fps": 30, "crf": 18, "loudnessLUFS": -14},
        "segments": out_segs,
        "captions": {"enabled": True, "style": {
            "font": "Montserrat-Bold", "fallbackFont": "NotoSansDevanagari-Bold", "size": 60, "color": "#FFF8EE",
            "strokeColor": "#000000", "strokeWidth": 0, "y": 0.70, "maxCharsPerLine": 22, "highlightColor": "#E8B54A",
            "box": {"color": "#770A08", "opacity": 0.88, "radius": "pill", "padX": 28, "padY": 14, "shadow": True}},
            "items": items},
        "overlays": overlays,
        "music": {"file": "music.mp3", "gainDb": -18, "duckUnderVO": True, "fadeInSec": 0.5, "fadeOutSec": 1.0, "enabled": False},
        "sfx": [],
        "variations": [{"name": "V1", "layers": {"music": False, "overlays": "all"}}],
    }
    json.dump(plan, open("edit-plan.json", "w"), indent=2, ensure_ascii=False)
    print("wrote edit-plan.json:", len(out_segs), "segments,", len(items), "caption items")


if __name__ == "__main__":
    main()
