// Render every drawer-<size>.svg to PNG (2x) and a single-page PDF.
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const sizes = require('./sizes.json');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  for (const [size, h] of Object.entries(sizes)) {
    const p = await b.newPage({ viewport: { width: 1520, height: h }, deviceScaleFactor: 2 });
    await p.goto(`file://${__dirname}/drawer-${size}.svg`);
    await p.screenshot({ path: `${__dirname}/drawer-${size}.png` });
    await p.pdf({ path: `${__dirname}/drawer-${size}.pdf`, width: '1520px', height: `${h}px`, printBackground: true, pageRanges: '1' });
    await p.close();
  }
  await b.close();
})();
