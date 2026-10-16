# C299-A edit log

Song: `C299 A.mp3` 240.039 s (master). Video: 7201 frames @ 30 fps = 240.033 s. Clips: 60 × Kling 716×1284 @ 24 fps, 5.042 s (L), no audio.
Scaling: lanczos cover-scale to 1080×1920 + centre crop (716×1284 is slightly narrower than 9:16, ~8 px trimmed top/bottom). No padding.
Frame-rate: 24→30 by frame duplication (fps filter), no blending. Slow-downs via setpts, no blending. Holds via tpad clone.
Transition: hard cuts everywhere except a 6-frame (0.2 s) crossfade into line 40; line 39's clip runs 6 extra frames underneath it so the line-40 boundary stays put.
Audio: song only, loudnorm two-pass → −14.0 LUFS integrated, −1.0 dBTP, AAC 48 kHz 192 kbps.
Timing: faster-whisper large-v3 (int8, CPU) word timestamps, lyrics fuzzy-aligned (rapidfuzz, global alignment) in order. Line start = first matched word; line 01 forced to 0.00; line 60 runs to end of audio; instrumental gaps belong to the preceding line.
Clip mapping: Drive filenames are `1.mp4`…`60.mp4` → line number; every first frame was visually checked against its line description. (`C299-A-frames.zip` was not in the Drive folder, so no phash pass was possible.)

