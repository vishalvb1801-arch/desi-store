"""CTC forced alignment of the exact romanised lyrics to a vocal stem (torchaudio MMS_FA)."""
import torch, torchaudio, json, re, sys
import soundfile as sf
import torchaudio.functional as F
from torchaudio.pipelines import MMS_FA as bundle
wav_path, lyrics_path, out_path = sys.argv[1:4]
lines = [l.strip() for l in open(lyrics_path) if l.strip() and not l.startswith('[')]
def norm_words(line):
    return [w for w in re.sub(r"[^a-z' ]", ' ', line.lower().replace('-', ' ')).split() if w.strip("'")]
data, sr = sf.read(wav_path, dtype='float32', always_2d=True)
wav = torch.from_numpy(data.T.copy())
wav = torchaudio.functional.resample(wav.mean(0, keepdim=True), sr, bundle.sample_rate)
model = bundle.get_model(with_star=True).eval()
D = bundle.get_dict(star='*')
# emissions in 30 s windows with 4 s context each side
seg, ctx = 30 * 16000, 4 * 16000
ems = []
with torch.inference_mode():
    n = wav.shape[1]; pos = 0
    while pos < n:
        a, b = max(0, pos - ctx), min(n, pos + seg + ctx)
        e, _ = model(wav[:, a:b])
        fps = e.shape[1] / ((b - a) / 16000)
        s = int(round((pos - a) / 16000 * fps)); t = s + int(round(min(seg, n - pos) / 16000 * fps))
        ems.append(e[:, s:t]); pos += seg
em = torch.cat(ems, 1)
frame_dur = wav.shape[1] / 16000 / em.shape[1]
tokens, owner = [], []   # owner: (line, word) or None for star
words = []
for li, line in enumerate(lines):
    tokens.append(D['*']); owner.append(None)
    for w in norm_words(line):
        wi = len(words); words.append(dict(line=li, word=w))
        for ch in w:
            if ch in D: tokens.append(D[ch]); owner.append(wi)
tokens.append(D['*']); owner.append(None)
ali, scores = F.forced_align(em, torch.tensor([tokens], dtype=torch.int32), blank=0)
ali, scores = ali[0], scores[0].exp()
spans = F.merge_tokens(ali, scores)
assert len(spans) == len(tokens), (len(spans), len(tokens))
for sp, ow in zip(spans, owner):
    if ow is None: continue
    w = words[ow]
    w.setdefault('start', sp.start * frame_dur); w['end'] = sp.end * frame_dur
    w.setdefault('sc', []).append(sp.score)
for w in words:
    sc = w.pop('sc', [0.0]); w['score'] = sum(sc) / len(sc)
res = []
for li, line in enumerate(lines):
    ws = [w for w in words if w['line'] == li]
    res.append(dict(line_no=li + 1, text=line, start=ws[0]['start'], end=ws[-1]['end'],
                    score=sum(w['score'] for w in ws) / len(ws), words=ws))
json.dump(res, open(out_path, 'w'), indent=1)
for r in res: print(f"{r['line_no']:2d} {r['start']:7.2f} {r['end']:7.2f} {r['score']:.2f}  {r['text'][:60]}")
