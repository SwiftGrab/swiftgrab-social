// Usage: node kit/render.js kit/videos/<name>.html out.mp4 [seconds=16]
const { chromium } = require('playwright'); const { spawn } = require('child_process'); const path = require('path');
(async () => {
  const [src, out, secs] = process.argv.slice(2); const dur = +(secs || 16), fps = 30;
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on('pageerror', e => console.log('PAGE ERROR', e.message));
  await p.goto('file://' + path.resolve(src)); await p.waitForTimeout(500);
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out]);
  for (let i = 0; i < dur * fps; i++) {
    await p.evaluate(t => frame(t), i / fps);
    const buf = await p.screenshot({ type: 'jpeg', quality: 90 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); await b.close(); console.log('rendered', out);
})();
