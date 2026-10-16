# C300-W — "Just Tired" (Wife version) · EIS Ayurvedic Pain Relief Oil · FINAL (cut to B.mp3 as sung)

**Deliverable:** `renders/C300-W-final.mp4`. That file isn't in git; the delivery link is in the reply. Specs: 1080×1920, 30 fps, H.264 CRF 20 preset slow, AAC 192 kbps, +faststart. Duration __DUR__ s against B.mp3's 229.04 s. One file only: no SFX, no music bed, no other versions.
**Audio:** B.mp3, unedited, 0.00 to the end. The song sings different lyrics from the original C300-W lyric sheet, so every caption follows what B.mp3 actually sings (`handoff/transcript.json`, whisper medium.en). The onsets were cross-checked against a second whisper pass and the vocal-band energy.
**Plan:** `edit-plan.json` v1 has 56 segments and V1 only. The validator passes; its warnings are listed below. `handoff/build_c300w.py` renders the MP4, and `handoff/c300w.ass` holds the captions and text overlays.

## Section → clip map
| section | time (s) | sung | clips |
|---|---|---|---|
| Intro + hook | 0.00–11.00 | "I kept this close, so close to my heart" | 1, 2 (hook1 "SHE WAS HIDING SOMETHING" 0–7 s, no captions under it) |
| Verse 1 + pre-chorus | 11.00–64.85 | "Every evening I come home smiling … Afraid of what comes into view" | 3–17 |
| Chorus 1 + instrumental | 64.85–100.85 | "I'm just tired, ji … And I need you to see me true" | 18–29 (23–26 = terrace call: "As you hear my voice shake…", 27–29 curtain / hallway / dawn chai over the instrumental) |
| Verse 2 | 100.85–128.50 | "You found a letter on the table / And the colour left your face …" | **30 (first 1.15 s) → 31 strips → 32 "since when"** on found / colour / hurt; 33 knee reveal, 34, 35 |
| Bridge (turn) | 128.50–147.78 | "I never meant to break your trust … worn my voice away" | crossfade 0.4 s → 36, 37 (comes home), **56 bottle reveal**, 40 |
| Chorus 2 | 147.78–181.20 | "I'm just tired, ji / Tired of living half a life … Please hear me before we say goodbye" | 41, 42, 43 (first 1.2 s + freeze), 44, 45, 46, **47 morph in full (hard cut, slow 1.55×)**, 48 |
| Ending | 181.20–222.03 | "Maybe love can hold the fracture … We can learn to breathe again tonight" | 49, 50, 51, 52 (quilt), 53 (chai), 54 (terrace), 51↺, 49↺, 55 |
| CTA end card | 222.03–229.04 | "Stay with me now, let us begin again" | 56 slow 1.39× push-in (7.01 s) + logo + "50% OFF TODAY" + "CASH ON DELIVERY · 30-day guarantee" |

**Why the sections don't split exactly as briefed (1–11 verse / 12–22 choruses):** "You found a letter" is sung at 100.85 s, so for 30–32 to land on it, all of clips 1–29 have to fit before 100.85 s. The verse therefore carries 1–17 (one clip per sung line), and chorus 1 carries 18–29.

