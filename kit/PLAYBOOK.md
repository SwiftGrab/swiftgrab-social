# SwiftGrab daily video playbook

Every day: make **3 new vertical videos** (1080×1920, 24–30 s, 30 fps, with a **voice-over** and quiet music) that show the **real** SwiftGrab app,
upload them to this repo, and schedule them in Metricool for **tomorrow** on Instagram (Reel), Facebook (Reel), TikTok and YouTube (Short).

Owner: Sevada (salesswiftgrab@gmail.com). Prefers short, simple English. Timezone America/Los_Angeles.
Metricool brand id **7635540**. Website **getswiftgrab.com**. Product: SwiftGrab, a download manager for Windows 10 & 11.

## Facts you may use (never invent others)
- 30-day free trial with every feature. Then buy once, keep it, no subscription: **Single PC $19.99**, **Family $29.99 (3 PCs)**.
- Downloads split into parts with up to 8 connections at once; resume after Wi-Fi drops or a restart; queue and **scheduler**; **speed limit**.
- Auto-sorts downloads into Downloads\Video, Music, Images, Compressed, Documents, Programs.
- Duplicate check: asks before downloading the same file again (Download again / Skip / Open file / Show in folder).
- Browser add-on for Chrome, Edge, Brave and Firefox: catches browser downloads; popup shows media found on the page with Best quality; "Save all images" from this tab / tabs to the right / all tabs.
- Clipboard watch: copy a download link and SwiftGrab offers to download it.
- Digitally signed (Windows shows a verified publisher), updates itself (app and add-on), no ads, no tracking.

## Rules
- Show the **real app**: use the screenshots in `kit/screens/` (app-main, addon-popup, addon-settings, app-license, tut-*). Dialogs not in a screenshot are drawn in the app's dark style with `real.css` (`.qt`). Logo/icon only from `kit/logo.svg` / `kit/icon.svg`.
- Made-up websites and file names only (example.com style). No real brands' logos, no real people, no copyrighted music (use `kit/music.py`).
- **Never** advertise downloading from YouTube, Instagram, TikTok or other named platforms, and never say it bypasses limits or paywalls. Video-saving scenes carry the small line "Only download videos you have the right to save."
- Speed numbers on screen get the small line "Illustration. Real speed depends on your connection and the server."
- Every caption contains the website and download lines (see Captions).

## Topics (rotate; pick the 3 least recently used in `kit/LOG.md`, all different)
1. Resume after Wi-Fi drops (78% → continues, even after restart)
2. Speed: one big file in 8 parts at once, live MB/s
3. Scheduler: queue big downloads for tonight, wake up to everything done
4. Save every picture on a page (this tab / tabs to the right / all tabs)
5. Clipboard watch: copy a link, SwiftGrab is ready
6. Speed limit: download keeps going, video call/game stays smooth
7. Smart folders: auto-sorted into Video, Music, Images…
8. Duplicate check: opens the copy you already have
9. The video on a page, Best quality, one click (with the "right to save" line)
10. Buy once, no subscription (real prices)
11. Browser integration: click Download in the browser, SwiftGrab takes over
12. Trust: signed, verified publisher, auto-updates, no ads, no tracking
13. Easy setup in 4 steps: download → install → add-on → pairing code (use tut-* screenshots)
14. 30-day free trial, every feature
15. Pause & resume many downloads / the queue (main window with several rows)
Vary the hook each time; never reuse a hook sentence that is already in LOG.md.

## Voice-over (required on every video since Oct 31)
Every video has a calm voice explaining **what SwiftGrab does and how to use it**, and the screen always shows exactly what the voice is saying at that moment (voice says "press Resume" → cursor clicks Resume, ring on it). Subtitles of each line run at the bottom for muted viewers.
1. Write the script first: `kit/voice/<YYYY-MM-DD>-<slug>.json` (copy `kit/voice/2026-10-31-how-to-use.json`). 5–6 short lines, each with its start time `t`; one idea per line; simple words; last line at secs−4 is the call to action ("Try it free for thirty days, at get swift grab dot com."). Write the product name as "Swift Grab" in the spoken text (the subtitle can say SwiftGrab). Never say a site or platform name.
2. Setup once: `pip install --break-system-packages --no-index --no-deps -q kit/tts/*.whl` (offline, voice model is in kit/tts).
3. Music for the full length: `BARS=14 python3 kit/music.py <n> /tmp/m.wav` (28 s; BARS=12 → 24 s, end-card hit at secs−4).
4. `python3 kit/voice.py kit/voice/<file>.json /tmp/<slug>-audio.wav /tmp/m.wav` → prints each line's start–end time. If it says TOO LONG, shorten that line or move the next one. Voice: `af_heart` (default); keep the same voice on all videos so the brand sounds the same.
5. Build the HTML scenes on those times (copy `kit/videos/2026-10-31-how-to-use.html`: it has the `CAPS` subtitle list and the scene/cursor/ring timing pattern). Each click or ring happens while the voice says that word.
6. Render with the length: `node kit/render.js <html> /tmp/<slug>_v.mp4 28`, then mix: `ffmpeg -y -i /tmp/<slug>_v.mp4 -i /tmp/<slug>-audio.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart media/<date>/swiftgrab-<slug>-raw.mp4` (the audio is already loudness-normalised), then the cover step.

