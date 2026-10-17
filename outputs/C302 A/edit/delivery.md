# C302 A — delivery (edit-plan v1)

**Status: rendered as-is on request (2026-10-17)** → `renders/C302-A-V1.mp4` (4:16, 215 MB). It still has the blockers below:
the garbled labels on clip_25 / 26 / 28 / 31 / 60 are visible, and the song ends without the CTA lines.
Checks: 1080x1920 at 30 fps, H.264 High, yuv420p, AAC 48 kHz; video 256.167 s vs audio 256.149 s (under 1 frame); −14.0 LUFS, true peak −0.9 dBTP after AAC encoding;
blackdetect (d=0.05) found 0 black frames; moov before mdat (faststart). Not copied to Drive: no Drive for desktop here, and the Drive connector can't upload a file this size.

## Blockers

### 1. Product clips that failed label QC (regenerate)
| clip | what's wrong |
|---|---|
| clip_25 [P] | Garbled label: "DR. REHMAN'S", "PAIN RLLOIL", "PAIN RELLLEEF OIL", "AYUNYEEYC MBWCIEINE" |
| clip_26 [P] | Garbled label: "BAIN RELIEF" / "PAIN BELJEF" |
| clip_28 [P] | Wrong design and garbled: "ESSENTIALL & OF INDIA", garbled Devanagari lines, "10% MOH PIIE FREE"; no "Ayurvedic" line |
| clip_31 [P] | Wrong brand and text: "BIS", "Ayvvdedic PAIN RELEIF OIIL", "PAIN PELLEFF OIIL", "100 ml" |
| clip_56 [P] | Badge misspelled: "15+ AYUVVERS HERBS" (main label is fine) |
| clip_58 [P] | Garbled: "ESSNES OF WATORE", "NATURAL RELLET", badge "UPTO & 15% …" |
| clip_60 [P] | Misspelled: badge "AYURVEDIC MERRS", bottom line "REDULET INFLAMMATION"; the cap doubles during the zoom |

clip_38 and clip_39 pass: crimson-maroon and gold, white cap, "EIS · ESSENCE OF NATURE · Ayurvedic PAIN RELIEF OIL · 200 ml", all spelled correctly.
Note: clip_56 and clip_58 aren't in this cut anyway (see blocker 2).

### 2. The song (C302 A.mp3) stops after line 49
Whisper, run three times, plus per-window re-transcription, shows the song going straight from
"My nani walks in … come up smooth. Priya's face changed," to "that's a bonus, see, but it's not for her anymore. It's for me."
and ending at 296.9 s. **Lines 50–58 and the first part of 59 aren't sung:** the Priya/Kunal payoff
("Wow, you look really good" … "I needed to see me, clear"), the second product name, "Nine ninety-nine",
"Fifty percent off right now, cash on delivery", and "One bottle. That's all it took for me."
So the plan has 51 segments (lines 1–49, then "that's a bonus, see" over clip_59 and the last line over clip_60), and the ad runs **4:16**.
The offer overlays (50% OFF · CASH ON DELIVERY, ₹999, logo) still sit on the last two segments, but the sung CTA is missing.
Two other unsung bits: "in a warm til oil" (line 39) and "she couldn't move" (line 49). The captions show only what's sung.
**To fix:** regenerate the song so it includes lines 50–59 (or a version under 5 minutes with the CTA kept), or accept this shorter ending.

