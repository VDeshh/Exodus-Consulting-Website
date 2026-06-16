// ---- Nav scrolled state + background blur past hero ----
const nav = document.getElementById('nav');
const bgVideo = document.getElementById('bgVideo');
const onScroll = () => {
  const y = window.scrollY;
  if (nav) nav.classList.toggle('scrolled', y > 20);
  // blur the background train once the hero (one viewport) is scrolled past
  if (bgVideo) bgVideo.classList.toggle('dim', y > window.innerHeight * 0.7);
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
