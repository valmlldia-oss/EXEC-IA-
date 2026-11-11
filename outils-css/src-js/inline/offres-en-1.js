
(function(){
  var PDFS={FR:'/assets/Les%205%20Essentiels_The%205%20Essentials_Los%205%20Esenciales.html',EN:'/assets/Les%205%20Essentiels_The%205%20Essentials_Los%205%20Esenciales.html',ES:'/assets/Les%205%20Essentiels_The%205%20Essentials_Los%205%20Esenciales.html'};
  var LANG='EN';
  var BLOCKED=new Set(['gmail.com','googlemail.com','yahoo.com','yahoo.fr','yahoo.co.uk','hotmail.com','hotmail.fr','hotmail.co.uk','outlook.com','outlook.fr','live.com','live.fr','icloud.com','me.com','mac.com','proton.me','protonmail.com','pm.me','aol.com','zoho.com','ymail.com','mail.com','gmx.com','gmx.fr','gmx.de','laposte.net','free.fr','orange.fr','wanadoo.fr','sfr.fr','bbox.fr','neuf.fr','numericable.fr','club-internet.fr','aliceadsl.fr','cegetel.net']);

  var fm=document.getElementById('nl-form'),sb=document.getElementById('nl-submit-btn'),errEl=document.getElementById('nl-global-err');

  function resetToIntro(){
    if(fm){fm.reset();fm.querySelectorAll('input').forEach(function(i){i.classList.remove('err');});}
    if(sb){sb.disabled=false;sb.textContent='Get the resource';}
    if(errEl){errEl.style.display='none';errEl.textContent='';}
    document.getElementById('nl-box-success').style.display='none';
    document.getElementById('nl-box-form').style.display='none';
    document.getElementById('nl-box-intro').style.display='';
  }

  var revBtn=document.getElementById('nl-reveal-btn');
  if(revBtn)revBtn.addEventListener('click',function(){
    document.getElementById('nl-box-success').style.display='none';
    document.getElementById('nl-box-intro').style.display='none';
    document.getElementById('nl-box-form').style.display='block';
    setTimeout(function(){document.getElementById('nl-fullname').focus();},80);
  });

  var closeBtn=document.getElementById('nl-close-form');
  if(closeBtn)closeBtn.addEventListener('click',resetToIntro);

  var newBtn=document.getElementById('nl-new-signup');
  if(newBtn)newBtn.addEventListener('click',function(){
    resetToIntro();
    setTimeout(function(){
      document.getElementById('nl-box-intro').style.display='none';
      document.getElementById('nl-box-form').style.display='block';
      setTimeout(function(){document.getElementById('nl-fullname').focus();},80);
    },20);
  });

  if(!fm)return;
  fm.addEventListener('submit',async function(e){
    e.preventDefault();
    errEl.style.display='none';errEl.textContent='';
    fm.querySelectorAll('input').forEach(function(i){i.classList.remove('err');});
    var n=fm.elements['fullname'].value.trim(),r=fm.elements['role'].value.trim(),c=fm.elements['company'].value.trim(),em=fm.elements['email'].value.trim(),ok=true;
    if(!n){document.getElementById('nl-fullname').classList.add('err');ok=false;}
    if(!r){document.getElementById('nl-role').classList.add('err');ok=false;}
    if(!c){document.getElementById('nl-company').classList.add('err');ok=false;}
    var domain=(em.split('@')[1]||'').toLowerCase();
    if(!em){document.getElementById('nl-email').classList.add('err');ok=false;}
    else if(!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(em)){document.getElementById('nl-email').classList.add('err');ok=false;}
    else if(BLOCKED.has(domain)){document.getElementById('nl-email').classList.add('err');errEl.textContent='Please use your work email address.';errEl.style.display='block';ok=false;}
    if(!ok){if(!errEl.textContent){errEl.textContent='Please complete all required fields.';errEl.style.display='block';}return;}
    var prenom=n.split(' ')[0];
    document.getElementById('nl-success-name').textContent=prenom;
    document.getElementById('nl-doc-link').href=PDFS[LANG];
    document.getElementById('nl-box-form').style.display='none';
    document.getElementById('nl-box-success').style.display='block';
    fetch('/api/airtable',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({fullname:n,role:r,company:c,email:em,langue:LANG,document_telecharge:'The 5 Essentials',source:'EXECIA_PRUNE'})}).catch(function(){});
  });
})();
