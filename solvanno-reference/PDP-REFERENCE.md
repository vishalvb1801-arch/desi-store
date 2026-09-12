# SOLVANNO PDP — Design Reference

**Source:** `theme_export__www-solvanno-com-phx-test__12SEP2026-0408am.zip`
**Reference page:** `templates/product.solvanno-milk-thistle.json` (SOLVANNO™ Milk Thistle Support)

This is the canonical Solvanno product page. Every future product PDP should be
built by copying this template, swapping the content, and changing nothing about
the token values, section order, or layout rules unless there is a reason.

The full working kit is in [`kit/`](kit/) — 13 sections, 5 snippets, and the
Milk Thistle template JSON exactly as exported.

---

## 1. Design tokens

All tokens are defined once in `snippets/sol-tokens.liquid` and scoped per
section via `#shopify-section-{{ id }}`. Each section exposes only the colour
settings it uses; every token still resolves because the snippet carries
fallbacks.

| Token | Value | Role |
|---|---|---|
| `--sol-maroon` | `#364811` | Primary brand olive. Headings on light, icon fills, accents. |
| `--sol-maroon-deep` | `#24330f` | Deep olive. Dark section backgrounds. |
| `--sol-maroon-darkest` | `#191f12` | Near-black olive. Footer background. |
| `--sol-gold` | `#9cae01` | Lime-gold. Buttons, badges, progress fills. |
| `--sol-gold-light` | `#9cae01` | Accent on dark backgrounds. |
| `--sol-cream` | `#f4f6e9` | Panel fill on light sections (benefit box). |
| `--sol-cream-light` | `#f0f4d6` | Heading colour on dark; pale tint on light. |
| `--sol-ink` | `#1e2413` | Body text. |
| `--sol-muted` | `#545a48` | Secondary text, captions, meta. |
| `--sol-soft` | `#545a48` | Tertiary text. |
| `--sol-green` | `#4a8b2c` | Check marks, "verified" states. |
| `--sol-line` | `#e3e6d6` | Borders, dividers, progress tracks. |
| `--sol-max` | `480px` | Mobile content width. |

Additional literals used in the Milk Thistle page:

| Colour | Value | Where |
|---|---|---|
| Page ground | `#fafaf5` | Off-white background on light sections. |
| Star gold | `#e0a526` | Rating stars, "What to Expect" accent. |
| CTA green | `#b7ce2e` | `.sol-btn` background (brighter than `--sol-gold`). |
| CTA label | `#2c4a2a` | Text on the CTA, and the hero H1. |
| Benefit box border | `#EFE0C9` | Warm hairline on the cream benefit panel. |
| Gallery frame | `#dde7c2` | 1px border on the hero image stage. |

> **Naming note:** the `maroon` tokens are legacy names from the kit's origin.
> They carry olive-green values now. Keep the names — every section references
> them — and only change the values.

### Background rhythm

The page alternates so no two adjacent sections share a ground:

```
announcement   dark  #364811
hero           white #ffffff
trust badges   dark  #24330f
video testim.  light #fafaf5
social proof   dark  #364811
stats          light #fafaf5   ← convex curve divider, 48px
ingredients    light #fafaf5
expert videos  light #fafaf5
what to expect dark  #364811
comparison     light #fafaf5
FAQ            dark  #364811
reviews        light #fafaf5
footer         dark  #191f12
```

---

## 2. Typography

Loaded by `snippets/sol-fonts.liquid` (rendered by every section; the browser
de-dupes). Playfair Display + DM Sans + Manrope, `display=swap`, non-blocking
via `media="print" onload`.

- **Display / headings** — `--sol-serif`: `'Playfair Display', Georgia, 'Times New Roman', serif`, weight 600.
- **Body / UI** — `--sol-sans`: `'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, system-ui, sans-serif`.
- **Manrope** — used only inside custom-liquid blocks (delivery/stock strip).

### Type scale (mobile → ≥750px → ≥1200px)

