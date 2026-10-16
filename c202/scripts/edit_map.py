import json, csv, sys
base = sys.argv[1]
plan = json.load(open(f'{base}/work/edit_plan.json'))
HL = list(csv.DictReader(open(f'{base}/out/hinglish-timing.csv')))
def lines_in(a, b):
    ks = [int(r['line_no']) for r in HL if float(r['start']) < b - 0.05 and (float(r['end']) > a + 0.05 or float(r['start']) >= a - 0.05)]
    return ks
with open(f'{base}/out/c202-edit-map.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['line_no', 'hinglish_line', 'start', 'end', 'source_clip', 'in', 'out', 'speed'])
    for p in plan:
        ks = [k for k in lines_in(p['start'], p['end']) if k >= p['line_no']] or [p['line_no']]
        ln = str(ks[0]) if len(ks) == 1 else f'{ks[0]}-{ks[-1]}'
        txt = ' / '.join(HL[k - 1]['hinglish_line'] for k in ks)
        if p['cut'] not in ('snap', 'start'): txt = '(cont.) ' + txt
        pcs = p['pieces']
        out = f"{pcs[0][1]:.3f}" if len(pcs) == 1 else f"{pcs[0][1]:.3f} then reverse to {pcs[1][1]:.3f}"
        w.writerow([ln, txt, f"{p['start']:.3f}", f"{p['end']:.3f}", p['clip'], f"{pcs[0][0]:.3f}", out, f"{p['speed']:.3f}"])
