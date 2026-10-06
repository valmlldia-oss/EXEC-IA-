/* ── Mini-diagnostic ROBOT (article Perspectives n° 9 · FR/EN/ES) ──
   Uniquement des clics. Les choix restent dans le navigateur (localStorage).
   Rien n'est envoyé, sauf si le visiteur demande un retour personnalisé :
   e-mail + case de consentement obligatoire, envoi via /api/diagnostic.
   La langue suit <html lang>. */
(function () {
  var root = document.getElementById('mini-diagnostic');
  if (!root) return;
  var lang = (document.documentElement.lang || 'fr').slice(0, 2);

  var I18N = {
    fr: {
     sendTitle: "Recevoir un retour personnalisé", sendLead: "Laissez votre e-mail : Valérie vous répond elle-même, sous 48 heures ouvrées.", emailLabel: "Votre e-mail professionnel", consentLabel: "J'accepte qu'EXEC'IA me recontacte au sujet de ce diagnostic.", sendLabel: "Recevoir mon retour", sending: "Envoi en cours…", sentOk: "Merci ! Votre diagnostic est bien arrivé. Valérie vous répond personnellement sous 48 heures ouvrées.", errEmail: "Indiquez une adresse e-mail valide.", errConsent: "Cochez la case pour que nous puissions vous recontacter.", errSend: "L'envoi n'a pas abouti. Réessayez dans un instant, ou écrivez à contact@exec-ia.ai.", legal: "Votre e-mail et votre diagnostic servent uniquement à vous répondre. Ils ne sont ni revendus ni confiés à une IA.", legalLink: "mentions-legales.html#donnees",
      tasks: [["Déplacer et transporter du matériel", "robot", 4], ["Ranger et réapprovisionner", "robot", 3], ["Contrôler visuellement un produit ou un équipement", "mixte", 3], ["Réaliser des tâches répétitives de manutention", "robot", 4], ["Intervenir dans un environnement pénible ou à risque", "mixte", 2], ["Gérer un imprévu nécessitant jugement et arbitrage", "humain", 5]],
      futur: ["La relation client", "Le pilotage et la supervision des robots", "Le conseil et l'expertise", "L'organisation et la coordination", "La formation des équipes", "À définir"],
      vacant: ["Manutention", "Préparation de commandes", "Nettoyage", "Surveillance de nuit", "Contrôle qualité", "Accueil", "Aucun pour l'instant"],
      labels: { robot: "Robot", mixte: "Partagé", humain: "Humain" },
      perWeek: "h/sem.", hours: "h",
      groupAria: "Qui fera « {t} » demain ?", rangeAria: "Heures par semaine pour « {t} »",
      assigned: "Temps attribué aux tâches : {a} h sur {w} h",
      none: "Aucune tâche classée « Robot »",
      vEmpty: "Indiquez le temps consacré à chaque tâche pour voir votre résultat.",
      vRobot: "Une grande part de votre semaine est potentiellement **robotisable**.\nLe vrai sujet devient l'arbitrage :\nquelles tâches confier, à quel coût, et que faire du temps libéré ?",
      vMixte: "Une part notable de votre semaine passerait en mode **partagé** : le robot assiste, l'humain garde la main.\nOrganisation et formation comptent autant que la machine.",
      vHumain: "L'essentiel de votre semaine reste **humain**.\nUn robot pourrait décharger quelques tâches\nsans changer le cœur de l'activité.",
      copied: "Diagnostic copié ✓", selected: "Texte sélectionné ci-dessous", copyLabel: "Copier mon diagnostic",
      toastOk: "Collez-le où vous voulez avec Cmd + V (Mac) ou Ctrl + V (PC). Le voici :",
      toastManual: "Votre navigateur bloque la copie automatique : le texte ci-dessous est sélectionné, copiez-le avec Cmd + C (Mac) ou Ctrl + C (PC).",
      cTitle: "Mini-diagnostic ROBOT · EXEC'IA", cWeek: "Semaine de travail : {w} h",
      cRobot: "Temps potentiellement robotisable : {h} h/semaine ({p} %)", cMixte: "Temps en mode partagé : {h} h/semaine", cHumain: "Temps qui reste humain : {h} h/semaine",
      cTasks: "Mes tâches :", cFirst: "À confier en premier :", cFutur: "Le temps libéré irait vers : ", cVacant: "Poste difficile à pourvoir qu'un robot pourrait tenir : ",
      cLink: "Faire le mini-diagnostic : ", cSign: "exec-ia.ai · Décidez avant d'investir",
      url: "https://exec-ia.ai/perspective-robots-humanoides-token-tax.html#mini-diagnostic"
    },
    en: {
     sendTitle: "Get personal feedback", sendLead: "Leave your email: Valérie will reply herself within two working days.", emailLabel: "Your work email", consentLabel: "I agree that EXEC'IA may contact me about this diagnostic.", sendLabel: "Get my feedback", sending: "Sending…", sentOk: "Thank you! Your diagnostic has arrived. Valérie will reply personally within two working days.", errEmail: "Please enter a valid email address.", errConsent: "Please tick the box so we can get back to you.", errSend: "Sending failed. Please try again in a moment, or write to contact@exec-ia.ai.", legal: "Your email and diagnostic are used only to reply to you. They are never sold or handed to an AI.", legalLink: "mentions-legales-en.html#donnees",
      tasks: [["Moving and carrying equipment", "robot", 4], ["Storing and restocking", "robot", 3], ["Visually inspecting a product or equipment", "mixte", 3], ["Repetitive handling tasks", "robot", 4], ["Working in a strenuous or hazardous environment", "mixte", 2], ["Handling the unexpected with judgement and trade-offs", "humain", 5]],
      futur: ["Customer relationships", "Steering and supervising robots", "Advice and expertise", "Organisation and coordination", "Training the teams", "To be defined"],
      vacant: ["Handling", "Order picking", "Cleaning", "Night security", "Quality control", "Reception", "None for now"],
      labels: { robot: "Robot", mixte: "Shared", humain: "Human" },
      perWeek: "h/wk", hours: "h",
      groupAria: "Who will do “{t}” tomorrow?", rangeAria: "Hours per week for “{t}”",
      assigned: "Time assigned to tasks: {a} h out of {w} h",
      none: "No task classified as “Robot”",
      vEmpty: "Enter the time spent on each task to see your result.",
      vRobot: "A large share of your week could be **handed to a robot**.\nThe real question becomes the trade-off:\nwhich tasks, at what cost, and what to do with the time freed up?",
      vMixte: "A sizeable share of your week would move to **shared** mode: the robot assists, people stay in control.\nOrganisation and training matter as much as the machine.",
      vHumain: "Most of your week stays **human**.\nA robot could take a few tasks off your hands\nwithout changing the core of the work.",
      copied: "Diagnostic copied ✓", selected: "Text selected below", copyLabel: "Copy my diagnostic",
      toastOk: "Paste it wherever you like with Cmd + V (Mac) or Ctrl + V (PC). Here it is:",
      toastManual: "Your browser blocks automatic copying: the text below is selected, copy it with Cmd + C (Mac) or Ctrl + C (PC).",
      cTitle: "ROBOT mini-diagnostic · EXEC'IA", cWeek: "Working week: {w} h",
      cRobot: "Time that could go to a robot: {h} h/week ({p} %)", cMixte: "Shared time: {h} h/week", cHumain: "Time that stays human: {h} h/week",
      cTasks: "My tasks:", cFirst: "Hand over first:", cFutur: "Freed-up time would go to: ", cVacant: "Hard-to-fill role a robot could cover: ",
      cLink: "Take the mini-diagnostic: ", cSign: "exec-ia.ai · Decide before you invest",
      url: "https://exec-ia.ai/perspective-robots-humanoides-token-tax-en.html#mini-diagnostic"
    },
    es: {
     sendTitle: "Recibir una opinión personalizada", sendLead: "Deje su correo: Valérie le responderá personalmente en un plazo de dos días hábiles.", emailLabel: "Su correo profesional", consentLabel: "Acepto que EXEC'IA me contacte en relación con este diagnóstico.", sendLabel: "Recibir mi opinión", sending: "Enviando…", sentOk: "¡Gracias! Su diagnóstico ha llegado. Valérie le responderá personalmente en un plazo de dos días hábiles.", errEmail: "Indique una dirección de correo válida.", errConsent: "Marque la casilla para que podamos contactarle.", errSend: "El envío no se ha completado. Inténtelo de nuevo en un momento o escriba a contact@exec-ia.ai.", legal: "Su correo y su diagnóstico solo sirven para responderle. Nunca se venden ni se confían a una IA.", legalLink: "mentions-legales-es.html#datos",
      tasks: [["Desplazar y transportar material", "robot", 4], ["Ordenar y reponer", "robot", 3], ["Controlar visualmente un producto o un equipo", "mixte", 3], ["Tareas repetitivas de manipulación", "robot", 4], ["Intervenir en un entorno penoso o de riesgo", "mixte", 2], ["Gestionar un imprevisto que exige criterio y arbitraje", "humain", 5]],
      futur: ["La relación con el cliente", "El pilotaje y la supervisión de los robots", "El asesoramiento y la pericia", "La organización y la coordinación", "La formación de los equipos", "Por definir"],
      vacant: ["Manipulación", "Preparación de pedidos", "Limpieza", "Vigilancia nocturna", "Control de calidad", "Recepción", "Ninguno por ahora"],
      labels: { robot: "Robot", mixte: "Compartido", humain: "Humano" },
      perWeek: "h/sem.", hours: "h",
      groupAria: "¿Quién hará «{t}» mañana?", rangeAria: "Horas por semana para «{t}»",
      assigned: "Tiempo asignado a las tareas: {a} h de {w} h",
      none: "Ninguna tarea clasificada como «Robot»",
      vEmpty: "Indique el tiempo dedicado a cada tarea para ver su resultado.",
      vRobot: "Una gran parte de su semana es potencialmente **robotizable**.\nLa verdadera cuestión pasa a ser el arbitraje:\n¿qué tareas confiar, a qué coste y qué hacer con el tiempo liberado?",
      vMixte: "Una parte notable de su semana pasaría a modo **compartido**: el robot asiste, la persona mantiene el control.\nLa organización y la formación cuentan tanto como la máquina.",
      vHumain: "Lo esencial de su semana sigue siendo **humano**.\nUn robot podría aliviar algunas tareas\nsin cambiar el núcleo de la actividad.",
      copied: "Diagnóstico copiado ✓", selected: "Texto seleccionado abajo", copyLabel: "Copiar mi diagnóstico",
      toastOk: "Péguelo donde quiera con Cmd + V (Mac) o Ctrl + V (PC). Aquí lo tiene:",
      toastManual: "Su navegador bloquea la copia automática: el texto de abajo está seleccionado, cópielo con Cmd + C (Mac) o Ctrl + C (PC).",
      cTitle: "Minidiagnóstico ROBOT · EXEC'IA", cWeek: "Semana de trabajo: {w} h",
      cRobot: "Tiempo potencialmente robotizable: {h} h/semana ({p} %)", cMixte: "Tiempo en modo compartido: {h} h/semana", cHumain: "Tiempo que sigue siendo humano: {h} h/semana",
      cTasks: "Mis tareas:", cFirst: "Confiar primero:", cFutur: "El tiempo liberado iría a: ", cVacant: "Puesto difícil de cubrir que un robot podría ocupar: ",
      cLink: "Hacer el minidiagnóstico: ", cSign: "exec-ia.ai · Decida antes de invertir",
      url: "https://exec-ia.ai/perspective-robots-humanoides-token-tax-es.html#mini-diagnostic"
    }
  };
  var T = I18N[lang] || I18N.fr;
  function fill(s, o) { return s.replace(/\{(\w)\}/g, function (m, k) { return o[k] != null ? o[k] : m; }); }
  function $(id) { return root.querySelector('#' + id); }

  var KEY = 'exec-ia-rbd-' + lang;
  var state = { week: 35, tasks: null, futur: [], vacant: [] };
  try { var saved = JSON.parse(localStorage.getItem(KEY) || 'null'); if (saved && saved.tasks && saved.tasks.length === T.tasks.length) state = saved; } catch (e) {}
  function save() { try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {} }
  if (!state.tasks) state.tasks = T.tasks.map(function (t) { return { t: t[0], v: t[1], h: t[2] }; });
  function sumH() { return state.tasks.reduce(function (a, r) { return a + (r.h || 0); }, 0); }

  var wk = $('rbd-week'), wo = $('rbd-week-out');

  function chips(el, list, key) {
    el.innerHTML = '';
    list.forEach(function (label) {
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'rbd-chip'; b.textContent = label;
      b.setAttribute('aria-pressed', state[key].indexOf(label) >= 0 ? 'true' : 'false');
      b.addEventListener('click', function () {
        var i = state[key].indexOf(label);
        if (i < 0) state[key].push(label); else state[key].splice(i, 1);
        b.setAttribute('aria-pressed', i < 0 ? 'true' : 'false');
        save();
      });
      el.appendChild(b);
    });
  }

  function syncWeek() {
    wk.value = state.week; wo.textContent = state.week + ' h';
    Array.prototype.forEach.call(root.querySelectorAll('.rbd-task input[type=range]'), function (el) { el.max = String(state.week); });
  }
  function fit() {
    var t = sumH(); if (t <= state.week) return;
    var f = state.week / t;
    state.tasks.forEach(function (r) { r.h = Math.floor(r.h * f); });
  }

  function renderTasks() {
    var box = $('rbd-tasks'); box.innerHTML = '';
    state.tasks.forEach(function (r, i) {
      var d = document.createElement('div'); d.className = 'rbd-task';
      var n = document.createElement('div'); n.className = 'rbd-task-name'; n.textContent = r.t;
      var seg = document.createElement('div'); seg.className = 'rbd-seg';
      seg.setAttribute('role', 'group'); seg.setAttribute('aria-label', fill(T.groupAria, { t: r.t }));
      ['robot', 'mixte', 'humain'].forEach(function (v) {
        var b = document.createElement('button'); b.type = 'button'; b.setAttribute('data-v', v);
        b.textContent = T.labels[v]; b.setAttribute('aria-pressed', r.v === v ? 'true' : 'false');
        b.addEventListener('click', function () {
          r.v = v;
          Array.prototype.forEach.call(seg.children, function (c) { c.setAttribute('aria-pressed', c.getAttribute('data-v') === v ? 'true' : 'false'); });
          compute(); save();
        });
        seg.appendChild(b);
      });
      var hw = document.createElement('div'); hw.className = 'rbd-hours';
      var rg = document.createElement('input'); rg.type = 'range'; rg.id = 'rbd-r' + i; rg.min = '0'; rg.max = String(state.week); rg.step = '1'; rg.value = r.h;
      rg.setAttribute('aria-label', fill(T.rangeAria, { t: r.t }));
      var out = document.createElement('output'); out.htmlFor = 'rbd-r' + i; out.textContent = r.h + ' ' + T.perWeek;
      rg.addEventListener('input', function () {
        var others = sumH() - r.h, v = Math.min(+rg.value, Math.max(0, 80 - others));
        if (+rg.value !== v) rg.value = v;
        r.h = v;
        if (others + v > state.week) { state.week = others + v; syncWeek(); }
        out.textContent = r.h + ' ' + T.perWeek; compute(); save();
      });
      hw.appendChild(rg); hw.appendChild(out);
      d.appendChild(n); d.appendChild(seg); d.appendChild(hw); box.appendChild(d);
    });
  }

  function compute() {
    var s = { robot: 0, mixte: 0, humain: 0 };
    state.tasks.forEach(function (r) { if (r.h > 0) s[r.v] += r.h; });
    var listed = s.robot + s.mixte + s.humain, tot = Math.max(state.week, listed);
    s.humain += tot - listed;
    var p = function (x) { return tot ? x / tot * 100 : 0; }, pr = Math.round(p(s.robot)), pm = Math.round(p(s.mixte));
    $('rbd-pct').textContent = pr;
    $('rbd-b-robot').style.width = p(s.robot) + '%';
    $('rbd-b-mixte').style.width = p(s.mixte) + '%';
    $('rbd-b-humain').style.width = p(s.humain) + '%';
    $('rbd-h-robot').textContent = s.robot; $('rbd-h-mixte').textContent = s.mixte; $('rbd-h-humain').textContent = s.humain;
    $('rbd-assigned').textContent = fill(T.assigned, { a: listed, w: state.week });
    var first = state.tasks.filter(function (r) { return r.v === 'robot' && r.h > 0; }).sort(function (a, b) { return b.h - a.h; }).slice(0, 3).map(function (r) { return r.t; });
    var ul = $('rbd-first'); ul.innerHTML = '';
    (first.length ? first : [T.none]).forEach(function (t) { var li = document.createElement('li'); li.textContent = t; if (!first.length) li.className = 'rbd-none'; ul.appendChild(li); });
    var v = !tot ? T.vEmpty : pr >= 40 ? T.vRobot : (pr + pm >= 40 ? T.vMixte : T.vHumain);
    var vEl = $('rbd-verdict'); vEl.innerHTML = '';
    v.split(/\*\*(.+?)\*\*/).forEach(function (part, i) {
      if (i % 2) { var sp = document.createElement('span'); sp.className = 'rbd-sb'; sp.textContent = part; vEl.appendChild(sp); }
      else vEl.appendChild(document.createTextNode(part));
    });
    return { s: s, pr: pr, v: v.replace(/\*\*/g, ''), first: first };
  }

  function renderAll() { fit(); syncWeek(); chips($('rbd-futur'), T.futur, 'futur'); chips($('rbd-vacant'), T.vacant, 'vacant'); renderTasks(); compute(); }

  wk.addEventListener('input', function () { state.week = +wk.value; wo.textContent = state.week + ' h'; fit(); renderTasks(); compute(); save(); });
  $('rbd-reset').addEventListener('click', function () { state.tasks.forEach(function (r) { r.h = 0; }); save(); renderAll(); });

  function buildText() {
    var c = compute(), L = [T.cTitle, '', fill(T.cWeek, { w: state.week }), fill(T.cRobot, { h: c.s.robot, p: c.pr }), fill(T.cMixte, { h: c.s.mixte }), fill(T.cHumain, { h: c.s.humain }), '', c.v, '', T.cTasks];
    state.tasks.forEach(function (r) { if (r.h > 0) L.push('- ' + r.t + ' (' + r.h + ' ' + T.hours + ') : ' + T.labels[r.v]); });
    if (c.first.length) { L.push('', T.cFirst); c.first.forEach(function (t) { L.push('✓ ' + t); }); }
    if (state.futur.length) L.push(T.cFutur + state.futur.join(', '));
    if (state.vacant.length) L.push(T.cVacant + state.vacant.join(', '));
    L.push('', T.cLink + T.url, T.cSign);
    return L.join('\n');
  }

  var btn = $('rbd-copy'), lbl = btn.querySelector('span');
  btn.addEventListener('click', function () {
    var txt = buildText(), out = $('rbd-copy-out'), toast = $('rbd-toast');
    out.hidden = false; out.value = txt; out.focus(); out.select();
    try { out.setSelectionRange(0, txt.length); } catch (e) {}
    var ok = false; try { ok = document.execCommand('copy'); } catch (e) {}
    function flash(t) { lbl.textContent = t; clearTimeout(btn._t); btn._t = setTimeout(function () { lbl.textContent = T.copyLabel; }, 4000); }
    function done() { flash(T.copied); toast.textContent = T.toastOk; }
    function manual() { flash(T.selected); toast.textContent = T.toastManual; }
    if (ok) done();
    try { navigator.clipboard.writeText(txt).then(done, function () { if (!ok) manual(); }); } catch (e) { if (!ok) manual(); }
  });

  /* Retour personnalisé : e-mail + consentement obligatoire, puis envoi à EXEC'IA */
  (function () {
    var col = root.querySelector('.rbd-copy-col');
    if (!col) return;
    var f = document.createElement('form');
    f.className = 'rbd-send'; f.noValidate = true;
    f.innerHTML = '<p class="rbd-send-title"></p><p class="rbd-send-lead"></p>' +
      '<label class="rbd-send-label" for="rbd-email"></label>' +
      '<input class="rbd-send-input" type="email" id="rbd-email" name="email" autocomplete="email" required maxlength="254">' +
      '<label class="rbd-consent"><input type="checkbox" id="rbd-consent" required><span></span></label>' +
      '<input type="text" name="website" class="rbd-hp" tabindex="-1" autocomplete="off" aria-hidden="true">' +
      '<button type="submit" class="rbd-btn rbd-btn--send"><span></span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h13M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></button>' +
      '<p class="rbd-send-msg" role="status" aria-live="polite"></p>' +
      '<p class="rbd-send-legal"><span></span> <a></a></p>';
    f.querySelector('.rbd-send-title').textContent = T.sendTitle;
    f.querySelector('.rbd-send-lead').textContent = T.sendLead;
    f.querySelector('.rbd-send-label').textContent = T.emailLabel;
    f.querySelector('.rbd-consent span').textContent = T.consentLabel;
    var sendLbl = f.querySelector('.rbd-btn--send span'); sendLbl.textContent = T.sendLabel;
    f.querySelector('.rbd-send-legal span').textContent = T.legal;
    var lk = f.querySelector('.rbd-send-legal a'); lk.href = T.legalLink; lk.textContent = '→';
    lk.setAttribute('aria-label', 'Données personnelles');
    col.appendChild(f);
    var msg = f.querySelector('.rbd-send-msg'), em = f.querySelector('#rbd-email'), ck = f.querySelector('#rbd-consent'), sb = f.querySelector('.rbd-btn--send');
    function say(t, ok) { msg.textContent = t; msg.classList.toggle('is-ok', !!ok); msg.classList.toggle('is-err', !ok); }
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var mail = em.value.trim();
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(mail)) { say(T.errEmail); em.focus(); return; }
      if (!ck.checked) { say(T.errConsent); ck.focus(); return; }
      sb.disabled = true; sendLbl.textContent = T.sending; say('', true);
      fetch('/api/diagnostic', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: mail, consent: true, diagnostic: buildText(), pct: compute().pr, langue: lang, page: location.pathname, website: f.website.value })
      }).then(function (r) {
        if (!r.ok) throw new Error('send');
        say(T.sentOk, true); em.value = ''; ck.checked = false; sendLbl.textContent = T.sendLabel;
      }).catch(function () {
        say(T.errSend); sb.disabled = false; sendLbl.textContent = T.sendLabel;
      });
    });
  })();

  renderAll();
})();
