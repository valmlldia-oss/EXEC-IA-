/* Footer : (1) aligne le bord gauche du logo et des mentions légales sur celui du logo de la navbar (même ligne verticale) ;
   (le lien Plan du site se cale sur le slogan) ; (2) ajuste la taille du slogan (deux lignes de même taille) à la largeur disponible. */
(function () {
  function align() {
    var n = document.querySelector('#nav .nav-brand, nav .nav-brand');
    var f = document.querySelector('.footer-brand-mark');
    var b = document.querySelector('.footer-brand');
    var l = document.querySelector('.footer-bottom .footer-plan');
    if (!f || !b) return;
    b.style.position = 'relative'; b.style.left = '0px';
    if (l) { l.style.position = 'relative'; l.style.left = '0px'; }
    /* Pages sans barre de navigation (mentions légales, confidentialité) : même ligne de référence que le logo de la navbar */
    var ref = n ? n.getBoundingClientRect().left : (window.innerWidth <= 600 ? 10 : (window.innerWidth < 1024 ? 20 : 24));
    var d = ref - f.getBoundingClientRect().left;
    b.style.left = d + 'px';
    if (l) l.style.left = d + 'px';
    fitTag();
  }
  function fitTag() {
    var tag = document.querySelector('.footer-brand .footer-tag');
    if (!tag) return;
    var parts = tag.querySelectorAll('.footer-tag-lead, .footer-tag-rest');
    if (window.innerWidth <= 600) { parts.forEach(function (p) { p.style.removeProperty('font-size'); }); return; }
    var site = document.querySelector('.footer-col--site'), contact = document.querySelector('.footer-col--contact');
    var tl = tag.getBoundingClientRect().left, br = b2().getBoundingClientRect();
    var next = site && site.getBoundingClientRect().top < br.bottom ? site : contact;
    var avail = next.getBoundingClientRect().left - tl - 22;
    var size = 30;
    function set(px) { parts.forEach(function (p) { p.style.setProperty('font-size', px + 'px', 'important'); }); }
    function width() {
      var w = 0;
      parts.forEach(function (p) { var r = document.createRange(); r.selectNodeContents(p); w = Math.max(w, r.getBoundingClientRect().width); });
      return w;
    }
    set(size);
    while (size > 11 && width() > avail) { size -= 0.25; set(size); }
  }
  function b2() { return document.querySelector('.footer-brand'); }
  var t;
  function later() { clearTimeout(t); t = setTimeout(align, 60); }
  window.addEventListener('resize', later);
  window.addEventListener('load', align);
  document.addEventListener('DOMContentLoaded', align);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(align);
  align();
})();
