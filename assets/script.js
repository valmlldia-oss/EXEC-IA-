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

/* ── Tool info modals ── */
const TOOLS = {
  fr: {
    claude: {
      name:'Claude', cat:'Intelligence artificielle · Anthropic',
      subtitle:'Mon copilote stratégique',
      desc:'Claude m\'aide à analyser des documents complexes, préparer des synthèses exécutives et produire des contenus à forte valeur décisionnelle.',
      when:'Lorsque la qualité des décisions et la vitesse d\'analyse sont critiques.',
      cases:['<tc>Notes COMEX</tc>','<tc>Synthèses stratégiques</tc>','Analyse documentaire','Développement web avec Claude Code'],
      value:'Réduit le temps de préparation des réunions de direction et améliore la qualité des décisions.',
      watch:'Claude ne remplace pas le jugement stratégique. Il structure, il synthétise — mais la décision finale reste humaine.',
      execia:'C\'est mon outil de référence pour réfléchir, structurer et produire.',
      maturity:'Intermédiaire · Avancé',
      avis:'Claude est l\'outil que je recommande en priorité aux dirigeants qui souhaitent accélérer leur réflexion stratégique.'
    },
    chatgpt: {
      name:'ChatGPT', cat:'Intelligence artificielle · OpenAI',
      subtitle:'Mon partenaire de réflexion',
      desc:'ChatGPT accélère l\'exploration d\'idées et le challenge des hypothèses.',
      when:'Lorsque <tc>plusieurs scénarios</tc> doivent être explorés rapidement.',
      cases:['Brainstorming stratégique','Analyse de scénarios','Résolution de problèmes','Productivité quotidienne'],
      value:'<tc>Accélère la prise de décision</tc> et favorise l\'émergence de nouvelles opportunités.',
      watch:'Sa popularité peut induire un usage superficiel. L\'outil est puissant quand il est utilisé avec intention.',
      execia:'Il apporte vitesse, polyvalence et exploration.',
      maturity:'Découverte · Intermédiaire',
      avis:'Un excellent partenaire pour élargir le champ des possibles avant arbitrage.'
    },
    make: {
      name:'Make', cat:'Automatisation · No-code',
      subtitle:'Mon moteur d\'automatisation',
      desc:'Make connecte les outils et automatise les processus métier.',
      when:'Lorsque les équipes perdent du temps sur des <tc>tâches répétitives</tc>.',
      cases:['Automatisation de workflows','Synchronisation de données','Processus métier','Déploiement d\'agents IA'],
      value:'<tc>Améliore la productivité</tc> et réduit les tâches sans valeur ajoutée.',
      watch:'Automatiser un processus défaillant le rend défaillant à grande vitesse. La phase de diagnostic est indispensable.',
      execia:'Il transforme les décisions en exécution.',
      maturity:'Intermédiaire',
      avis:'L\'automatisation devient pertinente lorsqu\'elle soutient directement les objectifs business.'
    },
    airtable: {
      name:'Airtable', cat:'Base de données · No-code',
      subtitle:'Mon centre de pilotage',
      desc:'Airtable structure l\'information et facilite le suivi des initiatives.',
      when:'Lorsque la <tc>visibilité sur les priorités</tc> devient insuffisante.',
      cases:['Pilotage de projets','Bases de données métier','Suivi d\'indicateurs','Gestion des processus'],
      value:'Améliore la visibilité, la coordination et le pilotage.',
      watch:'Airtable n\'est pas un outil de Business Intelligence. Bien définir le périmètre d\'usage en amont.',
      execia:'Il apporte structure et gouvernance.',
      maturity:'Découverte · Intermédiaire',
      avis:'Une bonne décision repose sur une information fiable et accessible.'
    },
    gamma: {
      name:'Gamma', cat:'Création IA · Présentations',
      subtitle:'Mon accélérateur de communication',
      desc:'Gamma transforme rapidement les idées en supports professionnels.',
      when:'Lorsqu\'une recommandation doit être comprise et validée rapidement.',
      cases:['Présentations exécutives','Supports COMEX','Recommandations stratégiques','Restitutions clients'],
      value:'Accélère la communication et l\'adhésion.',
      watch:'Gamma structure et met en forme — il ne construit pas la réflexion à votre place.',
      execia:'Il transforme les idées en supports de décision.',
      maturity:'Découverte · Intermédiaire',
      avis:'Une stratégie n\'a de valeur que si elle est comprise et portée par l\'organisation.'
    },
    notion: {
      name:'Notion', cat:'Workspace · No-code',
      subtitle:'Mon espace de pilotage et de capitalisation',
      desc:'Notion organise les connaissances, les projets et les contenus.',
      when:'Lorsqu\'une organisation souhaite structurer son <tc>capital de connaissances</tc>.',
      cases:['Documentation','Calendriers éditoriaux','Gestion de projets','Capitalisation des connaissances'],
      value:'Réduit la dispersion de l\'information et améliore l\'<tc>alignement</tc> des équipes.',
      watch:'Notion peut rapidement devenir un espace désorganisé si l\'architecture n\'est pas pensée en amont.',
      execia:'Il constitue le socle de l\'organisation.',
      maturity:'Découverte · Intermédiaire',
      avis:'Les organisations performantes savent retrouver la bonne information au bon moment.'
    },
    perplexity: {
      name:'Perplexity', cat:'Recherche IA · Veille stratégique',
      subtitle:'Mon assistant de recherche',
      desc:'Perplexity accélère la recherche d\'informations fiables et la veille.',
      when:'Lorsqu\'il faut comprendre rapidement un marché, une tendance ou un concurrent.',
      cases:['Veille sectorielle','Recherche stratégique','Analyse concurrentielle','Vérification des sources'],
      value:'Améliore la qualité des informations utilisées pour décider.',
      watch:'Les sources doivent toujours être vérifiées pour les sujets critiques. Perplexity est un accélérateur, pas un oracle.',
      execia:'Il permet d\'accéder rapidement à des informations sourcées.',
      maturity:'Découverte',
      avis:'La qualité des décisions dépend souvent de la qualité des informations disponibles.'
    }
  }
};

