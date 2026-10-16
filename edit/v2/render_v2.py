import json, subprocess, os
from concurrent.futures import ThreadPoolExecutor
P=json.load(open('plan.json')); fr=P['frames']; FPS=30
plan=json.load(open('fit_plan.json'))
LT=json.load(open('../work/lt_matched.json'))['LT']
CLIP="/home/user/desi-store/input/C299 A/C299 A/{}.mp4"
os.makedirs('seg',exist_ok=True)
def fwd(t):
    sh=0
    for c in P['cuts']:
        if t>=c['inn']: sh+=c['removed']
        elif t>c['out']: return None
    return t-sh
def job(clip,s0,s1,f,n,out):
    vf=(f"trim=start={s0}:end={s1},setpts=(PTS-STARTPTS)*{f:.6f},fps={FPS},"
        "scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,setsar=1,"
        f"tpad=stop_mode=clone:stop_duration=0.2,trim=end_frame={n},setpts=N/{FPS}/TB,format=yuv420p")
    return ["ffmpeg","-v","error","-y","-i",CLIP.format(clip),"-an","-vf",vf,"-frames:v",str(n),
            "-c:v","libx264","-preset","medium","-crf","10","-pix_fmt","yuv420p","-r",str(FPS),out]
jobs=[]; meta=[]
for p in plan:
    i=p['line']; n=p['frames']
    if i==58:
        fif=[t for t in LT if t['line']==57 and t['t']=='fifteen'][0]['s']
        split=round(fwd(fif)*FPS)-fr[57]; nA=split; nB=n-split
        fA=(nA/FPS)/2.0; fB=(nB/FPS)/(121/24-0.6)
        jobs.append(job(58,0,2.0-0.001,fA,nA,'seg/58a.mp4')); jobs.append(job(31,0.6,121/24,fB,nB,'seg/58b.mp4'))
        meta.append(dict(line=58,parts=[dict(clip=58,src=[0,2.0],f=round(fA,3),frames=nA),dict(clip=31,src=[0.6,5.042],f=round(fB,3),frames=nB)]))
        continue
    end=p['win']-(0.001 if p['note'].startswith('dropped') else 0)
    jobs.append(job(i,0,end,p['f'],n,f'seg/{i:02d}.mp4'))
    meta.append(dict(line=i,parts=[dict(clip=i,src=[0,round(p['win'],3)],f=p['f'],frames=n)]))
json.dump(meta,open('render_meta.json','w'),indent=1)
def run(c):
    subprocess.run(c,check=True); o=c[-1]
    nf=subprocess.run(["ffprobe","-v","error","-count_frames","-select_streams","v:0","-show_entries","stream=nb_read_frames","-of","csv=p=0",o],capture_output=True,text=True).stdout.strip()
    want=int(c[c.index('-frames:v')+1]); return o,want,int(nf)
bad=0
with ThreadPoolExecutor(4) as ex:
    for o,w,g in ex.map(run,jobs):
        if w!=g: bad+=1; print('MISMATCH',o,w,g)
print('segments',len(jobs),'mismatches',bad)
