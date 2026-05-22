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

/* ── Tool info modals ── */
const TOOLS = {
  fr: {
    ui: { usage: 'Usage idéal', pricing: 'Tarif', execia: 'Pourquoi je l\'utilise' },
    claude:     { name:'Claude',     cat:'Grand modèle · LLM · Freemium',
      desc:'Assistant IA conversationnel d\'Anthropic. Analyse, rédige et raisonne en langage naturel avec une précision remarquable.',
      usage:'Rédaction C-Suite · Synthèses de boards · Prompt engineering · Préparation de réunions',
      pricing:'Gratuit (limité) · Pro 20 $/mois · API à l\'usage',
      execia:'Mon outil central pour la production de contenus dirigeants et l\'automatisation de workflows.' },
    chatgpt:    { name:'ChatGPT',    cat:'Grand modèle · LLM · Freemium',
      desc:'LLM d\'OpenAI, le plus utilisé au monde. Vision, voix et accès web en temps réel intégrés.',
      usage:'Créativité · Analyse d\'images · Recherche web · Conversations vocales',
      pricing:'Gratuit · Plus 20 $/mois · Team / Enterprise',
      execia:'Complémentaire à Claude pour la multimodalité et l\'accès web instantané.' },
    make:       { name:'Make',       cat:'Automatisation · No-code · Freemium',
      desc:'Plateforme d\'automatisation visuelle no-code. Connecte plus de 1 700 applications en quelques clics.',
      usage:'Scénarios automatisés · Synchronisation de données · Notifications · Workflows métiers',
      pricing:'Freemium · Core 9 $/mois · Pro 16 $/mois',
      execia:'Automatise les tâches répétitives pour libérer du temps stratégique à haute valeur.' },
    airtable:   { name:'Airtable',   cat:'Base de données · No-code · Freemium',
      desc:'Base de données visuelle et flexible, à mi-chemin entre tableur et base de données relationnelle.',
      usage:'Gestion de projets · Suivi de campagnes · Centralisation de données · Tableaux de bord',
      pricing:'Freemium · Team 20 $/mois · Business 45 $/mois',
      execia:'Structure les données complexes et pilote les projets avec une vue d\'ensemble claire.' },
    gamma:      { name:'Gamma',      cat:'Création IA · Présentations · Freemium',
      desc:'Outil de création de présentations par IA. Génère slides, documents et mini-sites en quelques minutes.',
      usage:'Présentations C-Suite · Offres commerciales · Rapports · Landing pages',
      pricing:'Gratuit (limité) · Plus 10 $/mois · Pro 20 $/mois',
      execia:'Crée des supports visuels professionnels sans designer, en quelques clics.' },
    notion:     { name:'Notion',     cat:'Workspace · No-code · Freemium',
      desc:'Workspace tout-en-un pour noter, organiser et collaborer. Notes, bases de données, wikis et projets centralisés.',
      usage:'Documentation · Gestion de projets · Wikis · CRM léger · Prises de notes',
      pricing:'Gratuit · Plus 10 $/mois · Business 18 $/mois',
      execia:'Centralise toute la documentation et les suivis dans un espace de travail unique.' },
    perplexity: { name:'Perplexity', cat:'Recherche IA · Freemium',
      desc:'Moteur de recherche IA avec citations sourcées en temps réel. Combine LLM et web indexé.',
      usage:'Veille stratégique · Recherche documentée · Fact-checking · Synthèses de marché',
      pricing:'Gratuit (limité) · Pro 20 $/mois',
      execia:'Veille stratégique rapide et fiable, avec sources vérifiables à l\'appui.' }
  },
  en: {
    ui: { usage: 'Ideal use', pricing: 'Pricing', execia: 'Why I use it' },
    claude:     { name:'Claude',     cat:'Foundation model · LLM · Freemium',
      desc:'Anthropic\'s conversational AI assistant. Analyses, writes and reasons in natural language with remarkable precision.',
      usage:'C-Suite writing · Board summaries · Prompt engineering · Strategic meeting prep',
      pricing:'Free (limited) · Pro $20/mo · API pay-per-use',
      execia:'My core tool for executive content production and workflow automation.' },
    chatgpt:    { name:'ChatGPT',    cat:'Foundation model · LLM · Freemium',
      desc:'OpenAI\'s LLM, the most widely used worldwide. Integrates vision, voice and real-time web access.',
      usage:'Creativity · Image analysis · Real-time web search · Voice conversations',
      pricing:'Free · Plus $20/mo · Team / Enterprise',
      execia:'Complements Claude for multimodality and instant web access.' },
    make:       { name:'Make',       cat:'Automation · No-code · Freemium',
      desc:'No-code visual automation platform. Connects 1,700+ apps into seamless automated workflows.',
      usage:'Automated scenarios · Data sync · Notifications · Business workflows',
      pricing:'Freemium · Core $9/mo · Pro $16/mo',
      execia:'Automates repetitive tasks to free up high-value strategic time.' },
    airtable:   { name:'Airtable',   cat:'Database · No-code · Freemium',
      desc:'Flexible visual database, halfway between spreadsheet and relational database.',
      usage:'Project management · Campaign tracking · Data centralisation · Dashboards',
      pricing:'Freemium · Team $20/mo · Business $45/mo',
      execia:'Structures complex data and drives projects with a clear overview.' },
    gamma:      { name:'Gamma',      cat:'AI creation · Presentations · Freemium',
      desc:'AI-powered presentation creator. Generates slides, documents and mini-sites in minutes.',
      usage:'C-Suite presentations · Commercial proposals · Reports · Landing pages',
      pricing:'Free (limited) · Plus $10/mo · Pro $20/mo',
      execia:'Creates professional visual materials without a designer, in a few clicks.' },
    notion:     { name:'Notion',     cat:'Workspace · No-code · Freemium',
      desc:'All-in-one workspace for notes, organisation and collaboration. Databases, wikis and projects in one place.',
      usage:'Documentation · Project management · Team wikis · Light CRM · Note-taking',
      pricing:'Free · Plus $10/mo · Business $18/mo',
      execia:'Centralises all documentation and tracking in a single workspace.' },
    perplexity: { name:'Perplexity', cat:'AI search · Freemium',
      desc:'AI search engine with real-time sourced citations. Combines LLM with indexed web.',
      usage:'Strategic monitoring · Sourced research · Fact-checking · Market summaries',
      pricing:'Free (limited) · Pro $20/mo',
      execia:'Fast, reliable strategic monitoring with verifiable sources.' }
  },
  es: {
    ui: { usage: 'Uso ideal', pricing: 'Precio', execia: 'Por qué lo uso' },
    claude:     { name:'Claude',     cat:'Gran modelo · LLM · Freemium',
      desc:'Asistente IA conversacional de Anthropic. Analiza, redacta y razona en lenguaje natural con precisión notable.',
      usage:'Redacción C-Suite · Síntesis de dirección · Prompt engineering · Preparación de reuniones',
      pricing:'Gratuito (limitado) · Pro 20 $/mes · API por uso',
      execia:'Mi herramienta central para la producción de contenidos directivos y la automatización.' },
    chatgpt:    { name:'ChatGPT',    cat:'Gran modelo · LLM · Freemium',
      desc:'LLM de OpenAI, el más utilizado del mundo. Integra visión, voz y acceso web en tiempo real.',
      usage:'Creatividad · Análisis de imágenes · Búsqueda web · Conversaciones de voz',
      pricing:'Gratuito · Plus 20 $/mes · Team / Enterprise',
      execia:'Complementa a Claude para multimodalidad y acceso web instantáneo.' },
    make:       { name:'Make',       cat:'Automatización · Sin código · Freemium',
      desc:'Plataforma de automatización visual sin código. Conecta más de 1.700 aplicaciones.',
      usage:'Escenarios automatizados · Sincronización · Notificaciones · Flujos de trabajo',
      pricing:'Freemium · Core 9 $/mes · Pro 16 $/mes',
      execia:'Automatiza tareas repetitivas para liberar tiempo estratégico de alto valor.' },
    airtable:   { name:'Airtable',   cat:'Base de datos · Sin código · Freemium',
      desc:'Base de datos visual y flexible, entre hoja de cálculo y base de datos relacional.',
      usage:'Gestión de proyectos · Seguimiento · Centralización de datos · Dashboards',
      pricing:'Freemium · Team 20 $/mes · Business 45 $/mes',
      execia:'Estructura datos complejos y gestiona proyectos con visión de conjunto.' },
    gamma:      { name:'Gamma',      cat:'Creación IA · Presentaciones · Freemium',
      desc:'Herramienta de creación de presentaciones por IA. Genera diapositivas, documentos y mini-sitios en minutos.',
      usage:'Presentaciones C-Suite · Propuestas comerciales · Informes · Landing pages',
      pricing:'Gratuito (limitado) · Plus 10 $/mes · Pro 20 $/mes',
      execia:'Crea materiales visuales profesionales sin diseñador, en pocos clics.' },
    notion:     { name:'Notion',     cat:'Workspace · Sin código · Freemium',
      desc:'Workspace todo en uno para notas, organización y colaboración. Bases de datos, wikis y proyectos centralizados.',
      usage:'Documentación · Gestión de proyectos · Wikis · CRM ligero · Notas',
      pricing:'Gratuito · Plus 10 $/mes · Business 18 $/mes',
      execia:'Centraliza toda la documentación y el seguimiento en un espacio único.' },
    perplexity: { name:'Perplexity', cat:'Búsqueda IA · Freemium',
      desc:'Motor de búsqueda IA con citas en tiempo real. Combina LLM y web indexada.',
      usage:'Vigilancia estratégica · Investigación documentada · Fact-checking · Síntesis',
      pricing:'Gratuito (limitado) · Pro 20 $/mes',
      execia:'Vigilancia estratégica rápida y fiable, con fuentes verificables.' }
  }
};