| Element | Mobile | Tablet | Desktop |
|---|---|---|---|
| Hero H1 | 31px / 1.12 | 34px → 40px | 44px |
| Hero subtitle | 14px / 1.5 | 15px → 16px | 16px |
| Section heading (serif) | 26–30px / 1.18 | — | — |
| Stat number | 52px | — | — |
| Benefit text | 13px / 1.45 | 13.5px | — |
| CTA label | 19px, 700, `.14em` tracking | — | — |
| Buy-box price | 26px, 700, serif | — | — |
| Badge / eyebrow | 10–12px, 700, `.08em` tracking, uppercase | — | — |
| Feature pill | 9.5px / 1.25, 500 | — | — |

Section headings accept a `heading_size` setting per section — Milk Thistle uses
26 (comparison, FAQ), 27 (experts, reviews), 33 (what to expect).

---

## 3. Layout system

**Mobile-first, 480px content width.** Every section takes `content_width`
(default 480) and centres itself. The desktop layout is additive — it lives
entirely inside `@media (min-width: …)` blocks, so the mobile rendering is never
touched by desktop rules.

### Breakpoints

| Query | Purpose |
|---|---|
| `max-width: 359px` / `389px` | Small-phone typography trims. |
| `min-width: 750px` | Two-column hero (976px max), 3-up trust marks. |
| `min-width: 1200px` | Wide hero (1280px max), 552px gallery column, 48px gutter. |
| `prefers-reduced-motion: reduce` | Disables every animation (13 occurrences — keep this). |

### The hero grid trick

`.sol-hero__media` and `.sol-hero__buy` are `display: contents` on mobile, so
children lay out as if the wrappers did not exist. At ≥750px they become real
grid columns:

```css
.sol-hero { display: grid; grid-template-columns: minmax(0,47%) minmax(0,1fr);
            grid-template-rows: min-content min-content 1fr; column-gap: 28px; }
.sol-hero__media { grid-column: 1; grid-row: 1; }
.sol-hero__buy   { grid-column: 2; grid-row: 1 / span 3; }
.sol-bfaq        { grid-column: 1; grid-row: 2; }   /* FAQ under the gallery */
.sol-hero__marks { grid-column: 1; grid-row: 3; }   /* trust marks under FAQ */
```

Social proof and the warning block move with `order: 10 / 11` on desktop rather
than a second DOM position. Copy this pattern — do not duplicate markup.

### Radii & elevation

- `999px` — pills, avatars, check circles, nav buttons (24 uses; the default).
- `10–12px` — cards, panels, the CTA, the benefit box.
- `14px` — the gallery stage and the desktop buy-box FAQ.
- `4px` — small save-badge chips.
- CTA shadow: `0 6px 18px rgba(123,19,21,.28)`.
- Pill shadow: `0 2px 8px rgba(0,0,0,.25)`.

### Vertical rhythm

Section padding on the Milk Thistle page, in px:

| Section | top | bottom |
|---|---|---|
| hero | 8 | 0 (padding-x 12) |
| trust badges | 34 | 34 |
| video testimonials | 30 | 30 |
| social proof | 34 | 34 |
| stats | 36 | 0 (curve closes it) |
| ingredients | 34 | 34 |
| expert videos | 22 | 26 |
| what to expect | 34 | 34 |
| comparison | 34 | 34 |
| FAQ | 18 | 30 |
| reviews | 32 | 32 |
| footer | 30 | 100 (clears the sticky bar) |

**34/34 is the default.** Deviate only where a section carries its own internal
padding or a divider.

---

## 4. Section-by-section blueprint

The page runs 13 sections in a fixed conversion order. Reuse the order.

### 1. `sol-announcement-bar` — dark, scrolling ticker
Three rotating messages with icons, 24s scroll, `✦` separator, 12px.
Milk Thistle copy: `FREE US SHIPPING OVER $50` (truck) · `38,472+ HAPPY CUSTOMERS` (families) · `90-DAY MONEY-BACK GUARANTEE` (discount).

