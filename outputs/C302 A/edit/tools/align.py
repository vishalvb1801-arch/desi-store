"""Align the lyric map (tools/lyrics.txt) to whisper word timestamps -> handoff/transcript.json."""
import json, re, sys, difflib
NUM = {"one":"1","two":"2","three":"3","four":"4","five":"5","six":"6","seven":"7","eight":"8","nine":"9","ten":"10",
       "eleven":"11","twelve":"12","fifteen":"15","twenty":"20","twenties":"20s","thirty":"30","fifty":"50",
       "thirtysix":"36","ninetynine":"99","am":"am"}
def toks(s):
    s = s.lower().replace("thirty-six", "thirtysix").replace("ninety-nine", "ninetynine").replace("a.m.", "am")
    s = s.replace("-", " ").replace("6am", "6 am").replace("’", "'")
    out = []
    for w in re.findall(r"[a-z0-9']+", s):
        w = w.strip("'")
        if not w: continue
        out.append(NUM.get(w, w))
    return out
def load_words(files):
    ws = []
    for f, lo, hi in files:
        for seg in json.load(open(f)):
            for w in seg["words"]:
                if lo <= w["s"] < hi:
                    for t in toks(w["w"]):
                        ws.append({"t": t, "s": w["s"], "e": w["e"], "raw": w["w"].strip()})
    return ws
def main(lyrics, out, files):
    lines = open(lyrics).read().strip().split("\n")
    lw = []  # (line, idx, token)
    for li, l in enumerate(lines, 1):
        for k, t in enumerate(toks(l)):
            lw.append([li, k, t, None, None])
    ww = load_words(files)
    sm = difflib.SequenceMatcher(a=[x[2] for x in lw], b=[w["t"] for w in ww], autojunk=False)
    for a, b, n in sm.get_matching_blocks():
        for k in range(n):
            lw[a + k][3], lw[a + k][4] = ww[b + k]["s"], ww[b + k]["e"]
    res = []
    for li, l in enumerate(lines, 1):
        items = [x for x in lw if x[0] == li]
        res.append({"line": li, "text": l, "words": [{"w": x[2], "s": x[3], "e": x[4]} for x in items]})
    json.dump(res, open(out, "w"), indent=1)
    for r in res:
        m = [w for w in r["words"] if w["s"] is not None]
        miss = [w["w"] for w in r["words"] if w["s"] is None]
        span = f"{m[0]['s']:7.2f}-{m[-1]['e']:7.2f}" if m else "   --   "
        print(f"{r['line']:2d} {span} matched {len(m)}/{len(r['words'])}  missing: {' '.join(miss)[:90]}")
if __name__ == "__main__":
    sp = sys.argv[3]
    main(sys.argv[1], sys.argv[2], [(f"{sp}/w_start.json", 0, 41.5), (f"{sp}/whisper_large.json", 41.5, 283.0), (f"{sp}/w_end.json", 283.0, 999)])