## Segment table
| # | role | line | vo in–out | shots + fit | stretch× |
|---|---|---|---|---|---|
| 01 | hook | My best friend Kunal walked into the Diwali night, | 8.77–13.53 (4.76s @ 0.00) | clip_1 slow 4.76s | 0.94 |
| 02 | hook | Priya on his arm, lifting her up in the camera light. And me? | 14.05–19.93 (5.88s @ 4.76) | clip_2 slow 5.88s | 1.17 |
| 03 | hook | I couldn't even bend to touch my nani's feet. | 23.17–27.57 (4.40s @ 10.64) | clip_3 slow 4.40s | 0.87 |
| 04 | hook | The only reason I held my head up on that street | 28.35–32.75 (4.40s @ 15.04) | clip_4 slow 4.40s | 0.87 |
| 05 | hook | was what my tailor gave me just the week before. So let me take it … | 32.75–41.67 (8.92s @ 19.44) | clip_5 slow 5.10s + clip_21 trim 3.82s | 1.01 / — |
| 06 | body | Me and Priya, six long years, never did get wed, "Let's wait till y… | 47.11–61.15 (14.04s @ 28.36) | clip_6 slow 8.00s + clip_1 slow 6.04s | 1.59 / 1.20 |
| 07 | body | paid her EMIs, double shifts, drove her papa, played my role. | 61.37–65.69 (4.32s @ 42.40) | clip_7 slow 4.32s | 0.86 |
| 08 | body | Planned every birthday while she "needed space," | 66.09–70.31 (4.22s @ 46.72) | clip_8 slow 4.22s | 0.84 |
| 09 | body | and how'd she pay me back? With my best friend's face. Kunal. My be… | 70.31–77.63 (7.32s @ 50.94) | clip_51 trim 3.60s + clip_9 trim 3.72s | — / — |
| 10 | body | Found out through his own sister in my DMs: "Bhai, I thought you sh… | 77.63–83.46 (5.83s @ 58.26) | clip_10 slow 5.83s | 1.16 |
| 11 | body | Three months later, she moved out the door. | 83.46–87.11 (3.65s @ 64.09) | clip_11 trim 3.65s | — |
| 12 | body | Four months on, I wasn't missing her anymore, I missed who I though… | 87.11–93.47 (6.36s @ 67.74) | clip_12 slow 6.36s | 1.26 |
| 13 | body | Mostly I was in pain, the kind no sleep could fix, | 96.79–100.78 (3.99s @ 74.10) | clip_13 trim 3.99s | — |
| 14 | body | thirty-six, but in the mirror I looked fifty, no tricks. | 100.78–105.65 (4.87s @ 78.09) | clip_14 slow 4.87s | 0.97 |
| 15 | body | Twelve-hour days on my bike, my back locked every dawn, | 106.07–110.02 (3.95s @ 82.96) | clip_15 trim 3.95s | — |
| 16 | body | my knees cracked on the stairs, every bit of me was gone. | 110.02–114.76 (4.74s @ 86.91) | clip_16 slow 4.74s | 0.94 |
| 17 | body | I tried it all: physio, the gym at six a.m., | 114.76–119.77 (5.01s @ 91.65) | clip_17 slow 5.01s | 0.99 |
| 18 | body | the belts, the sprays, the balms, I bought every one of them. | 120.07–124.51 (4.44s @ 96.66) | clip_18 slow 4.44s | 0.88 |
| 19 | body | Painkillers till my stomach burned, the ache came right back. | 125.35–128.98 (3.63s @ 101.10) | clip_19 trim 3.63s | — |
| 20 | body | My body gave up on me the same way Priya did, just like that. | 128.98–135.49 (6.51s @ 104.73) | clip_20 slow 6.51s | 1.29 |
| 21 | body | Then I'm at Iqbal chacha's for my Diwali kurta fit, | 141.25–145.55 (4.30s @ 111.24) | clip_21 slow 4.30s | 0.85 |
| 22 | body | twelve years he's stitched my clothes, he knows me every bit. | 145.95–150.29 (4.34s @ 115.54) | clip_22 slow 4.34s | 0.86 |
| 23 | body | Mid-measurement he says, "Stand straight." I can't. He stops. | 150.87–154.24 (3.37s @ 119.88) | clip_29 trim 3.37s | — |
| 24 | body | "What's going on with you?" Right there, tears dropped. | 154.24–158.20 (3.96s @ 123.25) | clip_24 trim 3.96s | — |
| 25 | body | Under his counter, he pulled out a bottle with herbs on it. | 158.20–161.66 (3.46s @ 127.21) | clip_25 [P] hold 3.46s | — |
| 26 | body | "My client who's a physiotherapist put me onto this. | 161.66–165.14 (3.48s @ 130.67) | clip_26 [P] hold 3.48s | — |
| 27 | body | Not those sprays, not the YouTube nuskhe, no, fifteen Ayurvedic her… | 165.14–172.10 (6.96s @ 134.15) | clip_27 slow 6.96s | 1.38 |
| 28 | body | "Chacha, I'm not spending more on something that does nothing." | 172.10–175.91 (3.81s @ 141.11) | clip_28 [P] hold 3.81s | — |
| 29 | body | He looked me dead in the eyes: "If it doesn't work, your stitching'… | 176.13–181.13 (5.00s @ 144.92) | clip_29 slow 5.00s | 0.99 |
| 30 | body | Twelve years, never one rupee off. | 181.41–184.13 (2.72s @ 149.92) | clip_30 trim 2.72s | — |
| 31 | body | So I took it home, rubbed it in every night before bed. | 184.87–188.66 (3.79s @ 152.64) | clip_31 [P] hold 3.79s | — |
| 32 | body | A week in, I texted him, "Why is this working?" I said, | 188.66–192.39 (3.73s @ 156.43) | clip_32 trim 3.73s | — |
| 33 | body | "when nothing else did?" And he wrote back: "Because it was never j… | 192.39–199.46 (7.07s @ 160.16) | clip_33 trim 3.62s + clip_16 trim 3.45s | — / — |
| 34 | body | Twelve hours on that bike and all that stress, your muscles stayed … | 199.46–204.80 (5.34s @ 167.23) | clip_34 slow 5.34s | 1.06 |
| 35 | body | Sprays sit on the skin, an hour later they're gone, | 204.80–207.08 (2.28s @ 172.57) | clip_35 trim 2.28s | — |
| 36 | body | warm oil massaged in slow gets down where it's wrong. No oil fixes … | 207.08–211.90 (4.82s @ 174.85) | clip_36 slow 4.82s | 0.96 |
| 37 | body | but sleeping without pain is a good start for you." | 211.90–215.23 (3.33s @ 179.67) | clip_13 trim 3.33s | — |
| 38 | body | It's called EIS Ayurvedic Pain Relief Oil, | 215.83–220.40 (4.57s @ 183.00) | clip_38 [P] hold 4.57s | — |
| 39 | body | Mahanarayan, Nirgundi, Ashwagandha, | 221.05–224.17 (3.12s @ 187.57) | clip_39 [P] hold 3.12s | — |
| 40 | body | Week one, I slept straight through the night. Week two, the morning… | 224.93–234.31 (9.38s @ 190.69) | clip_37 slow 4.40s + clip_40 slow 4.98s | 0.87 / 0.99 |
| 41 | body | Week three, the stairs stopped scaring me. | 234.31–238.61 (4.30s @ 200.07) | clip_41 slow 4.30s | 0.85 |
| 42 | body | A month in, cross-legged at puja, I got up free, didn't even hold t… | 238.89–245.92 (7.03s @ 204.37) | clip_32 slow 7.03s | 1.39 |
| 43 | body | Six weeks in, the society match, twenty overs, played it all. Not t… | 245.92–255.49 (9.57s @ 211.40) | clip_4 slow 4.80s + clip_14 slow 4.77s | 0.95 / 0.95 |
| 44 | body | The me I was supposed to be. | 257.80–262.25 (4.45s @ 220.97) | clip_44 slow 4.45s | 0.88 |
| 45 | body | Next society function, first one on the floor, in that same Diwali … | 266.16–274.28 (8.12s @ 225.42) | clip_45 slow 4.06s + clip_52 slow 4.06s | 0.81 / 0.81 |
| 46 | body | Nothing extra. No belt. No painkiller. | 274.28–278.16 (3.88s @ 233.54) | clip_46 trim 3.88s | — |
| 47 | body | And there's Priya. Kunal next to her. | 278.16–283.85 (5.69s @ 237.42) | clip_47 slow 5.69s | 1.13 |
| 48 | body | My nani walks in, I bend, touch her feet, come up smooth. | 283.85–288.07 (4.22s @ 243.11) | clip_48 slow 4.22s | 0.84 |
| 49 | body | Priya's face changed, | 288.61–290.65 (2.04s @ 247.33) | clip_49 trim 2.04s | — |
| 50 | cta | that's a bonus, see, | 290.65–292.57 (1.92s @ 249.37) | clip_59 trim 1.92s | — |
| 51 | cta | but it's not for her anymore. It's for me. | 292.57–297.45 (4.88s @ 251.29) | clip_60 [P] hold 4.88s | — |


