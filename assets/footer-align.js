/* Aligne le bord gauche du logo du footer sur celui du logo de la barre de navigation (même ligne verticale) ; le bloc marque entier se décale, texte compris. */
(function () {
  function align() {
    var n = document.querySelector('#nav .nav-brand, nav .nav-brand');
    var f = document.querySelector('.footer-brand-mark');
    var b = document.querySelector('.footer-brand');
    if (!n || !f || !b) return;
    b.style.position = 'relative';
    b.style.left = '0px';
    var d = n.getBoundingClientRect().left - f.getBoundingClientRect().left;
    b.style.left = d + 'px';
  }
  var t;
  function later() { clearTimeout(t); t = setTimeout(align, 60); }
  window.addEventListener('resize', later);
  window.addEventListener('load', align);
  document.addEventListener('DOMContentLoaded', align);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(align);
  align();
})();
