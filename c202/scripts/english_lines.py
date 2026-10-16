"""English line table: hand-segmented line starts (english_lines.tsv) + vocal ends from Whisper word timestamps."""
import json, sys
base = sys.argv[1]
r = json.load(open(f'{base}/work/eng_whisper.json')); ws = [w for s in r['segments'] for w in s['words']]
L = [l.rstrip('\n').split('\t') for l in open(f'{base}/english_lines.tsv')]
starts = [float(x[1]) for x in L] + [999]
out = []
for i, (n, s, t) in enumerate(L):
    inl = [w for w in ws if starts[i] - 0.05 <= w['start'] < starts[i + 1] - 0.05]
    out.append(dict(line_no=int(n), start=float(s), end=round(inl[-1]['end'], 2), text=t))
json.dump(out, open(f'{base}/work/english_lines.json', 'w'), indent=1)
