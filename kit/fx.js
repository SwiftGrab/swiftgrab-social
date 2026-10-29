// Extra motion for the beat-synced ads (120 BPM, beat = 0.5 s). Everything is a pure function of t.
const BEAT = 0.5;
const pulse = t => t < 4 ? 0 : Math.exp(-((t % BEAT) / BEAT) * 6);           // kick pulse after the drop
const easeBack = x => { x = clamp(x); const c = 1.9; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };

// pop-in with overshoot, optional exit
function pop(el, t, a, b, f = .4) {
  const i = seg(t, a, a + f), o = b == null ? 0 : seg(t, b - .25, b);
  const s = easeBack(i) * (1 - o * .2);
  el.style.opacity = Math.min(clamp(i * 3), 1 - o);
  el.style.transform = `scale(${s})`;
  return i;
}
// words fly in one by one (data-w on spans)
function words(el, t, a, step = .12, b = null) {
  el.style.opacity = b != null && t > b ? 1 - seg(t, b - .001, b + .25) : 1;
  el.querySelectorAll('span.w').forEach((w, k) => {
    const x = seg(t, a + k * step, a + k * step + .35);
    w.style.display = 'inline-block';
    w.style.opacity = clamp(x * 2);
    w.style.transform = `translateY(${(1 - easeBack(x)) * 80}px) rotate(${(1 - ease(x)) * (k % 2 ? 8 : -8)}deg)`;
    if (b != null && t > b) w.style.transform += ` translateY(${-ease(seg(t, b, b + .3)) * 60}px)`;
  });
}
function splitWords(el) {
  el.innerHTML = el.innerHTML.split(/(<[^>]+>|\s+)/).map(p => p.startsWith('<') || /^\s*$/.test(p) ? p : `<span class="w">${p}</span>`).join('');
}
// full-screen flash on transitions
function flash(t, times) {
  let v = 0; for (const x of times) v = Math.max(v, Math.exp(-Math.max(0, t - x) * 9) * (t >= x ? 1 : 0));
  $('#flash').style.opacity = v * .85;
}
// diagonal wipe: a bright band sweeping across at time a
function wipe(t, a) {
  const x = seg(t, a - .3, a + .3);
  const w = $('#wipe'); w.style.opacity = x > 0 && x < 1 ? 1 : 0;
  w.style.transform = `translateX(${lerp(-1800, 1800, ease(x))}px) skewX(-18deg)`;
}
// seeded particles
function rnd(seed) { let s = seed; return () => (s = (s * 16807) % 2147483647) / 2147483647; }
function makeParticles(n, seed) {
  const box = $('#parts'), r = rnd(seed), list = [];
  for (let i = 0; i < n; i++) {
    const d = document.createElement('i'); box.appendChild(d);
    list.push({ d, a: r() * Math.PI * 2, v: 500 + r() * 900, s: 10 + r() * 22, c: ['#FFC21A', '#3EE0FF', '#2F7BFF', '#3DDC97', '#ffffff'][i % 5] });
  }
  return list;
}
function burst(list, t, t0, cx, cy) {
  const k = t - t0;
  list.forEach(p => {
    if (k < 0 || k > 1.4) { p.d.style.opacity = 0; return; }
    const dist = p.v * (1 - Math.exp(-k * 3)) / 3 * 3;
    const x = cx + Math.cos(p.a) * dist, y = cy + Math.sin(p.a) * dist + 300 * k * k;
    Object.assign(p.d.style, { left: x + 'px', top: y + 'px', width: p.s + 'px', height: p.s + 'px', background: p.c, opacity: 1 - k / 1.4, transform: `rotate(${k * 400}deg)` });
  });
}
// floating light streaks in the background (always moving)
function streaks(t) {
  document.querySelectorAll('.streak').forEach((s, i) => {
    const sp = 260 + i * 70, y = (i * 233) % 1920;
    s.style.transform = `translate(${((t * sp + i * 400) % 1800) - 400}px, ${y}px) rotate(-20deg)`;
  });
}
function beatBg(t) {
  const p = pulse(t);
  $('.bg').style.transform = `scale(${1 + p * .05})`;
  $('.grid').style.opacity = .6 + p * .4;
}
function endcard2(tag) {
  const d = document.createElement('div'); d.className = 'layer end'; d.id = 'end'; d.style.top = '520px';
  d.innerHTML = `<img class="logo" src="logo.svg"><div class="tag">${tag}</div>
  <div class="pill">Try it free for 30 days</div><div class="url">getswiftgrab.com</div><div class="small">For Windows 10 &amp; 11</div>`;
  document.body.appendChild(d);
}
function chrome() {
  document.body.insertAdjacentHTML('beforeend', `<div id="parts"></div><div id="wipe"></div><div id="flash"></div>`);
  const sb = document.createElement('div'); sb.id = 'streaks';
  for (let i = 0; i < 7; i++) sb.insertAdjacentHTML('beforeend', '<div class="streak"></div>');
  document.body.insertBefore(sb, document.body.children[2]);
}