const modal     = document.getElementById('tool-modal');
const modalClose = document.getElementById('tmodal-close');

function tc(str) {
  return (str || '').replace(/<tc>(.*?)<\/tc>/g, '<span class="tc">$1</span>');
}
function openToolModal(toolId) {
  const data = TOOLS.fr[toolId];
  if (!data) return;
  document.getElementById('tmi-logo').src             = `assets/logos/${toolId}.png`;
  document.getElementById('tmi-logo').alt             = data.name;
  document.getElementById('tmi-name').textContent     = data.name;
  document.getElementById('tmi-subtitle').textContent = data.subtitle || '';
  document.getElementById('tmi-maturity').textContent = data.maturity || '';
  document.getElementById('tmi-desc').textContent     = data.desc;
  document.getElementById('tmi-when').innerHTML       = tc(data.when || '');
  const casesList = document.getElementById('tmi-cases');
  casesList.innerHTML = '';
  (data.cases || []).forEach(c => {
    const li = document.createElement('li');
    li.innerHTML = tc(c);
    casesList.appendChild(li);
  });
  document.getElementById('tmi-value').innerHTML      = tc(data.value || '');
  document.getElementById('tmi-watch').textContent    = data.watch || '';
  document.getElementById('tmi-execia').textContent   = data.execia || '';
  document.getElementById('tmi-avis').textContent     = data.avis || '';
  modal.classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeToolModal() {
  modal.classList.remove('open');
  document.body.style.overflow = '';
  document.querySelectorAll('.tool-logo-item.active').forEach(i => i.classList.remove('active'));
}

document.querySelectorAll('.tool-logo-item[data-tool]').forEach(item => {
  item.addEventListener('click', () => {
    const isActive = item.classList.contains('active');
    document.querySelectorAll('.tool-logo-item.active').forEach(i => i.classList.remove('active'));
    if (isActive) { closeToolModal(); return; }
    item.classList.add('active');
    openToolModal(item.dataset.tool);
  });
});

modalClose?.addEventListener('click', closeToolModal);
modal?.addEventListener('click', e => { if (e.target === modal) closeToolModal(); });
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeToolModal(); });

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
