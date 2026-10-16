# C300-H — "Just Tired" (Husband version) · EIS Ayurvedic Pain Relief Oil · first cut

**Plan:** `edit-plan.json` v1 · 60 segments · 235.05 s (3:55) · one output **V1**, with subtitles, hook1, CTA and logo burned in · music off (the song is the VO, `media/vo.mp3`) · every cut is a hard cut, no crossfades · validator: OK.

**Inputs:** Drive › C300 › A (`A.mp3` → `media/vo.mp3`, `C300-H-clips/clip_1…62.mp4` → `clips/`). Folder A has **no** `C300-H-script.docx`, `frame-prompts.json` or `motion-prompts.json`. Lines 1–51 come from the brief; lines 52–62 are transcribed from the song (whisper medium.en, `handoff/transcript.json`). Every clip is 5.04 s, 716×1284.

## Read first — where this differs from the brief or the standards
1. **Lines 31 and 32 are not sung.** The song goes from "…and the worst was yet to show" (118.6 s) straight into "She scrolled through every message". So there's no segment for "That night she took my phone while I was in the shower" or "Ready for another woman's name…". **clip_31 and clip_32 are unused.** clip_31 (she lifts his phone off the nightstand, shower steam) is the setup the story is missing. To restore that beat, swap clip_31 into seg31 (L33) on the Shot Board. That gives 60 segments for 62 clips.
2. **Contiguous VO, intro and outro kept**, as you asked. This overrides the skill's sung-VO rule that cuts out instrumental stretches. Singing starts at 0.0 s, so there's no real intro. The 4.6 s outro (230.4→235.05) plays on the end card. Instrumental stretches kept inside segments are listed under *Song skips*.
3. **Hook is 3.68 s, not 7–8 s.** One segment per lyric line makes seg01 just line 1. The validator warns about this. clip_1 → clip_2 still reads as one 7 s opening. If you want the hook rule met, merge L1+L2 into seg01 (0.00–7.04, clip_1 + clip_2).
4. **Most lines are 3–3.6 s, so most shots are `trim`.** Below 4.03 s a 5 s clip would need `slow` under 0.8×, so `trim` keeps the clip's first 2–4 s. Lines that keep the whole clip with `slow`: L5, L12, L13, L19, L20, L21, L22, L45, L46, L50, L51, L52, L57, L58. Product lines L44, L49, L61 use `hold`.
5. **Captions are Latin-script English**, because the song is English. They use the brief's spelling ("jaan", not whisper's "John"/"young"). They are timed from the transcript words, ≤ 22 characters per chunk. The song runs ~16–18 characters per second, so 19 chunks are 0.6–0.8 s (validator warnings). Going longer would mean dropping words.

## Clips to regenerate
| clip | used in | problem |
|---|---|---|
| **clip_62** | not used | **Garbled label** all through the clip: "Ayurvelic", "DEBANNS OF DHANAAD" in place of ESSENCE OF NATURE, and a Devanagari-style strip in place of NATURAL RELIEF • STRONG ACTION. Regenerate the CTA end card (husband holds bottle to camera, wife beside). Until then, seg60 (L62) uses **clip_49 `trim` 2.8 s → clip_44 `hold`**: both labels are correct, and both are reused once, far from their first use. |
| clip_17 | seg17 (L17) | Letterboxed: a 180 px black bar along the bottom (content is 716×1104). It will show as a black band. Regenerate, or crop/scale on the timeline. |
| clip_6, clip_8 | seg06, seg08 | Wife face drift: white-haired, ~65, compared with the grey-streaked ~45 wife in clip_1/2/54. clip_6's clock also blurs to "10:4". |
| clip_24 | seg24 | Wife reads older than in clip_25/28 (the same phone call). Milder; check it. |

Wife's look varies slightly across many clips (hair darker in clip_7, 11, 33). Within tolerance, but the operator should look. Husband stays consistent throughout. The after-state (maroon shirt, slimmer) starts at clip_52 and holds to the end.

## Missing shots
None. Every sung line has its own clip. The one line ≥ 7 s (L22, 8.90 s) gets two shots: clip_3 (reused, 7 s → 82 s) + clip_22.

## Product placement (checked on the contact sheets)
The product first appears at seg42 / L44, "An amber bottle: EIS Ayurvedic Pain Relief Oil": clip_44 `hold`, label correct. One SFX placeholder (`shimmer.wav`, −8 dB) at 0.0 of that segment. Labels read correctly on the zoomed frames of clip_44, 49 and 61. The bottles in clip_45 and clip_48 are small and soft, but crimson and on-colour. No product appears before L44: clip_35's red glow is the husband's spine, not the bottle. The mechanism has full shots of its own: clip_46 (tablet never reaches the spine), clip_47 (spray sits on the skin), clip_48 (massage glow). clip_52 is the transformation: one clip, same face, entering on a hard cut.

