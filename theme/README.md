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
announcement · hero · faq · trust · videos · stats · ingredients
how-to-use · timeline · comparison · offer-repeat · guarantee · reviews · footer
```

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
| `templates/product.eis-oil.json` | Announcement bar copy: 3 messages with icons |

Publishing is a manual step in Shopify admin (Online Store → Themes → the draft
theme → Publish). It cannot be automated from here: theme file writes and theme
publishing against the live storefront are both blocked.

## Known gaps

- **The product has no images.** `media` is empty, so the hero gallery renders
  blank on a live, buyable page. This is the most visible defect on the PDP.
- **The product has no description**, though the hero draws its copy from
  section blocks rather than `descriptionHtml`, so this is cosmetic.
- **The header is untouched.** A redesign was discussed and deliberately
  deferred. Note it is rendered from `layout/theme.liquid` via
  `{% section 'eis-header' %}`, so it appears on *every page of the store* —
  changing it is not a PDP-scoped edit.
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
