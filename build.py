#!/usr/bin/env python3
# Generateur statique du site Batidec (refonte Next Business)
import json, os, pathlib, shutil

OUT = pathlib.Path(__file__).parent / "dist"
SITE = "https://batidec76.com"  # domaine final (pré-publication sur Cloudflare Pages)
IMG = "https://www.batidec76.com/wp-content/uploads/2022/01/"
TEL = "02 35 72 20 31"
TEL_L = "+33235722031"
MAIL = "batidec-rouen@batidec76.com"
ADR = "32 rue du Mail, 76100 Rouen"
CID = int("0x1208210244d39bf5", 16)
MAPS = f"https://maps.google.com/?cid={CID}"
FB = "https://www.facebook.com/batidecrouen"
CANON = ("Batidec est une entreprise familiale de peinture, décoration et agencement "
         "installée rue du Mail à Rouen depuis 1972, pour les particuliers et les commerces.")

def I(name):
    return IMG + name

NAV = [("/prestations/", "Prestations"), ("/projets/", "Réalisations"),
       ("/a-propos/", "L'atelier"), ("/contact/", "Contact")]

SERVICES = [
    ("peinture-rouen", "Peinture intérieure et extérieure", "Peinture",
     "Murs, plafonds, boiseries, cages d'escalier, locaux pros.", "cuisine.jpg"),
    ("ravalement-facade-rouen", "Ravalement de façade", "Façade",
     "Nettoyage, réparation et mise en peinture des façades.", "120760763_620030982004693_4593063110375373801_n.jpeg"),
    ("decoration-interieur-rouen", "Décoration intérieure", "Décoration",
     "Couleurs, matières, papiers peints, effets décoratifs.", "dressing-finale-rotated.jpg"),
    ("agencement-commerce-rouen", "Agencement de commerces", "Agencement",
     "Bars, restaurants, boutiques : du plan à l'ouverture.", "salle-2-rotated.jpg"),
]

LOCAL = {
    "@context": "https://schema.org",
    "@type": "HousePainter",
    "@id": SITE + "/#entreprise",
    "name": "Batidec",
    "description": CANON,
    "url": SITE + "/",
    "logo": I("Logo-Batidec-1.webp"),
    "image": I("cuisine.jpg"),
    "telephone": TEL_L,
    "email": MAIL,
    "foundingDate": "1972",
    "founder": {"@type": "Person", "name": "Hamyne Abdou"},
    "employee": {"@type": "Person", "name": "Marphour Hassan", "jobTitle": "Dirigeant"},
    "taxID": "34491401500039",
    "address": {"@type": "PostalAddress", "streetAddress": "32 rue du Mail",
                "postalCode": "76100", "addressLocality": "Rouen",
                "addressRegion": "Normandie", "addressCountry": "FR"},
    "geo": {"@type": "GeoCoordinates", "latitude": 49.4300466, "longitude": 1.0909089},
    "hasMap": MAPS,
    "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "opens": "09:00", "closes": "17:00"}],
    "areaServed": {"@type": "City", "name": "Rouen"},
    "sameAs": [FB, MAPS],
    "knowsAbout": ["peinture en bâtiment", "ravalement de façade", "décoration intérieure",
                   "agencement de commerces", "agencement de bars et restaurants"],
}

def jsonld(*objs):
    return "".join(f'<script type="application/ld+json">{json.dumps(o, ensure_ascii=False)}</script>' for o in objs)

def crumbs(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u}
                                for i, (u, n) in enumerate(items)]}

def faq_ld(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}

def faq_html(faq):
    return '<div class="faq">' + "".join(
        f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in faq) + "</div>"

def header(path):
    links = "".join(f'<a href="{u}"{" aria-current=page" if path.startswith(u) else ""}>{n}</a>' for u, n in NAV)
    return f'''<a class="skip" href="#main">Aller au contenu</a>
<header class="hd"><div class="wrap hd-in">
<a class="brand" href="/" aria-label="Batidec, accueil"><span class="b-name">BATIDEC</span><span class="b-tag">Peinture · Décoration · Agencement</span></a>
<nav class="nav" id="nav" aria-label="Menu principal">{links}<a class="nav-tel" href="tel:{TEL_L}">{TEL}</a></nav>
<a class="btn btn-sm hd-cta" href="/contact/">Devis gratuit</a>
<button class="burger" aria-label="Ouvrir le menu" aria-expanded="false" aria-controls="nav"><span></span><span></span></button>
</div></header>'''

