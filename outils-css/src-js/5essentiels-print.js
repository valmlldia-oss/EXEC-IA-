// Bouton « Télécharger en PDF » des 5 Essentiels : la politique de sécurité du site
// interdit les gestionnaires d'événements écrits dans la page, l'ouverture de la boîte d'impression passe donc par ce fichier.
document.querySelectorAll('.btn-download').forEach(function (b) {
  b.addEventListener('click', function () { window.print(); });
});
