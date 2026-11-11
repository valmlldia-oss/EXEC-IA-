/* HubSpot (compte EU1 149740125) : le suivi n'est chargé que si la bannière de consentement
   HubSpot est publiée pour le domaine visité. Sans bannière, aucun cookie de suivi n'est déposé.
   Le chargement démarre après l'affichage complet de la page (load + 1,5 s) : la page reste rapide,
   le bandeau cookies apparaît quelques secondes après l'arrivée du visiteur. */
(function () {
  var ID = '149740125';
  var HOST = location.hostname;
  function load() {
    var s = document.createElement('script');
    s.type = 'text/javascript';
    s.id = 'hs-script-loader';
    s.async = true;
    s.defer = true;
    s.src = 'https://js-eu1.hs-scripts.com/' + ID + '.js';
    document.head.appendChild(s);
    document.querySelectorAll('.cookie-prefs-wrap').forEach(function (e) { e.hidden = false; });
  }
  function go() {
    if (!window.fetch) return;
    fetch('https://js-eu1.hs-banner.com/v2/' + ID + '/banner.js', { cache: 'no-store' })
      .then(function (r) { return r.ok ? r.text() : ''; })
      .then(function (t) { if (t.indexOf('"' + HOST + '":[{') > -1) load(); })
      .catch(function () {});
  }
  function later() { setTimeout(go, 1500); }
  if (document.readyState === 'complete') later(); else window.addEventListener('load', later);
})();