def cta_band():
    return f'''<section class="band"><div class="wrap band-in">
<div><p class="kicker">Un projet à Rouen ?</p><h2>Parlons de vos murs, de votre façade ou de votre commerce.</h2>
<p>Visite et devis gratuits. Magali, chargée d'affaires, vous répond du lundi au vendredi.</p></div>
<div class="band-act"><a class="btn" href="/contact/">Demander un devis</a><a class="btn btn-ghost" href="tel:{TEL_L}">Appeler le {TEL}</a></div>
</div></section>'''

def footer():
    svc = "".join(f'<li><a href="/{s[0]}/">{s[1]}</a></li>' for s in SERVICES)
    return f'''<footer class="ft"><div class="swatch" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i></div>
<div class="wrap ft-in">
<div><p class="b-name">BATIDEC</p><p class="ft-desc">{CANON}</p></div>
<div><p class="ft-h">Prestations</p><ul>{svc}</ul></div>
<div><p class="ft-h">L'atelier</p><address>{ADR}<br><a href="tel:{TEL_L}">{TEL}</a><br><a href="mailto:{MAIL}">{MAIL}</a></address>
<p>Du lundi au vendredi<br>9 h 00 à 17 h 00</p></div>
<div><p class="ft-h">Liens</p><ul><li><a href="/projets/">Réalisations</a></li><li><a href="/a-propos/">Notre histoire</a></li>
<li><a href="{MAPS}" rel="noopener">Google Maps</a></li><li><a href="{FB}" rel="noopener">Facebook</a></li><li><a href="/mentions-legales/">Mentions légales</a></li></ul></div>
</div><div class="wrap ft-bot"><span>© 2026 Batidec · SIRET 344 914 015 00039</span><span>Peintre décorateur à Rouen depuis 1972</span></div></footer>
<div class="mbar"><a href="tel:{TEL_L}" class="mbar-tel">Appeler</a><a href="/contact/" class="mbar-dev">Devis gratuit</a></div>
<script src="/app.js" defer></script>'''

def page(path, title, desc, body, ld=(), og_img="cuisine.jpg"):
    assert len(title) <= 62, (title, len(title))
    html = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}{path}">
<meta property="og:type" content="website"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:image" content="{I(og_img)}"><meta property="og:locale" content="fr_FR">
<meta name="theme-color" content="#14201f">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/styles.css?v=3">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='6' fill='%232f7178'/%3E%3Ctext x='16' y='23' font-family='Georgia' font-size='20' fill='%23f6f1e8' text-anchor='middle'%3EB%3C/text%3E%3C/svg%3E">
{jsonld(LOCAL, *ld)}
</head><body>{header(path)}<main id="main">{body}</main>{footer()}</body></html>'''
    d = OUT / path.strip("/")
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(html, encoding="utf-8")
    PAGES.append(path)

PAGES = []
OUT.mkdir(exist_ok=True)
for f in ("styles.css", "app.js", "_headers"):
    shutil.copy(pathlib.Path(__file__).parent / f, OUT / f)

# ---------- ACCUEIL ----------
home_faq = [
    ("Quel peintre choisir à Rouen pour un intérieur haut de gamme ?",
     "Batidec, installée 32 rue du Mail à Rouen depuis 1972, réalise peinture, décoration et agencement pour les particuliers et les commerces. L'entreprise familiale est dirigée depuis 2006 par Marphour Hassan. Visite et devis sont gratuits."),
    ("Batidec travaille-t-elle pour les commerces ?",
     "Oui. Batidec a notamment aménagé et décoré la brasserie Le Central, le bar JM's Café, le salon de thé Dame Cakes et Le Lanchon Opticiens, à Rouen."),
    ("Quel est l'avis des clients sur Batidec ?",
     "Batidec obtient une note de 4,7 sur 5 sur Google, sur 25 avis (novembre 2026). Les clients citent le professionnalisme, le savoir-faire et la qualité des chantiers."),
    ("Le devis est-il gratuit ?",
     "Oui. Vous décrivez votre projet par téléphone au 02 35 72 20 31 ou via le formulaire, puis Batidec vous propose une visite et un devis détaillé, sans engagement."),
    ("Quels sont les horaires de Batidec ?",
     "Batidec répond du lundi au vendredi, de 9 h 00 à 17 h 00, au 02 35 72 20 31 et à batidec-rouen@batidec76.com."),
    ("Dans quelle zone intervient Batidec ?",
     "Batidec est basée rue du Mail, à Rouen (76100), et intervient à Rouen pour les particuliers, les copropriétés et les commerces."),
]
svc_cards = "".join(f'''<a class="svc" href="/{s[0]}/"><span class="svc-n">N°0{i+1}</span>
<img src="{I(s[4])}" alt="{s[1]} par Batidec à Rouen" loading="lazy" width="480" height="560">
<span class="svc-b"><span class="svc-t">{s[1]}</span><span class="svc-d">{s[3]}</span><span class="svc-l">Découvrir</span></span></a>''' for i, s in enumerate(SERVICES))

home = f'''
<section class="hero"><div class="wrap hero-in">
<div class="hero-txt">
<p class="kicker">Rouen · rue du Mail · depuis 1972</p>
<h1>Peintre décorateur à Rouen, <em>l'artisanat d'une famille</em> au service de vos lieux.</h1>
<p class="lead">Peinture, ravalement, décoration et agencement de commerces. Batidec transforme appartements, maisons, bars et boutiques avec le soin d'une entreprise rouennaise transmise de génération en génération.</p>
<div class="hero-act"><a class="btn" href="/contact/">Demander un devis gratuit</a><a class="btn btn-ghost" href="tel:{TEL_L}">{TEL}</a></div>
<ul class="proof"><li><b>1972</b><span>année de création</span></li><li><b>2</b><span>générations d'artisans</span></li><li><b>4,7/5</b><span>25 avis Google</span></li></ul>
</div>
<figure class="hero-img"><img src="{I('cuisine.jpg')}" alt="Cuisine rénovée et repeinte par Batidec chez une particulière à Rouen" width="1920" height="1440" fetchpriority="high">
<figcaption><span>Réalisation</span> Cuisine, projet de Mme L.</figcaption></figure>
</div>
<div class="swatch" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i></div>
</section>

