// Helpers for real-screenshot scenes (needs lib.js + fx.js first).
// The app-main.webp screenshot is 1600x750. Useful points (in screenshot pixels):
//   Add URL button (84,130) · Video folder in sidebar (105,261) · Scheduler (1187,130) · Settings (1323,130)
//   Rows (y centre): ubuntu 237, Holiday trip 279, project-assets 323, podcast 365, game-update 409, photos-backup 451, setup-tools 495, annual-report 537
// addon-popup.webp is 560x653: Best quality row (y 383), first Download button (450,395), Save all images "This tab" (86,282).

// Show a screenshot box: fades/pops in at a, out at b, slow zoom from z0 to z1 around (ox,oy) in screenshot pixels.
function shot(el, t, a, b, z0 = 1, z1 = 1.08, ox = 800, oy = 375, natW = 1600) {
  const v = Math.min(ease(seg(t, a, a + .4)), b == null ? 1 : 1 - ease(seg(t, b - .3, b)));
  const w = el.offsetWidth, k = w / natW;
  el.style.opacity = v;
  el.style.transformOrigin = `${ox * k}px ${oy * k}px`;
  el.style.transform = `scale(${lerp(z0, z1, ease(seg(t, a, b == null ? a + 4 : b)))}) translateY(${(1 - ease(seg(t, a, a + .4))) * 60}px)`;
  return v;
}
// Highlight ring over a screenshot area (screenshot pixels), inside the .shot element.
function ring(el, t, a, b, x, y, w, h, natW = 1600) {
  const box = el.parentElement, k = box.offsetWidth / natW;
  Object.assign(el.style, { left: x * k + 'px', top: y * k + 'px', width: w * k + 'px', height: h * k + 'px' });
  const v = Math.min(seg(t, a, a + .2), b == null ? 1 : 1 - seg(t, b - .2, b));
  el.style.opacity = v * (0.75 + 0.25 * Math.sin(t * 10));
}
// Move the cursor (page pixels) from p0 to p1 between a and b; click at b (+ .15s squeeze).
function cursorMove(c, t, a, b, p0, p1, hideAt) {
  const k = ease(seg(t, a, b));
  c.style.left = lerp(p0[0], p1[0], k) + 'px'; c.style.top = lerp(p0[1], p1[1], k) + 'px';
  c.style.opacity = t >= a && (hideAt == null || t < hideAt) ? 1 : 0;
  c.style.transform = t > b && t < b + .18 ? 'scale(.82)' : '';
}
// Screenshot pixel -> page pixel, for a .shot at (left, top) with display width w.
function sp(left, top, w, x, y, natW = 1600) { const k = w / natW; return [left + x * k, top + y * k]; }
// Page position of a screenshot pixel, correct even while the shot is zoomed.
function at(shotEl, x, y, natW = 1600) {
  let m = shotEl.querySelector('.mk'); if (!m) { m = document.createElement('i'); m.className = 'mk'; m.style.cssText = 'position:absolute;width:1px;height:1px'; shotEl.appendChild(m); }
  const k = shotEl.offsetWidth / natW; m.style.left = x * k + 'px'; m.style.top = y * k + 'px';
  const r = m.getBoundingClientRect(); return [r.left, r.top];
}
// Camera move on a .shot: keep screenshot pixel (px,py) at page point (qx,qy) with zoom z.
// Pass two camera states and a 0..1 mix to glide between them.
function cam(el, s0, s1, mix, natW = 1600) {
  const k = el.offsetWidth / natW, L = el.offsetLeft, T = el.offsetTop;
  const st = s => ({ z: s[0], tx: s[3] - L - s[1] * k * s[0], ty: s[4] - T - s[2] * k * s[0] });
  const a = st(s0), b = st(s1), m = ease(mix);
  el.style.transformOrigin = '0 0';
  el.style.transform = `translate(${lerp(a.tx, b.tx, m)}px,${lerp(a.ty, b.ty, m)}px) scale(${lerp(a.z, b.z, m)})`;
}