## Song skips (sung VO)
Nothing is cut; the VO is contiguous as you asked. These instrumental / held-note stretches play inside a segment, and the picture keeps moving through each one (`slow`, no freeze):
- 67.5–71.9 s: held "jaan…" → "Same three words" (seg19/seg20)
- 75.9–78.3 s: after "bedroom light" (seg20)
- 89.7–91.7 s: after "lying 'bout why" (seg22)
- 162.9–164.0 s: after "Then decide" (seg43)
- 179.3–180.5 s: after "camphor, mint" (seg47)
- 230.4–235.05 s: outro on the end card (seg60)

If any of these feels long, the fix is the contiguity rule: cut the stretch (0.35 s after the last word / 0.25 s before the next).

## Provisional — check after Snap to VO
- Held notes give whisper loose word timings. The starts of L20 ("Same…", ~71.9 s) and L21 ("I'm just tired, jaan", ~78.3 s) are estimated as the word's end − 0.5 s. Check both by ear, along with L22's held "tired… of".
- Line splits that whisper ran together (L24|25, L27|28, L29|30, L37|38, L38|39, L54|55 at "again", L55|56 at "for | Not tonight") are cut at the word the lyric rhymes on. Check that each cut lands on the beat.
- Caption times are relative to their segments. Snap to VO moves the boundaries but doesn't retime captions, so recheck the long held-note lines (seg05, seg19–22, seg62).
- CTA: `ORDER NOW · COD` (cta, y 0.10) + `logo.png` (y 0.88) from 1.0 s to the end of seg60. There's no price, since none was supplied (brand rule: never invent one).
- hook1: "I lied to her / every night" on seg01 0–3.68 s. It's an open loop; seg01 has no captions.