### 2. `sol-product-hero` — the buy box
The largest section (3,350 lines). Everything below the gallery is an
**orderable block**, so the buy-box stack is rearrangeable in the customiser
without touching code.

- **Gallery** — reads `product.media` first (video included, MP4 over GIF); `gallery_image` blocks are the fallback for products without media and disappear automatically once real media exists. Square `aspect-ratio: 1/1`, `object-fit: contain` so 4:5 and 16:9 uploads show whole. Feature pills overlay top-left, nav bottom-right, 4.5 thumbnails in view.
- **Title** — serif, centred, `#2c4a2a`.
- **Benefit list** — 7 `benefit` blocks in a cream panel (`#f4f6e9`, border `#EFE0C9`, radius 12, margin `16px 0 24px`), each with a 19px green check circle. Format: **bold claim** + ` – ` + plain-text proof. Milk Thistle's 7: liver detox (80% silymarin), bloating/digestion, energy/clarity, blood sugar, 8 actives in one capsule, third-party tested, 90-day guarantee.
- **Offer ladder** — deliberately **not** hard-coded. The section exposes an app-block slot inside "Choose Your Supply"; MoonBundle owns offer selection and Add to Cart. The native `.sol-btn` is a fallback (`show_fallback_atc`).
- **Trust stack**, in order: social proof row (avatar trio + animated count 10,000→36,243 + 4.8/5) → payment marks (visa, mastercard, amex, paypal, applepay, shoppay) → money-back promise → stock bar (7% "Almost sold out") → delivery estimate (2–5 business days, geo flag).
- **Buy-box FAQ** — 5 accordions: Description, Money-Back Guarantee, Shipping & Delivery, Is Checkout Secure?, Contact Us. Desktop moves this under the gallery.
- **Sticky bar** — reveals `after_buy_box`, action `scroll_to_atc`, on desktop too, shows rating `4.8/5 · 38,472 reviews`.

### 3. `sol-trust-badges` — dark, 3-up
Three icon + two-line labels, 28px icons. Milk Thistle: `80% / SILYMARIN`, `THIRD-PARTY / LAB TESTED`, `90-DAY / GUARANTEE`. Line break is a literal newline in the label.

### 4. `sol-video-testimonials` — light
2.2 cards in view, 9:16 clips, each with an MP4 URL, poster, name and city
(Howard R. / Portland, OR). Heading: "Real People, Real Results".

### 5. `sol-social-proof` — dark
Five customer `face` images, then 8 `review` blocks as 1.2-in-view cards. Each
review = 5 stars + quote + **two outcome tags** + avatar + name + city +
verified. Tags are the mechanism — `Reduced Bloating`, `More Energy`,
`Better Sleep`, `Doctor Approved`. Heading: "Why 38,472+ People Trust …".

### 6. `sol-stats-block` — light, convex curve divider
Three animated percentage bars (89% / 92% / 86%) with icons, a desktop product
photo, footnote "Based on customer feedback*", and a 48px convex curve in
`#fafaf5` closing the section.

### 7. `sol-ingredients-grid` — light, 3 columns
One `herb` block per active: name, dose + standardisation (`300mg · 80% Silymarin`),
a 4:3 image at radius 8, and a "MORE INFO" detail panel. Floating bottle image
overlays the heading row (45° angle, 48px wide, −96px offset, 76 bleed, 80 shadow).

### 8. `sol-expert-videos` — light
Eyebrow `EXPERTS RECOMMENDED`, two-line serif heading, then 200px expert cards
with name + credential + years ("Dr. Emily Carter / Integrative MD, 15 yrs").
Progress bar on.

### 9. `sol-what-to-expect` — dark `#364811`, gold `#e0a526`
Four auto-cycling timeline stages (6s each), each with a looping video, a stage
name, a time badge, and exactly three outcome bullets:

| Stage | Badge |
|---|---|
| Clearing Out | DAYS 1–14 |
| Energy Returns | WEEKS 3–6 |
| Deep Support | MONTHS 2–3 |
| Full Restoration | MONTHS 4–6 |

