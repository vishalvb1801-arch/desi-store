# C300-H — "Just Tired" (Husband version) · EIS Ayurvedic Pain Relief Oil · v2 (notes applied)

**Plan:** `edit-plan.json` **v2** · 59 segments · 235.05 s (3:55) · one output **V1**: captions, hook1, CTA and logo burned in, music off (the song is `media/vo.mp3`) · every cut is a hard cut · validator: OK. The only warning is the expected "V2 is missing", which is ignored by design.
**appliedNotes:** n1, n2, n5, n6, n8, n9. **Still open:** n3, n4, n7 (partly applied; the reasons are below).
Only the existing 62 clips are used. Nothing was regenerated, and clip_32 and clip_62 are unused.

## Notes
| note | what changed | where | status |
|---|---|---|---|
| n1 | L1+L2 merged into one hook: 0.00–7.04 s. Shots: clip_1 `trim` 3.00 s → clip_2 `slow` 4.04 s (0.80×, so clip_2 plays in full and ends on his alarmed face). hook1 = "SHE THOUGHT HE / WAS CHEATING" (27/28 chars) over L1 (0–3.68 s). L2's captions follow from 3.68 s. Segment ids are renumbered from here on (59 segments, was 60). | seg01 | applied |
| n2 | "She scrolled through every message": clip_31 `trim` 1.60 s (picks up his phone, shower steam) → clip_33 `trim` 1.64 s. | seg30 (118.64–121.88) | applied |
| n3 | Captions rebuilt for this ad only: up to 44 chars as two lines of ≤ 22, with the break forced by `\n` (`maxCharsPerLine` 44). Neighbouring chunks within a line are merged and breaks land on punctuation or phrase starts: 190 → 113 items, all ≥ 1.2 s except the one below. Kept "jaan". Colours: text cream `#FFF4DC`, highlight gold `#F2C14E`, outline crimson `#770A08` at 8 px. **Open:** (a) the contract's caption style has no box/background key (font, size, color, strokeColor, strokeWidth, y, maxCharsPerLine, highlightColor only), and the parser rejects unknown keys, so a crimson *box* can't be set from the JSON. Crimson outline is the closest. Set the box in Stage 4's caption style, or the app needs a `boxColor` key. (b) seg35, L38 "'Cause in my head, the truth made me less of a man", is 49 chars sung in 2.00 s: one chunk would exceed 44, and two chunks can't both reach 1.2 s. It plays as 1.12 s + 0.88 s. | all captions | open (a, b) |
| n4 | Strong-end clips now play their ends: clip_2 `slow` 0.80× (hook); clip_44 at the reveal is `hold` and plays in full; clip_57 is `slow` 1.09×; clip_52 is `slow` 1.03×, in full, on a hard cut; clip_61 changed from `trim` to `slow` 0.81× so the push-in survives; CTA clip_44 is `hold` 5.04 s and plays in full (see n5). **Open: clip_8.** L8 is 2.84 s, and `slow` ≥ 0.8× needs ≥ 4.03 s, so it stays `trim` and shows 0–2.84 s: the finger on the switch (0.8–2.0 s) is in, but the room going dark and her turning away (~3–5 s) are not. The contract has no in-point/offset, so the fix is on the Shot Board: set clip_8's in-point to ~2.2 s. Other strong-end clips on lines under 4.03 s have the same limit and stay `trim`: clip_11 (tear drop at ~3.3 s, line 3.20 s), clip_29, clip_30, clip_39, clip_43. | seg01, 41, 54, 49, 58, 59 · seg07 | open (clip_8) |
| n5 | clip_62 is used nowhere. The CTA is clip_49 `trim` 1.31 s (front label + herbs) → clip_44 `hold`, which plays the full bottle reveal to the last frame at the file end. | seg59 | applied |
| n6 | The contract has no zoom/crop/scale on a shot, so clip_17 is out. clip_18 and clip_16 would both be adjacent-segment reuses (seg17 and seg15 use them), so instead L17 uses **clip_9** (top-down: him awake at night, her turned away). That's a reuse 25 s after its first use (seg08), non-adjacent. No black on screen anywhere: every clip in the plan except clip_17 is a full 716×1284 frame. | seg16 | applied |
| n7 | clip_6 and clip_24: `trim` keeps the start of each, which is the widest framing; her face stays about the same size through both. clip_6 also reads "10:40" cleanly in its first ~1.8 s, before the clock blurs. **Open: clip_8.** Its smallest-face/turned-away part is its end (her face is large in the close-up at 0.8–2.0 s). Same fix as n4: Shot Board in-point ~2.2 s. | seg05, seg23 · seg07 | open (clip_8) |
| n8 | Checked on a spectrogram of 66–82 s plus a re-run of whisper on just that window. The "S" of "Same" bursts at ~71.85 s; voicing for the second "I'm" starts at ~78.0 s; whisper's window timing says 71.66 / 77.90 s. Cuts moved to the onsets: L19|L20 **71.56 → 71.80**, L20|L21 **77.96 → 78.00**. | seg18/19/20 | applied |
| n9 | One output (V1). This file and `edit-plan.json` are copied to Drive › C300 › A and committed to `claude/loving-rubin-8t9pkf`. The Drive copy of the plan is the same JSON written compactly on one line; it was downloaded back and checked byte-for-byte. | — | applied |