## Clip decisions
- **Avoided completely:** clip_38 (garbled label: "Ayuvedic", "ESSNSE OF WOEOA", "16x STEENETH"), clip_39 (brand reads "BIS") and clip_57 (garbled label: "Ayrereeic", "270 ml").
- **clip_56** is used twice: as the bottle reveal (137.10 s, where 38 would have gone) and as the CTA end card. The two uses are 85 s apart.
- **clip_43:** shows 0–1.2 s, then freezes on a fully frontal, clean label. The first render froze at 1.9 s; QA caught that the bottle had already turned and the label read "IN RELIEF", so I re-rendered it.
- **clip_42:** the bottle is a small prop on the nightstand; its label is fine.
- **clip_30:** shows only 1.15 s of the wide start (the husband's face drifts to a beardless close-up later in the clip).
- **clip_10:** shows only 3.20 s (the bed warps from 4.0 s).
- **clip_46:** shows only 2.77 s, before her hand grips the rail (~3.0 s).
- **Reuses (fill time, never adjacent):** clip_51 (188.63 and 208.43 s) and clip_49 (181.20 and 211.82 s). Both are after-state shots.
- **Product placement:** no product shows before the "he comes home" beat (clip_37). clip_42 at 151.96 s is the first product after the reveal.
- **Frame fill:** every clip is scaled to fill 1080×1920 and centre-cropped (716×1284 → 1080×1937, 17 px cropped). Nothing is padded.
- **Transitions:** one crossfade (0.4 s) into clip_36; every other cut is hard, the morph included.
- **Fit:** `slow` where the key moment is at the end (31, 33, 47, 52, the CTA push-in, plus the hook and longer lines), never past 1.6×. Everything else is `trim`.

## Text
- **Captions** (.ass, burned in): Poppins Bold 58 px, cream #FFF4E0 on a solid crimson #770A08 box (BorderStyle 3), one gold #D4A23A keyword per chunk. Up to 2 lines / ≤44 chars, centred at 72% height. No chunk is shorter than 2.27 s. "ji" is spelled "ji", and the song's "color" is written "colour".
- **Overlays:**
  - hook1, 0–7 s: "SHE WAS HIDING SOMETHING" (y 0.16).
  - Bottle reveal, 137.3–142.6 s: "EIS AYURVEDIC / PAIN RELIEF OIL" (top) + "15+ Ayurvedic herbs" (gold, y 0.85).
  - Over clips 40–41, 142.8–152.0 s: "Tablets mask it. / Sprays sit on the skin."
  - Over clips 42–43, 152.1–158.6 s: "10 minutes of warm / massage before bed".
- **CTA:** EIS logo (the Supabase URL; Drive has no EIS logo), "50% OFF TODAY" (gold, top) and "CASH ON DELIVERY · 30-day guarantee" (y 0.85). The text bands don't overlap the captions.

## QA
__QA__

## Validator warnings (expected)
- seg45 (clip_47 morph, 7.8 s) and seg56 (CTA, 7.0 s) have one shot each. That's by design: the morph plays in full, and the end card is a single push-in.
- Captions that span a segment cut are split in the JSON. That produces two 0.5 s items, which play as one continuous chunk in the render.
- The overlay text is longer than the contract's headline/sub limits. It is wrapped onto two lines in the render.
- "V2 is missing" (one output by design).
- **Stage 4 can't fully reproduce this plan:** the contract has no freeze-at-in-point, so clip_43 is written as `trim` in `edit-plan.json`, which would show the turning label. The MP4 is the reference.

## Shot table
| # | time (s) | dur | clip | fit | sung over it |
|---|---|---|---|---|---|
| 01 | 0.00–5.76 | 5.76 | clip_1 | slow 1.14× | (intro) |
| 02 | 5.76–11.00 | 5.24 | clip_2 | slow 1.04× | I kept this close, so close to my heart |
| 03 | 11.00–15.70 | 4.70 | clip_3 | trim, first 4.70 s | I kept this close, so close to my heart |
| 04 | 15.70–20.30 | 4.60 | clip_4 | trim, first 4.60 s | (instrumental) |
| 05 | 20.30–23.00 | 2.70 | clip_5 | trim, first 2.70 s | Every evening I come home smiling |
| 06 | 23.00–26.80 | 3.80 | clip_6 | trim, first 3.80 s | And I set my face like nothing's wrong |
| 07 | 26.80–30.45 | 3.65 | clip_7 | trim, first 3.65 s | You ask me, how was your day, ji? |
| 08 | 30.45–33.50 | 3.05 | clip_8 | trim, first 3.05 s | And I say fine, though I know it's not |
| 09 | 33.50–36.90 | 3.40 | clip_9 | trim, first 3.40 s | There is a room inside my chest |
| 10 | 36.90–40.10 | 3.20 | clip_10 | trim, first 3.20 s | Where I keep the words I never said |
| 11 | 40.10–43.45 | 3.35 | clip_11 | trim, first 3.35 s | I wanted peace, I wanted time |
| 12 | 43.45–48.00 | 4.55 | clip_12 | trim, first 4.55 s | I thought the truth could wait a while |
| 13 | 48.00–51.70 | 3.70 | clip_13 | trim, first 3.70 s | But the silence has a way tonight |
| 14 | 51.70–55.20 | 3.50 | clip_14 | trim, first 3.50 s | And it follows me from room to room |
| 15 | 55.20–59.60 | 4.40 | clip_15 | trim, first 4.40 s | I stand at the edge of my own reply |
| 16 | 59.60–61.40 | 1.80 | clip_16 | trim, first 1.80 s | Afraid of what comes into view |
| 17 | 61.40–64.85 | 3.45 | clip_17 | trim, first 3.45 s | Afraid of what comes into view |
| 18 | 64.85–68.65 | 3.80 | clip_18 | trim, first 3.80 s | I'm just tired, ji |
| 19 | 68.65–72.46 | 3.81 | clip_19 | trim, first 3.81 s | Tired of holding what I can't undo |
| 20 | 72.46–75.40 | 2.94 | clip_20 | trim, first 2.94 s | I'm just tired, ji |
| 21 | 75.40–78.60 | 3.20 | clip_21 | trim, first 3.20 s | Tired of pretending I can choose |
| 22 | 78.60–82.04 | 3.44 | clip_22 | trim, first 3.44 s | As you hear my voice shake a little |
| 23 | 82.04–85.84 | 3.80 | clip_23 | trim, first 3.80 s | It's because I'm finally letting through |
| 24 | 85.84–88.54 | 2.70 | clip_24 | trim, first 2.70 s | I'm just tired, ji |
| 25 | 88.54–91.00 | 2.46 | clip_25 | trim, first 2.46 s | And I need you to see me true |
| 26 | 91.00–94.20 | 3.20 | clip_26 | trim, first 3.20 s | And I need you to see me true |
| 27 | 94.20–96.70 | 2.50 | clip_27 | trim, first 2.50 s | (instrumental) |
| 28 | 96.70–98.90 | 2.20 | clip_28 | trim, first 2.20 s | (instrumental) |
| 29 | 98.90–100.85 | 1.95 | clip_29 | trim, first 1.95 s | (instrumental) |
| 30 | 100.85–102.00 | 1.15 | clip_30 | trim, first 1.15 s | You found a letter on the table |
| 31 | 102.00–107.05 | 5.05 | clip_31 | slow 1.00× | You found a letter on the table / And the colour left your face |
| 32 | 107.05–113.75 | 6.70 | clip_32 | slow 1.33× | I saw the hurt before the question / It was standing in the space |
| 33 | 113.75–120.22 | 6.47 | clip_33 | slow 1.28× | I meant to tell you in the morning / But my courage failed again |
| 34 | 120.22–123.67 | 3.45 | clip_34 | trim, first 3.45 s | Now the truth is in the light |
| 35 | 123.67–128.50 | 4.83 | clip_35 | slow 0.96× | And I cannot hide from it, my friend |
| 36 | 128.50–132.30 | 3.80 | clip_36 | trim, first 3.80 s | And I cannot hide from it, my friend |
| 37 | 132.30–137.10 | 4.80 | clip_37 | trim, first 4.80 s | I never meant to break your trust |
| 38 | 137.10–142.62 | 5.52 | clip_56 | slow 1.09× | I never meant to turn away / But carrying this alone |
| 39 | 142.62–147.78 | 5.16 | clip_40 | slow 1.02× | has worn my voice away |
| 40 | 147.78–151.96 | 4.18 | clip_41 | slow 0.83× | I'm just tired, ji |
| 41 | 151.96–155.45 | 3.49 | clip_42 | trim, first 3.49 s | Tired of living half a life |
| 42 | 155.45–158.60 | 3.15 | clip_43 | first 1.2 s + freeze | I'm just tired, ji |
| 43 | 158.60–161.86 | 3.26 | clip_44 | trim, first 3.26 s | Tired of cutting truth to size |
| 44 | 161.86–166.50 | 4.64 | clip_45 | trim, first 4.64 s | If my eyes look like they are begging / It's because I don't know how to lie |
| 45 | 166.50–169.27 | 2.77 | clip_46 | trim, first 2.77 s | It's because I don't know how to lie |
| 46 | 169.27–177.10 | 7.83 | clip_47 | slow 1.55× | I'm just tired, ji / Please hear me before we say goodbye |
| 47 | 177.10–181.20 | 4.10 | clip_48 | trim, first 4.10 s | Please hear me before we say goodbye |
| 48 | 181.20–185.33 | 4.13 | clip_49 | slow 0.82× | Maybe love can hold the fracture |
| 49 | 185.33–188.63 | 3.30 | clip_50 | trim, first 3.30 s | Maybe truth can let us stay |
| 50 | 188.63–191.82 | 3.19 | clip_51 | trim, first 3.19 s | If we walk through this together |
| 51 | 191.82–197.90 | 6.08 | clip_52 | slow 1.21× | We may find a kinder way |
| 52 | 197.90–201.62 | 3.72 | clip_53 | trim, first 3.72 s | I'm just tired, ji |
| 53 | 201.62–208.43 | 6.81 | clip_54 | slow 1.35× | But I am still here by your side / I'm just tired, ji |
| 54 | 208.43–211.82 | 3.39 | clip_51 | trim, first 3.39 s | And I wanna make this right |
| 55 | 211.82–215.28 | 3.46 | clip_49 | trim, first 3.46 s | If you can hold my hand for one more moment |
| 56 | 215.28–222.03 | 6.75 | clip_55 | slow 1.34× | We can learn to breathe again tonight / I'm just tired, ji |
| 57 | 222.03–229.04 | 7.01 | clip_56 | slow 1.39× | Stay with me now, let us begin again |
