
(function(){
  document.querySelectorAll('.accord-btn').forEach(function(btn){
    btn.addEventListener('click',function(){
      var open=btn.getAttribute('aria-expanded')==='true';
      document.querySelectorAll('.accord-btn').forEach(function(b){
        b.setAttribute('aria-expanded','false');
        b.nextElementSibling.style.maxHeight=null;
      });
      if(!open){
        btn.setAttribute('aria-expanded','true');
        btn.nextElementSibling.style.maxHeight=btn.nextElementSibling.scrollHeight+'px';
      }
    });
  });
})();

(function(){
  function openFromHash(){
    var id=(location.hash||'').slice(1); if(!id) return;
    var item=document.getElementById(id);
    if(!item||!item.classList.contains('accord-item')) return;
    var btn=item.querySelector('.accord-btn');
    if(btn&&btn.getAttribute('aria-expanded')!=='true') btn.click();
    setTimeout(function(){ window.scrollTo({top:item.getBoundingClientRect().top+window.pageYOffset-110,behavior:'instant'}); },120);
  }
  window.addEventListener('load',openFromHash);
  window.addEventListener('hashchange',openFromHash);
})();
