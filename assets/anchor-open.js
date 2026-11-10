/* Arrivée sur une ancre : ouvre le <details> visé (et ses parents) puis place l'élément sous le menu fixe. */
(function(){
  function navH(){var n=document.getElementById('nav');return n?n.getBoundingClientRect().height:0;}
  function go(){
    var id=''; try{id=decodeURIComponent((location.hash||'').slice(1));}catch(e){id=(location.hash||'').slice(1);}
    if(!id) return;
    var el=document.getElementById(id); if(!el) return;
    for(var n=el;n;n=n.parentElement){ if(n.tagName==='DETAILS') n.open=true; }
    function place(){ window.scrollTo({top:el.getBoundingClientRect().top+window.pageYOffset-navH()-24,behavior:'instant'}); }
    setTimeout(place,80); setTimeout(place,600);
  }
  window.addEventListener('load',go);
  window.addEventListener('hashchange',go);
})();
