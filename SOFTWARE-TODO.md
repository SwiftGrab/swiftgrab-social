# Software wishes to add to the PC's NEXT_UPDATE.md (PC wasn't linked when noted)

## Refresh button in the add-on pop-up (asked 2026-11-12, NOT now - next update)
On Instagram / TikTok etc. the pop-up sometimes offers the wrong video or picture (an older
slide or the previous post after scrolling). Add a small "Refresh" button to the pop-up that
re-scans the page right now (current slide / the video that is playing / the post in view)
and rebuilds the list, without reloading the page. Keep the "Download this video/picture"
row on top after refreshing.
Files: extension/src/popup.* (button), content.js (rescan message -> slideFile/pageMedia again).

## Update pop-up when the window is opened later (noted 2026-11-25, next update)
If SwiftGrab is hidden in the tray when the daily update check finds a new version, only the tray
balloon shows; opening the window later shows just the blue link. Show the UpdateDialog the next
time the window is opened (once per version, unless "Skip this version"). ui/main_window.py check_updates/show_normal.
Seen with 1.9.14: 5 PCs got update.json, only 2 installer downloads after a day.
