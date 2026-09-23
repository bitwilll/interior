// Render every drawer-<size>.svg to PNG (2x) + PDF, and a 3D preview PNG per layout.
// 3D: pages are served from this folder via request interception; three.js comes from
// THREE_JS (a local three.module.js) when set, else from the CDN in render3d.html.
const fs = require('fs');
const path = require('path');
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const sizes = require('./sizes.json');
const THREE_JS = process.env.THREE_JS;

(async () => {
  const b = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium',
    args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'],
  });
  for (const [size, h] of Object.entries(sizes)) {
    const p = await b.newPage({ viewport: { width: 1520, height: h }, deviceScaleFactor: 2 });
    await p.goto(`file://${__dirname}/drawer-${size}.svg`);
    await p.screenshot({ path: `${__dirname}/drawer-${size}.png` });
    await p.pdf({ path: `${__dirname}/drawer-${size}.pdf`, width: '1520px', height: `${h}px`, printBackground: true, pageRanges: '1' });
    await p.close();
  }
  for (const size of process.argv.slice(2)) {
    const p = await b.newPage({ viewport: { width: 2400, height: 1500 } });
    p.on('console', (m) => m.type() === 'error' && console.error('[page]', m.text()));
    p.on('pageerror', (e) => console.error('[page]', e.message));
    if (THREE_JS) await p.route('https://cdn.jsdelivr.net/**', (r) =>
      r.fulfill({ body: fs.readFileSync(THREE_JS), contentType: 'text/javascript' }));
    await p.route('http://drawer.local/**', (r) => {
      const f = path.join(__dirname, new URL(r.request().url()).pathname);
      r.fulfill({ body: fs.readFileSync(f), contentType: f.endsWith('.json') ? 'application/json' : 'text/html' });
    });
    await p.goto(`http://drawer.local/render3d.html?size=${size}`);
    await p.waitForFunction(() => document.title === 'rendered', null, { timeout: 120000 });
    await p.screenshot({ path: `${__dirname}/render3d-${size}.png` });
    await p.close();
  }
  await b.close();
})();
