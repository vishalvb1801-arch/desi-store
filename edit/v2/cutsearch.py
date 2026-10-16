import numpy as np, json, librosa, soundfile as sf
db=np.load('vocal_db.npy')
B=np.array(json.load(open('beats.json'))['beats'])
nv,sr=sf.read('stems/htdemucs/song/no_vocals.wav'); nv=nv.mean(1)
y=librosa.resample(nv,orig_sr=sr,target_sr=22050)
C=librosa.feature.chroma_cqt(y=y,sr=22050,hop_length=512)
O=librosa.onset.onset_strength(y=y,sr=22050,hop_length=512)
fr=librosa.time_to_frames(B,sr=22050,hop_length=512)
Cs=librosa.util.sync(C,fr); Os=librosa.util.sync(O[None,:],fr)
def feat(k):
    a=np.concatenate([Cs[:,k:k+4].ravel(), 3*Os[:,k:k+4].ravel()/Os.max()]); return a/np.linalg.norm(a)
def vend(t0,t1,th=-30):
    seg=db[int(t0*100):int(t1*100)]; idx=np.where(seg>th)[0]; return t0+(idx[-1]+1)/100
def vstart(t0,t1,th=-30):
    seg=db[int(t0*100):int(t1*100)]; idx=np.where(seg>th)[0]; return t0+idx[0]/100
E={'a4a':(vend(13.0,14.8),vstart(15.0,17.0)),'a4b':(vend(31.8,34.0),vstart(34.0,35.0)),
   'a3':(vend(96.8,98.6),vstart(100.8,101.8)),'a1':(206.56,vstart(217.9,218.8))}
res={}
for g,(le,ns) in E.items():
    print(f"{g}: vocal end {le:.2f}  next onset {ns:.2f}  gap {ns-le:.2f}")
    cands=[]
    for i,bi in enumerate(B):
        if not (le+0.0 <= bi <= le+1.0): continue
        for j,bj in enumerate(B):
            if not (ns-1.0 <= bj <= ns-0.05) or j<=i: continue
            post=bi-le; pre=ns-bj
            cands.append(dict(gap=round(post+pre,2),post=round(post,2),pre=round(pre,2),N=j-i,sim=round(float(feat(i)@feat(j)),3),out=round(bi,3),inn=round(bj,3)))
    for c in sorted(cands,key=lambda c:abs(c['gap']-0.6))[:6]: print('   ',c)
    res[g]=dict(le=le,ns=ns,cands=cands)
json.dump(res,open('cut_cands.json','w'))
print('a2 vocal end', vend(233.0,236.0))
