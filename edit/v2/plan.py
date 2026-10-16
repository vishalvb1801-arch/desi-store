import numpy as np, json, csv
db=np.load('vocal_db.npy'); B=np.array(json.load(open('beats.json'))['beats'])
FPS=30; SONG=240.039188
def nearest_beat(t): return int(np.argmin(abs(B-t)))
# ---- audio cuts (song time) ----
# name, vocal end (le), next onset (ns), beats removed N, post-pad target
spec=[('a4a',13.94,16.43,4),('a4b',33.18,34.72,2),('a3',98.20,101.58,6),('a1',206.56,218.63,23)]
cuts=[]
for name,le,ns,N in spec:
    G=ns-le
    # removed length from the local beat grid
    i=nearest_beat(le+0.3); rem=B[i+N]-B[i]
    gap=G-rem
    pre=min(0.25,gap*0.5) if gap<0.6 else 0.25
    post=gap-pre
    out=le+post; inn=out+rem
    cuts.append(dict(name=name,le=le,ns=ns,N=N,removed=rem,gap=gap,post=post,pre=pre,out=out,inn=inn))
END_SRC=233.77+0.5
def fwd(t):            # song time -> v2 time (None if removed)
    sh=0
    for c in cuts:
        if t>=c['inn']: sh+=c['removed']
        elif t>c['out']: return None
    return t-sh
NEWLEN=fwd(END_SRC)
# ---- word times, refined at true onsets ----
LT=json.load(open('../work/lt_matched.json'))['LT']
def onset_after_dip(ws):
    a=int((ws-0.2)*100); b=int((ws+0.55)*100)
    for k in range(a,b):
        if db[k]>-30 and db[max(0,k-15):k].min()<-38: return k/100
    return None
lines=[l.rstrip('\n').split('\t') for l in open('../work/lines.tsv')]
first_tok={}
for k,t in enumerate(LT):
    if t['line'] not in first_tok: first_tok[t['line']]=k
starts=[]; refl=[]
for li in range(60):
    t=LT[first_tok[li]]
    ws=t.get('s')
    if li==30: ws=116.0   # 'EIS' undetected; line starts at 'Ayurvedic'
    r=onset_after_dip(ws) if li>0 else 0.0
    st=r if (r is not None and r>=ws-0.2) else ws
    starts.append(st); refl.append((li+1, round(ws,2), round(st,2)))
starts[0]=0.0
new_starts=[fwd(s) for s in starts]
assert all(x is not None for x in new_starts)
fr=[round(x*FPS) for x in new_starts]+[round(NEWLEN*FPS)]
json.dump(dict(cuts=cuts,END_SRC=END_SRC,NEWLEN=NEWLEN,starts_song=starts,new_starts=new_starts,frames=fr,refined=refl),open('plan.json','w'),indent=1,default=float)
print('cuts:'); [print('  ',{k:(round(v,3) if isinstance(v,float) else v) for k,v in c.items()}) for c in cuts]
print('new length', round(NEWLEN,3), 'frames', fr[-1])
print('refined line starts (line, whisper, used):', [r for r in refl if abs(r[1]-r[2])>0.05])