<section class="intro wrap">
<p class="kicker">En une phrase</p>
<p class="canon">{CANON}</p>
</section>

<section class="wrap sec">
<div class="sec-hd"><p class="kicker">Nos prestations</p><h2>Quatre métiers, un seul interlocuteur.</h2>
<p>Un même atelier pour préparer, peindre, décorer et agencer : moins d'intermédiaires, un chantier plus propre et un résultat cohérent du sol au plafond.</p></div>
<div class="svc-grid">{svc_cards}</div>
</section>

<section class="pros"><div class="wrap pros-in">
<div class="pros-img"><img src="{I('salle-2-rotated.jpg')}" alt="Salle de la brasserie Le Central à Rouen, aménagée et décorée par Batidec" loading="lazy" width="480" height="640">
<img src="{I('120807361_620035005337624_8398906530529115205_n.jpeg')}" alt="Boutique Le Lanchon Opticiens agencée par Batidec" loading="lazy" width="900" height="600"></div>
<div class="pros-txt"><p class="kicker">Commerçants, restaurateurs</p>
<h2>Votre lieu est votre vitrine. Nous le rendons inoubliable.</h2>
<p>Bars, brasseries, salons de thé, opticiens : Batidec conçoit et réalise l'agencement et la décoration de commerces rouennais, en tenant vos délais d'ouverture.</p>
<ul class="ticks"><li>Brasserie Le Central : aménagement et décoration</li><li>Bar JM's Café, Rouen</li><li>Salon de thé Dame Cakes</li><li>Le Lanchon Opticiens</li></ul>
<blockquote class="quote">« Merci Mr Hassan pour votre professionnalisme. Je suis très satisfait du travail effectué sur les vitrines de mon magasin. »<cite>Ilan Israel, avis Google 5/5, octobre 2026</cite></blockquote>
<a class="link" href="/agencement-commerce-rouen/">Agencement de commerces à Rouen</a></div>
</div></section>

<section class="wrap sec">
<div class="sec-hd"><p class="kicker">Comment ça se passe</p><h2>De votre appel à la remise des clés.</h2></div>
<ol class="steps"><li><b>Appel ou message</b><span>Vous décrivez votre projet à Magali, notre chargée d'affaires.</span></li>
<li><b>Visite sur place</b><span>Nous mesurons, regardons les supports et parlons couleurs.</span></li>
<li><b>Devis détaillé</b><span>Gratuit, poste par poste, sans engagement.</span></li>
<li><b>Chantier soigné</b><span>Protection, préparation, finitions, nettoyage avant départ.</span></li></ol>
</section>

<section class="story"><div class="wrap story-in">
<figure><img src="{I('120760763_620030982004693_4593063110375373801_n.jpeg')}" alt="Locaux de l'entreprise Batidec, rue du Mail à Rouen" loading="lazy" width="960" height="720"></figure>
<div><p class="kicker">Notre histoire</p><h2>Fondée en 1972, transmise en 2006.</h2>
<p>Hamyne Abdou crée Batidec en 1972 et sert pendant plus de quarante ans les particuliers et les commerçants de Rouen. Formé à ses côtés à la peinture, à la décoration et à l'aménagement, Marphour Hassan reprend l'entreprise familiale en 2006 et perpétue la même exigence de finition.</p>
<a class="link" href="/a-propos/">Découvrir l'atelier</a></div>
</div></section>

