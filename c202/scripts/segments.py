import numpy as np, sys, json
base=sys.argv[1]
m=np.load(base+'/work/eng_match.npy'); fps=30000/1001
clip=m[:,0].astype(int); fr=m[:,1].astype(int); sc=m[:,2]
# median-filter clip id to kill single-frame mismatches
from collections import Counter
cl=clip.copy()
for i in range(len(cl)):
    w=clip[max(0,i-3):i+4]; cl[i]=Counter(w).most_common(1)[0][0]
segs=[];s=0
for i in range(1,len(cl)+1):
    if i==len(cl) or cl[i]!=cl[s]:
        segs.append((s,i-1)); s=i
# merge tiny segments (<4 frames) into neighbour
out=[]
for a,b in segs:
    if out and b-a<3: out[-1]=(out[-1][0],b)
    else: out.append((a,b))
res=[]
for a,b in out:
    c=Counter(cl[a:b+1]).most_common(1)[0][0]
    sel=[i for i in range(a,b+1) if clip[i]==c]
    t=np.array(sel)/fps; f=fr[sel]/24.0
    slope=np.polyfit(t,f,1)[0] if len(sel)>3 else 1.0
    res.append(dict(start=round(a/fps,3),end=round((b+1)/fps,3),clip=f'clip_{c+1:02d}.mp4',
        clip_in=round(fr[sel[0]]/24,3),clip_out=round((fr[sel[-1]]+1)/24,3),speed=round(slope,3),score=round(float(sc[a:b+1].mean()),3),
        frames=b-a+1, reversed=bool(slope<0)))
json.dump(res,open(base+'/work/eng_segments.json','w'),indent=1)
for r in res: print(r)
