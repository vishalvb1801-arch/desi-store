"""Build hinglish-timing.csv: forced-alignment line times, manual fixes, onset sharpening on the vocal stem."""
import json, csv, sys, numpy as np, soundfile as sf
base = sys.argv[1]
A = json.load(open(f'{base}/work/hin_align.json'))
# Manual fix (verified by Whisper + vocal silencedetect): line 39 is sung 175.2-179.8 s, aligner smeared it.
A[38]['start'], A[38]['end'] = 175.23, 179.78
A[37]['end'] = min(max(A[37]['end'], 173.30), 173.85)
v, sr = sf.read(f'{base}/work/sep/htdemucs/C202-Hindi-VO/vocals.wav', always_2d=True)
v = v.mean(1); hop = int(sr * 0.01)
n = len(v) // hop; rms = np.sqrt((v[:n*hop].reshape(n, hop) ** 2).mean(1)) + 1e-9
db = 20 * np.log10(rms / rms.max())
def onset(t):
    """latest upward crossing of -32 dB within [t-0.45, t+0.15] s"""
    a, b = int((t - 0.45) * 100), int((t + 0.15) * 100)
    best = None
    for i in range(max(a, 1), min(b, n)):
        if db[i - 1] < -32 <= db[i]: best = i
    return best / 100 if best is not None else t
rows = []
for L in A:
    o = onset(L['start']); s = o if -0.2 <= o - L['start'] <= 0 else L['start']   # sharpen only slightly earlier
    rows.append([L['line_no'], L['text'], round(s, 2), round(L['end'], 2)])
for i, r in enumerate(rows):   # end never past the next start
    if i + 1 < len(rows): r[3] = min(r[3], rows[i + 1][2])
    r.append(round(r[3] - r[2], 2))
with open(f'{base}/out/hinglish-timing.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['line_no', 'hinglish_line', 'start', 'end', 'duration'])
    w.writerows(rows)
for r, L in zip(rows, A):
    print(f"{r[0]:2d} {r[2]:7.2f} {r[3]:7.2f} {r[4]:5.2f}  (align {L['start']:.2f}, shift {r[2]-L['start']:+.2f})  {r[1][:50]}")
