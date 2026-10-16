# C202 Hinglish re-edit pipeline

Run from `c202/` with inputs in `src/` (zip, Hindi VO, English final, English song) and the zip unpacked to `input/`.

1. `match_english.py` + `segments.py`: frame-match every English-final frame to the source clips -> `work/eng_segments.json`
2. `transcribe.py` (openai-whisper, word timestamps) on the English audio; `english_lines.py` -> English line table
3. demucs vocal stem, `align_lyrics.py` (torchaudio MMS_FA forced alignment of `lyrics.txt`), `hin_timing.py` -> `out/hinglish-timing.csv`
4. `plan_edit.py` -> `out/english-map.csv`, `work/edit_plan.json`; `render_segments.py`; `make_subs.py` -> `.ass`/`.srt`
5. ffmpeg concat + ass burn-in + VO -> `out/C202-Hinglish_Final.mp4`; `edit_map.py`; `qa.py`