| Line | Clip | Start | End | Target T (s) | Frames | Action | Speed | Hold (s) | Caption y | Flags |
|---|---|---|---|---|---|---|---|---|---|---|
| 01 | 1.mp4 (beat01_hook_doorway) | 0.000 | 4.433 | 4.433 | 133 | trim | 100% | – | 1300 |  |
| 02 | 2.mp4 (beat02_age_gap) | 4.433 | 8.067 | 3.633 | 109 | trim | 100% | – | 1300 |  |
| 03 | 3.mp4 (beat03_kavita_break) | 8.067 | 10.333 | 2.267 | 68 | trim | 100% | – | 1450 | close-up: caption low (y 1450) |
| 04 | 4.mp4 (beat04_shalini_flight) | 10.333 | 15.933 | 5.600 | 168 | slow | 90% | – | 1300 |  |
| 05 | 5.mp4 (beat05_come_home) | 15.933 | 19.433 | 3.500 | 105 | trim | 100% | – | 1300 |  |
| 06 | 6.mp4 (beat06_door_push) | 19.433 | 23.667 | 4.233 | 127 | trim | 100% | – | 1300 |  |
| 07 | 7.mp4 (beat07_sofa_dark) | 23.667 | 29.033 | 5.367 | 161 | slow | 94% | – | 1300 |  |
| 08 | 8.mp4 (beat08_mirror_first) | 29.033 | 34.400 | 5.367 | 161 | slow | 94% | – | 1300 |  |
| 09 | 9.mp4 (beat09_mirror_face) | 34.400 | 37.133 | 2.733 | 82 | trim | 100% | – | 1450 | close-up: caption low (y 1450) |
| 10 | 10.mp4 (beat10_xray_pain) | 37.133 | 40.600 | 3.467 | 104 | trim | 100% | – | 1300 |  |
| 11 | 11.mp4 (beat11_railing) | 40.600 | 44.267 | 3.667 | 110 | trim | 100% | – | 1300 |  |
| 12 | 12.mp4 (beat12_mehendi_chair) | 44.267 | 47.067 | 2.800 | 84 | trim | 100% | – | 1300 |  |
| 13 | 13.mp4 (beat13_saree_fail) | 47.067 | 49.867 | 2.800 | 84 | trim | 100% | – | 1300 |  |
| 14 | 14.mp4 (beat14_mirror_tear) | 49.867 | 54.667 | 4.800 | 144 | trim | 100% | – | 1300 |  |
| 15 | 15.mp4 (beat15_failed_fixes) | 54.667 | 58.667 | 4.000 | 120 | trim | 100% | – | 1300 |  |
| 16 | 16.mp4 (beat16_doctor) | 58.667 | 64.733 | 6.067 | 182 | slow | 83% | – | 1300 |  |
| 17 | 17.mp4 (beat17_promenade_slow) | 64.733 | 69.767 | 5.033 | 151 | trim | 100% | – | 1300 |  |
| 18 | 18.mp4 (beat18_mirror_ghost) | 69.767 | 73.467 | 3.700 | 111 | trim | 100% | – | 1300 |  |
| 19 | 19.mp4 (beat19_open_affair) | 73.467 | 77.467 | 4.000 | 120 | trim | 100% | – | 1300 |  |
| 20 | 20.mp4 (beat20_bed_alone) | 77.467 | 81.267 | 3.800 | 114 | trim | 100% | – | 1300 |  |
| 21 | 21.mp4 (beat21_call_sister) | 81.267 | 85.767 | 4.500 | 135 | trim | 100% | – | 1300 |  |
| 22 | 22.mp4 (beat22_sister_kerala) | 85.767 | 90.167 | 4.400 | 132 | trim | 100% | – | 1300 |  |
| 23 | 23.mp4 (beat23_airport) | 90.167 | 93.867 | 3.700 | 111 | trim | 100% | – | 1300 |  |
| 24 | 24.mp4 (beat24_shoulders) | 93.867 | 101.067 | 7.200 | 216 | slow | 70% | – | 1300 |  |
| 25 | 25.mp4 (beat25_bottle_reveal) | 101.067 | 103.567 | 2.500 | 75 | trim | 100% | – | 620 | caption moved 330→620: at 330 it sat across both women's eyes; 620 is between chins and bottle cap, label clear |
| 26 | 26.mp4 (beat26_women_sixty) | 103.567 | 106.100 | 2.533 | 76 | trim | 100% | – | 1300 |  |
| 27 | 27.mp4 (beat27_skeptic) | 106.100 | 107.967 | 1.867 | 56 | trim | 100% | – | 1300 |  |
| 28 | 28.mp4 (beat28_cgi_spray) | 107.967 | 110.400 | 2.433 | 73 | trim | 100% | – | 1300 |  |
| 29 | 29.mp4 (beat29_warm_palms) | 110.400 | 113.233 | 2.833 | 85 | trim | 100% | – | 1300 |  |
| 30 | 30.mp4 (beat30_night_massage) | 113.233 | 116.000 | 2.767 | 83 | trim | 100% | – | 1300 |  |
| 31 | 31.mp4 (beat31_herbs_hero) | 116.000 | 120.400 | 4.400 | 132 | trim | 100% | – | 210 | first word 'eis' not detected by whisper; line starts at first matched word; caption above the cap (y 210) |
| 32 | 32.mp4 (beat32_cgi_warmth) | 120.400 | 123.133 | 2.733 | 82 | trim | 100% | – | 1300 |  |
| 33 | 33.mp4 (beat33_sleep) | 123.133 | 125.733 | 2.600 | 78 | trim | 100% | – | 1300 |  |
| 34 | 34.mp4 (beat34_puja) | 125.733 | 129.267 | 3.533 | 106 | trim | 100% | – | 1300 |  |
| 35 | 35.mp4 (beat35_daughter_call) | 129.267 | 131.200 | 1.933 | 58 | trim | 100% | – | 1300 |  |
| 36 | 36.mp4 (beat36_carter_road) | 131.200 | 133.867 | 2.667 | 80 | trim | 100% | – | 1300 |  |
| 37 | 37.mp4 (beat37_yoga) | 133.867 | 137.267 | 3.400 | 102 | trim | 100% | – | 1300 |  |
| 38 | 38.mp4 (beat38_cupboard) | 137.267 | 141.667 | 4.400 | 132 | trim | 100% | – | 1300 |  |
| 39 | 39.mp4 (beat39_transform_pleat) | 141.667 | 145.767 | 4.300 | 129 | trim | 100% | – | 1300 | +6 frames under the crossfade into 40 |
| 40 | 40.mp4 (beat40_glowup_mirror) | 145.767 | 149.767 | 4.000 | 120 | trim | 100% | – | 1300 | 6-frame crossfade in |
| 41 | 41.mp4 (beat41_meet_vikram) | 149.767 | 153.133 | 3.367 | 101 | trim | 100% | – | 1300 |  |
| 42 | 42.mp4 (beat42_rooftop) | 153.133 | 156.233 | 3.100 | 93 | trim | 100% | – | 1300 |  |
| 43 | 43.mp4 (beat43_husband_enters) | 156.233 | 159.067 | 2.833 | 85 | trim | 100% | – | 1300 |  |
| 44 | 44.mp4 (beat44_blue_shirt) | 159.067 | 162.267 | 3.200 | 96 | trim | 100% | – | 1300 |  |
| 45 | 45.mp4 (beat45_he_stares) | 162.267 | 165.200 | 2.933 | 88 | trim | 100% | – | 1300 |  |
| 46 | 46.mp4 (beat46_ghost_face) | 165.200 | 168.867 | 3.667 | 110 | trim | 100% | – | 1450 | close-up: caption low (y 1450); face pushes in; last phrase sits on the chin, below the mouth |
| 47 | 47.mp4 (beat47_washroom) | 168.867 | 171.933 | 3.067 | 92 | trim | 100% | – | 1300 |  |
| 48 | 48.mp4 (beat48_stranger_asks) | 171.933 | 175.267 | 3.333 | 100 | trim | 100% | – | 1300 |  |
| 49 | 49.mp4 (beat49_show_phone) | 175.267 | 177.300 | 2.033 | 61 | trim | 100% | – | 1300 |  |
| 50 | 50.mp4 (beat50_orders) | 177.300 | 180.067 | 2.767 | 83 | trim | 100% | – | 1300 |  |
| 51 | 51.mp4 (beat51_alone_corridor) | 180.067 | 182.467 | 2.400 | 72 | trim | 100% | – | 1300 |  |
| 52 | 52.mp4 (beat52_what_did_you_do) | 182.467 | 184.667 | 2.200 | 66 | trim | 100% | – | 1300 |  |
| 53 | 53.mp4 (beat53_walk_past) | 184.667 | 187.867 | 3.200 | 96 | trim | 100% | – | 1300 |  |
| 54 | 54.mp4 (beat54_laugh_vikram) | 187.867 | 194.333 | 6.467 | 194 | slow | 78% | – | 1300 |  |
| 55 | 55.mp4 (beat55_rooftop_edge) | 194.333 | 198.200 | 3.867 | 116 | trim | 100% | – | 1300 |  |
| 56 | 56.mp4 (beat56_sangeet_dance) | 198.200 | 202.033 | 3.833 | 115 | trim | 100% | – | 1300 |  |
| 57 | 57.mp4 (beat57_hero_face) | 202.033 | 218.500 | 16.467 | 494 | slow+hold | 67% | 8.90 | 1450 | absorbs the 11.9 s instrumental before the CTA (vocal ends 206.56) → 8.9 s freeze on last frame; close-up: caption low (y 1450) |
| 58 | 58.mp4 (beat58_cta_hold) | 218.500 | 225.233 | 6.733 | 202 | slow | 75% | – | 1300 → 215 at 221.17 | in-clip camera cut at 221.17 s; after it the bottle fills the left half top-to-bottom, so captions move above the label (over cap/background) |
| 59 | 59.mp4 (beat59_cta_vanity) | 225.233 | 230.567 | 5.333 | 160 | slow | 95% | – | 810 | caption moved 330→810: at 330 it covered Kavita's face; 810 is above the bottle cap, label clear |
| 60 | 60.mp4 (beat60_cta_night) | 230.567 | 240.033 | 9.467 | 284 | slow+hold | 67% | 1.90 | 1300 | runs to final audio frame; ~1.9 s freeze on last frame |
