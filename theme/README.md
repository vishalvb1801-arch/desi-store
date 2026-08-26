# EIS — Ayurvedic Pain Relief Oil PDP

Source of truth for the custom PDP work on **eliteindianstore.com**.

Only the files this project has changed live here — this is **not** a full theme
checkout. Everything else in the theme is untouched and lives only in Shopify.

## Where things run

| | |
|---|---|
| Store | eliteindianstore.com (EIS) |
| Product | Ayurvedic Pain Relief Oil — `/products/ayurvedic-pain-relief-oil` |
| Template | `product.eis-oil.json`, assigned via the product's `templateSuffix` |
| Live theme | **Fv3<> of Horizon** — `gid://shopify/OnlineStoreTheme/186785857843` |
| Draft theme | **EIS PDP — Fv3 of Horizon** — `gid://shopify/OnlineStoreTheme/188315926835` |

The PDP is composed of 14 custom `eis-*` sections, in this order:

```
announcement · hero · faq · trust · videos · social-proof · stats
ingredients · how-to-use · timeline · comparison · offer-repeat
guarantee · reviews · footer
```

That is 15 sections — `social-proof` was added after `videos`.

## Status

**Live already** — the product is assigned to `product.eis-oil.json`, so all 14
sections render on the storefront.

**Staged on the draft theme, NOT live.** The four files in this directory are
uploaded to the draft theme and take effect only when that theme is published:

| File | Change |
|---|---|
| `layout/theme.liquid` | Hides the global `footer-group` on the `eis-oil` template only, so the PDP shows one footer instead of two |
| `sections/eis-announcement-bar.liquid` | Fade-rotate replaced with a CSS-only right-to-left marquee; icons; adjustable spacing and height |
| `snippets/eis-icon.liquid` | New — 9 inline SVG stroke icons used by the announcement bar |
| `templates/product.eis-oil.json` | Announcement bar copy: 3 messages with icons; hero review avatar |
| `sections/eis-faq-accordion.liquid` | New five questions; accordion starts fully closed |
| `sections/eis-trust-badges.liquid` | Heading count 50,000 → 36,243; icon glyph size is now a setting (28px) |
| `sections/eis-video-testimonials.liquid` | Grid → horizontal snap scroller with its own scroll bar; captions → name, city, verified tick |
| `sections/eis-social-proof.liquid` | New — face strip, rating, headline, swipeable review cards with benefit chips and a segmented indicator |
| `sections/eis-product-hero.liquid` | Google mark beside the hero review name, behind a `review_google` toggle |
| `sections/eis-stats-block.liquid` | Heading count 50,000 → 36,243; curved bottom edge (SVG, colour/depth are settings) |
| `sections/eis-ingredients-grid.liquid` | Phone-only bottle cut-out tipped 45° each side of the *15 Herbs* heading; tilt, width, bleed, row height, heading gutter and shadow are settings |

Publishing is a manual step in Shopify admin (Online Store → Themes → the draft
theme → Publish). It cannot be automated from here: theme file writes and theme
publishing against the live storefront are both blocked.

## Known gaps

- **The bottle cut-out is derived, not an original asset.** The merchant's
  render is a JPEG on solid black. `assets/eis-bottle-cutout.png` in this
  repo was produced from it by flood-filling the border-connected black
  region to transparent (threshold 26, 0.8px feather) and is uploaded to
  Shopify Files as `eis-bottle-cutout.png`. If the packshot is ever
  re-rendered, redo the key — the section needs an **upright PNG with a
  transparent background and no baked-in shadow**, because the tilt is a
  CSS `rotate()` on the image and the shadow a `drop-shadow()` on its
  wrapper. A shadow rendered into the file would tip over with the bottle;
  a solid background would show as a rotated rectangle.
- **The bottles clip if nudged too far up.** `.eis-herbs` sets
  `overflow: clip` to stop the rotated images causing sideways page scroll,
  which means a bottle taller than the section gets cut flat at the top
  edge. The shipped defaults (22% wide, 88px bleed, 150px row, +8px nudge)
  were measured to clear it at 390px; raising the width or lowering the
  nudge can reintroduce it.
