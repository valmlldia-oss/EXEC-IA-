
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
