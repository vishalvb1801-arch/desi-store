import whisper, json, sys
audio, lang, model, out = sys.argv[1:5]
m = whisper.load_model(model, download_root='/home/user/desi-store/c202/work/models')
prompt = sys.argv[5] if len(sys.argv) > 5 else None
r = m.transcribe(audio, language=lang, word_timestamps=True, condition_on_previous_text=False,
                 initial_prompt=prompt, temperature=0, fp16=False)
json.dump(r, open(out, 'w'), ensure_ascii=False, indent=1)
for s in r['segments']: print(f"{s['start']:7.2f} {s['end']:7.2f} {s['text']}")
