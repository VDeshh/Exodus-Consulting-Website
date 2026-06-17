// ---- Nav scrolled state + background blur & slow-mo past hero ----
const nav = document.getElementById('nav');
const bgVideo = document.getElementById('bgVideo');
const bgVideoEl = bgVideo ? bgVideo.querySelector('video') : null;
const FAST_RATE = 1;     // normal speed while on the hero
const SLOW_RATE = 0.6;   // gentle slow-motion once past the hero (smoother than a deep slow-mo, which stutters on a fixed-fps video)
let rateTarget = FAST_RATE, rateRaf = null;
const easeRate = () => {
  if (!bgVideoEl) { rateRaf = null; return; }
  const cur = bgVideoEl.playbackRate;
  const next = cur + (rateTarget - cur) * 0.08;
  if (Math.abs(rateTarget - next) < 0.01) { bgVideoEl.playbackRate = rateTarget; rateRaf = null; return; }
  bgVideoEl.playbackRate = next;
  rateRaf = requestAnimationFrame(easeRate);
};
const onScroll = () => {
  const y = window.scrollY;
  if (nav) nav.classList.toggle('scrolled', y > 20);
  // blur + slow the background train once the hero (one viewport) is scrolled past
  const pastHero = y > window.innerHeight * 0.7;
  if (bgVideo) bgVideo.classList.toggle('dim', pastHero);
  const wantRate = pastHero ? SLOW_RATE : FAST_RATE;
  if (bgVideoEl && wantRate !== rateTarget) {
    rateTarget = wantRate;
    if (!rateRaf) rateRaf = requestAnimationFrame(easeRate);
  }
};
onScroll();
window.addEventListener('scroll', onScroll, { passive: true });

// ---- Mobile nav toggle ----
const navToggle = document.getElementById('navToggle');
const navLinks = document.getElementById('navLinks');
if (navToggle && navLinks) {
  navToggle.addEventListener('click', () => navLinks.classList.toggle('open'));
  navLinks.querySelectorAll('a').forEach(a => a.addEventListener('click', () => navLinks.classList.remove('open')));
}

// ---- Scroll reveal ----
const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const reveals = document.querySelectorAll('.reveal');
if (reduce) {
  reveals.forEach(el => el.classList.add('in'));
} else {
  const io = new IntersectionObserver((entries, obs) => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); obs.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -10% 0px' });
  reveals.forEach(el => io.observe(el));
}

// ---- Active nav link ----
const anchors = document.querySelectorAll('.nav-links a[href^="#"]');
const secs = [...anchors].map(l => document.querySelector(l.getAttribute('href'))).filter(Boolean);
if (secs.length) {
  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        anchors.forEach(l => l.classList.remove('active'));
        const a = document.querySelector(`.nav-links a[href="#${e.target.id}"]`);
        if (a) a.classList.add('active');
      }
    });
  }, { rootMargin: '-45% 0px -50% 0px' });
  secs.forEach(s => obs.observe(s));
}

// ---- Calendly popup ----
const CAL = 'https://calendly.com/josh-fennecapp/30-min?hide_gdpr_banner=1&background_color=241b38&text_color=ffffff&primary_color=7b4dff';
document.querySelectorAll('[data-calendly]').forEach(el => {
  el.addEventListener('click', e => {
    if (window.Calendly) { e.preventDefault(); Calendly.initPopupWidget({ url: CAL }); }
    else if (!el.getAttribute('href')) { window.open('https://calendly.com/josh-fennecapp/30-min', '_blank'); }
  });
});
