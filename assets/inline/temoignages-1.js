// Témoignages.
// Ordinateur (cartes côte à côte) : une flèche déplie ou replie les trois citations ensemble (cartes alignées).
// Mobile (cartes empilées) : seule la citation touchée s'ouvre, et elle reste sous les yeux.
// Lien direct : temoignages.html#holger, #sandrine ou #wissam ouvre et montre le bon témoignage.
(function () {
  var folds = Array.prototype.slice.call(document.querySelectorAll('.testi-fold'));
  var syncing = false;
  function sideBySide() {
    var cards = document.querySelectorAll('.testi-grid > .testi');
    return cards.length > 1 && Math.abs(cards[0].getBoundingClientRect().top - cards[1].getBoundingClientRect().top) < 4;
  }
  folds.forEach(function (d) {
    d.addEventListener('toggle', function () {
      if (syncing || !sideBySide()) return;
      syncing = true;
      folds.forEach(function (o) { if (o !== d && o.open !== d.open) o.open = d.open; });
      syncing = false;
    });
  });
  function openFromHash() {
    var id = (location.hash || '').slice(1);
    if (!id) return;
    var card = document.getElementById(id);
    if (!card || !card.classList.contains('testi')) return;
    card.classList.add('visible');
    var fold = card.querySelector('.testi-fold');
    if (fold && !fold.open) fold.open = true;
    card.scrollIntoView({ block: 'start' });
  }
  openFromHash();
  window.addEventListener('hashchange', openFromHash);
})();
