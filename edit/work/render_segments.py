# Render each line's segment at its exact frame count, per the T vs L rules.
import csv, subprocess, json, sys
FPS=30; SRC_FPS=24; L_FRAMES=121; L=L_FRAMES/SRC_FPS
CLIPDIR="/home/user/desi-store/input/C299 A/C299 A"
rows=list(csv.DictReader(open('/home/user/desi-store/edit/timings.csv')))
plan=[]
for r in rows:
    i=int(r['line']); n=int(r['frames'])
    if i==39: n+=6   # 6 extra frames of line 39 feed the crossfade into line 40
    T=n/FPS
    if T<=L+1e-9: factor=1.0; act='trim'; hold=0.0
    elif T<=1.5*L+1e-9: factor=T/L; act='slow'; hold=0.0
    else: factor=1.5; act='slow+hold'; hold=T-1.5*L
    vf=(f"setpts=PTS*{factor:.6f},fps={FPS},"
        "scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,setsar=1,"
        f"tpad=stop_mode=clone:stop_duration=12,trim=end_frame={n},setpts=N/{FPS}/TB,format=yuv420p")
    out=f"/home/user/desi-store/edit/work/seg/{i:02d}.mp4"
    cmd=["ffmpeg","-v","error","-y","-i",f"{CLIPDIR}/{i}.mp4","-an","-vf",vf,"-frames:v",str(n),
         "-c:v","libx264","-preset","medium","-crf","10","-pix_fmt","yuv420p","-r",str(FPS),out]
    plan.append(dict(line=i,frames=n,T=T,factor=factor,action=act,hold=hold,cmd=cmd,out=out))
json.dump([{k:v for k,v in p.items() if k!='cmd'} for p in plan], open('/home/user/desi-store/edit/work/fit_plan.json','w'), indent=1)
from concurrent.futures import ThreadPoolExecutor
def run(p):
    subprocess.run(p['cmd'],check=True)
    nf=subprocess.run(["ffprobe","-v","error","-count_frames","-select_streams","v:0","-show_entries","stream=nb_read_frames","-of","csv=p=0",p['out']],capture_output=True,text=True).stdout.strip()
    return p['line'], p['frames'], int(nf)
import os; os.makedirs('/home/user/desi-store/edit/work/seg',exist_ok=True)
with ThreadPoolExecutor(4) as ex:
    for line,want,got in ex.map(run,plan):
        print(line,want,got,'OK' if want==got else 'MISMATCH',flush=True)
