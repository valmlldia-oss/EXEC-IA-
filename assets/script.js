/* ── Bloquer le scroll-restore du navigateur (évite les sauts au chargement) ── */
if ('scrollRestoration' in history) history.scrollRestoration = 'manual';

/* ── Nav scroll ── */
const nav = document.getElementById('nav');
const onScroll = () => nav.classList.toggle('scrolled', scrollY > 56);
window.addEventListener('scroll', onScroll, { passive: true });
onScroll();

/* ── Helper : scroll vers un élément sans saut ── */
function smoothScrollTo(id) {
  const target = document.getElementById(id);
  if (!target) return;
  document.querySelector('.nav-links')?.classList.remove('open');
  /* Double-RAF : 1er frame = fermeture menu / 2e frame = layout stabilisé */
  requestAnimationFrame(() => requestAnimationFrame(() => {
    const navH = document.getElementById('nav')?.offsetHeight || 80;
    const top = target.getBoundingClientRect().top + window.scrollY - navH;
    window.scrollTo({ top, behavior: 'smooth' });
  }));
}

/* ── Smooth anchor scrolling (JS only — no CSS scroll-behavior) ── */
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', function(e) {
    const id = this.getAttribute('href').slice(1);
    if (!id) return;
    if (!document.getElementById(id)) return;
    e.preventDefault();
    smoothScrollTo(id);
  });
});

/* ── Gérer le hash initial dans l'URL (évite le saut natif au chargement) ── */
window.addEventListener('DOMContentLoaded', () => {
  if (location.hash) {
    const id = location.hash.slice(1);
    /* Remonter immédiatement en haut, puis scroller en douceur */
    window.scrollTo(0, 0);
    setTimeout(() => smoothScrollTo(id), 120);
  }
});

/* ── Mobile menu ── */
const burger = document.querySelector('.nav-burger');
const links  = document.querySelector('.nav-links');
burger?.addEventListener('click', () => links.classList.toggle('open'));
links?.querySelectorAll('a').forEach(a => a.addEventListener('click', () => links.classList.remove('open')));

/* ── Scroll reveal ── */
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); observer.unobserve(e.target); }});
}, { threshold: 0.01, rootMargin: '0px 0px -40px 0px' });
document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
/* Fallback : tout rendre visible après 2.5s si l'observateur ne s'est pas déclenché */
setTimeout(() => {
  document.querySelectorAll('.reveal:not(.visible)').forEach(el => el.classList.add('visible'));
}, 2500);

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

/* ── ROI Simulator ── */
(function () {
  const collab = document.getElementById('rs-collab');
  const heures = document.getElementById('rs-h');
  const taux   = document.getElementById('rs-t');
  if (!collab) return;
  const lang = document.documentElement.lang || 'fr';
  function fmtMoney(n) {
    const r = Math.round(n);
    if (lang === 'en') return '€ ' + r.toLocaleString('en-GB');
    if (lang === 'es') return r.toLocaleString('es-ES') + ' €';
    return r.toLocaleString('fr-FR') + ' €';
  }
  function update() {
    const c = +collab.value, h = +heures.value, t = +taux.value;
    const hM = c * h * 4.33;
    document.getElementById('rsv-collab').textContent = c;
    document.getElementById('rsv-h').textContent      = h + ' h';
    document.getElementById('rsv-t').textContent      = t + ' €/h';
    document.getElementById('roi-out-h').textContent  = Math.round(hM) + ' h';
    document.getElementById('roi-out-m').textContent  = fmtMoney(hM * t);
    document.getElementById('roi-out-an').textContent = fmtMoney(hM * t * 12);
  }
  [collab, heures, taux].forEach(s => s.addEventListener('input', update));
  update();
})();

/* ── Agents carousel ── */
(function () {
  const outer = document.getElementById('agentsTrack');
  if (!outer) return;
  const track = outer.querySelector('.agents-track');
  const cards = outer.querySelectorAll('.agent-card');
  const dots  = document.querySelectorAll('[data-idx]');
  const btnPrev = document.getElementById('agentsPrev');
  const btnNext = document.getElementById('agentsNext');
  let current = 0;

  function cardWidth() {
    const c = cards[0];
    if (!c) return 445;
    return c.offsetWidth + parseInt(getComputedStyle(track).gap || '20');
  }

  function goTo(idx) {
    current = Math.max(0, Math.min(idx, cards.length - 1));
    outer.scrollTo({ left: current * cardWidth(), behavior: 'smooth' });
    dots.forEach((d, i) => d.classList.toggle('active', i === current));
    if (btnPrev) btnPrev.disabled = current === 0;
    if (btnNext) btnNext.disabled = current === cards.length - 1;
  }

  btnPrev?.addEventListener('click', () => goTo(current - 1));
  btnNext?.addEventListener('click', () => goTo(current + 1));
  dots.forEach(d => d.addEventListener('click', () => goTo(+d.dataset.idx)));

  outer.addEventListener('scroll', () => {
    const idx = Math.round(outer.scrollLeft / cardWidth());
    if (idx !== current) { current = idx; dots.forEach((d, i) => d.classList.toggle('active', i === current)); }
  }, { passive: true });

  /* Drag / mouse */
  let drag = false, startX = 0, startScroll = 0;
  outer.addEventListener('mousedown', e => { drag = true; startX = e.pageX; startScroll = outer.scrollLeft; outer.style.scrollBehavior = 'auto'; });
  outer.addEventListener('mouseleave', () => { drag = false; outer.style.scrollBehavior = ''; });
  outer.addEventListener('mouseup',    () => { drag = false; outer.style.scrollBehavior = ''; });
  outer.addEventListener('mousemove',  e => { if (!drag) return; e.preventDefault(); outer.scrollLeft = startScroll - (e.pageX - startX); });

  goTo(0);
})();