Portrait frames, 300px mobile / 250px wide, max 1280px. Footnote states the dose.

### 10. `sol-comparison-table` — light
Seven rows, `SOLVANNO` vs `Other Brands`, every row ✓/✗, a 130px bottle image in
the brand column. Row height 62, column width 78. Rows are *differentiators*,
not generic features.

### 11. `sol-faq-accordion` — dark
16 questions, one open at a time, `enable_seo_schema: true` (emits FAQPage JSON-LD
— keep this on). Footer CTA with the support email. Question order runs:
what is it → does it work → how long → who is it for → how to take → supply
length → lifestyle → best time → what makes us different → safety → tried others
→ guarantee → shipping → checkout → contact.

### 12. `sol-reviews` — light
Six photo reviews, 1.5 in view, 1:1 images, 5-line quote clamp, avatar + name +
"Verified purchase", and a `READ MORE REVIEWS` link.

### 13. `sol-footer` — darkest `#191f12`
Logo `SOLVANNO` + tagline `SUPPORT FROM WITHIN`, newsletter capture, contact
block with the full postal address, 5 policy links, certification badges
(`MADE IN THE USA 🇺🇸`, `GMP CERTIFIED`), payment badges, FDA disclaimer,
copyright. Bottom padding 100px to clear the sticky bar.

---

## 5. Copy formulas

These patterns repeat across the page and should be preserved per product:

- **Social-proof number** — one figure, used everywhere: `38,472`. Announcement bar, social-proof heading, hero rating, sticky bar. Pick one number per product and never vary it.
- **Rating** — `4.8/5`, 5 stars, always paired with the review count.
- **Guarantee** — `90-Day Money-Back Guarantee`, stated in the announcement bar, benefit list, trust badge, buy-box FAQ, comparison row, and FAQ. Six touches.
- **Hero benefit line** — `**Bold outcome** – supporting proof` where the proof is a dose, a standardisation, or a certification.
- **Review quote** — first person, one specific outcome, a time marker ("six weeks in", "two months in"), no superlatives.
- **Stat label** — `reported/felt/said` + outcome. Always hedged, always footnoted.
- **Ingredient role** — `dose · standardisation` (`300mg · 80% Silymarin`). Number first.

---

## 6. Building a PDP for a new product

1. Duplicate `kit/templates/product.solvanno-milk-thistle.json` as `product.<handle>.json`.
2. Keep all 13 sections and their order. Delete a section only if the product genuinely has no content for it — do not reorder.
3. Keep every colour setting as-is. The palette is the brand.
4. Swap content in this order — hero title → 7 benefits → ingredient blocks → comparison rows → what-to-expect stages → FAQ → reviews.
5. Set one social-proof number and one rating, then propagate to all four places.
6. Re-shoot or re-crop: gallery images square, review images 1:1, ingredient images 4:3, video clips 9:16.
7. Leave `show_fallback_atc` off if MoonBundle is running; the app block owns the offer ladder.
8. Keep `enable_seo_schema: true` on the FAQ.
9. Check the 359px and 389px breakpoints — several labels are trimmed there.
10. Verify `prefers-reduced-motion` still kills every animation you add.

### Gotchas carried over from the kit

- `sol-product-hero.liquid` was already split — desktop CSS lives in `snippets/sol-hero-desktop.liquid` because the section file hit Shopify's size limit and uploads failed **silently, with no error**. If you grow the hero, split again rather than debug a no-op upload.
- `.sol-sp` is taken by `sol-social-proof`; the hero's own social-proof row uses `.sol-hsp`. Namespace new classes.
- `{% render 'sol-fonts' %}` runs in every section so each one is copy-paste portable. For production you can move the three tags into `layout/theme.liquid` and delete the render calls.
- The gallery prefers `product.media` over `gallery_image` blocks by design — block images vanish the moment real media is uploaded. Don't "fix" this.
