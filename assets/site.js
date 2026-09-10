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
