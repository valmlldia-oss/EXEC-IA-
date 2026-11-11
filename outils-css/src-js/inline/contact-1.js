
(function () {
  var box = document.getElementById('diagBox');
  if (!box) return;
  var tags = [];
  var qs = box.querySelectorAll('.diag-q');
  var dots = box.querySelectorAll('.diag-dot');
  var results = box.querySelectorAll('.diag-result');
  var restart = box.querySelector('.diag-restart');
  var leadStep = box.querySelector('.diag-lead');
  var leadForm = document.getElementById('diagLeadForm');
  var leadErr = document.getElementById('diagLeadErr');
  var BLOCKED = new Set(['gmail.com','googlemail.com','yahoo.com','yahoo.fr','yahoo.co.uk','hotmail.com','hotmail.fr','hotmail.co.uk','outlook.com','outlook.fr','live.com','live.fr','icloud.com','me.com','mac.com','proton.me','protonmail.com','pm.me','aol.com','zoho.com','ymail.com','mail.com','gmx.com','gmx.fr','gmx.de','laposte.net','free.fr','orange.fr','wanadoo.fr','sfr.fr','bbox.fr','neuf.fr','numericable.fr','club-internet.fr','aliceadsl.fr','cegetel.net']);

  function computeWinner() {
    var count = { align: 0, tech: 0, unclear: 0 };
    tags.forEach(function (t) { count[t]++; });
    var winner = 'align';
    if (count.tech > count[winner]) winner = 'tech';
    if (count.unclear > count[winner]) winner = 'unclear';
    return winner;
  }

  function showResult(winner) {
    box.querySelector('.diag-progress').classList.add('is-done');
    results.forEach(function (r) {
      r.classList.toggle('is-active', r.getAttribute('data-result') === winner);
    });
    box.classList.add('is-result');
  }

  box.addEventListener('click', function (e) {
    var opt = e.target.closest('.diag-opt');
    if (opt) {
      var q = opt.closest('.diag-q');
      var step = parseInt(q.getAttribute('data-q'), 10);
      tags.push(opt.getAttribute('data-tag'));
      q.classList.remove('is-active');
      if (step < 3) {
        var next = box.querySelector('.diag-q[data-q="' + (step + 1) + '"]');
        next.classList.add('is-active');
        dots.forEach(function (d) {
          d.classList.toggle('is-active', parseInt(d.getAttribute('data-dot'), 10) <= step + 1);
        });
      } else {
        leadStep.classList.add('is-active');
        setTimeout(function () { leadForm.elements['fullname'].focus(); }, 80);
      }
      return;
    }
    if (e.target.closest('.diag-restart')) {
      tags = [];
      box.classList.remove('is-result');
      box.querySelector('.diag-progress').classList.remove('is-done');
      results.forEach(function (r) { r.classList.remove('is-active'); });
      leadStep.classList.remove('is-active');
      leadForm.reset();
      leadForm.querySelectorAll('input').forEach(function (i) { i.classList.remove('err'); });
      leadErr.style.display = 'none';
      leadErr.textContent = '';
      qs.forEach(function (q) { q.classList.remove('is-active'); });
      qs[0].classList.add('is-active');
      dots.forEach(function (d) {
        d.classList.toggle('is-active', d.getAttribute('data-dot') === '1');
      });
    }
  });

  if (leadForm) {
    leadForm.addEventListener('submit', function (e) {
      e.preventDefault();
      leadErr.style.display = 'none';
      leadErr.textContent = '';
      leadForm.querySelectorAll('input').forEach(function (i) { i.classList.remove('err'); });

      var n = leadForm.elements['fullname'].value.trim();
      var r = leadForm.elements['role'].value.trim();
      var c = leadForm.elements['company'].value.trim();
      var em = leadForm.elements['email'].value.trim();
      var ok = true;

      if (!n) { leadForm.elements['fullname'].classList.add('err'); ok = false; }
      if (!r) { leadForm.elements['role'].classList.add('err'); ok = false; }
      if (!c) { leadForm.elements['company'].classList.add('err'); ok = false; }
      var domain = (em.split('@')[1] || '').toLowerCase();
      if (!em) { leadForm.elements['email'].classList.add('err'); ok = false; }
      else if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(em)) { leadForm.elements['email'].classList.add('err'); ok = false; }
      else if (BLOCKED.has(domain)) { leadForm.elements['email'].classList.add('err'); leadErr.textContent = "Merci d'utiliser votre adresse e-mail professionnelle."; leadErr.style.display = 'block'; ok = false; }
      if (!ok) {
        if (!leadErr.textContent) { leadErr.textContent = "Merci de compléter l'ensemble des champs obligatoires."; leadErr.style.display = 'block'; }
        return;
      }

      var winner = computeWinner();
      leadStep.classList.remove('is-active');
      showResult(winner);

      fetch('/api/airtable', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ fullname: n, role: r, company: c, email: em, langue: 'FR', document_telecharge: 'Diagnostic Express', source: 'EXECIA_PRUNE_DIAGNOSTIC', resultat: winner })
      }).catch(function () {});
    });
  }
})();
