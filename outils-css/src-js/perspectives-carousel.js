/* Perspectives : un carrousel par catégorie (défilement horizontal, flèches, tactile, clavier). Aucune bibliothèque. */
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('.pv-carousel').forEach(function (c) {
    var vp = c.querySelector('.pv-viewport');
    var prev = c.querySelector('.pv-arrow--prev');
    var next = c.querySelector('.pv-arrow--next');
    if (!vp || !prev || !next) return;
    var raf = 0;
    function step() {
      var card = vp.querySelector('.persp-card');
      var grid = vp.firstElementChild;
      if (!card || !grid) return vp.clientWidth;
      var gap = parseFloat(getComputedStyle(grid).columnGap) || 0;
      return card.getBoundingClientRect().width + gap;
    }
    function update() {
      var max = vp.scrollWidth - vp.clientWidth;
      var can = max > 2;
      var hidePrev = !can || vp.scrollLeft <= 2;
      var hideNext = !can || vp.scrollLeft >= max - 2;
      if (hidePrev && document.activeElement === prev && !hideNext) next.focus();
      if (hideNext && document.activeElement === next && !hidePrev) prev.focus();
      prev.hidden = hidePrev;
      next.hidden = hideNext;
    }
    function go(dir) {
      vp.scrollBy({ left: dir * step(), behavior: reduce ? 'auto' : 'smooth' });
      setTimeout(update, 450);
      setTimeout(update, 900);
    }
    prev.addEventListener('click', function () { go(-1); });
    next.addEventListener('click', function () { go(1); });
    vp.addEventListener('scroll', function () {
      if (raf) return;
      raf = setTimeout(function () { raf = 0; update(); }, 50);
    }, { passive: true });
    vp.addEventListener('scrollend', update);
    c.addEventListener('keydown', function (e) {
      if (e.target.closest && e.target.closest('.pv-arrow')) return;
      if (e.key === 'ArrowRight') { go(1); } else if (e.key === 'ArrowLeft') { go(-1); }
    });
    window.addEventListener('resize', update);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(update);
    window.addEventListener('load', update);
    update();
  });
})();
