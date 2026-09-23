
(function(){
  var banner=document.getElementById('cookie-banner');
  var key='execia_cookies';
  if(!banner||localStorage.getItem(key))return;
  setTimeout(function(){banner.classList.add('visible');document.body.classList.add('cookie-banner-open');},800);
  document.getElementById('cookie-accept').addEventListener('click',function(){
    localStorage.setItem(key,'accepted');
    banner.classList.remove('visible');
    document.body.classList.remove('cookie-banner-open');
  });
  document.getElementById('cookie-refuse').addEventListener('click',function(){
    localStorage.setItem(key,'refused');
    banner.classList.remove('visible');
    document.body.classList.remove('cookie-banner-open');
  });
})();
