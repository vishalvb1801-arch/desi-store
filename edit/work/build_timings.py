import json, csv
AUDIO=240.039188; FPS=30; NF=round(AUDIO*FPS)
lines=[l.rstrip('\n').split('\t') for l in open('lines.tsv')]
LT=json.load(open('lt_matched.json'))['LT']
rep=json.load(open('align_report.json'))
est=[float(l[2]) for l in lines]
starts=[None]*60; flags=['']*60
for li in range(60):
    r=rep[li]
    ok = r['start'] is not None and r['frac']>=0.5 and r['first_idx']<=1
    if ok:
        starts[li]=r['start']
        if r['first_idx']==1:
            first=[t for t in LT if t['line']==li][0]['t']
            flags[li]=f"first word '{first}' not detected by whisper; line starts at first matched word"
    else:
        flags[li]=f"low-confidence match ({r['nmatch']}/{r['ntok']} words, first matched idx {r['first_idx']}); placed proportionally"
starts[0]=0.0
# monotonic check; anything going backwards gets re-placed
for li in range(1,60):
    if starts[li] is not None and starts[li-1] is not None and starts[li]<=starts[li-1]:
        starts[li]=None; flags[li]+=' non-monotonic start; placed proportionally'
# proportional placement for unknowns between known neighbours
li=0
while li<60:
    if starts[li] is None:
        a=li-1; b=li
        while b<60 and starts[b] is None: b+=1
        t0=starts[a]; t1=starts[b] if b<60 else AUDIO
        tot=sum(est[a:b]); acc=0
        for k in range(a,b):
            if k>a: starts[k]=t0+(t1-t0)*acc/tot
            acc+=est[k]
        li=b
    else: li+=1
fr=[round(s*FPS) for s in starts]+[NF]; fr[0]=0
with open('/home/user/desi-store/edit/timings.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['line','start','end','frames','target_s','clip','action','flag'])
    for i in range(60):
        n=fr[i+1]-fr[i]; T=n/FPS; Lc=121/24
        act='trim' if T<=Lc else ('slow' if T<=1.5*Lc else 'slow+hold')
        w.writerow([lines[i][0], f"{fr[i]/FPS:.3f}", f"{fr[i+1]/FPS:.3f}", n, f"{T:.3f}", f"C299 A/{i+1}.mp4 ({lines[i][1]})", act, flags[i].strip()])
assert all(fr[i+1]>fr[i] for i in range(60)), 'non-increasing'
assert fr[-1]==NF and sum(fr[i+1]-fr[i] for i in range(60))==NF
json.dump(dict(starts=starts, frames=fr), open('line_starts.json','w'))
print('total frames', NF, 'ok')
for i in range(60):
    if flags[i]: print(i+1, flags[i])
