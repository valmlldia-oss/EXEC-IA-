
    (function(){
      var cards = document.querySelectorAll('.constat-flip');
      cards.forEach(function(c){
        function toggle(){
          var f = c.classList.toggle('is-flipped');
          c.setAttribute('aria-pressed', f ? 'true' : 'false');
        }
        c.addEventListener('click', toggle);
        c.addEventListener('keydown', function(e){
          if(e.key === 'Enter' || e.key === ' '){ e.preventDefault(); toggle(); }
        });
      });
    })();
    