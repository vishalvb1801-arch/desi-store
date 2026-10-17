"""Split each lyric line into caption chunks (<=22 chars, phrase boundaries, one *highlight*)."""
import re, json, sys
MAX = 22
STOP = set("""a an the and or but so to of in on at for with my me i i'm it it's its is was were be he she her his him you your
that that's this just all no not up out into by from did do does can can't could couldn't what what's who who's how how'd
there there's then than our we they them still now right back every one some more any""".split())
PRIORITY = {"kunal":5,"priya":5,"eis":9,"pain":3,"oil":6,"herbs":5,"ayurvedic":6,"free":6,"diwali":4,"nani's":4,"tailor":4,
 "twenties":3,"emis":3,"best":2,"friend's":3,"school":3,"dms":3,"door":3,"fifty":4,"bike":3,"stairs":3,"physio":3,"balms":3,
 "painkillers":4,"stomach":3,"kurta":4,"straight":4,"tears":4,"bottle":5,"physiotherapist":4,"nuskhe":4,"fifteen":5,
 "nothing":3,"year":4,"rupee":5,"night":3,"working":4,"back":2,"stress":4,"inflamed":4,"skin":3,"slow":3,"sleeping":4,
 "mahanarayan":5,"nirgundi":5,"ashwagandha":5,"slept":4,"light":3,"scaring":4,"puja":4,"wall":4,"overs":4,"old":3,
 "supposed":4,"floor":4,"tall":4,"belt":4,"painkiller":4,"smooth":4,"move":4,"good":4,"eye":4,"anybody":4,"read":5,
 "mirror":5,"through":2,"here":5,"clear":5,"ninety-nine":8,"alone":5,"tonight":5,"percent":6,"delivery":7,"history":4,
 "bottle.":5,"bonus":5,"for":0,"me.":0,"settled":4,"believed":4,"space":4,"face":4,"sister":3,"months":2,"anymore":4,
 "fix":3,"locked":3,"gone":4,"them":0,"burned":4,"just":0,"fit":3,"stitched":3,"stops":3,"dropped":4,"off":4,"bed":4,
 "texted":3,"wrong":4,"start":4,"camera":3,"feet":4,"head":3,"wed":3,"role":3,"walks":2,"changed":4,"moving":4,"looking":3}
def clean(line):
    line = line.replace('"', '').replace('“', '').replace('”', '')
    return line.split()
def strip_end(s):
    return s.rstrip(',.;:')
def cost_split(words):
    n = len(words); INF = 1e9
    best = [INF] * (n + 1); prev = [0] * (n + 1); best[0] = 0
    for j in range(1, n + 1):
        for i in range(j - 1, -1, -1):
            txt = strip_end(' '.join(words[i:j]))
            if len(txt) > MAX: break
            c = 1.0
            last = words[j - 1]
            if j < n and not re.search(r'[,.?!:;]$', last): c += 1.5      # prefer punctuation breaks
            if j < n and last.lower() in STOP: c += 2.0                    # don't end on a function word
            if len(txt) < 9: c += 2.5
            elif len(txt) < 13: c += 0.8
            # starting a chunk mid-phrase after a sentence end is fine; ending sentence mid-chunk is a soft penalty
            inner = words[i:j - 1]
            if any(re.search(r'[.?!]$', w) for w in inner): c += 1.2
            if best[i] + c < best[j]: best[j] = best[i] + c; prev[j] = i
    out, j = [], n
    while j > 0: out.append((prev[j], j)); j = prev[j]
    return out[::-1]
def highlight(ws):
    def key(w): return re.sub(r"[^a-z0-9'\-]", '', w.lower())
    scored = [(PRIORITY.get(key(w), 0 if key(w) in STOP else 1 + len(key(w)) / 10), k) for k, w in enumerate(ws)]
    sc, k = max(scored)
    if sc <= 1.25: return None
    return k
def chunk_line(line):
    words = clean(line); res = []
    for i, j in cost_split(words):
        ws = words[i:j]; k = highlight(ws)
        disp = list(ws); disp[-1] = strip_end(disp[-1]) or disp[-1]
        if k is not None:
            w = disp[k]; m = re.match(r"^([^A-Za-z0-9]*)(.*?)([,.?!:;]*)$", w)
            disp[k] = f"{m.group(1)}*{m.group(2)}*{m.group(3)}"
        res.append({"words": (i, j), "text": ' '.join(disp)})
    return words, res
if __name__ == '__main__':
    for n, line in enumerate(open(sys.argv[1]).read().strip().split('\n'), 1):
        _, ch = chunk_line(line)
        print(n, ' | '.join(c['text'] for c in ch))
