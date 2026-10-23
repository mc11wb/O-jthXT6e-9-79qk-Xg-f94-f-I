/* ============================================================
   BoosterStop — JS commun à toutes les pages
   Bannière cookies + mise à jour du consentement GA4.
   Le snippet GA4 (gtag + consent default) est dans _includes/head.html.
   ============================================================ */

(function(){
  try{
    if(!localStorage.getItem('bs_cookie_consent')){
      var b=document.getElementById('cookieBanner'); if(b) b.classList.add('show');
    }
  }catch(e){ var b=document.getElementById('cookieBanner'); if(b) b.classList.add('show'); }
})();

function setCookieConsent(accepted){
  try{
    localStorage.setItem('bs_cookie_consent', accepted?'accepted':'essential');
    localStorage.setItem('bs_cookie_ts', new Date().toISOString());
  }catch(e){}
  /* Consent Mode v2 : informe GA4 immédiatement, sans attendre le prochain chargement */
  if(typeof gtag==='function'){
    gtag('consent','update',{'analytics_storage':accepted?'granted':'denied'});
  }
  var b=document.getElementById('cookieBanner'); if(b) b.classList.remove('show');
}

/* Menu de langue (<details class="lang-dd">) : se referme au clic à
   l'extérieur et avec la touche Échap. */
(function(){
  var dd=document.querySelectorAll('.lang-dd');
  if(!dd.length) return;
  document.addEventListener('click',function(e){
    for(var i=0;i<dd.length;i++){ if(dd[i].open && !dd[i].contains(e.target)) dd[i].open=false; }
  });
  document.addEventListener('keydown',function(e){
    if(e.key!=='Escape') return;
    for(var i=0;i<dd.length;i++){ if(dd[i].open){ dd[i].open=false; var s=dd[i].querySelector('summary'); if(s) s.focus(); } }
  });
})();
