(function(){
var b=document.querySelector('.burger'),n=document.getElementById('nav');
if(b)b.addEventListener('click',function(){var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o)});
if('IntersectionObserver'in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -60px 0px'});
document.querySelectorAll('.sec-hd,.svc,.steps li,.story-in>*,.pros-in>*,.proj,.row,.faq details').forEach(function(el){el.classList.add('rv');io.observe(el)})}
var f=document.getElementById('devis');
if(f)f.addEventListener('submit',function(e){e.preventDefault();var d=new FormData(f);
if(d.get('site'))return;
if(!d.get('nom')||!d.get('tel')||!d.get('msg')){document.getElementById('fmsg').textContent='Merci de remplir nom, téléphone et détails du projet. Ou appelez le 02 35 72 20 31.';return}
var body='Nom : '+d.get('nom')+'\nTéléphone : '+d.get('tel')+'\nE-mail : '+(d.get('email')||'')+'\nProjet : '+d.get('type')+'\n\n'+d.get('msg');
location.href='mailto:batidec-rouen@batidec76.com?subject='+encodeURIComponent('Demande de devis : '+d.get('type'))+'&body='+encodeURIComponent(body);
document.getElementById('fmsg').textContent='Votre messagerie va s\'ouvrir avec la demande. Si rien ne se passe, appelez le 02 35 72 20 31.'})
})();
