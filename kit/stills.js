// Usage: node kit/stills.js kit/videos/<name>.html outprefix 2.5 6 10 13.5  -> outprefix_<t>.jpg
const { chromium } = require('playwright'); const path = require('path');
(async () => { const [src, pre, ...ts] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on('pageerror', e => console.log('PAGE ERROR', e.message));
  await p.goto('file://' + path.resolve(src)); await p.waitForTimeout(500);
  for (const t of ts) { await p.evaluate(t => frame(+t), t); await p.screenshot({ path: `${pre}_${t}.jpg`, type: 'jpeg', quality: 70 }); }
  await b.close(); })();
