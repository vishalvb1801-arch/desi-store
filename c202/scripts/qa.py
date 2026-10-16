import json, csv, re, subprocess, sys
base = sys.argv[1]; out = f'{base}/out/C202-Hinglish_Final.mp4'
FPS = 30
def run(cmd): return subprocess.run(cmd, capture_output=True, text=True)
res = {}
# 1 black frames
r = run(['ffmpeg', '-hide_banner', '-i', out, '-vf', 'blackdetect=d=0.04:pix_th=0.10', '-an', '-f', 'null', '-'])
black = re.findall(r'black_start:\S+ black_end:\S+ black_duration:\S+', r.stderr)
print('1. blackdetect intervals:', len(black), black[:5])
# 2 durations
pr = lambda sel, ent: run(['ffprobe', '-v', 'error', '-select_streams', sel, '-show_entries', ent, '-of', 'csv=p=0', out]).stdout.strip()
vdur = float(pr('v', 'stream=duration')); adur = float(pr('a', 'stream=duration'))
src = float(run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f'{base}/src/C202-Hindi-VO.mp3']).stdout)
nf = int(run(['ffprobe', '-v', 'error', '-count_packets', '-select_streams', 'v', '-show_entries', 'stream=nb_read_packets', '-of', 'csv=p=0', out]).stdout)
print(f'2. video {vdur:.4f}s ({nf} frames) | audio stream {adur:.4f}s | source VO {src:.4f}s | video-VO = {vdur-src:+.4f}s ({(vdur-src)*FPS:+.2f} frames)')
# 3 cut + subtitle vs line start
plan = json.load(open(f'{base}/work/edit_plan.json'))
HL = list(csv.DictReader(open(f'{base}/out/hinglish-timing.csv')))
ev = json.load(open(f'{base}/work/sub_events.json'))
cuts = {p['line_no']: p['start'] for p in plan if p['cut'] in ('snap', 'start')}
# verify actual cuts in the rendered file with scene detection
r = run(['ffmpeg', '-hide_banner', '-i', f'{base}/work/video_nosubs.mp4', '-vf', "select='gt(scene,0.25)',showinfo", '-an', '-f', 'null', '-'])
scenes = [float(x) for x in re.findall(r'pts_time:([0-9.]+)', r.stderr)]
miss = []; rows = []
for h in HL:
    k = int(h['line_no']); st = float(h['start'])
    sub = min((e['start'] for e in ev if e['line'] == k), default=None)
    sub_d = (round(sub * 100) / 100 - st) * FPS
    if k in cuts:
        cut_d = (cuts[k] - st) * FPS if k > 1 else 0.0
        near = min(scenes, key=lambda s: abs(s - cuts[k])) if scenes and k > 1 else 0.0
        det = abs(near - cuts[k]) * FPS if k > 1 else 0.0
        cut_txt = f'{cut_d:+.2f}f' + (f' (scene-detected {det:.1f}f off)' if k > 1 else ' (line 1 visual starts at 0.00)')
    else:
        cut_d = 0; cut_txt = 'no cut: clip continues across line (same as English)'
    ok = abs(cut_d) <= 2 and abs(sub_d) <= 2 and (k == 1 or k not in cuts or det <= 2)
    if not ok: miss.append(k)
    rows.append((k, st, cut_txt, f'{sub_d:+.2f}f'))
for r_ in rows: print(f'   L{r_[0]:2d} start {r_[1]:7.2f}  cut {r_[2]:55s} sub {r_[3]}')
print('3. lines missing +-2 frames:', miss or 'none')
# 4 product
first = min(p['start'] for p in plan if p['clip'] in ('clip_24.mp4',))
prod_clips = ['clip_24.mp4', 'clip_25.mp4', 'clip_26.mp4', 'clip_27.mp4', 'clip_37.mp4', 'clip_38.mp4', 'clip_41.mp4', 'clip_42.mp4']
print(f'4. first product frame at {first:.3f}s = line 26 start {float(HL[25]["start"]):.2f}s;',
      'product shots on lines', sorted({p["line_no"] for p in plan if p["clip"] in prod_clips}))
# 5 subtitle text exactness
bad = []
for h in HL:
    k = int(h['line_no']); got = ' '.join(' '.join(e['rows']) for e in ev if e['line'] == k)
    if got != h['hinglish_line']: bad.append((k, got))
srt = open(f'{base}/out/C202-Hinglish.srt', encoding='utf-8').read().strip().split('\n\n')
maxrows = max(len(b.split('\n')) - 2 for b in srt)
lyr = [l.strip() for l in open(f'{base}/lyrics.txt') if l.strip() and not l.startswith('[')]
same_src = all(a == h['hinglish_line'] for a, h in zip(lyr, HL))
gaps = [round(ev[i + 1]['start'] - ev[i]['end'], 3) for i in range(len(ev) - 1) if 0 < ev[i + 1]['start'] - ev[i]['end'] < 0.15]
print(f'5. text mismatches vs LYRICS: {bad or "none"} | lyrics source matches brief: {same_src} | events {len(ev)} | max rows {maxrows} | flicker gaps <0.15s: {gaps or "none"}')
print('   positions:', {p: sorted({e["line"] for e in ev if e["pos"] == p}) for p in ('top', 'up')})
# frozen picture > 0.5 s
r = run(['ffmpeg', '-hide_banner', '-i', f'{base}/work/video_nosubs.mp4', '-vf', 'freezedetect=n=0.0005:d=0.5', '-an', '-f', 'null', '-'])
print('   freezedetect (>0.5s, n=0.0005):', re.findall(r'freeze_start: ([0-9.]+)', r.stderr) or 'none')
