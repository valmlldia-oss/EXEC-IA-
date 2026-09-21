(function () {
  var lang = (document.documentElement.lang || 'fr').slice(0, 2);
  if (['fr', 'en', 'es'].indexOf(lang) < 0) lang = 'fr';

  var T = {
    fr: { open: 'Poser une question', title: 'Une question&nbsp;?', intro: 'Écrivez-moi, je réponds personnellement par e-mail.', msg: 'Votre question', email: 'Votre e-mail professionnel', send: 'Envoyer', sending: 'Envoi…', ok: 'Merci, votre question est bien arrivée. Je vous réponds personnellement par e-mail.', err: 'L’envoi a échoué. Écrivez-nous à contact@exec-ia.ai.', close: 'Fermer', legal: 'Vos données servent uniquement à vous répondre. <a href="mentions-legales.html#donnees">En savoir plus</a>' },
    en: { open: 'Ask a question', title: 'A question?', intro: 'Write to me, I reply personally by email.', msg: 'Your question', email: 'Your business email', send: 'Send', sending: 'Sending…', ok: 'Thank you, your question has arrived. I will reply personally by email.', err: 'Sending failed. Please write to contact@exec-ia.ai.', close: 'Close', legal: 'Your data is used only to reply to you. <a href="mentions-legales-en.html#donnees">Learn more</a>' },
    es: { open: 'Hacer una pregunta', title: '¿Una pregunta?', intro: 'Escríbame, respondo personalmente por correo electrónico.', msg: 'Su pregunta', email: 'Su correo profesional', send: 'Enviar', sending: 'Enviando…', ok: 'Gracias, su pregunta ha llegado. Le responderé personalmente por correo electrónico.', err: 'El envío ha fallado. Escríbanos a contact@exec-ia.ai.', close: 'Cerrar', legal: 'Sus datos se utilizan únicamente para responderle. <a href="mentions-legales-es.html#datos">Más información</a>' }
  }[lang];

  var css = [
    '#qw-bubble{position:fixed;bottom:24px;right:24px;z-index:900;width:56px;height:56px;border-radius:50%;border:none;cursor:pointer;background:#C75F62;color:#FAF6F2;font-size:1.4rem;box-shadow:0 6px 20px rgba(99,59,74,.25);transition:transform .2s}',
    '#qw-bubble:hover{transform:scale(1.06)}',
    '#qw-bubble:focus-visible,#qw-send:focus-visible,#qw-close:focus-visible{outline:2px solid #633B4A;outline-offset:2px}',
    '#qw-panel{position:fixed;bottom:92px;right:24px;z-index:900;width:340px;max-width:calc(100vw - 32px);display:none;flex-direction:column;background:#F4EDE7;border:1px solid #D9C9C3;border-radius:14px;box-shadow:0 12px 40px rgba(99,59,74,.22);font-family:Inter,system-ui,sans-serif;color:#633B4A;overflow:hidden}',
    '#qw-panel.open{display:flex}',
    '#qw-head{display:flex;justify-content:space-between;align-items:center;background:#633B4A;color:#FAF6F2;padding:14px 16px;font-size:.95rem;font-weight:600}',
    '#qw-close{background:none;border:none;color:#FAF6F2;font-size:1.3rem;cursor:pointer;line-height:1}',
    '#qw-form{display:flex;flex-direction:column;gap:10px;padding:16px}',
    '#qw-form p{margin:0;font-size:.85rem;line-height:1.5}',
    '#qw-form textarea,#qw-form input[type=email]{font:inherit;font-size:.88rem;color:#633B4A;background:#FAF6F2;border:1px solid #D9C9C3;border-radius:8px;padding:10px 12px;width:100%;box-sizing:border-box}',
    '#qw-form textarea{min-height:96px;resize:vertical}',
    '#qw-form textarea:focus,#qw-form input:focus{outline:2px solid #C75F62;outline-offset:0;border-color:#C75F62}',
    '#qw-send{align-self:flex-start;background:#C75F62;color:#FAF6F2;border:none;border-radius:999px;padding:10px 22px;font:inherit;font-size:.88rem;font-weight:600;cursor:pointer}',
    '#qw-send[disabled]{opacity:.6;cursor:default}',
    '#qw-legal{font-size:.74rem;opacity:.8}#qw-legal a{color:#C75F62}',
    '#qw-status{font-size:.85rem;line-height:1.5}',
    '.qw-hp{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}'
  ].join('');
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  var bubble = document.createElement('button');
  bubble.id = 'qw-bubble'; bubble.type = 'button'; bubble.setAttribute('aria-label', T.open); bubble.setAttribute('aria-expanded', 'false'); bubble.textContent = '💬';

  var panel = document.createElement('div');
  panel.id = 'qw-panel'; panel.setAttribute('role', 'dialog'); panel.setAttribute('aria-label', T.open);
  panel.innerHTML =
    '<div id="qw-head"><span>' + T.title + '</span><button id="qw-close" type="button" aria-label="' + T.close + '">×</button></div>' +
    '<form id="qw-form" novalidate><p>' + T.intro + '</p>' +
    '<textarea id="qw-msg" required maxlength="2000" placeholder="' + T.msg + '" aria-label="' + T.msg + '"></textarea>' +
    '<input id="qw-mail" type="email" required maxlength="254" autocomplete="email" placeholder="' + T.email + '" aria-label="' + T.email + '">' +
    '<div class="qw-hp" aria-hidden="true"><input id="qw-web" type="text" name="website" tabindex="-1" autocomplete="off"></div>' +
    '<button id="qw-send" type="submit">' + T.send + '</button>' +
    '<p id="qw-legal">' + T.legal + '</p><p id="qw-status" role="status" aria-live="polite"></p></form>';

  document.body.appendChild(bubble); document.body.appendChild(panel);

  function toggle(open) {
    panel.classList.toggle('open', open);
    bubble.setAttribute('aria-expanded', String(open));
    if (open) panel.querySelector('#qw-msg').focus(); else bubble.focus();
  }
  bubble.addEventListener('click', function () { toggle(!panel.classList.contains('open')); });
  panel.querySelector('#qw-close').addEventListener('click', function () { toggle(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && panel.classList.contains('open')) toggle(false); });

  var form = panel.querySelector('#qw-form'), status = panel.querySelector('#qw-status'), send = panel.querySelector('#qw-send');
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var msg = form.querySelector('#qw-msg').value.trim(), mail = form.querySelector('#qw-mail').value.trim();
    if (msg.length < 3) { form.querySelector('#qw-msg').focus(); return; }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(mail)) { form.querySelector('#qw-mail').focus(); return; }
    send.disabled = true; send.textContent = T.sending; status.textContent = '';
    fetch('/api/question', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: msg, email: mail, langue: lang.toUpperCase(), page: location.pathname, website: form.querySelector('#qw-web').value })
    }).then(function (r) {
      if (!r.ok) throw new Error(r.status);
      status.textContent = T.ok; form.querySelector('#qw-msg').value = ''; form.querySelector('#qw-mail').value = '';
      send.textContent = T.send;
    }).catch(function () {
      status.textContent = T.err; send.textContent = T.send; send.disabled = false;
    }).then(function () { setTimeout(function () { send.disabled = false; }, 4000); });
  });
})();