## Clips not used
- **clip_62:** the label is garbled. It needs a regenerate before it can go in; you said no regenerations this round.
- **clip_17:** a black bar in every frame (content 716×1104). Replaced (n6).
- **clip_32:** L32 isn't sung (n2).

## Check in Stage 4
- **Two-line captions:** confirm the app honours `\n` in caption text and renders `maxCharsPerLine: 44` as two lines (the `\n` sets the break; each line is ≤ 22 chars). Quote marks are dropped from the sung dialogue in captions ("Said Is THIS her?") so they don't count toward the length.
- **Caption times are relative to their segments.** If you Snap to VO, recheck the held-note lines (seg04, seg18–21, seg59).
- **CTA:** `ORDER NOW · COD` (y 0.10) and `logo.png` (y 0.88) run from 1.0 s to the end of seg59. There's no price; none was supplied.
- **Instrumental stretches still inside segments** (VO is contiguous, as asked in the first-cut brief): 67.5–71.8 s (seg18), 75.9–78.0 s (seg19), 89.7–91.7 s (seg21), 162.9–164.0 s (seg42/43), 179.3–180.5 s (seg46/47), outro 230.4–235.05 s (seg59, which ends on clip_44's final frame).

## Segment table
| # | lyric | role | line | vo in–out (s) | shots + fit | stretch× |
|---|---|---|---|---|---|---|
| 01 | L1+L2 | hook | My wife shut the bedroom door on our anniversary night / … | 0.00–7.04 (7.04) | clip_1 `trim` 3.00s + clip_2 `slow` 4.04s | first 3.00s / 0.80 |
| 02 | L3 | body | But I'd been hiding something, something I couldn't let h… | 7.04–10.26 (3.22) | clip_3 `trim` 3.22s | first 3.22s |
| 03 | L4 | body | So I said the only words that kept her far away from me | 10.26–13.68 (3.42) | clip_4 `trim` 3.42s | first 3.42s |
| 04 | L5 | body | "I'm just tired, jaan… it's been a long day" | 13.68–20.06 (6.38) | clip_5 `slow` 6.38s | 1.27 |
| 05 | L6 | body | Ten-forty on the clock, she smiled, and then she said "okay" | 20.06–23.60 (3.54) | clip_6 `trim` 3.54s | first 3.54s |
| 06 | L7 | body | But that "okay" was hiding a question she would carry eve… | 23.60–27.14 (3.54) | clip_7 `trim` 3.54s | first 3.54s |
| 07 | L8 | body | She switched off the lamp and turned the other way | 27.14–29.98 (2.84) | clip_8 `trim` 2.84s | first 2.84s |
| 08 | L9 | body | And I lay beside the woman I have loved for twenty-four y… | 29.98–33.96 (3.98) | clip_9 `trim` 3.98s | first 3.98s |
| 09 | L10 | body | Two feet away, listening to a sound I still can hear | 33.96–37.02 (3.06) | clip_10 `trim` 3.06s | first 3.06s |
| 10 | L11 | body | Her pretending to be sleeping, so I wouldn't see her tears | 37.02–40.22 (3.20) | clip_11 `trim` 3.20s | first 3.20s |
| 11 | L12 | body | Nobody tells you it's not one night… it's the first of a … | 40.22–44.84 (4.62) | clip_12 `slow` 4.62s | 0.92 |
| 12 | L13 | body | I kept one secret in my glovebox, another in my office dr… | 44.84–49.06 (4.22) | clip_13 `slow` 4.22s | 0.84 |
| 13 | L14 | body | And every night by ten-fifteen, I was "too tired" once more | 49.06–52.28 (3.22) | clip_14 `trim` 3.22s | first 3.22s |
| 14 | L15 | body | Sat out my nephew's wedding while she danced and looked a… | 52.28–55.88 (3.60) | clip_15 `trim` 3.60s | first 3.60s |
| 15 | L16 | body | And I couldn't tell her why I wasn't standing there | 55.88–58.70 (2.82) | clip_16 `trim` 2.82s | first 2.82s |
| 16 | L17 | body | Then at 2 AM I'd slip out of our bed and shut the door | 58.70–61.90 (3.20) | clip_9 `trim` 3.20s | first 3.20s |
| 17 | L18 | body | Out on the balcony, my phone glowing… and she saw | 61.90–64.94 (3.04) | clip_18 `trim` 3.04s | first 3.04s |
| 18 | L19 | body | I'm just tired, jaan… | 64.94–71.80 (6.86) | clip_19 `slow` 6.86s | 1.36 |
| 19 | L20 | body | Same three words every night, under the bedroom light | 71.80–78.00 (6.20) | clip_20 `slow` 6.20s | 1.23 |
| 20 | L21 | body | I'm just tired, jaan… | 78.00–82.54 (4.54) | clip_21 `slow` 4.54s | 0.90 |
| 21 | L22 | body | But I'm tired… of lying 'bout why | 82.54–91.44 (8.90) | clip_3 `slow` 4.45s + clip_22 `slow` 4.45s | 0.88 / 0.88 |
| 22 | L23 | body | Then one Sunday I came home early, heard her on the phone | 91.44–95.32 (3.88) | clip_23 `trim` 3.88s | first 3.88s |
| 23 | L24 | body | Crying to her sister Neelu, saying things I'd never known | 95.32–98.66 (3.34) | clip_24 `trim` 3.34s | first 3.34s |
| 24 | L25 | body | "Eight months, Neelu… he won't touch me, won't even hold … | 98.66–101.92 (3.26) | clip_25 `trim` 3.26s | first 3.26s |
| 25 | L26 | body | I've dyed my greys, I've lost six kilos, and I still don'… | 101.92–105.16 (3.24) | clip_26 `trim` 3.24s | first 3.24s |
| 26 | L27 | body | He's on that balcony at 2 AM, on his phone… and I know who | 105.16–108.59 (3.43) | clip_27 `trim` 3.43s | first 3.43s |
| 27 | L28 | body | There's someone else, Neelu… what else could he be doing … | 108.59–111.94 (3.35) | clip_28 `trim` 3.35s | first 3.35s |
| 28 | L29 | body | And I stood there in that hallway, watching my little lie… | 111.94–115.18 (3.24) | clip_29 `trim` 3.24s | first 3.24s |
| 29 | L30 | body | Into something worse than the truth… and the worst was ye… | 115.18–118.64 (3.46) | clip_30 `trim` 3.46s | first 3.46s |
| 30 | L33 | body | She scrolled through every message, every call, and found… | 118.64–121.88 (3.24) | clip_31 `trim` 1.60s + clip_33 `trim` 1.64s | first 1.60s / first 1.64s |
| 31 | L34 | body | Just what I'd typed at 2 AM… and it wasn't who she'd blamed | 121.88–125.30 (3.42) | clip_34 `trim` 3.42s | first 3.42s |
| 32 | L35 | body | "Back pain only at night"… "How do I hide it from my wife?" | 125.30–128.88 (3.58) | clip_35 `trim` 3.58s | first 3.58s |
| 33 | L36 | body | She stood there in the doorway, held that phone up to my … | 128.88–131.96 (3.08) | clip_36 `trim` 3.08s | first 3.08s |
| 34 | L37 | body | Said "Is THIS her? Is this the other woman?" and she fell… | 131.96–135.30 (3.34) | clip_37 `trim` 3.34s | first 3.34s |
| 35 | L38 | body | 'Cause in my head, the truth made me less of a man | 135.30–137.30 (2.00) | clip_38 `trim` 2.00s | first 2.00s |
| 36 | L39 | body | Than the lie that nearly took her… but she already had a … | 137.30–139.76 (2.46) | clip_39 `trim` 2.46s | first 2.46s |
| 37 | L40 | body | Next morning she called her mother back in Nashik on the … | 139.76–143.60 (3.84) | clip_40 `trim` 3.84s | first 3.84s |
| 38 | L41 | body | Ma said "Your Papa's back went at fifty… and there's some… | 143.60–146.96 (3.36) | clip_41 `trim` 3.36s | first 3.36s |
| 39 | L42 | body | What I did for him each night, ten minutes, before he'd s… | 146.96–149.94 (2.98) | clip_42 `trim` 2.98s | first 2.98s |
| 40 | L43 | body | That night there was something on my pillow, and a promis… | 149.94–153.66 (3.72) | clip_43 `trim` 3.72s | first 3.72s |
| 41 | L44 | body | An amber bottle: EIS Ayurvedic Pain Relief Oil, fifteen h… | 153.66–158.72 (5.06) | clip_44 `hold` 5.06s | full + freeze 0.02s |
| 42 | L45 | body | I laughed, "Another oil?" She said "Lie down. Turn over. … | 158.72–163.70 (4.98) | clip_45 `slow` 4.98s | 0.99 |
| 43 | L46 | body | She said "It's not your age, jaan… it's what your tablets… | 163.70–168.64 (4.94) | clip_46 `slow` 4.94s | 0.98 |
| 44 | L47 | body | Inflammation, locked in deep, where sprays just sit up on… | 168.64–171.96 (3.32) | clip_47 `trim` 3.32s | first 3.32s |
| 45 | L48 | body | Warm massage works the stiffness loose, so fifteen herbs … | 171.96–175.66 (3.70) | clip_48 `trim` 3.70s | first 3.70s |
| 46 | L49 | body | Mahanarayan, Nirgundi, Ashwagandha, camphor, mint" | 175.66–180.22 (4.56) | clip_49 `hold` 4.56s | first 4.56s |
| 47 | L50 | body | Night one, her hands on my back, first time she'd touched… | 180.22–184.50 (4.28) | clip_50 `slow` 4.28s | 0.85 |
| 48 | L51 | body | Night three, I slept straight through… and woke to find h… | 184.50–189.54 (5.04) | clip_51 `slow` 5.04s | 1.00 |
| 49 | L52 | body | Week six, back on morning walks, standing tall, and Frida… | 189.54–194.74 (5.20) | clip_52 `slow` 5.20s | 1.03 |
| 50 | L53 | body | That Friday I stayed up, didn't fall asleep at ten | 194.74–198.66 (3.92) | clip_53 `trim` 3.92s | first 3.92s |
| 51 | L54 | body | She came out in that red saree, nervous like our first ni… | 198.66–202.66 (4.00) | clip_54 `trim` 4.00s | first 4.00s |
| 52 | L55 | body | She whispered "Tired?" and I gave the answer she'd waited… | 202.66–206.62 (3.96) | clip_55 `trim` 3.96s | first 3.96s |
| 53 | L56 | body | "Not tonight, jaan… not ever again" | 206.62–209.72 (3.10) | clip_56 `trim` 3.10s | first 3.10s |
| 54 | L57 | body | She switched off the lamp, and this time she turned my way | 209.72–215.20 (5.48) | clip_57 `slow` 5.48s | 1.09 |
| 55 | L58 | body | "I'm not tired, jaan"… no more lying 'bout why | 215.20–219.93 (4.73) | clip_58 `slow` 4.73s | 0.94 |
| 56 | L59 | body | To every man two feet from his wife | 219.93–222.68 (2.75) | clip_59 `trim` 2.75s | first 2.75s |
| 57 | L60 | body | Saying "just tired" every night | 222.68–224.62 (1.94) | clip_60 `trim` 1.94s | first 1.94s |
| 58 | L61 | body | She doesn't think you're tired… she thinks it's her | 224.62–228.70 (4.08) | clip_61 `slow` 4.08s | 0.81 |
| 59 | L62 | cta | Tell her why. | 228.70–235.05 (6.35) | clip_49 `trim` 1.31s + clip_44 `hold` 5.04s | first 1.31s / full |
_`trim`: "first Xs" is how much of the clip is seen. `hold`: "full" means it plays the whole clip._
