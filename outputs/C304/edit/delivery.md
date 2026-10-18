# C304 — EIS Ayurvedic Pain Relief Oil · sung-story (Pixar 3D) · delivery

**Output:** `C304-final.mp4` (one file) · 1080×1920 · 30 fps · H.264 CRF 18 + AAC 192k · 2:49.27 (169.27 s) · subtitles, hook headline and logo burned in · audio = the song only (loudness-normalised to −14 LUFS), no music bed, no SFX.
**Plan:** `edit-plan.json` v1 · 37 segments · 76 shots · 146 caption chunks · validated with `validate_plan.py --clip-map handoff/clip-map.json` → OK. The only warnings are the ones the brief says to ignore: V2 missing, song skips, hook length, and captions under hook1.
**Inputs (from Drive folder `C304`):** `videos/clip_1…78.mp4` → `clips/`, `Voiceover.mp3` (the song, 196.23 s) → `media/vo.mp3`, `Reference Video.mp4` (C303 final) → `reference/`. The EIS logo was **not in the C304 folder**; I used the round "EIS" logo from the Drive `EIS` brand folder (file `3`) → `media/logo.png`. There was no `C304-script.docx` in Drive, so the lyrics and line map come from the brief (`handoff/lyrics.json`).

## How the timing was measured
- The song was transcribed with word timestamps (faster-whisper medium.en; `handoff/transcript_raw.json`), and the 37 lyric lines were aligned to it (`handoff/transcript.json`, 445/452 words matched).
- The vocal was separated with Demucs, and the vocal-stem energy map sets every instrumental edge and every line boundary. Contiguous lines cut in the breath between them; a skip cuts 0.12 s after the last sung word and 0.08 s before the next first word.
- **Stretched first words caught:** Whisper had pulled four line starts back into the instrumental before them. Each of those lines now starts at its real first sung word (vocal stem): line 9 37.38 → 37.71, line 13 63.62 → 64.23, line 25 129.02 → 129.51, line 35 180.34 → 180.66.
- Singing runs 0.03 s → 194.60 s. seg01 starts at 0.00. The end card holds 1.60 s after the last sung word ("me"), then the ad ends at song time 196.20.

