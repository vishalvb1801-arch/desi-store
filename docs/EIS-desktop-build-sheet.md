# EIS PDP — desktop & iPad build sheet

Measured from the supplied Claude Design file (EIS Desktop PDP · Full Page),
rendered at both artboards and inspected programmatically. Mobile is frozen:
every rule below goes inside a `min-width` media query, and
`tools/mobile-snapshot.mjs check` must stay clean at 360/390/430.

## Breakpoints

| artboard | viewport | content wrapper |
|---|---|---|
| desktop  | 1440px | 1280px |
| iPad     | 1024px |  976px |

Existing sections already break at 750px. Use:
- `@media (min-width: 750px)`  — tablet/iPad treatment
- `@media (min-width: 1200px)` — full desktop treatment

## Per-section column counts (desktop → iPad)

| section | desktop | iPad |
|---|---|---|
| hero: page split (gallery \| buy box) | 2-col, gallery 552px | 2-col, gallery 448px |
| hero: thumbnails | 5-col | 5-col |
| hero: trust badges | 3-col | 3-col |
| video testimonials (Real People) | 3 across | 3 across |
| social proof: face strip | 4-col | 4-col |
| social proof: review cards | 4-col | 2-col |
| stats (After 36,243 Bottles) | 2-col | 2-col |
| ingredients (15 Herbs) | 3-col | 3-col |
| experts (Doctors Recommend) | 3-col, 840px | 3-col, full |
| timeline: nodes | 4-col | 4-col |
| timeline: stage cards | 4 across | 4 across |
| how-to-use: page split | 2-col | 2-col |
| how-to-use: step cards | 2x2 | 2x2 |
| comparison table | 3-col, 998px | 3-col, full |
| FAQ | 2-col | 2-col |
| reviews | 3-col | 2-col |

## Hero — structural notes

Desktop moves two blocks from the buy-box column into the LEFT column,
under the gallery:
1. the buy-box FAQ (`.eis-bfaq`)
2. the trust badges section (`eis-trust-badges`) — sits under the gallery
   in the design, but is a separate section in the theme, so it stays where
   it is and only its own desktop rules change.

The design also orders the buy box as: title, subtitle, doctors pill,
benefits, ATC, payment marks, Cashfree, stock bar, delivery, social proof,
warning — i.e. the social proof row sits LOW, not above the title as it does
on mobile. Achieve with flex `order` on the desktop column only; never move
it in the DOM, or mobile changes.

## Rules

- No DOM moves. Desktop layout is CSS only (grid/flex + `order`), so the
  mobile fingerprint cannot shift.
- Class prefixes stay section-unique: section `{% style %}` is page-wide.
- After every section, run:
  `PW_PATH=... node tools/mobile-snapshot.mjs check`
