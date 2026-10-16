import json, csv
P=json.load(open('plan.json')); fr=P['frames']; cuts=P['cuts']
meta={m['line']:m for m in json.load(open('render_meta.json'))}
fit={p['line']:p for p in json.load(open('fit_plan.json'))}
old=list(csv.DictReader(open('../timings.csv')))
def fwd(t):
    sh=0
    for c in cuts:
        if t>=c['inn']: sh+=c['removed']
        elif t>c['out']: return c['out']-sh
    return t-sh
def mmss(t): m=int(t//60); return f"{m}:{t-60*m:05.2f}"
C={c['name']:c for c in cuts}
rows=[]
def add(item,old,new,what): rows.append((item,old,new,what))
c=C['a1']; add('a1',f"{mmss(206.56)}–{mmss(218.63)} (12.07 s between 'lose' and 'EIS')",f"{mmss(fwd(206.56))}–{mmss(fwd(218.63))} (0.53 s)",
  f"Removed {mmss(c['out'])}–{mmss(c['inn'])} = 23 beats ({c['removed']:.2f} s), phase-locked, 100 ms crossfade. 'Lose' is a held C5 note + run to 3:34.85 on the vocal stem; it is released with a 0.39 s fade on the vocal stem only (3:26.50–3:26.89), instrumental untouched. Close-up freeze 3:29.5–3:38.5 gone: line 57 is now 5.1 s on its 5.04 s clip (1.01×).")
add('a2',f"{mmss(233.77)}–4:00.04 outro (frozen from 3:58.1)",f"ends {mmss(P['NEWLEN'])}",f"Cut 0.50 s after 'me.' (vocal ends {mmss(233.77)}). 120 ms audio tail fade; picture runs to the last frame, no fade to black.")
c=C['a3']; add('a3',f"{mmss(98.20)}–{mmss(101.58)} (3.38 s after 'work to do.')",f"{mmss(fwd(98.2))}–{mmss(fwd(101.58))} (0.39 s)",f"Removed {mmss(c['out'])}–{mmss(c['inn'])} = 6 beats ({c['removed']:.2f} s), 100 ms crossfade.")
c=C['a4a']; add('a4',f"{mmss(13.94)}–{mmss(16.43)} (2.49 s after 'show me.')",f"{mmss(fwd(13.94))}–{mmss(fwd(16.43))} (0.45 s)",f"Removed {mmss(c['out'])}–{mmss(c['inn'])} = 4 beats / 1 bar ({c['removed']:.2f} s), lands cleanly on the beat.")
c=C['a4b']; add('a4',f"{mmss(33.18)}–{mmss(34.72)} (1.54 s after 'stared back')",f"{mmss(fwd(33.18))}–{mmss(fwd(34.72))} (0.54 s)",f"Removed {mmss(c['out'])}–{mmss(c['inn'])} = 2 beats ({c['removed']:.2f} s), lands cleanly on the beat.")
add('a5',"2:25.77–2:25.97 crossfade into 'Cause I finally'",f"hard cut at {mmss(fr[39]/30)}","6-frame dissolve removed; line 39 no longer runs under line 40.")
sl=[('0:36.90–0:37.13','closer mirror (clip 9 after its in-clip cut at 2.50 s)',9),('0:43.81–0:44.27','reused stairs wide (clip 11 after its cut at 3.21 s)',11),
    ('1:55.78–1:56.00','alternate knee rub (clip 30 after its cut at 2.54 s)',30),('2:08.90–2:09.27','praying hands close-up (clip 34 after its cut at 3.17 s)',34),
    ("2:51.83–2:51.93","phone with 'BIS' label (clip 47 after its cut at 2.96 s)",47),('3:04.51–3:04.67','husband close-up (clip 52 after its cut at 2.04 s)',52),
    ('3:07.67–3:07.87','Vikram close-up (clip 53 after its cut at 3.00 s)',53)]
for o,w,l in sl:
    p=fit[l]; how=(f"tail shot dropped; preceding shot slowed to {p['f']:.2f}× to fill" if p['note'].startswith('dropped') else "line now ends before the in-clip cut (tighter timing), sliver never reached")
    add('a6',f"{o} {w}",f"line {l}: {mmss(fr[l-1]/30)}–{mmss(fr[l]/30)}",how)
for l in (5,35):
    add('a6 (extra)',f"line {l} tail after in-clip cut","",f"same fix applied: {fit[l]['note']}")
m=meta[58]['parts']; s=(fr[57]+m[0]['frames'])/30
add('a7',"3:41.17–3:45.23 bottle close-up with misspelled label ('Ayyvabeic', 'PAIN RELEFF')",f"{mmss(s)}–{mmss(fr[58]/30)}",
  f"Replaced with the clean-label hero shot (clip 31, the 1:56 shot, source 0.6–5.04 s at {m[1]['f']:.2f}×). Clip 58's clean opening shot is kept up to 'Fifteen herbs'. Captions there sit above the cap (y 210).")
with open('C299-A_v2_changes.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['item','old (C299-A_final.mp4)','new (C299-A_v2.mp4)','change']); w.writerows(rows)
# per-line table
L=[]
for i,r in enumerate(old):
    L.append((r['line'],mmss(float(r['start'])),mmss(fr[i]/30),f"{float(r['target_s']):.2f}",f"{(fr[i+1]-fr[i])/30:.2f}",
              '+'.join(f"clip {p['clip']}" for p in meta[i+1]['parts'])))
with open('C299-A_v2_lines.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['line','old start','new start','old length s','new length s','clips']); w.writerows(L)
print(len(rows),'change rows;', len(L),'line rows')
for r in rows: print(r[0],'|',r[1],'|',r[2])
