const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const p = await b.newPage({ viewport: { width: 1520, height: 1500 }, deviceScaleFactor: 2 });
  await p.goto('file://' + __dirname + '/drawer-organizer.svg');
  await p.screenshot({ path: __dirname + '/drawer-organizer.png' });
  await p.pdf({ path: __dirname + '/drawer-organizer.pdf', width: '1520px', height: '1500px', printBackground: true, pageRanges: '1' });
  await b.close();
})();
