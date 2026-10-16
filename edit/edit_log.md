# C299-B — edit log

Source clips: 61 × Kling, 716×1284 @ 24 fps, 121 frames (5.042 s each). Scaled to 1080×1920 with lanczos, filled by scale + centre crop (≈8 px off top and bottom), no padding. Output 30 fps. Line timing comes from faster-whisper large-v3 word timestamps, fuzzy-aligned to the lyric map; the lyric text on screen is always the map text.

Fit rule: T ≤ L → keep the first T s · L < T ≤ 1.5L → slow to T (setpts, no blending) · T > 1.5L → slow ×1.5 then hold the last frame.

| Line | Clip(s) | Start | End | Target T | Frames | Action | Caption position | Flags |
|---|---|---|---|---|---|---|---|---|
| 01 | clip_1 | 0.000 | 5.800 | 5.800s | 174 | slow ×1.150 | standard (y≈1300) | singing starts at 3.22s; 0–3.22s is the music intro and clip_1 covers it (no caption until the first word) |
| 02 | clip_2 | 5.800 | 8.840 | 3.040s | 91 | trim to first 3.03s | standard (y≈1300) |  |
| 03 | clip_3 | 8.840 | 11.300 | 2.460s | 74 | trim to first 2.47s | low (box bottom at y=1450, close-up) |  |
| 04 | clip_4 | 11.300 | 21.280 | 9.980s | 299 | slow ×1.5 + hold last frame 2.40s | standard (y≈1300) | freeze-frame hold 2.40s |
| 05 | clip_5 | 21.280 | 24.720 | 3.440s | 104 | trim to first 3.47s | standard (y≈1300) |  |
| 06 | clip_6 | 24.720 | 30.920 | 6.200s | 186 | slow ×1.230 | standard (y≈1300) |  |
| 07 | clip_7 | 30.920 | 35.660 | 4.740s | 142 | trim to first 4.73s | standard (y≈1300) |  |
| 08 | clip_8 | 35.660 | 47.320 | 11.660s | 350 | slow ×1.5 + hold last frame 4.10s | standard (y≈1300) | freeze-frame hold 4.10s |
| 09 | clip_9 | 47.320 | 49.820 | 2.500s | 75 | trim to first 2.50s | standard (y≈1300) |  |
| 10 | clip_10 | 49.820 | 52.640 | 2.820s | 84 | trim to first 2.80s | standard (y≈1300) |  |
| 11 | clip_11 | 52.640 | 55.560 | 2.920s | 88 | trim to first 2.93s | standard (y≈1300) |  |
| 12 | clip_12 | 55.560 | 58.420 | 2.860s | 86 | trim to first 2.87s | standard (y≈1300) |  |
| 13 | clip_13 | 58.420 | 62.040 | 3.620s | 108 | trim to first 3.60s | standard (y≈1300) |  |
| 14 | clip_14 | 62.040 | 69.200 | 7.160s | 215 | slow ×1.421 | standard (y≈1300) |  |
| 15 | clip_15 | 69.200 | 72.400 | 3.200s | 96 | trim to first 3.20s | standard (y≈1300) |  |
| 16 | clip_16 | 72.400 | 82.760 | 10.360s | 311 | slow ×1.5 + hold last frame 2.80s | standard (y≈1300) | freeze-frame hold 2.80s |
| 17 | clip_17 | 82.760 | 85.260 | 2.500s | 75 | trim to first 2.50s | standard (y≈1300) |  |
| 18 | clip_18 | 85.260 | 89.220 | 3.960s | 119 | trim to first 3.97s | standard (y≈1300) |  |
| 19 | clip_19 | 89.220 | 92.380 | 3.160s | 94 | trim to first 3.13s | standard (y≈1300) |  |
| 20 | clip_20 | 92.380 | 98.580 | 6.200s | 186 | slow ×1.230 | standard (y≈1300) |  |
| 21 | clip_21 | 98.580 | 102.080 | 3.500s | 105 | trim to first 3.50s | standard (y≈1300) |  |
| 22 | clip_22 | 102.080 | 106.080 | 4.000s | 120 | trim to first 4.00s | standard (y≈1300) |  |
| 23 | clip_23 | 106.080 | 110.200 | 4.120s | 124 | trim to first 4.13s | standard (y≈1300) |  |
| 24 | clip_24 | 110.200 | 116.160 | 5.960s | 179 | slow ×1.183 | standard (y≈1300) |  |
| 25 | clip_25 | 116.160 | 118.900 | 2.740s | 82 | trim to first 2.73s | top (y≈330, product) |  |
| 26 | clip_26 | 118.900 | 122.140 | 3.240s | 97 | trim to first 3.23s | standard (y≈1300) |  |
| 27 | clip_27 | 122.140 | 124.920 | 2.780s | 84 | trim to first 2.80s | top (y≈330, product) |  |
| 28 | clip_28 | 124.920 | 127.560 | 2.640s | 79 | trim to first 2.63s | standard (y≈1300) |  |
| 29 | clip_29 | 127.560 | 130.500 | 2.940s | 88 | trim to first 2.93s | top (y≈330, product) |  |
| 30 | clip_30 | 130.500 | 133.240 | 2.740s | 82 | trim to first 2.73s | top (y≈330, product) |  |
| 31 | clip_31 | 133.240 | 138.600 | 5.360s | 161 | slow ×1.064 | top (y≈330, product) |  |
| 32 | clip_32 | 138.600 | 141.500 | 2.900s | 87 | trim to first 2.90s | standard (y≈1300) |  |
| 33 | clip_33 | 141.500 | 146.540 | 5.040s | 151 | trim to first 5.03s | standard (y≈1300) |  |
| 34 | clip_34 | 146.540 | 149.320 | 2.780s | 84 | trim to first 2.80s | standard (y≈1300) |  |
| 35 | clip_35 | 149.320 | 152.180 | 2.860s | 85 | trim to first 2.83s | standard (y≈1300) |  |
| 36 | clip_36 | 152.180 | 154.800 | 2.620s | 79 | trim to first 2.63s | standard (y≈1300) |  |
| 37 | clip_37 | 154.800 | 159.860 | 5.060s | 152 | slow ×1.005 | standard (y≈1300) |  |
| 38 | clip_38 | 159.860 | 162.680 | 2.820s | 84 | trim to first 2.80s | standard (y≈1300) |  |
| 39 | clip_39 | 162.680 | 165.220 | 2.540s | 77 | trim to first 2.57s | standard (y≈1300) |  |
| 40 | clip_40 | 165.220 | 167.980 | 2.760s | 82 | trim to first 2.73s | standard (y≈1300) | 6-frame crossfade in from line 39 |
| 41 | clip_41 | 167.980 | 170.960 | 2.980s | 90 | trim to first 3.00s | standard (y≈1300) |  |
| 42 | clip_42 | 170.960 | 173.640 | 2.680s | 80 | trim to first 2.67s | standard (y≈1300) |  |
| 43 | clip_43 | 173.640 | 176.260 | 2.620s | 79 | trim to first 2.63s | standard (y≈1300) |  |
| 44 | clip_44 | 176.260 | 179.080 | 2.820s | 84 | trim to first 2.80s | standard (y≈1300) |  |
| 45 | clip_45 | 179.080 | 181.840 | 2.760s | 83 | trim to first 2.77s | standard (y≈1300) |  |
| 46 | clip_46 | 181.840 | 186.600 | 4.760s | 143 | trim to first 4.77s | low (box bottom at y=1450, close-up) |  |
| 47 | clip_47 | 186.600 | 189.320 | 2.720s | 82 | trim to first 2.73s | standard (y≈1300) |  |
| 48 | clip_48 | 189.320 | 191.980 | 2.660s | 79 | trim to first 2.63s | standard (y≈1300) |  |
| 49 | clip_49 | 191.980 | 194.460 | 2.480s | 75 | trim to first 2.50s | top (y≈330, product) |  |
| 50 | clip_50 | 194.460 | 196.760 | 2.300s | 69 | trim to first 2.30s | standard (y≈1300) |  |
| 51 | clip_51 | 196.760 | 199.540 | 2.780s | 83 | trim to first 2.77s | standard (y≈1300) |  |
| 52 | clip_52 | 199.540 | 199.940 | 0.400s | 12 | trim to first 0.40s | standard (y≈1300) | only 14% of the line's words are in the voiceover - timed on its first word; the voiceover sings only "Rohit" — "you look... what did you do?" is not in the audio; caption shows "Rohit" only |
| 53 | clip_53 + clip_54 | 199.940 | 201.900 | 1.960s | 59 | clip_53: trim to first 0.97s; clip_54: trim to first 1.00s | standard (y≈1300) | first word not matched - start backed off from first matched word (conf 50%); the voiceover sings "say a word, walked past her" — "I didn't" is swallowed and "back to my own" is not sung; caption drops "back to my own" |
| 54 | clip_55 | 201.900 | 205.480 | 3.580s | 107 | trim to first 3.57s | standard (y≈1300) |  |
| 55 | clip_56 | 205.480 | 208.340 | 2.860s | 86 | trim to first 2.87s | standard (y≈1300) |  |
| 56 | clip_57 | 208.340 | 210.720 | 2.380s | 72 | trim to first 2.40s | standard (y≈1300) |  |
| 57 | clip_58 | 210.720 | 216.820 | 6.100s | 183 | slow ×1.210 | low (box bottom at y=1450, close-up) |  |
| 58 | clip_59 | 216.820 | 222.020 | 5.200s | 156 | slow ×1.031 | standard (y≈1300) — product line, top position would cover the face; label clear |  |
| 59 | clip_60 | 222.020 | 225.060 | 3.040s | 91 | trim to first 3.03s | standard (y≈1300) — product line, top position would cover the face; label clear |  |
| 60 | clip_61 | 225.060 | 228.049 | 2.989s | 90 | trim to first 3.00s | standard height (y≈1300), nudged right to x=620 — product line, top position would cover the face; bottle on the nightstand at left stays clear |  |

## Captions

Montserrat ExtraBold 64 px, cream #FFF4E0 on an opaque EIS-maroon #7A1F2B box; the word being sung turns EIS gold #D4A537 (\k karaoke on the boxed layer, plus an unboxed cream layer whose \k timing lags one word, so only the current word is gold). 2–4 word phrases, one at a time, each leaves the screen 0.35 s after its last word (no caption through instrumental gaps). Product lines 25, 27, 29, 30, 31, 49 at y≈330. Product lines 58, 59, 60 kept at y≈1300 because at y≈330 the box sits on Rohit's face and the bottle is elsewhere in frame (raised hand / nightstand), checked frame by frame. Close-ups 03, 46, 57: box bottom at y=1450.

Audio: voiceover only, two-pass loudnorm (I=-14, limiter target -1.6 dBTP so the AAC encode lands under -1 dBTP), 48 kHz AAC 192k.

## Freeze-frame holds over 1 s (candidates to regenerate as longer clips)

- Line 04 — clip_4: 2.40s hold
- Line 08 — clip_8: 4.10s hold
- Line 16 — clip_16: 2.80s hold