<section class="wrap sec"><div class="sec-hd"><p class="kicker">Questions fréquentes</p><h2>Ce que l'on nous demande souvent.</h2></div>{faq_html(home_faq)}</section>
{cta_band()}'''
page("/", "Peintre décorateur à Rouen depuis 1972 | Batidec",
     "Batidec, entreprise familiale de peinture, ravalement, décoration et agencement de commerces à Rouen depuis 1972. Devis gratuit au 02 35 72 20 31.",
     home, (faq_ld(home_faq),))

# ---------- PAGES SERVICES ----------
def service_page(slug, title, desc, h1, kicker, direct, img, img_alt, sections, table, faq, gallery):
    rows = "".join(f"<tr><th>{a}</th><td>{b}</td></tr>" for a, b in table)
    secs = "".join(f'<h2>{h}</h2>{c}' for h, c in sections)
    gal = "".join(f'<figure><img src="{I(f)}" alt="{a}" loading="lazy"><figcaption>{a}</figcaption></figure>' for f, a in gallery)
    others = "".join(f'<li><a href="/{s[0]}/">{s[1]}</a></li>' for s in SERVICES if s[0] != slug)
    body = f'''<section class="phero"><div class="wrap phero-in">
<div><nav class="bc" aria-label="Fil d'Ariane"><a href="/">Accueil</a> / <a href="/prestations/">Prestations</a> / <span>{kicker}</span></nav>
<p class="kicker">{kicker} · Rouen</p><h1>{h1}</h1><p class="lead">{direct}</p>
<div class="hero-act"><a class="btn" href="/contact/">Devis gratuit</a><a class="btn btn-ghost" href="tel:{TEL_L}">{TEL}</a></div></div>
<figure class="phero-img"><img src="{I(img)}" alt="{img_alt}" fetchpriority="high"></figure></div></section>
<div class="wrap art"><article class="prose">{secs}
<h2>Batidec en repères</h2><table class="facts">{rows}</table>
<h2>Questions fréquentes</h2>{faq_html(faq)}</article>
<aside class="side"><div class="side-card"><p class="ft-h">Votre devis</p><p>Visite et devis gratuits à Rouen.</p>
<a class="btn btn-block" href="/contact/">Demander un devis</a><a class="btn btn-ghost btn-block" href="tel:{TEL_L}">{TEL}</a>
<p class="small">Lun. au ven., 9 h à 17 h<br>{ADR}</p></div>
<div class="side-card"><p class="ft-h">Autres prestations</p><ul>{others}</ul></div></aside></div>
{"<section class='wrap sec'><div class='sec-hd'><p class='kicker'>En images</p><h2>Réalisations liées</h2></div><div class='gal'>"+gal+"</div><p><a class='link' href='/projets/'>Toutes les réalisations</a></p></section>" if gallery else ""}
{cta_band()}'''
    page(f"/{slug}/", title, desc, body,
         (faq_ld(faq), crumbs([("/", "Accueil"), ("/prestations/", "Prestations"), (f"/{slug}/", kicker)]),
          {"@context": "https://schema.org", "@type": "Service", "name": h1, "serviceType": kicker,
           "provider": {"@id": SITE + "/#entreprise"}, "areaServed": {"@type": "City", "name": "Rouen"}}), img)

REP = [("Adresse", ADR), ("Création", "1972, entreprise familiale"), ("Dirigeant", "Marphour Hassan, depuis 2006"),
       ("Devis", "Gratuit, après visite"), ("Horaires", "Lundi au vendredi, 9 h à 17 h"), ("Téléphone", TEL)]

service_page("peinture-rouen", "Peintre en bâtiment à Rouen, intérieur et extérieur | Batidec",
    "Peinture intérieure et extérieure à Rouen : murs, plafonds, boiseries, locaux pros. Entreprise familiale depuis 1972. Devis gratuit au 02 35 72 20 31.",
    "Peintre en bâtiment à Rouen", "Peinture",
    "Batidec réalise la peinture intérieure et extérieure des logements, des parties communes et des locaux professionnels à Rouen, sur supports neufs comme existants. Préparation des supports, protection du mobilier et finitions soignées sont compris dans chaque chantier.",
    "cuisine.jpg", "Cuisine repeinte par Batidec à Rouen",
    [("Que comprend un chantier de peinture Batidec ?",
      "<p>Un chantier de peinture se joue d'abord dans la préparation. Batidec protège les sols et le mobilier, rebouche, ponce et traite les supports, puis applique les sous-couches et les couches de finition adaptées à chaque pièce.</p><ul><li>Murs et plafonds, pièces de vie et pièces humides</li><li>Boiseries, portes, plinthes, radiateurs</li><li>Cages d'escalier et parties communes</li><li>Bureaux, commerces et locaux professionnels</li></ul>"),
     ("Peinture sur existant ou sur neuf : quelle différence ?",
      "<p>Sur un support existant, il faut d'abord diagnostiquer : fissures, anciennes peintures, humidité. Sur du neuf, la priorité est l'impression du support pour une finition homogène. Batidec intervient dans les deux cas.</p>"),
     ("Combien coûte la peinture d'une pièce à Rouen ?",
      "<p>Le prix dépend de la surface, de l'état des murs et de la finition choisie. Batidec établit un devis gratuit après visite, poste par poste, pour que vous sachiez exactement ce que vous payez.</p>")],
    REP,
    [("Batidec peint-elle aussi les plafonds et les boiseries ?", "Oui, Batidec reprend murs, plafonds, portes, plinthes et boiseries, en intérieur comme en extérieur, à Rouen."),
     ("Faut-il vider la pièce avant le chantier ?", "Non. Le mobilier est regroupé et protégé par l'équipe. Les objets fragiles sont à ranger avant l'intervention."),
     ("Batidec intervient-elle dans les locaux professionnels ?", "Oui, bureaux, commerces et parties communes sont repeints, en organisant le chantier pour limiter la gêne pour votre activité."),
     ("Comment obtenir un devis de peinture ?", "Appelez le 02 35 72 20 31 ou remplissez le formulaire de contact : visite et devis sont gratuits.")],
    [("cuisine.jpg", "Cuisine rénovée, projet de Mme L."), ("salle-de-bain-rotated.jpg", "Salle de bain, projet de Mme L."), ("douche-rotated.jpg", "Douche, projet de Mme L.")])

service_page("ravalement-facade-rouen", "Ravalement de façade à Rouen | Batidec, depuis 1972",
    "Ravalement de façade à Rouen : nettoyage, réparation et peinture de façade pour maisons, immeubles et commerces. Devis gratuit au 02 35 72 20 31.",
    "Ravalement de façade à Rouen", "Façade",
    "Le ravalement de façade consiste à nettoyer, réparer puis protéger ou repeindre les murs extérieurs d'un bâtiment. Batidec réalise le ravalement des maisons, immeubles et devantures de commerces à Rouen, après un diagnostic gratuit de la façade.",
    "120760763_620030982004693_4593063110375373801_n.jpeg", "Façade des locaux Batidec, rue du Mail à Rouen",
    [("Quelles sont les étapes d'un ravalement ?",
      "<ol><li><b>Diagnostic</b> : état des enduits, fissures, salissures, humidité.</li><li><b>Nettoyage</b> du support adapté au matériau.</li><li><b>Réparations</b> : rebouchage des fissures, reprise des enduits.</li><li><b>Protection et peinture</b> avec un produit adapté à la façade.</li></ol>"),
     ("Quand faut-il ravaler sa façade ?",
      "<p>Une façade encrassée, fissurée ou qui laisse passer l'humidité doit être traitée. À Rouen, comme dans d'autres communes, la mairie peut aussi imposer un ravalement périodique : renseignez-vous auprès du service urbanisme avant de lancer les travaux.</p>"),
     ("Et l'isolation ?",
      "<p>Batidec réalise aussi des travaux d'isolation. Décrivez votre projet lors de votre demande de devis : nous vous dirons ce qui est possible sur votre bâtiment. <em>[À confirmer avec Batidec : type d'isolation réalisée]</em></p>")],
    REP,
    [("Batidec fait-elle le ravalement des immeubles ?", "Oui, maisons, immeubles en copropriété et devantures de commerces, à Rouen. Un diagnostic gratuit précède chaque devis."),
     ("Faut-il une autorisation pour ravaler sa façade à Rouen ?", "Un ravalement qui modifie l'aspect extérieur demande en général une déclaration préalable en mairie. Le service urbanisme de Rouen vous indiquera la démarche exacte."),
     ("Combien de temps dure un ravalement ?", "La durée dépend de la surface, de l'état de la façade et de la météo. Elle est précisée dans le devis après visite."),
     ("Comment obtenir un devis de ravalement ?", "Appelez le 02 35 72 20 31 ou utilisez le formulaire : le diagnostic et le devis sont gratuits.")],
    [])

service_page("decoration-interieur-rouen", "Décoration intérieure à Rouen, peintre décorateur | Batidec",
    "Peintre décorateur à Rouen : couleurs, papiers peints, effets décoratifs, rénovation d'intérieurs et de locaux. Entreprise familiale depuis 1972.",
    "Peintre décorateur à Rouen", "Décoration",
    "Un peintre décorateur conçoit et réalise l'ambiance d'un lieu : couleurs, matières, papiers peints et finitions. Batidec accompagne à Rouen les particuliers qui rénovent leur intérieur et les professionnels qui décorent un nouveau local.",
    "dressing-finale-rotated.jpg", "Dressing réalisé par Batidec, projet de Mme L.",
    [("Que peut faire un peintre décorateur pour mon intérieur ?",
      "<p>Batidec vous aide à choisir les teintes, harmonise pièces et volumes, puis réalise les travaux : peinture, pose de papiers peints, effets décoratifs, mise en valeur des boiseries et des rangements sur mesure.</p>"),
     ("Décorer un nouveau lieu ou rénover des locaux ?",
      "<p>Les deux. Pour un nouveau lieu, Batidec part d'une page blanche avec vous. Pour une rénovation, l'équipe garde ce qui fait le caractère du lieu et modernise le reste.</p>")],
    REP,
    [("Batidec aide-t-elle à choisir les couleurs ?", "Oui, le choix des teintes et des matières fait partie de l'accompagnement, avant tout chantier de décoration."),
     ("Batidec pose-t-elle du papier peint ?", "Oui, la pose de papiers peints fait partie des travaux de décoration réalisés par Batidec à Rouen."),
     ("Puis-je voir des réalisations ?", "Oui, la page Réalisations présente des intérieurs et des commerces décorés par Batidec à Rouen.")],
    [("dressing-finale-rotated.jpg", "Dressing, projet de Mme L."), ("dressing.jpg", "Rangements sur mesure, projet de Mme L."), ("etage-7.jpg", "Salon de thé Dame Cakes")])

service_page("agencement-commerce-rouen", "Agencement de bar, restaurant et boutique à Rouen | Batidec",
    "Agencement et décoration de commerces à Rouen : bars, brasseries, salons de thé, boutiques. Références : Le Central, JM's Café, Dame Cakes.",
    "Agencement de commerces à Rouen", "Agencement",
    "L'agencement d'un commerce, c'est l'organisation et la décoration de l'espace pour accueillir les clients et faciliter le travail. Batidec aménage à Rouen bars, brasseries, salons de thé et boutiques, de la conception à la peinture finale.",
    "salle-2-rotated.jpg", "Brasserie Le Central à Rouen, agencée par Batidec",
    [("Quels commerces Batidec a-t-elle aménagés à Rouen ?",
      "<ul><li><b>Brasserie Le Central</b> : aménagement et décoration</li><li><b>Bar JM's Café</b>, Rouen</li><li><b>Salon de thé Dame Cakes</b></li><li><b>Le Lanchon Opticiens</b></li></ul>"),
     ("Pourquoi confier l'agencement et la peinture à la même entreprise ?",
      "<p>Un seul interlocuteur coordonne le chantier : moins de délais entre corps de métier, une décoration pensée avec l'agencement, et un responsable unique du résultat avant votre ouverture.</p>"),
     ("Aménager une entreprise ou une maison",
      "<p>Batidec apporte aussi son regard professionnel aux bureaux et aux maisons : circulation, rangements, ambiance et finitions.</p>")],
    REP,
    [("Batidec peut-elle travailler en dehors des heures d'ouverture ?", "Le planning est défini avec vous lors du devis pour limiter l'impact sur votre activité."),
     ("Batidec aménage-t-elle les bars et restaurants ?", "Oui, Batidec a notamment aménagé et décoré la brasserie Le Central et le bar JM's Café à Rouen."),
     ("Comment se déroule un projet d'agencement ?", "Visite du local, échange sur vos besoins et votre image, devis détaillé gratuit, puis réalisation jusqu'aux finitions."),
     ("Comment contacter Batidec pour un commerce ?", "Appelez le 02 35 72 20 31 du lundi au vendredi, de 9 h à 17 h, ou écrivez via le formulaire.")],
    [("salle-2-rotated.jpg", "Brasserie Le Central"), ("rdc.jpg", "Bar JM's Café, Rouen"), ("etage-7.jpg", "Salon de thé Dame Cakes"),
     ("120807361_620035005337624_8398906530529115205_n.jpeg", "Le Lanchon Opticiens")])

# ---------- PRESTATIONS (hub, ancienne URL conservée) ----------
hub = "".join(f'''<a class="row" href="/{s[0]}/"><span class="svc-n">N°0{i+1}</span><span class="row-t">{s[1]}</span><span class="row-d">{s[3]}</span><span class="row-a">→</span></a>''' for i, s in enumerate(SERVICES))
page("/prestations/", "Prestations : peinture, façade, déco, agencement | Batidec",
     "Les prestations de Batidec à Rouen : peinture intérieure et extérieure, ravalement de façade, décoration intérieure et agencement de commerces.",
     f'''<section class="phero slim"><div class="wrap"><nav class="bc"><a href="/">Accueil</a> / <span>Prestations</span></nav><p class="kicker">Savoir-faire</p><h1>Nos prestations à Rouen</h1>
