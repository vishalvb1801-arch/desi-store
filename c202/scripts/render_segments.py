"""Render every planned segment to an exact-frame-count 1080x1920@30 intermediate (visually lossless)."""
import json, subprocess, sys, os
from concurrent.futures import ThreadPoolExecutor
base = sys.argv[1]
plan = json.load(open(f'{base}/work/edit_plan.json'))
os.makedirs(f'{base}/work/segs', exist_ok=True)
def job(p):
    out = f"{base}/work/segs/seg_{p['idx']:02d}.mp4"
    parts, labels = [], []
    for j, (a, b) in enumerate(p['pieces']):
        lo, hi = min(a, b), max(a, b)
        rev = ',reverse' if a > b else ''
        parts.append(f"[0:v]trim=start={lo}:end={hi},setpts=PTS-STARTPTS{rev},setpts=PTS/{p['speed']}[p{j}]")
        labels.append(f'[p{j}]')
    cat = f"{''.join(labels)}concat=n={len(labels)}:v=1:a=0[c]" if len(labels) > 1 else f"{labels[0]}null[c]"
    fc = ';'.join(parts + [cat, f"[c]fps=30,scale=1080:-2:flags=lanczos,crop=1080:1920,setsar=1,tpad=stop_mode=clone:stop_duration=1,format=yuv420p[v]"])
    cmd = ['ffmpeg', '-v', 'error', '-y', '-i', f"{base}/input/{p['clip']}", '-filter_complex', fc, '-map', '[v]',
           '-frames:v', str(p['frames']), '-c:v', 'libx264', '-crf', '8', '-preset', 'veryfast', '-r', '30', out]
    subprocess.run(cmd, check=True)
    n = subprocess.run(['ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v', '-show_entries', 'stream=nb_read_frames',
                        '-of', 'csv=p=0', out], capture_output=True, text=True).stdout.strip()
    return p['idx'], p['frames'], int(n)
with ThreadPoolExecutor(4) as ex:
    for idx, want, got in ex.map(job, plan):
        print(idx, want, got, 'OK' if want == got else 'MISMATCH')
