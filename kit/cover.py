"""Thumbnail fix: every platform uses a video's FIRST frame as its cover, and our videos start on an empty background.
Usage: python3 kit/cover.py <video.mp4> <seconds where the hook headline is fully visible, e.g. 3.5> <out-cover.jpg> <out-video.mp4>
Makes a branded cover (frame + SwiftGrab logo band, headline kept inside Instagram's 3:4 grid crop) and a copy of the
video whose first two frames are that cover. Schedule the out-video, and pass the cover's public URL as videoThumbnailUrl."""
import subprocess, sys, os
from PIL import Image, ImageDraw
src, t, cover, out = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
here = os.path.dirname(os.path.abspath(__file__)); raw = cover + '.raw.png'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', t, '-i', src, '-frames:v', '1', raw], check=True)
fr = Image.open(raw).convert('RGBA'); im = fr.copy(); im.alpha_composite(fr.crop((0, 170, 1080, 1560)), (0, 250))
band = Image.new('RGBA', (1080, 330)); g = ImageDraw.Draw(band)
for y in range(330): g.line([(0, y), (1080, y)], fill=(10, 16, 36, int(240 * min(1, y / 110))))
logo = Image.open(os.path.join(here, 'logo-band.png')).convert('RGBA'); logo = logo.crop(logo.getbbox())
logo = logo.resize((520, int(520 * logo.height / logo.width)))
im.alpha_composite(band, (0, 1590)); im.alpha_composite(logo, ((1080 - logo.width) // 2, 1640))
im.convert('RGB').save(cover, quality=92); os.remove(raw)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-loop', '1', '-t', '0.1', '-i', cover, '-filter_complex',
                "[1:v]scale=1080:1920,fps=30[c];[0:v][c]overlay=enable='lt(t,0.067)'[v]", '-map', '[v]', '-map', '0:a',
                '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-movflags', '+faststart', out], check=True)
print('cover', cover, 'video', out)
