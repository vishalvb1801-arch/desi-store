# C302 B — QC report (STOPPED before edit/render)

Inputs pulled from Drive with gdown (no Drive for desktop in this environment): `C302_B-clips.zip` → 60 clips (`clip_1…clip_60`, 716×1284, 24 fps, 5.04 s, no audio); `C302 B.mp3` → `media/vo.mp3` (300.04 s).
Contact sheets: `handoff/contact-sheets/`. Zoomed evidence: `handoff/qc/`.

## STOP 1 — product clips with a failed label

| Clip | Problem |
|---|---|
| clip_25 | Label reads **"BIS · ARTESUAN ARTSHAIAG OIL · PAIN RELLIEF · PAN 11.005"**, with chillies printed on it. Garbled and misspelled. |
| clip_26 | **Black cap** (should be white). Label text is garbled ("EIS" over unreadable lines) and the artwork is wrong. |
| clip_28 | Close-up label reads **"AYURVEIIC PANN RELIEF OIL · PAINNT RELEEIT · 50 ml"**: misspelled, a plain different design, wrong size. |
| clip_31 | Label reads **"BIS PAIN RELIEF OIL · 250 ml"**: wrong brand letter, bright-red off-design label, wrong size. |
| clip_58 | Minor: main label is correct, but the small print is garbled in the final frames ("1S" badge, "200 nnl"). Your call: regenerate or accept. |

Passed: clip_38, 39, 56, 60 (crimson-maroon label, gold "EIS · Essence of Nature · Ayurvedic PAIN RELIEF OIL · 200 ml", white cap).
No product appears before clip_25.

## STOP 2 — the song is broken after 4:27

Whisper (medium.en, on a Demucs vocal stem and on the full mix) gives:

- 0:00–0:09.5 instrumental intro, then lines 1–20 sung clearly (9.9–137.5 s).
- 137.5–155.9 s instrumental break. Lines 21–42 sung clearly (156.1–266.2 s), with breaks at 198.7–202.0 and 248.2–254.9.
- **267.2–295.1 s: gibberish.** The transcript reads "beat back path attacked … my love, oh quick, eat … I'm a chicken … grab a bit for a ticket … he needs some venus, see … but it's not shfaids, oh … good for me". About 18 lyric lines (43–60) are crammed into ~28 s and are not intelligible. Only fragments of the last lines are recognisable.
- 295.1–300.0 s: outro.

So lines 43–60 never get sung as written: the six-weeks/heels line, the mirror morph, the Diwali payoff, Rohan/Tanya, the mirror ending and the **whole CTA** ("It's called EIS…", "Fifty percent off… cash on delivery", "It's for me"). The edit can't follow the lyric map past clip_42, and captions can't honestly carry lyrics that aren't sung. The file is exactly 5:00, which is ElevenLabs Music's maximum length. The lyric sheet is too long for one 5-minute generation, so the model compressed and garbled the ending.

Fix options (your choice):
1. Regenerate the song in **two parts** (lines 1–30 and 31–60), each well under 5:00. The edit then skips the join like any other break.
2. Shorten the lyrics until the full sheet fits comfortably in about 4:30.
3. Regenerate only the ending (lines 43–60) and supply it as a second VO file.

## Other flagged clips (regenerate; would be worked around)

| Clip | Problem |
|---|---|
| clip_23 | Meena didi becomes a different character (black hair, darker skin, new face versus the grey-haired, bespectacled Meena in 21/24/33). Neha's face also drifts in the second half (messy hair, different face). |

Watch list (not flagged):
- clip_7: Neha's face softens and slims slightly in the profile/final frame. Mole is kept. Usable.
- clip_2: the dancing fiancée has a rounder face than the fiancée/Tanya in clip_1/47. Not Neha.
- clip_18: real third-party brands (**Volini**, **Moov**) are readable on the sprays. Check Meta/competitor-mention policy before running.

## Done so far (reusable once the clips and song are fixed)

- `handoff/clip-map.json` (60 clips, product flags, descriptions, lyric lines), `handoff/script.json`.
- Montserrat Bold installed for the pill captions.
- Vocal stem silence map (`handoff/vo-silence.json`) and whisper/aligned transcripts of the current song (`handoff/transcript-*.json`). These timings belong to *this* song only. A regenerated song gets measured fresh.
- Not done: `edit-plan.json`, validation, render, `delivery.md`. All timing depends on the corrected song.
