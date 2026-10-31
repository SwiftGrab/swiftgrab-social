// node kit/stories/make.js  -> media/stories/link-<n>.jpg (Story pictures with the website + GitHub links)
const { chromium } = require('playwright'); const path = require('path');
const V = [['The fast download manager for <b>Windows</b>', 'screens/app-main.webp'],
           ['One click in your browser. <b>SwiftGrab</b> does the rest.', 'screens/addon-popup.webp'],
           ['Downloads that <b>never start over</b>', 'screens/tut-working.webp'],
           ['Buy once. <b>No subscription.</b>', 'screens/app-license.webp']];
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  for (const [i, [t, img]] of V.entries()) {
    await p.goto('file://' + path.resolve(__dirname, 'link-story.html') + '?t=' + encodeURIComponent(t) + '&img=' + encodeURIComponent(img));
    await p.waitForTimeout(600);
    const out = path.resolve(__dirname, '../../media/stories/link-' + (i + 1) + '.jpg');
    await p.screenshot({ path: out, type: 'jpeg', quality: 90 }); console.log(out); }
  await b.close(); })();
