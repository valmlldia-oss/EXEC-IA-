(function(){
  var WEBHOOK_URL = 'https://hook.eu1.make.com/hpwovottqaxnrjna3tyvv6b84v6dn1yx';

  var style = document.createElement('style');
  style.textContent = [
    '#phare-bubble{position:fixed;bottom:24px;right:24px;width:56px;height:56px;border-radius:50%;background:var(--rose,#C75F62);color:var(--ivory,#F6F1EB);border:none;cursor:pointer;box-shadow:0 6px 20px rgba(99,59,74,.28);z-index:9999;font-size:24px;display:flex;align-items:center;justify-content:center;}',
    '#phare-panel{position:fixed;bottom:92px;right:24px;width:320px;max-width:calc(100vw - 32px);max-height:440px;background:var(--ivory,#F6F1EB);border:1px solid rgba(99,59,74,.18);border-radius:14px;box-shadow:0 12px 40px rgba(99,59,74,.25);z-index:9999;display:none;flex-direction:column;overflow:hidden;font-family:Inter,-apple-system,sans-serif;}',
    '#phare-panel.open{display:flex;}',
    '#phare-head{background:var(--plum,#633B4A);color:var(--ivory,#F6F1EB);padding:14px 16px;font-size:.9rem;font-weight:600;}',
    '#phare-log{flex:1;overflow-y:auto;padding:14px;display:flex;flex-direction:column;gap:8px;}',
    '.phare-msg{max-width:85%;padding:8px 12px;border-radius:10px;font-size:.85rem;line-height:1.4;}',
    '.phare-msg.visitor{align-self:flex-end;background:var(--rose,#C75F62);color:#fff;}',
    '.phare-msg.bot{align-self:flex-start;background:#fff;color:var(--plum,#633B4A);border:1px solid rgba(99,59,74,.15);}',
    '#phare-form{display:flex;border-top:1px solid rgba(99,59,74,.15);}',
    '#phare-input{flex:1;border:none;padding:10px 12px;font-size:.85rem;font-family:inherit;outline:none;background:#fff;}',
    '#phare-send{border:none;background:var(--rose,#C75F62);color:#fff;padding:0 16px;cursor:pointer;font-size:.85rem;}'
  ].join('');
  document.head.appendChild(style);

  var bubble = document.createElement('button');
  bubble.id = 'phare-bubble';
  bubble.setAttribute('aria-label', 'Ouvrir le chat');
  bubble.textContent = '💬';
  document.body.appendChild(bubble);

  var panel = document.createElement('div');
  panel.id = 'phare-panel';
  panel.innerHTML =
    '<div id="phare-head">EXEC\'IA — Une question ?</div>' +
    '<div id="phare-log"><div class="phare-msg bot">Bonjour, comment puis-je vous aider ?</div></div>' +
    '<form id="phare-form"><input id="phare-input" type="text" placeholder="Votre message..." autocomplete="off"><button id="phare-send" type="submit">Envoyer</button></form>';
  document.body.appendChild(panel);

  bubble.addEventListener('click', function(){
    panel.classList.toggle('open');
  });

  var log = panel.querySelector('#phare-log');
  var form = panel.querySelector('#phare-form');
  var input = panel.querySelector('#phare-input');

  function addMsg(text, who){
    var div = document.createElement('div');
    div.className = 'phare-msg ' + who;
    div.textContent = text;
    log.appendChild(div);
    log.scrollTop = log.scrollHeight;
  }

  form.addEventListener('submit', function(e){
    e.preventDefault();
    var message = input.value.trim();
    if (!message) return;
    addMsg(message, 'visitor');
    input.value = '';
    addMsg('...', 'bot');
    var typingEl = log.lastChild;

    fetch(WEBHOOK_URL, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        message: message,
        page: window.location.pathname,
        heure: new Date().toISOString()
      })
    })
    .then(function(r){ return r.json(); })
    .then(function(data){
      typingEl.textContent = (data && data.reply) ? data.reply : 'Merci pour votre message, nous revenons vers vous rapidement.';
    })
    .catch(function(){
      typingEl.textContent = 'Merci pour votre message, nous revenons vers vous rapidement.';
    });
  });
})();