/* ── CTA images carousel ── */
(function () {
  const outer = document.getElementById('ctaTrack');
  if (!outer) return;
  const track = outer.querySelector('.agents-cta-track');
  const cards = outer.querySelectorAll('.agents-cta-img-slot');
  const dots  = document.querySelectorAll('[data-cta-idx]');
  const btnPrev = document.getElementById('ctaPrev');
  const btnNext = document.getElementById('ctaNext');
  let current = 0;

  function cardWidth() {
    const c = cards[0];
    if (!c) return 445;
    return c.offsetWidth + parseInt(getComputedStyle(track).gap || '20');
  }

  function goTo(idx) {
    current = Math.max(0, Math.min(idx, cards.length - 1));
    outer.scrollTo({ left: current * cardWidth(), behavior: 'smooth' });
    dots.forEach((d, i) => d.classList.toggle('active', i === current));
    if (btnPrev) btnPrev.disabled = current === 0;
    if (btnNext) btnNext.disabled = current === cards.length - 1;
  }

  btnPrev?.addEventListener('click', () => goTo(current - 1));
  btnNext?.addEventListener('click', () => goTo(current + 1));
  dots.forEach(d => d.addEventListener('click', () => goTo(+d.dataset.ctaIdx)));

  outer.addEventListener('scroll', () => {
    const idx = Math.round(outer.scrollLeft / cardWidth());
    if (idx !== current) { current = idx; dots.forEach((d, i) => d.classList.toggle('active', i === current)); }
  }, { passive: true });

  let drag = false, startX = 0, startScroll = 0;
  outer.addEventListener('mousedown', e => { drag = true; startX = e.pageX; startScroll = outer.scrollLeft; outer.style.scrollBehavior = 'auto'; });
  outer.addEventListener('mouseleave', () => { drag = false; outer.style.scrollBehavior = ''; });
  outer.addEventListener('mouseup',    () => { drag = false; outer.style.scrollBehavior = ''; });
  outer.addEventListener('mousemove',  e => { if (!drag) return; e.preventDefault(); outer.scrollLeft = startScroll - (e.pageX - startX); });

  goTo(0);
})();

/* ── Calendly popup ── */
const CALENDLY_URL = 'https://calendly.com/VOTRE-NOM/decouverte-30min'; // ← Remplacer par votre URL Calendly
document.querySelectorAll('[data-calendly]').forEach(btn => {
  btn.addEventListener('click', e => {
    e.preventDefault();
    if (window.Calendly) Calendly.initPopupWidget({ url: CALENDLY_URL });
    else window.open(CALENDLY_URL, '_blank');
  });
});

/* ── Audio Player ── */
(function () {
  const audio    = document.getElementById('exec-audio');
  const playBtn  = document.getElementById('audioPlay');
  const icon     = document.getElementById('audioIcon');
  const fill     = document.getElementById('audioFill');
  const current  = document.getElementById('audioCurrent');
  const duration = document.getElementById('audioDuration');
  const bar      = document.querySelector('.audio-progress-bar');
  if (!audio || !playBtn) return;

  function fmt(s) {
    const m = Math.floor(s / 60), sec = Math.floor(s % 60);
    return m + ':' + String(sec).padStart(2, '0');
  }

  audio.addEventListener('loadedmetadata', () => {
    duration.textContent = fmt(audio.duration);
  });

  audio.addEventListener('timeupdate', () => {
    if (!audio.duration) return;
    fill.style.width = (audio.currentTime / audio.duration * 100) + '%';
    current.textContent = fmt(audio.currentTime);
  });

  audio.addEventListener('ended', () => {
    icon.innerHTML = '&#x25B6;';
    playBtn.classList.remove('playing');
    fill.style.width = '0%';
    current.textContent = '0:00';
  });

  playBtn.addEventListener('click', () => {
    if (audio.paused) {
      audio.play();
      icon.innerHTML = '&#x23F8;';
      playBtn.classList.add('playing');
    } else {
      audio.pause();
      icon.innerHTML = '&#x25B6;';
      playBtn.classList.remove('playing');
    }
  });

  bar.addEventListener('click', e => {
    const rect = bar.getBoundingClientRect();
    audio.currentTime = ((e.clientX - rect.left) / rect.width) * audio.duration;
  });

/* ── Suppression damier équipe de choc ── */
function removeCheckerboard(img) {
  const canvas = document.createElement('canvas');
  canvas.width  = img.naturalWidth;
  canvas.height = img.naturalHeight;
  canvas.className = img.className;
  canvas.style.cssText = img.style.cssText;
  canvas.style.width  = img.offsetWidth  + 'px';
  canvas.style.height = img.offsetHeight + 'px';
  canvas.style.display = 'block';
  const ctx = canvas.getContext('2d');
  ctx.drawImage(img, 0, 0);
  const data = ctx.getImageData(0, 0, canvas.width, canvas.height);
  const d = data.data;
  for (let i = 0; i < d.length; i += 4) {
    const r = d[i], g = d[i+1], b = d[i+2];
    const max = Math.max(r, g, b), min = Math.min(r, g, b);
    const saturation = max - min;
    if (saturation < 22 && r > 140) {
      const proximity = (r - 140) / 115;
      d[i+3] = Math.max(0, Math.round(d[i+3] * (1 - proximity)));
    }
  }
  ctx.putImageData(data, 0, 0);
  img.parentNode.replaceChild(canvas, img);
}

window.addEventListener('load', () => {
  const teamImg = document.querySelector('.agents-team-photo img');
  if (!teamImg) return;
  if (teamImg.complete) { removeCheckerboard(teamImg); }
  else { teamImg.addEventListener('load', () => removeCheckerboard(teamImg)); }
});
})();