<p class="lead">Batidec met son savoir-faire en rénovation et en agencement au service des particuliers et des professionnels rouennais : un atelier, quatre métiers complémentaires.</p></div></section>
<section class="wrap sec"><div class="rows">{hub}</div></section>{cta_band()}''',
     (crumbs([("/", "Accueil"), ("/prestations/", "Prestations")]),))

# ---------- PROJETS (ancienne URL conservée) ----------
PROJ = [
    ("Brasserie Le Central", "Aménagement et décoration d'un bar-brasserie.", ["salle-2-rotated.jpg", "salle-rotated.jpg", "salle-1-rotated.jpg"]),
    ("Projet de Mme L.", "Rénovation d'un intérieur : cuisine, salle de bain, dressing.", ["cuisine.jpg", "dressing-finale-rotated.jpg", "salle-de-bain-rotated.jpg", "douche-rotated.jpg", "dressing-2-rotated.jpg"]),
    ("Bar JM's Café, Rouen", "Agencement et décoration d'un bar rouennais.", ["rdc.jpg", "rdc-1.jpg", "rdc3.jpg"]),
    ("Salon de thé Dame Cakes", "Décoration et aménagement d'un salon de thé.", ["etage-7.jpg", "enseigne.jpg", "etage-8.jpg"]),
    ("Le Lanchon Opticiens", "Agencement d'une boutique d'optique.", ["120807361_620035005337624_8398906530529115205_n.jpeg"]),
]
pj = ""
for n, d, fs in PROJ:
    imgs = "".join(f'<img src="{I(f)}" alt="{n}, réalisation Batidec" loading="lazy">' for f in fs)
    pj += f'<article class="proj"><div class="proj-imgs n{min(len(fs),3)}">{imgs}</div><div class="proj-t"><h2>{n}</h2><p>{d}</p></div></article>'
page("/projets/", "Réalisations peinture et agencement à Rouen | Batidec",
     "Les réalisations de Batidec à Rouen : brasserie Le Central, bar JM's Café, salon de thé Dame Cakes, Le Lanchon Opticiens, intérieurs de particuliers.",
     f'''<section class="phero slim"><div class="wrap"><nav class="bc"><a href="/">Accueil</a> / <span>Réalisations</span></nav><p class="kicker">Portfolio</p><h1>Nos réalisations à Rouen</h1>
