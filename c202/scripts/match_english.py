import cv2, numpy as np, glob, os, sys, json
W,H=36,64
def frames(path, crop=None):
    cap=cv2.VideoCapture(path); out=[]
    while True:
        ok,f=cap.read()
        if not ok: break
        h,w=f.shape[:2]
        if crop: # centre-crop to 9:16
            th=int(round(w*16/9))
            if th<=h: y=(h-th)//2; f=f[y:y+th]
        g=cv2.cvtColor(cv2.resize(f,(W,H),interpolation=cv2.INTER_AREA),cv2.COLOR_BGR2GRAY).astype(np.float32)
        out.append(g)
    return np.array(out)
base=sys.argv[1]
clips=sorted(glob.glob(base+'/input/clip_*.mp4'))
mask=np.ones((H,W),bool); mask[int(H*0.66):int(H*0.84)]=False   # burned-in subtitle band
def vec(a):
    v=a[:,mask].reshape(len(a),-1); v=v-v.mean(1,keepdims=True); n=np.linalg.norm(v,axis=1,keepdims=True)+1e-6
    return v/n
C=[];idx=[]
for i,c in enumerate(clips):
    f=frames(c,crop=True); C.append(f); idx+= [(i,j) for j in range(len(f))]
C=vec(np.concatenate(C)); idx=np.array(idx)
E=vec(frames(base+'/src/C 202 English_Final.mp4'))
S=E@C.T
best=S.argmax(1); score=S.max(1)
np.save(base+'/work/eng_match.npy',np.stack([idx[best,0],idx[best,1],score],1))
print(len(E),len(C),'mean score',score.mean(),'min',score.min())