## Segment table
| # | lyric | role | line | vo in–out (s) | shots + fit | stretch× |
|---|---|---|---|---|---|---|
| 01 | L1 | hook | My wife shut the bedroom door on our anniversary night | 0.00–3.68 (3.68) | clip_1 `trim` 3.68s | plays 3.68s of 5.04 |
| 02 | L2 | body | Wore the red saree from our wedding, whispered "No excuse… | 3.68–7.04 (3.36) | clip_2 `trim` 3.36s | plays 3.36s of 5.04 |
| 03 | L3 | body | But I'd been hiding something, something I couldn't let h… | 7.04–10.26 (3.22) | clip_3 `trim` 3.22s | plays 3.22s of 5.04 |
| 04 | L4 | body | So I said the only words that kept her far away from me | 10.26–13.68 (3.42) | clip_4 `trim` 3.42s | plays 3.42s of 5.04 |
| 05 | L5 | body | "I'm just tired, jaan… it's been a long day" | 13.68–20.06 (6.38) | clip_5 `slow` 6.38s | 1.27 |
| 06 | L6 | body | Ten-forty on the clock, she smiled, and then she said "okay" | 20.06–23.60 (3.54) | clip_6 `trim` 3.54s | plays 3.54s of 5.04 |
| 07 | L7 | body | But that "okay" was hiding a question she would carry eve… | 23.60–27.14 (3.54) | clip_7 `trim` 3.54s | plays 3.54s of 5.04 |
| 08 | L8 | body | She switched off the lamp and turned the other way | 27.14–29.98 (2.84) | clip_8 `trim` 2.84s | plays 2.84s of 5.04 |
| 09 | L9 | body | And I lay beside the woman I have loved for twenty-four y… | 29.98–33.96 (3.98) | clip_9 `trim` 3.98s | plays 3.98s of 5.04 |
| 10 | L10 | body | Two feet away, listening to a sound I still can hear | 33.96–37.02 (3.06) | clip_10 `trim` 3.06s | plays 3.06s of 5.04 |
| 11 | L11 | body | Her pretending to be sleeping, so I wouldn't see her tears | 37.02–40.22 (3.20) | clip_11 `trim` 3.20s | plays 3.20s of 5.04 |
| 12 | L12 | body | Nobody tells you it's not one night… it's the first of a … | 40.22–44.84 (4.62) | clip_12 `slow` 4.62s | 0.92 |
| 13 | L13 | body | I kept one secret in my glovebox, another in my office dr… | 44.84–49.06 (4.22) | clip_13 `slow` 4.22s | 0.84 |
| 14 | L14 | body | And every night by ten-fifteen, I was "too tired" once more | 49.06–52.28 (3.22) | clip_14 `trim` 3.22s | plays 3.22s of 5.04 |
| 15 | L15 | body | Sat out my nephew's wedding while she danced and looked a… | 52.28–55.88 (3.60) | clip_15 `trim` 3.60s | plays 3.60s of 5.04 |
| 16 | L16 | body | And I couldn't tell her why I wasn't standing there | 55.88–58.70 (2.82) | clip_16 `trim` 2.82s | plays 2.82s of 5.04 |
| 17 | L17 | body | Then at 2 AM I'd slip out of our bed and shut the door | 58.70–61.90 (3.20) | clip_17 `trim` 3.20s | plays 3.20s of 5.04 |
| 18 | L18 | body | Out on the balcony, my phone glowing… and she saw | 61.90–64.94 (3.04) | clip_18 `trim` 3.04s | plays 3.04s of 5.04 |
| 19 | L19 | body | I'm just tired, jaan… | 64.94–71.56 (6.62) | clip_19 `slow` 6.62s | 1.31 |
| 20 | L20 | body | Same three words every night, under the bedroom light | 71.56–77.96 (6.40) | clip_20 `slow` 6.40s | 1.27 |
| 21 | L21 | body | I'm just tired, jaan… | 77.96–82.54 (4.58) | clip_21 `slow` 4.58s | 0.91 |
| 22 | L22 | body | But I'm tired… of lying 'bout why | 82.54–91.44 (8.90) | clip_3 `slow` 4.45s + clip_22 `slow` 4.45s | 0.88 / 0.88 |
| 23 | L23 | body | Then one Sunday I came home early, heard her on the phone | 91.44–95.32 (3.88) | clip_23 `trim` 3.88s | plays 3.88s of 5.04 |
| 24 | L24 | body | Crying to her sister Neelu, saying things I'd never known | 95.32–98.66 (3.34) | clip_24 `trim` 3.34s | plays 3.34s of 5.04 |
| 25 | L25 | body | "Eight months, Neelu… he won't touch me, won't even hold … | 98.66–101.92 (3.26) | clip_25 `trim` 3.26s | plays 3.26s of 5.04 |
| 26 | L26 | body | I've dyed my greys, I've lost six kilos, and I still don'… | 101.92–105.16 (3.24) | clip_26 `trim` 3.24s | plays 3.24s of 5.04 |
| 27 | L27 | body | He's on that balcony at 2 AM, on his phone… and I know who | 105.16–108.59 (3.43) | clip_27 `trim` 3.43s | plays 3.43s of 5.04 |
| 28 | L28 | body | There's someone else, Neelu… what else could he be doing … | 108.59–111.94 (3.35) | clip_28 `trim` 3.35s | plays 3.35s of 5.04 |
| 29 | L29 | body | And I stood there in that hallway, watching my little lie… | 111.94–115.18 (3.24) | clip_29 `trim` 3.24s | plays 3.24s of 5.04 |
| 30 | L30 | body | Into something worse than the truth… and the worst was ye… | 115.18–118.64 (3.46) | clip_30 `trim` 3.46s | plays 3.46s of 5.04 |
| 31 | L33 | body | She scrolled through every message, every call, and found… | 118.64–121.88 (3.24) | clip_33 `trim` 3.24s | plays 3.24s of 5.04 |
| 32 | L34 | body | Just what I'd typed at 2 AM… and it wasn't who she'd blamed | 121.88–125.30 (3.42) | clip_34 `trim` 3.42s | plays 3.42s of 5.04 |
| 33 | L35 | body | "Back pain only at night"… "How do I hide it from my wife?" | 125.30–128.88 (3.58) | clip_35 `trim` 3.58s | plays 3.58s of 5.04 |
| 34 | L36 | body | She stood there in the doorway, held that phone up to my … | 128.88–131.96 (3.08) | clip_36 `trim` 3.08s | plays 3.08s of 5.04 |
| 35 | L37 | body | Said "Is THIS her? Is this the other woman?" and she fell… | 131.96–135.30 (3.34) | clip_37 `trim` 3.34s | plays 3.34s of 5.04 |
| 36 | L38 | body | 'Cause in my head, the truth made me less of a man | 135.30–137.30 (2.00) | clip_38 `trim` 2.00s | plays 2.00s of 5.04 |
| 37 | L39 | body | Than the lie that nearly took her… but she already had a … | 137.30–139.76 (2.46) | clip_39 `trim` 2.46s | plays 2.46s of 5.04 |
| 38 | L40 | body | Next morning she called her mother back in Nashik on the … | 139.76–143.60 (3.84) | clip_40 `trim` 3.84s | plays 3.84s of 5.04 |
| 39 | L41 | body | Ma said "Your Papa's back went at fifty… and there's some… | 143.60–146.96 (3.36) | clip_41 `trim` 3.36s | plays 3.36s of 5.04 |
| 40 | L42 | body | What I did for him each night, ten minutes, before he'd s… | 146.96–149.94 (2.98) | clip_42 `trim` 2.98s | plays 2.98s of 5.04 |
| 41 | L43 | body | That night there was something on my pillow, and a promis… | 149.94–153.66 (3.72) | clip_43 `trim` 3.72s | plays 3.72s of 5.04 |
| 42 | L44 | body | An amber bottle: EIS Ayurvedic Pain Relief Oil, fifteen h… | 153.66–158.72 (5.06) | clip_44 `hold` 5.06s | freeze +0.02s |
| 43 | L45 | body | I laughed, "Another oil?" She said "Lie down. Turn over. … | 158.72–163.70 (4.98) | clip_45 `slow` 4.98s | 0.99 |
| 44 | L46 | body | She said "It's not your age, jaan… it's what your tablets… | 163.70–168.64 (4.94) | clip_46 `slow` 4.94s | 0.98 |
| 45 | L47 | body | Inflammation, locked in deep, where sprays just sit up on… | 168.64–171.96 (3.32) | clip_47 `trim` 3.32s | plays 3.32s of 5.04 |
| 46 | L48 | body | Warm massage works the stiffness loose, so fifteen herbs … | 171.96–175.66 (3.70) | clip_48 `trim` 3.70s | plays 3.70s of 5.04 |
| 47 | L49 | body | Mahanarayan, Nirgundi, Ashwagandha, camphor, mint" | 175.66–180.22 (4.56) | clip_49 `hold` 4.56s | plays 4.56s of 5.04 |
| 48 | L50 | body | Night one, her hands on my back, first time she'd touched… | 180.22–184.50 (4.28) | clip_50 `slow` 4.28s | 0.85 |
| 49 | L51 | body | Night three, I slept straight through… and woke to find h… | 184.50–189.54 (5.04) | clip_51 `slow` 5.04s | 1.00 |
| 50 | L52 | body | Week six, back on morning walks, standing tall, and Frida… | 189.54–194.74 (5.20) | clip_52 `slow` 5.20s | 1.03 |
| 51 | L53 | body | That Friday I stayed up, didn't fall asleep at ten | 194.74–198.66 (3.92) | clip_53 `trim` 3.92s | plays 3.92s of 5.04 |
| 52 | L54 | body | She came out in that red saree, nervous like our first ni… | 198.66–202.66 (4.00) | clip_54 `trim` 4.00s | plays 4.00s of 5.04 |
| 53 | L55 | body | She whispered "Tired?" and I gave the answer she'd waited… | 202.66–206.62 (3.96) | clip_55 `trim` 3.96s | plays 3.96s of 5.04 |
| 54 | L56 | body | "Not tonight, jaan… not ever again" | 206.62–209.72 (3.10) | clip_56 `trim` 3.10s | plays 3.10s of 5.04 |
| 55 | L57 | body | She switched off the lamp, and this time she turned my way | 209.72–215.20 (5.48) | clip_57 `slow` 5.48s | 1.09 |
| 56 | L58 | body | "I'm not tired, jaan"… no more lying 'bout why | 215.20–219.93 (4.73) | clip_58 `slow` 4.73s | 0.94 |
| 57 | L59 | body | To every man two feet from his wife | 219.93–222.68 (2.75) | clip_59 `trim` 2.75s | plays 2.75s of 5.04 |
| 58 | L60 | body | Saying "just tired" every night | 222.68–224.62 (1.94) | clip_60 `trim` 1.94s | plays 1.94s of 5.04 |
| 59 | L61 | body | She doesn't think you're tired… she thinks it's her | 224.62–228.70 (4.08) | clip_61 `hold` 4.08s | plays 4.08s of 5.04 |
| 60 | L62 | cta | Tell her why. | 228.70–235.05 (6.35) | clip_49 `trim` 2.80s + clip_44 `hold` 3.55s | plays 2.80s of 5.04 / plays 3.55s of 5.04 |
_`trim` keeps the start of the clip; "plays Xs of 5.04" is how much of the clip is seen._