<p class="lead">Commerces et intérieurs de particuliers : quelques chantiers menés par Batidec. Photos réelles de nos chantiers.</p></div></section>
<section class="wrap sec projs">{pj}</section>{cta_band()}''',
     (crumbs([("/", "Accueil"), ("/projets/", "Réalisations")]),), "salle-2-rotated.jpg")

# ---------- A PROPOS ----------
page("/a-propos/", "L'atelier Batidec, entreprise familiale à Rouen depuis 1972",
     "Batidec, créée en 1972 par Hamyne Abdou et dirigée depuis 2006 par Marphour Hassan : une entreprise familiale de peinture et décoration à Rouen.",
     f'''<section class="phero"><div class="wrap phero-in"><div><nav class="bc"><a href="/">Accueil</a> / <span>L'atelier</span></nav><p class="kicker">Depuis 1972</p>
<h1>Une entreprise familiale rouennaise</h1><p class="lead">{CANON}</p></div>
<figure class="phero-img"><img src="{I('120760763_620030982004693_4593063110375373801_n.jpeg')}" alt="Locaux Batidec, 32 rue du Mail à Rouen"></figure></div></section>
<div class="wrap art"><article class="prose">
<h2>Qui a fondé Batidec ?</h2><p>Hamyne Abdou crée Batidec en 1972. Pendant plus de quarante ans, il met son savoir-faire au service des particuliers et des commerçants de Rouen.</p>
<h2>Qui dirige Batidec aujourd'hui ?</h2><p>Marphour Hassan, formé à la peinture, à la décoration et à l'aménagement aux côtés d'Hamyne Abdou, reprend l'entreprise familiale en 2006. Il dirige aujourd'hui Batidec avec une équipe attentive aux détails.</p>
<h2>Qui répond à votre demande ?</h2><p>Magali, chargée d'affaires, reçoit les demandes de devis et organise la visite de votre projet.</p>
<h2>Notre engagement</h2><ul class="ticks"><li>Un travail de qualité, des finitions haut de gamme</li><li>Un interlocuteur unique du devis à la fin du chantier</li><li>Des chantiers propres et protégés</li></ul>
<table class="facts"><tr><th>Création</th><td>1972</td></tr><tr><th>Fondateur</th><td>Hamyne Abdou</td></tr><tr><th>Dirigeant</th><td>Marphour Hassan, depuis 2006</td></tr><tr><th>Adresse</th><td>{ADR}</td></tr><tr><th>SIRET</th><td>344 914 015 00039</td></tr></table>
</article><aside class="side"><div class="side-card"><p class="ft-h">Nous rencontrer</p><p>{ADR}<br>Lun. au ven., 9 h à 17 h</p><a class="btn btn-block" href="/contact/">Demander un devis</a><a class="btn btn-ghost btn-block" href="tel:{TEL_L}">{TEL}</a></div></aside></div>{cta_band()}''',
     (crumbs([("/", "Accueil"), ("/a-propos/", "L'atelier")]),), "120760763_620030982004693_4593063110375373801_n.jpeg")

# ---------- CONTACT ----------
page("/contact/", "Devis peinture et agencement à Rouen | Contact Batidec",
     "Demandez votre devis gratuit à Batidec, 32 rue du Mail à Rouen : 02 35 72 20 31, du lundi au vendredi de 9 h à 17 h.",
     f'''<section class="phero slim"><div class="wrap"><nav class="bc"><a href="/">Accueil</a> / <span>Contact</span></nav><p class="kicker">Devis gratuit</p><h1>Contacter Batidec à Rouen</h1>
