// Widescreen (1920x1080) render of a longform page, in a frame range so parts can run in parallel.
// Usage: node kit/longform/render-wide.js <html> out.mp4 <fromSec> <toSec>
const { chromium } = require('playwright'); const { spawn } = require('child_process'); const path = require('path');
(async () => {
  const [src, out, a, b] = process.argv.slice(2); const fps = 30;
  const f0 = Math.round(+a * fps), f1 = Math.round(+b * fps);
  const br = await chromium.launch(); const p = await br.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on('pageerror', e => console.log('PAGE ERROR', e.message));
  await p.goto('file://' + path.resolve(src)); await p.waitForTimeout(600);
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-i', '-', '-c:v', 'libx264',
    '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', out]);
  for (let i = f0; i < f1; i++) {
    await p.evaluate(t => frame(t), i / fps);
    const buf = await p.screenshot({ type: 'jpeg', quality: 90 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); await br.close(); console.log('rendered', out);
})();
