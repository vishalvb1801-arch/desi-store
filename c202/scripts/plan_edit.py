"""Map the English edit onto the Hinglish line grid and fit each clip (trim / slow <=1.6x / ping-pong)."""
import json, csv, sys
base = sys.argv[1]
FPS = 30; CLIP_LEN = 121 / 24; AUDIO_END = 210.050583
segs = json.load(open(f'{base}/work/eng_segments.json'))
EL = json.load(open(f'{base}/work/english_lines.json'))
HL = [dict(line_no=int(r['line_no']), text=r['hinglish_line'], start=float(r['start']), end=float(r['end']))
      for r in csv.DictReader(open(f'{base}/out/hinglish-timing.csv'))]
N = len(EL)
for i in range(N - 1): EL[i]['end'] = min(EL[i]['end'], EL[i + 1]['start'])
def line_of(t):
    k = 0
    for i, l in enumerate(EL):
        if l['start'] - 1e-6 <= t: k = i
    return k
def e2h(t):
    """piecewise-linear English->Hinglish time map anchored on each line's vocal start/end"""
    anchors = [(0.0, 0.0)]
    for e, h in zip(EL, HL):
        anchors += [(e['start'], h['start']), (e['end'], h['end'])]
    anchors.append((205.64, AUDIO_END))
    anchors = sorted(set(anchors))
    for (a0, b0), (a1, b1) in zip(anchors, anchors[1:]):
        if a0 <= t <= a1: return b0 + (b1 - b0) * (t - a0) / max(a1 - a0, 1e-6)
    return anchors[-1][1]
# ---- english-map.csv
with open(f'{base}/out/english-map.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['line_no', 'english_line', 'segment_start', 'segment_end', 'source_clip', 'clip_in', 'clip_out', 'speed'])
    for s in segs:
        a, b = line_of(s['start']), line_of(s['end'] - 0.05)
        ln = f"{a+1}" if a == b else f"{a+1}-{b+1}"
        txt = EL[a]['text'] if a == b else ' / '.join(EL[k]['text'] for k in range(a, b + 1))
        w.writerow([ln, txt, s['start'], s['end'], s['clip'], s['clip_in'], s['clip_out'], s['speed']])
# ---- snap English cuts to Hinglish line starts
import re
HA = json.load(open(f'{base}/work/hin_align.json'))
HW = []   # (start, clause_start?) for every Hinglish word
for L in HA:
    if L['line_no'] == 39: continue          # aligner smeared this line (fixed in hinglish-timing.csv)
    toks = L['text'].split(); wi = 0; prev_break = True
    for tok in toks:
        parts = [w for w in re.sub(r"[^a-z' ]", ' ', tok.lower().replace('-', ' ')).split() if w.strip("'")]
        for j, _ in enumerate(parts):
            HW.append((L['words'][wi]['start'], prev_break and j == 0)); wi += 1
        prev_break = bool(re.search(r'[,?."]$', tok))
def snap_word(t):
    near = [(abs(ws - t), ws) for ws, cl in HW if cl and abs(ws - t) <= 1.0]
    if near: return min(near)[1], 'clause'
    near = [(abs(ws - t), ws) for ws, cl in HW if abs(ws - t) <= 0.6]
    if near: return min(near)[1], 'word'
    return t, 'mapped'
cuts = []
used_lines = set()
for i, s in enumerate(segs):
    t = s['start']
    if i == 0: cuts.append((0.0, 0, 'start')); used_lines.add(0); continue
    # nearest English line start within [-0.8, +3.0] s of the cut, not already claimed by an earlier cut
    cand = [(abs(t - l['start']), k) for k, l in enumerate(EL) if -0.8 <= t - l['start'] <= 3.0 and k not in used_lines]
    if cand:
        k = min(cand)[1]; used_lines.add(k); cuts.append((HL[k]['start'], k, 'snap'))
    else:
        ht, how = snap_word(e2h(t)); cuts.append((ht, line_of(t), how))
fr = [round(c[0] * FPS) for c in cuts] + [round(AUDIO_END * FPS)]
plan = []
for i, s in enumerate(segs):
    n = fr[i + 1] - fr[i]; D = n / FPS
    cin = s['clip_in']; span = CLIP_LEN - cin
    if D <= span: speed, mode, cout = 1.0, 'trim', cin + D
    elif D <= 1.6 * span + 1e-9: speed, mode, cout = span / D, 'slow', CLIP_LEN
    else:
        cin = 0.0; span = CLIP_LEN
        if D <= 1.6 * span: speed, mode, cout = span / D, 'slow-full', CLIP_LEN
        else:   # forward at the 1.6x cap, then a reversed tail (then forward again...) for the remainder
            speed, cout = 1 / 1.6, CLIP_LEN
            p = 1
            while D > p * span * 1.6: p += 1
            mode = f'pingpong{p}'
    k = cuts[i][1]
    pieces = []   # (src_from, src_to) at `speed`; src_from > src_to means reversed
    if mode.startswith('pingpong'):
        rem = D * speed; a, b = cin, CLIP_LEN; fwd = True
        while rem > 1e-6:
            take = min(rem, b - a)
            pieces.append((a, a + take) if fwd else (b, b - take)); rem -= take; fwd = not fwd
    else:
        pieces.append((cin, cin + D * speed))
    plan.append(dict(idx=i, pieces=[(round(x, 4), round(y, 4)) for x, y in pieces], line_no=k + 1, cut=cuts[i][2], start=fr[i] / FPS, end=fr[i + 1] / FPS, frames=n,
                     clip=s['clip'], clip_in=round(cin, 3), clip_out=round(cout, 3), speed=round(speed, 4), mode=mode,
                     eng_speed=s['speed'], eng_out=s['clip_out']))
json.dump(plan, open(f'{base}/work/edit_plan.json', 'w'), indent=1)
for p in plan:
    flag = ' <past-eng-out' if p['clip_out'] > p['eng_out'] + 0.3 else ''
    print(f"{p['idx']:2d} L{p['line_no']:2d} {p['cut']:6s} {p['start']:7.2f}-{p['end']:7.2f} ({p['end']-p['start']:5.2f}s) {p['clip']} in {p['clip_in']:.2f} out {p['clip_out']:.2f} x{p['speed']:.3f} {p['mode']:9s} [eng x{p['eng_speed']} out {p['eng_out']}]{flag}")