## How to build a video
1. Copy a recent file in `kit/videos/` (the 2026-10-29-*.html ones show the real-screenshot style; `example-*.html` show pure motion graphics) to `kit/videos/<YYYY-MM-DD>-<slug>.html` (date = posting day). Keep `<base href="../">`.
2. Structure (120 BPM, beat = 0.5 s; the music drops at 4.0 s and hits again at 12.0 s):
   - 0–4 s **hook**: the problem, big words flying in (`words()`), a simple prop.
   - 4–8 s **SwiftGrab solves it**: real screenshot with `cam()` zoom, `ring()` highlight, cursor clicks (`cursorMove()`, `at()` for exact targets).
   - 8–12 s **result / proof**: what the user gets, chips or a checklist, confetti `burst()`.
   - 12–16 s **end card**: `endcard2('<short tagline with <b>highlight</b>>')` (logo, "Try it free for 30 days", getswiftgrab.com).
   Helpers: `kit/lib.js`, `kit/fx.js`, `kit/realfx.js` (screenshot coordinates are documented at its top). Text must stay inside 60 px side margins and never overlap.
3. Check: `node kit/stills.js kit/videos/<file>.html /tmp/x 2.5 5 7 10 13.5`, put the stills side by side in one image and **look at it**. Fix cut-off or overlapping text, empty frames, rings in the wrong place.
4. Render: `node kit/render.js kit/videos/<file>.html /tmp/<slug>_v.mp4` (≈1–2 min; run the three in parallel).
5. Music: see Voice-over above (a different n 1–6 for each of the day's 3 videos).
6. Mix: see Voice-over step 6 (voice + ducked music from kit/voice.py)
   then `ffprobe` it: 1080×1920, h264 + aac, 16 s.
7. **Cover (required — otherwise the posts look empty in the grid):** `python3 kit/cover.py media/<date>/swiftgrab-<slug>-raw.mp4 <time when the hook headline is fully visible, usually 3.5> media/covers/swiftgrab-<slug>-cover.jpg media/<date>/swiftgrab-<slug>.mp4`
   (so mix to `...-raw.mp4` in step 6, then make the final file with the cover; delete the -raw file before committing). Look at the cover image before scheduling.

## Real screen recordings (preferred when available)
Recordings from the owner live in `recordings/` (never show personal folders, file names, bookmarks, antivirus popups, other apps). Cut and crop with ffmpeg into 1000×562 clips, render the graphics page with an empty frame (see `kit/videos/2026-10-29-install-3-steps.html`, element #ph at left 40, top 620), then lay the clips over it with ffmpeg `overlay=40:620:enable='between(t,a,b)'`. Longer music: `BARS=12 python3 kit/music.py <n> out.wav` gives 24 s (end-card hit at 20 s); render with `node kit/render.js <html> out.mp4 24`.

## Upload
`git add`, commit (message "Videos for <date>"), `git push`. Public link for Metricool:
`https://raw.githubusercontent.com/SwiftGrab/swiftgrab-social/main/media/<YYYY-MM-DD>/swiftgrab-<slug>.mp4` — check it answers HTTP 200 with `curl -sI`.
Delete `media/` folders older than 3 days in the same commit (Metricool keeps its own copy once scheduled).

## Captions
```
<hook sentence with emoji> <1–2 sentences on the benefit>

🌐 Website: getswiftgrab.com
⬇️ Download free (30-day trial): getswiftgrab.com
Windows 10 & 11

<20–25 hashtags, all about the software (see Hashtags below)>
```
### Hashtags (owner's rule, Oct 31: every video, only hashtags related to the software)
Always start with this fixed set, in this order:
`#SwiftGrab #SwiftGrabApp #DownloadManager #DownloadAccelerator #Windows11 #Windows10 #PCSoftware #WindowsApps`
Then 12–17 more that fit the video's topic and are about downloading, Windows or the feature shown, for example:
#FasterDownloads #ResumeDownloads #DownloadScheduler #SpeedLimit #FileOrganization #SaveImages #BrowserExtension #ChromeExtension #FirefoxAddon #ClipboardManager #PCTips #TechTips #WindowsTips #ComputerTips #Productivity #HowTo #Tutorial #SoftwareTools #NoSubscription #FreeTrial
Never use hashtags unrelated to SwiftGrab (no trending or viral tags, no names of other apps, sites or platforms).
Titles under 60 characters: TikTok title, Facebook Reel title, YouTube title ending in "#shorts". YouTube tags: up to 15.

## Schedule (Metricool)
- `getScheduledPosts` for tomorrow; `getBestTimeToPostByNetwork` (instagram and tiktok) for tomorrow.
- Tomorrow must end up with **3 posts in total**: if some already exist, only add the missing number. Times at least 2 h apart, between 9:00 and 21:00, preferring the best hours (default 10:00, 13:00, 18:00 when no data). Never touch existing posts.
- `createScheduledPost` per video: providers instagram, facebook, tiktok, youtube; `instagramData {type:"REEL", showReelOnFeed:true}`, `facebookData {type:"REEL", title}`, `tiktokData {title, privacyOption:"PUBLIC_TO_EVERYONE", commercialContentOwnBrand:true}`, `youtubeData {title, type:"short", privacy:"public", madeForKids:false, category:"SCIENCE_TECHNOLOGY", tags}`. Media = the raw.githubusercontent.com link of the final video, and `videoThumbnailUrl` = the raw.githubusercontent.com link of its cover jpg.

## Log and report
Append one line per video to `kit/LOG.md`: `<post date> <time> | topic <n> | <hook> | <file>` and push.
Then send the owner ONE short message (SendUserMessage) with the 3 videos (SendUserFile, status "proactive") and the times they will post. If anything failed, say exactly what and what to do.
