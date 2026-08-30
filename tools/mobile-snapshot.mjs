/**
 * Mobile regression guard for the EIS PDP.
 *
 * Renders the draft theme's product page at phone widths and writes a
 * fingerprint of every element that matters: position, size, and the computed
 * styles most likely to drift. Run it before and after desktop work and diff
 * the two files — any mobile change shows up as a line in the diff.
 *
 *   node tools/mobile-snapshot.mjs baseline   # capture
 *   node tools/mobile-snapshot.mjs check      # compare against baseline
 *
 * Chromium here has no network, so the page is fetched with curl, its
 * stylesheets are inlined, and remote images become placeholders. That is
 * fine for geometry: layout comes from the CSS, not the pixels.
 */
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { createRequire } from 'node:module';

/* playwright-core may live outside the repo; PW_PATH points at it if so. */
const require = createRequire(import.meta.url);
const { chromium } = process.env.PW_PATH
  ? require(process.env.PW_PATH)
  : await import('playwright-core');

const WIDTHS = [360, 390, 430];
const PAGE = process.env.EIS_PAGE || 'preview/.cache/fullpage.html';
const OUT = 'tools/mobile-baseline.json';

/* Everything a desktop change could plausibly disturb. */
const SELECTORS = [
  '.eis-hero', '.eis-hero__stage', '.eis-hero__thumbs', '.eis-hero__rating',
  '.eis-hero__title', '.eis-hero__subtitle', '.eis-docs__pill',
  '.eis-hero__benefits', '.eis-btn', '.eis-hsp__row', '.eis-pm__row',
  '.eis-mbp', '.eis-mbp__banner', '.eis-mbp__badge', '.eis-mbp__refund',
  '.eis-stockbar', '.eis-deliv', '.eis-warn', '.eis-bfaq',
  '.eis-sticky__inner', '.eis-sticky__name', '.eis-sticky__rating',
  '.eis-trust', '.eis-stats', '.eis-herbs', '.eis-exp', '.eis-exp__card',
  '.eis-how', '.eis-how__step-media', '.eis-wte-section', '.eis-cmp',
  '.eis-faq', '.eis-rev', '.eis-sp',
];

const STYLES = ['fontSize', 'fontWeight', 'lineHeight', 'color',
  'backgroundColor', 'padding', 'margin', 'display', 'flexDirection'];

const mode = process.argv[2] || 'baseline';

const browser = await chromium.launch({
  executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
});

const snap = {};
for (const width of WIDTHS) {
  const page = await browser.newPage({ viewport: { width, height: 900 } });
  /* domcontentloaded, not load: the inlined CSS still references webfonts
     and this Chromium has no network, so 'load' never fires. */
  await page.goto('file://' + process.cwd() + '/' + PAGE,
    { waitUntil: 'domcontentloaded' });
  /* Kill transitions and animations: otherwise the sticky bar's slide-in
     races the measurement and its position differs run to run. */
  await page.addStyleTag({
    content: `*, *::before, *::after {
      transition: none !important;
      animation: none !important;
      scroll-behavior: auto !important;
    }`,
  });
  await page.waitForTimeout(500);
  /* Scroll far enough down that the sticky bar has revealed. */
  await page.evaluate(() => window.scrollTo(0, 4000));
  await page.waitForFunction(
    () => document.querySelector('.eis-sticky')?.classList.contains('is-visible'),
    null,
    { timeout: 5000 }
  ).catch(() => {});
  await page.waitForTimeout(400);

  snap[width] = await page.evaluate(
    ({ sels, styleKeys }) => {
      const out = {};
      for (const sel of sels) {
        const el = document.querySelector(sel);
        if (!el) { out[sel] = null; continue; }
        const r = el.getBoundingClientRect();
        const cs = getComputedStyle(el);
        const s = {};
        for (const k of styleKeys) s[k] = cs[k];
        /* Anything inside a fixed element is positioned against the viewport,
           so adding the scroll offset would record where the page happened to
           stop rather than where the element sits. Keep those
           viewport-relative — the sticky bar and everything in it. */
        let fixed = false;
        for (let n = el; n && n !== document.documentElement; n = n.parentElement) {
          if (getComputedStyle(n).position === 'fixed') { fixed = true; break; }
        }
        out[sel] = {
          w: Math.round(r.width),
          h: Math.round(r.height),
          x: Math.round(r.left + (fixed ? 0 : window.scrollX)),
          y: Math.round(r.top + (fixed ? 0 : window.scrollY)),
          anchor: fixed ? 'viewport' : 'page',
          clipped: el.scrollWidth > Math.ceil(r.width) + 1,
          ...s,
        };
      }
      out.__docWidth = document.documentElement.scrollWidth;
      return out;
    },
    { sels: SELECTORS, styleKeys: STYLES }
  );
  await page.close();
}
await browser.close();

if (mode === 'baseline') {
  writeFileSync(OUT, JSON.stringify(snap, null, 2) + '\n');
  const seen = Object.values(snap[WIDTHS[0]]).filter((v) => v && v.w).length;
  console.log(`baseline written to ${OUT} — ${seen} elements x ${WIDTHS.length} widths`);
} else {
  if (!existsSync(OUT)) { console.error(`no baseline at ${OUT}`); process.exit(1); }
  const base = JSON.parse(readFileSync(OUT, 'utf8'));
  const diffs = [];
  for (const width of WIDTHS) {
    for (const sel of Object.keys(base[width] || {})) {
      const a = base[width][sel], b = snap[width]?.[sel];
      if (JSON.stringify(a) !== JSON.stringify(b)) {
        diffs.push(`${width}px  ${sel}\n    was ${JSON.stringify(a)}\n    now ${JSON.stringify(b)}`);
      }
    }
  }
  if (!diffs.length) { console.log(`mobile unchanged at ${WIDTHS.join('/')}px`); }
  else { console.error(`MOBILE CHANGED — ${diffs.length} difference(s):\n\n` + diffs.join('\n\n')); process.exit(1); }
}