Total: 256.17s (51 segments). Hook = seg01–05 (28.4 s, 6 shots). CTA = seg50–51 (6.8 s, ending on a hold on clip_60).
"Stretch×" is shown for `slow` shots; `trim`/`hold` play at normal speed (— = clip is longer than the shot).

## Song skips (instrumental removed)
| skip | original range | length | where |
|---|---|---|---|
| intro | 0.00–8.77 | 8.77s | before seg01 |
| 1 | 13.53–14.05 | 0.52s | seg01 → seg02 |
| 2 | 19.93–23.17 | 3.24s | seg02 → seg03 |
| 3 | 27.57–28.35 | 0.78s | seg03 → seg04 |
| 4 | 41.67–47.11 | 5.44s | seg05 → seg06 |
| 5 | 61.15–61.37 | 0.22s | seg06 → seg07 |
| 6 | 65.69–66.09 | 0.40s | seg07 → seg08 |
| 7 | 93.47–96.79 | 3.32s | seg12 → seg13 |
| 8 | 105.65–106.07 | 0.42s | seg14 → seg15 |
| 9 | 119.77–120.07 | 0.30s | seg17 → seg18 |
| 10 | 124.51–125.35 | 0.84s | seg18 → seg19 |
| 11 | 135.49–141.25 | 5.76s | seg20 → seg21 |
| 12 | 145.55–145.95 | 0.40s | seg21 → seg22 |
| 13 | 150.29–150.87 | 0.58s | seg22 → seg23 |
| 14 | 175.91–176.13 | 0.22s | seg28 → seg29 |
| 15 | 181.13–181.41 | 0.28s | seg29 → seg30 |
| 16 | 184.13–184.87 | 0.74s | seg30 → seg31 |
| 17 | 215.23–215.83 | 0.60s | seg37 → seg38 |
| 18 | 220.40–221.05 | 0.65s | seg38 → seg39 |
| 19 | 224.17–224.93 | 0.76s | seg39 → seg40 |
| 20 | 238.61–238.89 | 0.28s | seg41 → seg42 |
| 21 | 255.49–257.80 | 2.31s | seg43 → seg44 |
| 22 | 262.25–266.16 | 3.91s | seg44 → seg45 |
| 23 | 288.07–288.61 | 0.54s | seg48 → seg49 |
| outro | 297.45–300.04 | 2.59s | after seg51 |


