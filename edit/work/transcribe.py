import sys, json, time
from faster_whisper import WhisperModel
model_name = sys.argv[1]; out = sys.argv[2]
t=time.time()
import wave, numpy as np
wf=wave.open("song16k.wav"); audio=np.frombuffer(wf.readframes(wf.getnframes()),dtype=np.int16).astype(np.float32)/32768.0
m = WhisperModel(model_name, device="cpu", compute_type="int8", cpu_threads=4)
segs, info = m.transcribe(audio, language="en", word_timestamps=True, beam_size=5,
    vad_filter=False, condition_on_previous_text=False,
    initial_prompt="Kavita, Shalini, Kerala, Vikram, Bandra, Carter Road, mehendi, saree, EIS Ayurvedic Pain Relief Oil, til oil.")
words=[]
for s in segs:
    print(f"{s.start:7.2f} {s.end:7.2f} {s.text}", flush=True)
    for w in s.words: words.append(dict(w=w.word, s=w.start, e=w.end, p=w.probability))
json.dump(words, open(out,"w"), indent=0)
print("done", time.time()-t)
