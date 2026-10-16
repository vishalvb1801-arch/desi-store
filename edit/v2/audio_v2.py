import numpy as np, soundfile as sf, json
P=json.load(open('plan.json')); cuts=P['cuts']; END=P['END_SRC']
x,sr=sf.read('song.wav')                     # original mix, 44.1k stereo
vo,_=sf.read('stems/htdemucs/song/vocals.wav'); nv,_=sf.read('stems/htdemucs/song/no_vocals.wav')
n=min(len(x),len(vo)); x=x[:n].copy(); vo=vo[:n]; nv=nv[:n]
S=lambda t:int(round(t*sr))
# a1: release the held 'lose' note on the vocal stem only (instrumental untouched)
a1=[c for c in cuts if c['name']=='a1'][0]
t_mix0,t_mix1=206.30,206.36          # 60 ms blend original -> stem sum
t_f0,t_f1=206.50,a1['out']+0.05       # vocal fade window
seg=slice(S(t_mix0),S(t_f1)+S(0.06))
t=np.arange(seg.start,seg.stop)/sr
g=np.clip((t_f1-t)/(t_f1-t_f0),0,1); g=np.where(t<t_f0,1.0,0.5-0.5*np.cos(np.pi*g))
stem=nv[seg]+vo[seg]*g[:,None]
w=np.clip((t-t_mix0)/(t_mix1-t_mix0),0,1)[:,None]
x[seg]=x[seg]*(1-w)+stem*w
# pieces between cuts, each extended 50 ms past its junction for a 100 ms crossfade
XF=0.10; H=XF/2
bounds=[0.0]+[v for c in cuts for v in (c['out'],c['inn'])]+[END]
pieces=[(bounds[k],bounds[k+1]) for k in range(0,len(bounds),2)]
out=np.zeros((0,2))
for k,(a,b) in enumerate(pieces):
    a2=a-H if k>0 else a; b2=b+H if k<len(pieces)-1 else b
    p=x[S(a2):S(b2)].copy()
    if k==0: out=p; continue
    m=S(XF); fo=np.linspace(1,0,m)[:,None]; fi=1-fo   # equal-gain: beat-matched, correlated material
    out=np.concatenate([out[:-m], out[-m:]*fo+p[:m]*fi, p[m:]])
# end 0.5 s after the last word: 120 ms tail fade on audio only (picture holds, no black)
m=S(0.12); out[-m:]*=np.linspace(1,0,m)[:,None]
sf.write('audio_v2_raw.wav',out,sr,subtype='PCM_24')
print('audio length', len(out)/sr, 'plan', P['NEWLEN'])