Every skip is a hard audio join (8 ms fades). The short ones (0.22–0.84 s) are between-line gaps just over the 0.8 s rule: **listen to the joins and check they land on the beat**.
The end has a 0.3 s fade because the reverb tail continues to 298.7 s.

Kept on purpose: short breaths **inside** a line (line 5 "before → So" 0.9 s, line 6 "wed → Let's" 1.0 s, line 40 "night → Week two" 0.9 s,
"anymore → It's for me" in the last line). A segment has one VO range, so they can't be cut without splitting the line.
Two longer instrumentals inside lines were handled by moving a phrase across the cut:
- "And me?" (line 3) closes seg02, because there's 3.2 s of instrumental before "I couldn't even bend".
- "Not the old me." (line 44) closes seg43, because there's 2.3 s of instrumental before "The me I was supposed to be". The clip_44 morph enters on a hard cut on that line.

## Missing shots / workarounds
- **seg23** (Stand straight / I can't): clip_23 is flagged, so it's covered by clip_29 (trim, Iqbal raising a finger as he speaks). Swap in a regenerated clip_23.
- **seg42** (cross-legged at puja / got up free): clip_42 is flagged. It's a single shot of clip_32 at 1.39× (happy at home, before-look) and needs a second shot. Swap in a regenerated clip_42.
- **seg43** (society match / twenty overs): clip_43 is flagged. Stand-ins are clip_4 (walking head-up) and clip_14 (old self in the mirror, under "Not the old me"). No cricket shot until clip_43 is regenerated.
- Reused once, ≥10 s after the first use ends, never in adjacent segments: clip_1 (seg06, the irony beat "And I believed her" over Priya in Kunal's arms), clip_21 (seg05 "my tailor"), clip_13 (seg37), clip_16 (seg33 "never just your back"), clip_29 (seg23, stand-in), clip_32 (seg42, stand-in), clip_4 + clip_14 (seg43, stand-ins).
- Unused clips (no audio for their lines) used as first-use second shots: clip_51 (seg09 "my best friend's face"), clip_52 (seg45 "standing tall").

## Clips to regenerate
- [P] clip_25, clip_26, clip_28, clip_31, clip_60 (label). clip_56 and clip_58 also fail, but they're only needed if the song gets its CTA back.
- clip_23: Arjun's face changed (younger, clean-shaven, shaggy hair, cream shirt + jeans instead of the blue shirt).
- clip_42: two Arjuns in frame (one sitting at the puja, one standing behind him).
- clip_43: the batsman turns into a different man after about 2.5 s (sharper jaw, no mole).
- Minor, kept: clip_36's mechanism opens on an elderly couple who aren't Iqbal; frames 3–4 are pure CGI.
- Checks that passed: no product before clip_25; Arjun's mole stays on the same cheek in every close-up I checked (clips 1, 6, 10, 28, 30, 46, 55, 56); the after-look (beard, cream kurta) appears only from clip_44 on.

## Provisional
- **Timings** come from faster-whisper large-v3 with word timestamps (three passes plus isolated re-alignment windows), and the lyric map is aligned word by word (`handoff/transcript.json`).
  Re-aligned line starts: line 2 "Priya" 14.30 (whisper smeared it from 13.30), line 5 "was" ≈33.0 (energy dip, smeared 32.36–34.04), line 10 "Found" 77.74, line 39 "Mahanarayan" ≈221.3 (energy),
  line 41 "Week" 234.46, line 44 "The" ≈258.05. Interpolated words (not recognised): "EMIs", "Bhai", "balms", "the ache", "Diwali kurta", "nuskhe", "Chacha", "week in", "when", "puja".
- **Captions:** 209 pills, text from the lyric map (never whisper), "E-I-S" shown as "EIS", with no gap from 0.00 s to the last word. Every chunk is at least 0.85 s, except seg35
  ("Sprays sit on the skin, an hour later they're gone", sung in 2.3 s), where three chunks get 0.76 s each, because the 22-character limit makes two chunks impossible.
- **Caption position on [P] shots** (renderer setting `tools/render-config.json → captionY`; the app contract has no per-segment caption y):
  clip_28 / clip_31 0.90, clip_38 0.92, clip_39 0.91 (below the bottle), clip_60 0.19 (above the bottle, under the offer text).
  **Conflict:** the ₹999 (y 0.80) and logo (y 0.88) positions you gave sit on the lower part of the clip_60 label (the "RELIEVES PAIN…/200 ml" band). They follow the brief as given; say if they should move.
- **CTA text** "50% OFF · CASH ON DELIVERY" is 26 characters (the contract limit is 24). It's your exact wording, so the validator warning stands.
- **`captions.style.box`** (pill) is new to the contract. The validator accepts it, but the app's parser may not; the external renderer (`tools/render.py`) draws the pills.
- **SFX:** no whoosh/shimmer file was supplied, so `sfx` is empty. To add one, drop `media/whoosh.wav` and add `{"file":"whoosh.wav","segment":"seg38","at":0.0,"gainDb":-6}`.
- **Logo:** there was no logo.png in the C302 A folder. `media/logo.png` is the EIS roundel from Drive → EIS → file "3" (peach disc, "EIS"), cut out as a transparent circle.
- **motion-prompts.json** wasn't in the Drive folder either, so the clip descriptions in `handoff/clip-map.json` are blank and the QC is from the contact sheets.

## Validator
`validate_plan.py edit-plan.json --clip-map handoff/clip-map.json` → **OK, 0 errors**. Remaining warnings, all expected:
- V2 missing (one output by design), and vo not contiguous ×21 (the song skips above)
- captions overlap hook1 (captions under the hook are required)
- hook per segment < 7 s (the hook is 5 lyric segments, 28.4 s in total) and seg50 CTA 1.9 s (the CTA is seg50 + seg51 = 6.8 s; the song has no more CTA lines)
- seg42 single shot (missing shot above), seg35 captions 0.76 s (above), CTA text 26 characters (above)

## Render (when unblocked)
From `outputs/C302 A/edit/`:
```
python3 tools/build_plan.py            # rebuilds edit-plan.json from transcript + chunks + tools/shots.json
python3 <editing-brain>/scripts/validate_plan.py edit-plan.json --clip-map handoff/clip-map.json
python3 tools/render.py edit-plan.json # -> ../renders/C302-A-V1.mp4
```
The renderer makes 1080x1920 at 30 fps, H.264 High, CRF 18, yuv420p, AAC 48 kHz at 192k, with +faststart. Clips are scaled 716x1284 → 1080x1920 with lanczos and cropped to fill the frame.
Every shot has an exact frame count, and a short clip freezes its last frame (tpad clone), so there's never a black frame. Clip audio is stripped, and the song is loudnorm two-pass to −14 LUFS / −1 dBTP.
Pills are Montserrat Bold 60 px #FFF8EE on #770A08 at 88 %, radius = half the height, soft shadow, gold highlight, 120 ms pop-in.
A 25 s excerpt test render (seg01–02, 38–39, 50–51) measured 1080x1920, 30 fps, High, −14.0 LUFS, video 25.133 s vs audio 25.130 s, with no blackdetect hits.
If the song is regenerated, re-run whisper + `tools/align.py`, then check the `START_FIX` / `WORD_SET` / `SEGMENTS` notes in `tools/build_plan.py`.