<p class="lead">Décrivez votre projet : Magali, chargée d'affaires, vous recontacte pour organiser la visite. Le devis est gratuit et sans engagement.</p></div></section>
<div class="wrap art"><form class="form" id="devis" novalidate>
<div class="f2"><label>Nom<input name="nom" required autocomplete="name"></label><label>Téléphone<input name="tel" type="tel" required autocomplete="tel"></label></div>
<label>E-mail<input name="email" type="email" autocomplete="email"></label>
<label>Votre projet<select name="type"><option>Peinture intérieure ou extérieure</option><option>Ravalement de façade</option><option>Décoration intérieure</option><option>Agencement de commerce</option><option>Autre</option></select></label>
<label>Détails (surface, adresse, délai souhaité)<textarea name="msg" rows="5" required></textarea></label>
<input class="hp" name="site" tabindex="-1" autocomplete="off" aria-hidden="true">
<button class="btn" type="submit">Envoyer ma demande</button>
<p class="small" id="fmsg">Votre messagerie s'ouvre avec la demande pré-remplie, adressée à {MAIL}. Vous pouvez aussi appeler le <a href="tel:{TEL_L}">{TEL}</a>.</p></form>
<aside class="side"><div class="side-card"><p class="ft-h">Coordonnées</p><address>Batidec<br>{ADR}<br><a href="tel:{TEL_L}">{TEL}</a><br><a href="mailto:{MAIL}">{MAIL}</a></address>
<p>Lundi au vendredi<br>9 h 00 à 17 h 00</p><a class="link" href="{MAPS}" rel="noopener">Itinéraire Google Maps</a></div></aside></div>''',
     (crumbs([("/", "Accueil"), ("/contact/", "Contact")]),))

page("/mentions-legales/", "Mentions légales | Batidec, peintre décorateur à Rouen",
     "Mentions légales du site de Batidec, entreprise de peinture, décoration et agencement à Rouen.",
     f'''<section class="phero slim"><div class="wrap"><h1>Mentions légales</h1></div></section><div class="wrap prose sec">