## Segment table
Fits: **trim**/**hold** shorter than the clip = the first N s of the clip at normal speed (stretch 1.00); **slow** = whole clip retimed (stretch = shot ÷ clip; all between 0.81× and 1.10×, so nothing is above 1.6×). Every cut sits in a gap between words; for two-shot lines it's the comma/phrase break wherever the 0.8 s minimum allows.

| # | role | line | song in–out | clips + fit | stretch× |
|---|---|---|---|---|---|
| 01 | hook | I saw you in bed with my best friend, my eyes were open wide | 0.00–3.97 (3.97s) | 1 trim 0.95s · 2 trim 1.02s · 3 trim 0.86s · 4 trim 1.14s | 1.00 (first 0.95s) · 1.00 (first 1.02s) · 1.00 (first 0.86s) · 1.00 (first 1.14s) |
| 02 | hook | Where was I? Awake all night in pain, while he was by your side | 3.97–8.16 (4.19s) | 5 trim 0.84s · 6 trim 1.49s · 7 trim 1.06s · 8 trim 0.80s | 1.00 (first 0.84s) · 1.00 (first 1.49s) · 1.00 (first 1.06s) · 1.00 (first 0.80s) |
| 03 | body | You're telling me about your day, I'm pressing on my spine | 8.16–12.92 (4.76s) | 9 trim 2.43s · 10 trim 2.33s | 1.00 (first 2.43s) · 1.00 (first 2.33s) |
| 04 | body | You ask me "Did you hear me?", I say "Sorry… I'm fine" | 12.92–16.99 (4.07s) | 11 trim 1.61s · 12 trim 2.46s | 1.00 (first 1.61s) · 1.00 (first 2.46s) |
| 05 | body | You're leaning for a goodnight kiss, my shoulder pulls me away | 16.99–21.34 (4.35s) | 13 trim 2.17s · 14 trim 2.18s | 1.00 (first 2.17s) · 1.00 (first 2.18s) |
| 06 | body | We said we'd leave at seven, but my knees just made me stay | 21.34–25.30 (3.96s) | 15 trim 1.63s · 16 trim 2.33s | 1.00 (first 1.63s) · 1.00 (first 2.33s) |
| 07 | body | Your jacket's gone, I'm still in bed, another night slips by | 25.30–29.56 (4.26s) | 17 trim 2.52s · 18 trim 1.74s | 1.00 (first 2.52s) · 1.00 (first 1.74s) |
| 08 | body | I scroll through "pain relief at night" till two, and wonder why | 29.56–35.05 (5.49s) | 19 trim 2.43s · 20 trim 3.06s | 1.00 (first 2.43s) · 1.00 (first 3.06s) |
| 09 | body | You say you're tired of reaching for someone never there | 37.63–42.33 (4.70s) | 21 trim 2.22s · 22 slow 2.48s | 1.00 (first 2.22s) · 0.82 |
| 10 | body | You say it's over, I look up, he's waiting on the stairs | 42.33–46.83 (4.50s) | 23 slow 2.56s · 24 trim 1.94s | 0.84 · 1.00 (first 1.94s) |
| 11 | body | I ask if we can talk this through, you say you made your choice | 46.83–51.16 (4.33s) | 25 trim 2.37s · 26 trim 1.96s | 1.00 (first 2.37s) · 1.00 (first 1.96s) |
| 12 | body | You roll your suitcase out the door, I can't find my voice | 51.16–56.45 (5.29s) | 27 slow 2.46s · 28 trim 2.83s | 0.81 · 1.00 (first 2.83s) |
| 13 | body | I'm scrolling through your pictures, you're out with him, so carefree | 64.15–68.20 (4.05s) | 29 trim 1.80s · 30 trim 2.25s | 1.00 (first 1.80s) · 1.00 (first 2.25s) |
| 14 | body | I wince just tying up my shoes, when did this become me? | 68.20–72.60 (4.40s) | 31 slow 2.69s · 32 trim 1.71s | 0.88 · 1.00 (first 1.71s) |
| 15 | body | The boss says, "Too many sick days, Raj, we're letting you go" | 72.60–77.20 (4.60s) | 33 slow 2.55s · 34 trim 2.05s | 0.84 · 1.00 (first 2.05s) |
| 16 | body | I pack my desk into a box and carry it home slow | 77.20–81.86 (4.66s) | 35 trim 2.29s · 36 trim 2.37s | 1.00 (first 2.29s) · 1.00 (first 2.37s) |
| 17 | body | I go home to my Nani's house, she sees me wince and stop | 81.86–86.28 (4.42s) | 37 trim 2.62s · 38 trim 1.80s | 1.00 (first 2.62s) · 1.00 (first 1.80s) |
| 18 | body | She says, "EIS Pain Relief Oil. Every night, just warm a drop" | 86.28–90.59 (4.31s) | 39 slow 3.30s · 40 hold 1.01s | 0.82 · 1.00 (first 1.01s) |
| 19 | body | She warms it in her palms and rubs it deep into my knee | 90.59–95.02 (4.43s) | 41 trim 2.25s · 42 trim 2.18s | 1.00 (first 2.25s) · 1.00 (first 2.18s) |
| 20 | body | Fifteen Ayurvedic herbs inside, Mahanarayan, Nirgundi | 95.02–101.65 (6.63s) | 43 hold 3.19s · 44 slow 3.44s | 1.00 (first 3.19s) · 0.85 |
| 21 | body | It soaks in past the skin, right down to where it's sore | 101.65–105.80 (4.15s) | 45 trim 1.83s · 46 trim 2.32s | 1.00 (first 1.83s) · 1.00 (first 2.32s) |
| 22 | body | It calms the swelling, warms the joint, I read and read some more | 105.80–110.26 (4.46s) | 47 slow 4.46s | 1.10 |
| 23 | body | Week 1, I warm it every night, and sleep straight through till dawn | 110.26–114.32 (4.06s) | 50 slow 4.06s | 1.00 |
| 24 | body | I make my list, I tick one off, then one more thing is done | 114.32–119.69 (5.37s) | 51 trim 2.38s · 52 slow 2.99s | 1.00 (first 2.38s) · 0.98 |
| 25 | body | Week 2, I'm taking on the things I used to leave for another day | 129.43–133.53 (4.10s) | 53 trim 2.15s · 54 trim 1.95s | 1.00 (first 2.15s) · 1.00 (first 1.95s) |
| 26 | body | I sketch the plan for my own business, push my doubts away | 133.53–137.76 (4.23s) | 55 trim 2.22s · 56 trim 2.01s | 1.00 (first 2.22s) · 1.00 (first 2.01s) |
| 27 | body | Week 3, I'm working on my body, Nani claps, "Ready? Here we go" | 137.76–142.18 (4.42s) | 57 trim 2.27s · 58 trim 2.15s | 1.00 (first 2.27s) · 1.00 (first 2.15s) |
| 28 | body | One more squat, my knees don't scream, I'm laughing, bending low | 142.18–146.69 (4.51s) | 59 slow 3.47s · 60 trim 1.04s | 0.86 · 1.00 (first 1.04s) |
| 29 | body | One morning, I walk in tall, the gym feels like my home | 146.69–150.80 (4.11s) | 61 trim 2.17s · 62 trim 1.94s | 1.00 (first 2.17s) · 1.00 (first 1.94s) |
| 30 | body | A girl walks up and smiles at me, she asks, "You train alone?" | 150.80–155.02 (4.22s) | 63 trim 2.24s · 64 trim 1.98s | 1.00 (first 2.24s) · 1.00 (first 1.98s) |
| 31 | body | My first big order comes in, I launched my shop last week | 155.02–159.55 (4.53s) | 65 trim 2.26s · 66 trim 2.27s | 1.00 (first 2.26s) · 1.00 (first 2.27s) |
| 32 | body | Week 4, we're laughing, walking hand in hand along the street | 159.55–163.84 (4.29s) | 67 trim 2.17s · 68 trim 2.12s | 1.00 (first 2.17s) · 1.00 (first 2.12s) |
| 33 | body | You stop and stare, say "Is that you?" I smile, "I'm doing fine" | 163.84–168.04 (4.20s) | 69 trim 2.13s · 70 trim 2.07s | 1.00 (first 2.13s) · 1.00 (first 2.07s) |
| 34 | body | "Hope you're doing well." We laugh and walk away, her hand in mine | 168.04–173.67 (5.63s) | 71 slow 3.30s · 72 trim 2.33s | 0.82 · 1.00 (first 2.33s) |
| 35 | body | Now I see what's right in front of me, and what I want my life to be | 180.58–184.96 (4.38s) | 73 trim 2.44s · 74 trim 1.94s | 1.00 (first 2.44s) · 1.00 (first 1.94s) |
| 36 | body | I'm making plans and keeping them, I'm moving like I'm free | 184.96–189.39 (4.43s) | 75 slow 2.50s · 76 trim 1.93s | 0.82 · 1.00 (first 1.93s) |
| 37 | cta | End the night with EIS, make a little room for me | 189.39–196.20 (6.81s) | 77 hold 2.86s · 78 hold 3.95s | 1.00 (first 2.86s) · 1.00 (first 3.95s) |

**Shot lengths:** 76 shots, every one ≥ 0.80 s (min 0.80, median 2.23, max 4.46). Hook shots: 0.95 · 1.02 · 0.86 · 1.14 | 0.84 · 1.49 · 1.06 · 0.80. Every cut is hard; there are no crossfades. There are no black frames: every 720p clip is scaled to cover 1080×1920 and centre-cropped, and the segments butt together frame-exact with nothing at the start or end.

## Song skips removed (original song time)
| # | removed | length | between |
|---|---|---|---|
| 1 | 35.05 → 37.63 | 2.58 s | line 8 "…and wonder why" → line 9 "You say you're tired…" |
| 2 | 56.45 → 64.15 | 7.70 s | line 12 "…I can't find my voice" → line 13 "I'm scrolling through your pictures…" |
| 3 | 119.69 → 129.43 | 9.74 s | line 24 "…one more thing is done" → line 25 "Week 2…" |
| 4 | 173.67 → 180.58 | 6.91 s | line 34 "…her hand in mine" → line 35 "Now I see…" |

Total removed: 26.93 s (196.20 s of song → 169.27 s ad). Each join has a 20 ms audio fade. **Listen to the four joins** to check the music lands cleanly on the beat. The song also has short breaths between lines (0.4–1.2 s), which stay in as phrasing. Those aren't instrumental stretches, and the picture keeps cutting through them.

## Clips to regenerate
| clip | line | reason |
|---|---|---|
| **48** | 22 "…I read and read some more" | Label small text is misspelled/garbled: the "Ayurvedic" script is mangled and the "15+ herbs" badge reads like "0997". Crimson, gold, white cap and "EIS PAIN RELIEF OIL" are correct, but under the brief's rule it's not used. **Not in the cut.** |
| **49** | 23 "Week 1, I warm it every night…" | Same small-text drift on the background bottle ("Ayurvedic" mangled, "250 ml"), and the bottle turns to its back panel mid-clip. **Not in the cut.** |

Clips 39, 40, 43, 77 and 78 pass the label check: crimson #770A08/#B31306, gold lettering, white cap, and "EIS / Ayurvedic / PAIN RELIEF OIL / 200 ml" readable. Clips 39 and 77 turn side-on mid-clip, so 39 plays whole (it ends front-facing) and 77 is cut after the label is front-facing again (from about 2.2 s). No product appears before clip 39.

## Missing shots (because of the two regenerates)
- **seg22** (line 22) runs on clip 47 alone (4.46 s, slow 1.10×). The "I read and read some more" beat (Raj reading the bottle) is missing until 48 is regenerated. Then the plan is `47 trim ~2.2 s · 48 hold`.
- **seg23** (line 23) runs on clip 50 alone (4.06 s, slow 1.00×). The "warm it every night" beat is missing until 49 is regenerated. Then the plan is `49 hold ~2.0 s · 50 trim`.

## Changes from the brief (and why)
1. **Clip 5 opens seg02 instead of closing the hook line.** Line 1 is sung in 3.7 s (seg01 = 3.97 s). Five shots of at least 0.8 s, all cut between words, don't fit. Four cuts on the phrases do: "I saw you in bed | with my best friend, | my eyes were | open wide", with clip 4's wide-eyed close-up on "open wide". Clip 5 (the pair caught under the duvet) opens seg02 on "Where was I?". All 8 hook clips are used, in order; the hook is seg01–02 = 8.16 s.
2. **CTA captions sit at y 0.42, not 0.70 (seg37 only).** On clips 77 and 78, y 0.70 lands right on "PAIN RELIEF" on the bottle, and the house rule says captions never cover the product label. y 0.42 sits on torsos, clear of faces and the bottle. Captions are at y 0.70 everywhere else. *The app's `captions.style.y` is global, so the plan JSON can't say this. If the app renders the plan as-is, those 4 chunks will sit on the label.*
3. **The logo sits at x 0.84, y 0.88 (bottom-right), not centred.** Centred at y 0.88 it covers the bottle's base on clip 78. C303 had no logo overlay, so there was no placement to copy. It's about 200 px across, pops in on the cut to clip 78 and holds to the end.
4. **No SFX.** There's no SFX file in Drive, and the brief made the clip-39 hit optional.

## Provisional / check on review
- **Trims keep the start of each clip** (the app contract has no trim-from-end). Where the payoff is late in a clip, the beat is softer than it could be: **clip 6** shows the intact photo (the crack starts after its 1.49 s), **clip 41** cuts before the golden glow (~3 s), and **clip 46** shows a partial red→gold. If the app gains a start offset, use 6 @1.6 s, 41 @1.8 s, 46 @1.8 s.
- **Caption sync:** chunks are timed from word timestamps and kept on screen at least 0.85 s by moving boundaries into the neighbouring chunk. On fast lines (4, 22, 32) a chunk can lead or trail the voice by up to about 0.3 s.
- **`captions.style.box` (rounded pill)** is new to the contract. The validator accepts it, but if the app's parser rejects `box`, the renderer needs pill support. The burned-in render already uses Pillow-drawn rounded pills, not ffmpeg or ASS boxes.
- **Hook headline:** C303 has no hook headline (see below), so I styled it in the house look: two stacked crimson pills, Montserrat ExtraBold 74 px, warm white with "best friend." in gold, centred at y 0.16, on screen 0–8.16 s (seg01 + seg02, as `hook1` + `hook1b` in the plan).
- **Logo source:** the round "EIS" mark from the Drive EIS folder. Swap `media/logo_src.png` if there's a newer brand file.

## vs C303 (reference, measured; style only, no C303 clips or timings used)
| | C303 (measured) | C304 |
|---|---|---|
| Pace | 77 shots in 128.3 s · median 1.47 s / mean 1.67 s (scene-cut `gt(scene,0.2)`) | 76 shots in 169.3 s · median 2.23 s / mean 2.23 s. Body shots are 2–2.5 s per the brief; the line map gives two clips per ~4.3 s line, so C304 can't go as fast as C303 without reusing clips. |
| Hook rhythm | 1.33 · 0.67 · 1.27 · 1.67 · 2.27… (4 fast shots in the first 5 s) | 0.95 · 1.02 · 0.86 · 1.14 · 0.84 · 1.49 · 1.06 · 0.80: same energy, every shot ≥ 0.8 s |
| Captions | Plain white bold sans, **no box**, yellow keyword, about y 0.82, 2–4 words per chunk, sentence case | The brief's EIS house look instead: crimson pill 88 %, warm-white Montserrat Bold 60 px, gold keyword, y 0.70, ≤ 22 chars, 120 ms pop-in. Chunking (2–4 words, one keyword) matches C303. |
| Hook headline | **None**; C303 opens on captions only | "My wife. / My best friend." at y 0.16, with captions running under it from the first word |
| End card | Bottle + herbs + family, held about 4.6 s on the song outro, **no logo overlay** | Clip 78 (bottle + herbs + family), 3.95 s, of which 1.6 s is held after the last word (≤ 2 s per brief). EIS logo at the bottom right. |
| Transitions | All hard cuts | All hard cuts; 59 (before → after) enters on a hard cut and plays whole |

## Files
- `edit-plan.json`: the plan · `C304-final.mp4`: the render (133 MB). **Not uploaded to Drive:** the Drive connector here only takes file content inline, and a 133 MB video can't go through it. The file was sent directly in the session; drop it into the `C304` folder.
- `handoff/clip-map.json` (78 clips, keyed by id) · `handoff/contact-sheets/N.jpg` (4 frames per clip, all reviewed)
- `handoff/transcript_raw.json` (Whisper) · `handoff/transcript.json` (aligned to the lyrics) · `handoff/song-timing.json` (skips) · `handoff/caption-chunks.json`
- `reference/C303-final.mp4`, `reference/c303_sheet.jpg`, `reference/c303_cuts.txt` (C303 scene cuts)
