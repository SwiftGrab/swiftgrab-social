const clamp=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
const ease=x=>1-Math.pow(1-clamp(x),3);
const seg=(t,a,b)=>clamp((t-a)/(b-a));
const lerp=(a,b,x)=>a+(b-a)*x;
const $=s=>document.querySelector(s);
function show(el,t,a,b,f=.35){const i=ease(seg(t,a,a+f)),o=b==null?1:1-ease(seg(t,b-f,b));const v=Math.min(i,o);
 el.style.opacity=v;el.style.transform=`translateY(${(1-i)*40}px) scale(${.96+.04*i})`;return v;}
function common(t){document.body.style.setProperty('--gx',(Math.sin(t*.6)*80)+'px');}
function endcard(){const d=document.createElement('div');d.className='layer end';d.id='end';d.style.top='560px';
 d.innerHTML=`<img class="logo" src="logo.svg"><div class="tag">Downloads that finish <b>faster</b> ⚡</div>
 <div class="pill">Try it free for 30 days</div><div class="url">getswiftgrab.com</div><div class="small">For Windows 10 &amp; 11</div>`;
 document.body.appendChild(d);}
const CURSOR='<svg viewBox="0 0 24 24"><path d="M4 2l15 9-7 1.5L9 20z" fill="#fff" stroke="#0A1024" stroke-width="1.4" stroke-linejoin="round"/></svg>';
