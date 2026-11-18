(function(){
var b=document.querySelector('.burger'),n=document.getElementById('nav'),hd=document.querySelector('.hd');
if(b)b.addEventListener('click',function(){var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o)});
var pl=document.querySelector('.nav a[href="/prestations/"]'),t;
if(pl&&hd&&matchMedia('(min-width:821px)').matches){
var op=function(){clearTimeout(t);hd.classList.add('mm-open')},cl=function(){t=setTimeout(function(){hd.classList.remove('mm-open')},180)};
pl.addEventListener('mouseenter',op);pl.addEventListener('mouseleave',cl);
var mm=document.querySelector('.mm');mm.addEventListener('mouseenter',op);mm.addEventListener('mouseleave',cl)}
if('IntersectionObserver'in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -60px 0px'});
document.querySelectorAll('.sec-hd,.uni,.ref,.steps li,.story-in>*,.split>*,.proj,.card,.faq details,.canon,.why>div,.av,.tr').forEach(function(el,i){el.classList.add('rv');el.style.transitionDelay=(i%4)*70+'ms';io.observe(el)})}
document.querySelectorAll('form[data-mailto]').forEach(function(f){f.addEventListener('submit',function(e){e.preventDefault();var d=new FormData(f);if(d.get('site'))return;
var m=f.querySelector('#fmsg,.qf-m');
if(!d.get('nom')||!d.get('tel')||!d.get('msg')){m.textContent='Merci d\'indiquer votre nom et votre téléphone. Ou appelez le 02 35 72 20 31.';return}
var body='Nom : '+d.get('nom')+'\nTéléphone : '+d.get('tel')+'\nE-mail : '+(d.get('email')||'')+'\nProjet : '+d.get('type')+'\n\n'+d.get('msg');
location.href='mailto:batidec-rouen@batidec76.com?subject='+encodeURIComponent('Demande de devis : '+d.get('type'))+'&body='+encodeURIComponent(body);
m.textContent='Votre messagerie va s\'ouvrir avec la demande. Si rien ne se passe, appelez le 02 35 72 20 31.'})});
})();