- **The stats curve colour is not automatic.** `curve_color` defaults to
  `#FFFFFF` because the section below it (`eis-ingredients-grid`) has a white
  background. Reorder the sections and this has to be re-matched by hand.
- **The product has no images.** `media` is empty, so the hero gallery renders
  blank on a live, buyable page. This is the most visible defect on the PDP.
- **The product has no description**, though the hero draws its copy from
  section blocks rather than `descriptionHtml`, so this is cosmetic.
- **The header is untouched.** A redesign was discussed and deliberately
  deferred. Note it is rendered from `layout/theme.liquid` via
  `{% section 'eis-header' %}`, so it appears on *every page of the store* —
  changing it is not a PDP-scoped edit.
- **Google mark on the hero review.** `review_google` (default on) renders
  Google's four-colour G beside the reviewer name. The merchant states this
  review originates from a genuine Google review, that the reviewer consented,
  and that legal advice was taken. Only keep this on where that holds — a
  Google mark beside a review Google did not verify is a trademark and
  consumer-protection problem. Toggle it off in the theme editor under
  *Hero review*.
- **UGC names are placeholders.** The three clip blocks ship with invented
  names and cities (Anita R. / Nagpur, Vikram S. / Jaipur, Dr. Meera N. /
  Kochi) purely as layout scaffolding. Replace them with the real people in
  the clips before this goes live — a verified tick beside an invented name
  is a false attribution, and the clips themselves are still placeholders.
- **Social-proof reviews are invented.** All 8 review blocks and both benefit
  chips are placeholder copy, and the 5 face slots are empty. Every card
  carries a "Verified" badge, which is a specific claim about a specific
  named person — replace the lot with real reviews, or switch
  `show_verified` off per block, before publishing.
- **Diabetes was deliberately excluded** from the review angles. India's
  Drugs & Magic Remedies (Objectionable Advertisements) Act names diabetes
  among the conditions for which advertising a remedy is prohibited, and a
  testimonial on a product page is advertising. Night leg cramps and
  on-feet-all-day cover adjacent ground lawfully.
- **Template formatting.** The theme's stored copy of
  `templates/product.eis-oil.json` is a compact variant (18197 bytes,
  6c8fbad1) while the copy here is pretty-printed. Semantically identical —
  verified by reading the stored file back — but the two are not byte-equal,
  so normalise before comparing checksums.
- **Unverified claims.** The PDP states "89% / 92% / 86%" outcome statistics,
  "GMP CERTIFIED", "LAB TESTED", "36,243+ Families Without Pain", and three
  named reviews with purchase dates, on a product created 2026-08-25 with no
  orders. If these are not substantiated they carry real exposure under Indian
  consumer-protection and ASCI advertising rules.

## Gotchas worth knowing

- **Inventory:** the variant has `tracksInventory: false`, so `totalInventory: 0`
  does *not* block Add to Cart. The product is buyable.
- **JSON templates:** Shopify pretty-prints them on read but stores raw bytes on
  write. To compare a local copy against a `checksumMd5` from the API, minify
  first and drop the comment header. The stored file is now pretty-printed
  (~20KB) where it used to be minified (~12KB) — same JSON, different bytes.
- **`layout/theme.liquid` does not use `sections/header-group.json`.** It has
  been customised to render `eis-header` directly. `header-group.json` still
  exists but is dead, and all of its `custom-liquid` blocks are disabled.
- **Marquee mechanics:** the track holds two identical copies of the message
  list and slides `-50%`. `min-width: 200%` keeps the loop gapless when the
  messages are narrower than the viewport; `flex: none` stops the track being
  shrunk to fit by its `overflow: hidden` flex parent. Remove either and the
  marquee breaks.

## Preview

`preview/announcement-bar-bench.html` renders the announcement bar with the real
section CSS and sliders for speed, height, text size and spacing. Open it in a
browser. It cannot reproduce how the section resolves inside Horizon — only a
logged-in Shopify preview shows that.
