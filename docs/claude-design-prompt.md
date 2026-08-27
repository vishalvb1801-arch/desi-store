# Prompt for Claude Design — EIS desktop PDP

Paste this into Claude Design. Attach `preview/eis-pdp-mobile-snapshot.html`
(the signed-off mobile build) and `docs/EIS-desktop-design-brief.html` (tokens
and section inventory).

---

I'm designing the **desktop layout** for a Shopify product page that already has
a finished, signed-off mobile design. I've attached the live mobile page as an
HTML snapshot — open it at 390px wide to see what exists today.

**Product:** EIS Ayurvedic Pain Relief Oil, an Indian D2C brand. Traditional
Ayurvedic positioning, sold mainly to people in India with knee, back and joint
pain. Warm, apothecary feel — maroon and gold on cream, not clinical.

**The problem to solve:** every section on this page caps its content at 480px,
and only 5 of 15 define any desktop behaviour. On a 1440px monitor the whole
page is a phone-width column stranded in the middle with ~480px of dead space
either side. There is no desktop layout — that's what I need you to design.

**Hard constraint:** the mobile design must not change. Design purely for
≥750px. Reuse these exact tokens rather than introducing new ones:

- Maroon `#7B1315` · Maroon deep `#5C0D0F` (hover) · Gold `#C9A24A`
- Cream `#FBF3E7` · Ink `#2A1C18` · Muted `#5E5147` · Green `#1E7A4D`
- Border `#E7D9C3` · Star `#FFD700` · Orange accent `#E8740C`
- Playfair Display (headings) · DM Sans (body) · Manrope (rating rows)

**Design at 1440px.** Add a 1024px artboard for anything that needs to differ.

## What to design, in priority order

1. **The buy box (hero)** — the one that genuinely needs a new layout, not just
   widening. Currently a single stacked column. On desktop it wants gallery
   left, buy column right. It contains, in order: image carousel with arrows
   and thumbnails, gold star rating row, product title, sub-heading, a
   "1,192+ Doctors' Choice" badge, five ticked benefit bullets, ADD TO CART,
   a social proof row (3 avatars + animated counter + rating), a row of 9
   payment logos, a low-stock bar with delivery estimate, a counterfeit
   warning box, and a 5-question FAQ accordion. That's a lot for one column —
   decide what belongs beside the gallery and what runs full width below.

2. **Sections that just need re-columning.** Stats (3 stacked → 3 across),
   ingredients (6 herbs stacked → 3×2 or 6 across), timeline (4 stages
   stacked → horizontal), FAQ (14 accordions → two columns?).

3. **Horizontal scrollers.** Video testimonials, expert clips, Google reviews
   and social proof are all mobile swipe carousels. On desktop they can stay
   scrollers or become static rows — your call, but be consistent.

## Already fixed, design around it

- A sticky Add to Cart bar exists with a desktop variant: 1240px wide, Playfair
  title, no thumbnail, larger button, pulse and sheen animation. It reveals only
  once the buy box has scrolled past.
- Add to Cart goes straight to checkout.
- No price appears anywhere on the page, deliberately.
- The product has no photography yet — the gallery, the four how-to-use step
  squares and the expert clips are all placeholders. Design as if real images
  exist; use the hatched placeholder look where they don't.

## What I need back

One artboard per section, exported as `.dc.html`. Real hex values and spacing in
the file rather than a flattened image, so nothing gets eyeballed in the
rebuild. Tell me which artboards are final and which are exploratory.