const modal     = document.getElementById('tool-modal');
const modalClose = document.getElementById('tmodal-close');

function openToolModal(toolId) {
  const lang = document.documentElement.lang || 'fr';
  const set  = TOOLS[lang] || TOOLS.fr;
  const data = set[toolId] || TOOLS.fr[toolId];
  const ui   = set.ui;
  if (!data) return;
  document.getElementById('tmi-logo').src = `assets/logos/${toolId}.png`;
  document.getElementById('tmi-logo').alt = data.name;
  document.getElementById('tmi-name').textContent = data.name;
  document.getElementById('tmi-cat').textContent  = data.cat;
  document.getElementById('tmi-desc').textContent = data.desc;
  document.getElementById('tmi-lbl-usage').textContent   = ui.usage;
  document.getElementById('tmi-usage').textContent       = data.usage;
  document.getElementById('tmi-lbl-pricing').textContent = ui.pricing;
  document.getElementById('tmi-pricing').textContent     = data.pricing;
  document.getElementById('tmi-lbl-execia').textContent  = ui.execia;
  document.getElementById('tmi-execia').textContent      = data.execia;
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

/* ── Calendly popup ── */
const CALENDLY_URL = 'https://calendly.com/VOTRE-NOM/decouverte-30min'; // ← Remplacer par votre URL Calendly
document.querySelectorAll('[data-calendly]').forEach(btn => {
  btn.addEventListener('click', e => {
    e.preventDefault();
    if (window.Calendly) Calendly.initPopupWidget({ url: CALENDLY_URL });
    else window.open(CALENDLY_URL, '_blank');
  });
});