<p><b>Éditeur</b> : Batidec, {ADR}. SIRET 344 914 015 00039. Téléphone {TEL}. E-mail {MAIL}. Directeur de la publication : Marphour Hassan.</p>
<p><b>Hébergement</b> : Cloudflare, Inc., 101 Townsend St, San Francisco, CA 94107, États-Unis.</p>
<p><b>Données personnelles</b> : les informations envoyées via le formulaire servent uniquement à répondre à votre demande de devis.</p></div>''')

# ---------- fichiers techniques ----------
(OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
(OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    + "".join(f"<url><loc>{SITE}{p}</loc><lastmod>2026-11-18</lastmod></url>" for p in PAGES) + "</urlset>\n")
(OUT / "llms.txt").write_text(f"# Batidec\n\n> {CANON}\n\n- Adresse : {ADR}\n- Téléphone : {TEL}\n- Horaires : lundi au vendredi, 9 h à 17 h\n- Création : 1972 (Hamyne Abdou) ; dirigeant depuis 2006 : Marphour Hassan\n\n## Pages\n"
    + "".join(f"- [{p}]({SITE}{p})\n" for p in PAGES))
(OUT / "_redirects").write_text("/project/* /projets/ 301\n/projets /projets/ 301\n")
print("ok", len(PAGES), "pages")
