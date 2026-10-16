# C300-W — "Just Tired" (Wife version) · EIS Ayurvedic Pain Relief Oil · BLOCKED: wrong song

**No `edit-plan.json` yet.** `B.mp3` in Drive › C300 › B isn't the C300-W song. It is 3:49 with a female vocal, but it sings different lyrics. None of the 57 lyric lines in the brief are sung in it.

## What B.mp3 actually sings
I ran whisper twice: medium.en with a lyric prompt, then small.en with no prompt. Both runs heard the same words. The full word-level transcript is in `handoff/transcript.json`.

| time (s) | sung |
|---|---|
| 5.8–23.1 | "I kept this close, so close to my heart / Every evening I come home smiling" |
| 23.1–36.9 | "You ask me, how was your day, ji? / And I say fine, though I know it's not" |
| 59.7–93.3 | chorus: "I'm just tired, ji / Tired of holding what I can't undo …" |
| 100.9–128.5 | "You found a letter on the table / And the color left your face …" |
| 147.8–177.1 | chorus ×2: "… Please hear me before we say goodbye" |
| 181.3–227.0 | "Maybe love can hold the fracture …" / "Stay with me now, let us begin again" |

The only overlap with the brief is the hook phrase "I'm just tired, ji". The song has no Suno/ji husband scene, no dabba, no terrace call to Ravi, no bottle, no herbs and no CTA. Applying "drop every line that isn't sung" would leave zero segments.

I checked the other songs in Drive and none of them is C300-W either:
- `A.mp3` (C300 › A) is the C300-H husband song.
- `C299 A.mp3` and `C299 B.mp3` are the "caught my husband/wife cheating" ads.

## Done (audio-independent; ready for when the right song is in)
- 57 clips downloaded. All are 716×1284, 5.04 s and 24 fps.
- `handoff/clip-map.json` has every clip described, and product = true on 38, 39, 42, 43, 56 and 57.
- `handoff/contact-sheets/` has 57 four-frame strips (0.2 / 1.7 / 3.3 / 4.95 s). I looked at every one.
- `handoff/label-zoom/` has native-resolution label crops of every product clip.

### Product label audit (zoomed)
| clip | verdict | why |
|---|---|---|
| 38 | **avoid** | Label is garbled: "Ayuvedic", "ESSNSE OF WOEOA", "NATRAAL RELIEEF", "16x STEENETH", "MOUEE MASSSOE". The colours, cap and oil are right. |
| 39 | **avoid** | Brand reads "BIS". |
| 57 | **avoid** | Label is garbled: "Ayrereeic", "270 ml", a "100…" badge. |
| 43 | use **0–2.0 s only** | The front label is clean. The bottle turns at ~2.25 s, and the back label (3–5 s) is garbled. |
| 42 | use | The bottle is a small background prop. "EIS" and "PAIN RELIEF" are correct, and the small text is soft, not misspelled. |
| 56 | use | Clean throughout: the best CTA / reveal clip. |

That leaves two clean hold-able product clips for the reveal (L38), the kneel (L39) and the CTA (L56–57): **43** (front, ≤ 2.0 s) and **56**. Two of those four beats will need a reuse or a non-product clip. I'll set that once timings exist.

### Other clip flags
- **clip_30:** face drift. The husband has a moustache and no beard for the whole clip. It shows most in the close-up end (3–5 s).
- **clip_10:** no black bar (the dark top is the night window), but the bed geometry warps from ~4.0 s, so keep it under 3.8 s.
- **clip_25, clip_28:** dark night grades with no black bars, checked at the edge rows.
- **clip_46:** her hand touches the rail from ~3.0 s, but the line says "didn't grip the rail". Favour the start.
- **clip_23:** she smiles while eavesdropping (off-tone). It settles by the end.
- **clip_11:** a happy couple and flying calendar pages, lighter than the "hundred nights" line.
- No clip has a letterbox / black bar.

## Needed to continue
Upload the C300-W song (the one that sings "My husband pulled me close in bed…") to Drive › C300 › B. I'll then transcribe it, cut the plan and deliver `edit-plan.json` + this file. Or, if B.mp3 is intentional, say so and I'll cut the 57 clips to the song as sung. The captions would then follow B.mp3's real lyrics, not the brief.
