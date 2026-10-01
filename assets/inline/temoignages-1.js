// Témoignages : une flèche déplie ou replie les trois citations ensemble (cartes alignées)
document.querySelectorAll('.testi-fold').forEach(function (d, _, all) {
  d.addEventListener('toggle', function () {
    all.forEach(function (o) { if (o !== d && o.open !== d.open) o.open = d.open; });
  });
});
