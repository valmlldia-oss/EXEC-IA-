/* ── Nav scroll ── */
const nav = document.getElementById('nav');
const onScroll = () => nav.classList.toggle('scrolled', scrollY > 56);
window.addEventListener('scroll', onScroll, { passive: true });
onScroll();

/* ── Mobile menu ── */
const burger = document.querySelector('.nav-burger');
const links  = document.querySelector('.nav-links');
burger?.addEventListener('click', () => links.classList.toggle('open'));
links?.querySelectorAll('a').forEach(a => a.addEventListener('click', () => links.classList.remove('open')));

/* ── Scroll reveal ── */
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); observer.unobserve(e.target); }});
}, { threshold: 0.12 });
document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

/* ── Language bar animation ── */
const barObserver = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.querySelectorAll('.lang-bar[data-w]').forEach(b => b.style.width = b.dataset.w);
      barObserver.unobserve(e.target);
    }
  });
}, { threshold: 0.3 });
document.querySelectorAll('.lt-wrap').forEach(el => barObserver.observe(el));

/* ── Calendly popup ── */
const CALENDLY_URL = 'https://calendly.com/VOTRE-NOM/decouverte-30min'; // ← Remplacer par votre URL Calendly
document.querySelectorAll('[data-calendly]').forEach(btn => {
  btn.addEventListener('click', e => {
    e.preventDefault();
    if (window.Calendly) Calendly.initPopupWidget({ url: CALENDLY_URL });
    else window.open(CALENDLY_URL, '_blank');
  });
});
