
(function(){
  var items = document.querySelectorAll('.offres-cat-item');
  function openItem(item){
    var btn = item.querySelector('.offres-cat-btn');
    var body = item.querySelector('.offres-cat-body');
    btn.setAttribute('aria-expanded','true');
    body.style.maxHeight = body.scrollHeight + 'px';
  }
  function closeItem(item){
    var btn = item.querySelector('.offres-cat-btn');
    var body = item.querySelector('.offres-cat-body');
    btn.setAttribute('aria-expanded','false');
    body.style.maxHeight = null;
  }
  items.forEach(function(item){
    var btn = item.querySelector('.offres-cat-btn');
    btn.addEventListener('click', function(){
      var isOpen = btn.getAttribute('aria-expanded') === 'true';
      items.forEach(closeItem);
      if(!isOpen) openItem(item);
    });
  });
  window.addEventListener('resize', function(){
    items.forEach(function(item){
      if(item.querySelector('.offres-cat-btn').getAttribute('aria-expanded') === 'true'){
        item.querySelector('.offres-cat-body').style.maxHeight = item.querySelector('.offres-cat-body').scrollHeight + 'px';
      }
    });
  });

  function scrollToEl(el){
    var nav = document.getElementById('nav');
    var navH = nav ? nav.offsetHeight : 0;
    var top = window.scrollY + el.getBoundingClientRect().top - navH - 16;
    window.scrollTo({ top: top, behavior: 'smooth' });
  }
  document.querySelectorAll('.offres-orientation-card').forEach(function(card){
    card.addEventListener('click', function(){
      var target = card.getAttribute('data-target');
      if(target === 'dg'){
        var dg = document.querySelector('.offre-dg');
        if(dg) scrollToEl(dg);
        return;
      }
      var idx = parseInt(target, 10);
      var item = items[idx];
      if(!item) return;
      var btn = item.querySelector('.offres-cat-btn');
      var wasOpen = btn.getAttribute('aria-expanded') === 'true';
      if(!wasOpen){ btn.click(); }
      if(wasOpen){ scrollToEl(item); } else { setTimeout(function(){ scrollToEl(item); }, 460); }
    });
  });
})();
