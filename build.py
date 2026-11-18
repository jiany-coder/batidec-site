#!/usr/bin/env python3
# Generateur statique du site Batidec (refonte Next Business) - v2
import json, pathlib, shutil

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "dist"
SITE = "https://batidec76.com"
WP = "https://www.batidec76.com/wp-content/uploads/2022/01/"
TEL = "02 35 72 20 31"
TEL_L = "+33235722031"
MAIL = "batidec-rouen@batidec76.com"
ADR = "32 rue du Mail, 76100 Rouen"
MAPS = "https://maps.google.com/?cid=%d" % int("0x1208210244d39bf5", 16)
FB = "https://www.facebook.com/batidecrouen"
DATE = "18 novembre 2026"
XP = 2026 - 1972
CANON = ("Batidec est une entreprise familiale de peinture, décoration, rénovation et agencement "
         "installée rue du Mail à Rouen depuis 1972, certifiée RGE et assurée en garantie décennale, "
         "pour les particuliers et les commerces.")
AVIS = [("H G (Famille D)", "il y a 11 mois", "Nous leur avons confié l'entier rez-de-chaussée de notre maison (enduit, ponçage, peinture, murs et plafonds, ragréage sol, pose...). Un travail très pro et très soigné de A à Z."),
        ("Alain M", "il y a 2 ans", "Immense merci à M. Hassan, qui nous a sauvé quand un autre artisan nous a lâché. En moins d'une semaine le carrelage de notre cuisine était posé. Du travail de super qualité, impeccable."),
        ("Ilan Israel", "octobre 2026", "Merci Mr Hassan pour votre professionnalisme. Je suis très satisfait du travail effectué sur les vitrines de mon magasin.")]
ICO = {"shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>', "leaf": '<path d="M5 19c0-9 6-14 15-14 0 9-5 15-14 15"/><path d="M5 19l8-8"/>', "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>', "star": '<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/>', "doc": '<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5M10 13h6M10 17h6"/>', "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21c1-4 4-6 8-6s7 2 8 6"/>', "brush": '<path d="M4 20c3 0 5-2 5-5l9-9 2 2-9 9c-3 0-5 2-7 3z"/>'}
def ico(k):
    return f'<svg class="ico" viewBox="0 0 24 24" aria-hidden="true">{ICO[k]}</svg>'
TRUST = [("clock", f"{XP} ans d'expérience", "Depuis 1972 à Rouen"), ("shield", "Garantie décennale", "Travaux assurés 10 ans"), ("leaf", "Entreprise RGE", "Éligible aux aides isolation"), ("star", "4,7/5 sur Google", "25 avis clients"), ("doc", "Devis gratuit", "Détaillé, sans engagement")]
def trust(cls=""):
    return f'<div class="trust {cls}"><div class="wrap trust-in">' + "".join(f'<div class="tr">{ico(i)}<span><b>{a}</b><small>{b}</small></span></div>' for i, a, b in TRUST) + "</div></div>"
def avis_html(items=None):
    items = items or AVIS
    return '<div class="avis">' + "".join(f'<figure class="av"><div class="stars" aria-label="5 étoiles sur 5">★★★★★</div><blockquote>« {t} »</blockquote><figcaption><b>{n}</b> · avis Google · {d}</figcaption></figure>' for n, d, t in items) + "</div>"


def W(f):  # photo reelle Batidec
    return WP + f

def U(i, w=1400):  # photo d'illustration (Unsplash)
    return f"https://images.unsplash.com/{i}?w={w}&q=72&auto=format&fit=crop"

ST = {  # photos d'illustration
    "hero": "photo-1725034474154-b4108c93bd3b", "peinture": "photo-1652829069834-2c05031199c5",
    "facade": "photo-1626471671222-9d89fe4c2668", "deco": "photo-1644331916380-99ba981d9ca0",
    "sol": "photo-1761053130711-2515ef532bb5", "carrelage": "photo-1523413307857-ef24c53571ae",
    "beton": "photo-1642755623141-23b3cb4284aa", "platre": "photo-1694521787149-ee0b6a3d9f78",
    "isolation": "photo-1607400201889-565b1ee75f8e", "renov": "photo-1600210491369-e753d80a41f3",
    "sdb": "photo-1638799869566-b17fa794c4de", "cuisine": "photo-1602028915047-37269d1a73f7",
    "verriere": "photo-1497366754035-f200968a6e72", "dressing": "photo-1672137233327-37b0c1049e77",
    "nuancier": "photo-1622250544703-997d69d856e3", "salon": "photo-1785441513748-8ef7034a4424",
}

# ---------------- prestations ----------------
# slug, nom court, titre H1, univers, image (("u",cle)|("w",fichier)), resume
S = {}
def svc(slug, name, h1, uni, img, short, title, desc, direct, secs, faq, gal=()):
    S[slug] = dict(slug=slug, name=name, h1=h1, uni=uni, img=img, short=short, title=title,
                   desc=desc, direct=direct, secs=secs, faq=faq, gal=gal)

svc("peinture-rouen", "Peinture intérieure et extérieure", "Peintre en bâtiment à Rouen", "Peinture & façade",
    ("u", "peinture"), "Murs, plafonds, boiseries, cages d'escalier, locaux pros.",
    "Peintre en bâtiment à Rouen, intérieur et extérieur | Batidec",
    "Peinture intérieure et extérieure à Rouen : murs, plafonds, boiseries, parties communes, locaux pros. Entreprise familiale depuis 1972. Devis gratuit.",
    "Batidec réalise la peinture intérieure et extérieure des logements, des parties communes et des locaux professionnels à Rouen, sur supports neufs comme existants. Protection, préparation des supports et finitions soignées sont compris dans chaque chantier.",
    [("Que comprend un chantier de peinture Batidec ?", "<p>Un beau résultat se joue dans la préparation : protection des sols et du mobilier, rebouchage, ponçage, sous-couche adaptée, puis deux couches de finition.</p><ul><li>Murs et plafonds, pièces de vie et pièces humides</li><li>Boiseries, portes, plinthes, radiateurs</li><li>Cages d'escalier et parties communes</li><li>Bureaux, commerces et locaux professionnels</li></ul>"),
     ("Peinture sur existant ou sur neuf : quelle différence ?", "<p>Sur l'existant, on diagnostique d'abord (fissures, anciennes peintures, humidité). Sur le neuf, l'impression du support garantit une finition homogène. Batidec intervient dans les deux cas.</p>"),
     ("Combien coûte la peinture d'une pièce à Rouen ?", "<p>Le prix dépend de la surface, de l'état des murs et de la finition. Batidec établit un devis gratuit après visite, poste par poste.</p>")],
    [("Batidec peint-elle aussi les plafonds et les boiseries ?", "Oui, murs, plafonds, portes, plinthes et boiseries, en intérieur comme en extérieur, à Rouen."),
     ("Faut-il vider la pièce avant le chantier ?", "Non. Le mobilier est regroupé et protégé par l'équipe ; rangez seulement les objets fragiles."),
     ("Batidec intervient-elle dans les locaux professionnels ?", "Oui : bureaux, commerces et parties communes, avec un planning qui limite la gêne pour votre activité.")],
    [("cuisine.jpg", "Cuisine repeinte, projet de Mme L."), ("salle-de-bain-rotated.jpg", "Salle de bain, projet de Mme L.")])

svc("ravalement-facade-rouen", "Ravalement de façade", "Ravalement de façade à Rouen", "Peinture & façade",
    ("u", "facade"), "Nettoyage, réparation et peinture des façades.",
    "Ravalement de façade à Rouen : maisons et immeubles | Batidec",
    "Ravalement de façade à Rouen : diagnostic, nettoyage, réparation des fissures et peinture de façade pour maisons, immeubles et commerces. Devis gratuit.",
    "Le ravalement de façade consiste à nettoyer, réparer puis protéger ou repeindre les murs extérieurs d'un bâtiment. Batidec réalise le ravalement des maisons, immeubles et devantures à Rouen, après un diagnostic gratuit.",
    [("Quelles sont les étapes d'un ravalement ?", "<ol><li><b>Diagnostic</b> : enduits, fissures, salissures, humidité.</li><li><b>Nettoyage</b> adapté au matériau.</li><li><b>Réparations</b> : fissures, reprises d'enduit.</li><li><b>Protection et peinture</b> de façade.</li></ol>"),
     ("Quand faut-il ravaler sa façade ?", "<p>Une façade encrassée, fissurée ou qui laisse passer l'humidité doit être traitée. La mairie peut aussi imposer un ravalement : renseignez-vous auprès du service urbanisme de Rouen.</p>")],
    [("Batidec fait-elle le ravalement des immeubles ?", "Oui : maisons, immeubles en copropriété et devantures de commerces à Rouen, avec diagnostic gratuit."),
     ("Faut-il une autorisation pour ravaler sa façade à Rouen ?", "Un ravalement qui modifie l'aspect extérieur demande en général une déclaration préalable en mairie."),
     ("Combien de temps dure un ravalement ?", "Selon la surface, l'état de la façade et la météo : la durée est précisée dans le devis.")])

svc("decoration-interieur-rouen", "Décoration et revêtements muraux", "Peintre décorateur à Rouen", "Décoration & revêtements",
    ("u", "deco"), "Couleurs, papiers peints, toile de verre, effets décoratifs.",
    "Peintre décorateur à Rouen, papier peint | Batidec",
    "Peintre décorateur à Rouen : conseil couleurs, pose de papier peint, toile de verre, revêtements muraux et effets décoratifs. Entreprise familiale depuis 1972.",
    "Un peintre décorateur conçoit et réalise l'ambiance d'un lieu : couleurs, matières et revêtements muraux. Batidec accompagne à Rouen les particuliers qui rénovent leur intérieur et les professionnels qui décorent un nouveau local.",
    [("Quels revêtements muraux pose Batidec ?", "<ul><li>Papiers peints et panoramiques</li><li>Toile de verre à peindre</li><li>Revêtements muraux décoratifs</li><li>Effets décoratifs et peintures à effet</li></ul>"),
     ("Batidec aide-t-elle à choisir les couleurs ?", "<p>Oui. Le conseil couleurs et matières fait partie de l'accompagnement : teintes, harmonies entre pièces, mise en valeur des volumes et des boiseries.</p>")],
    [("Batidec pose-t-elle du papier peint à Rouen ?", "Oui, papiers peints, panoramiques et toile de verre font partie des travaux de décoration de Batidec."),
     ("Toile de verre ou peinture directe ?", "La toile de verre masque les petites fissures et renforce le mur avant peinture ; Batidec vous conseille selon l'état du support."),
     ("Puis-je voir des réalisations ?", "Oui, la page Réalisations présente des intérieurs et des commerces décorés par Batidec.")],
    [("dressing-finale-rotated.jpg", "Dressing, projet de Mme L."), ("etage-7.jpg", "Salon de thé Dame Cakes")])

svc("revetement-sol-rouen", "Revêtements de sols et parquet", "Pose de parquet et revêtements de sols à Rouen", "Décoration & revêtements",
    ("u", "sol"), "Parquet, moquette, sols PVC et sols souples.",
    "Pose de parquet, moquette et sols PVC à Rouen | Batidec",
    "Pose de revêtements de sols à Rouen : parquet, moquette, lames PVC, sols souples. Préparation du support et finitions. Devis gratuit au 02 35 72 20 31.",
    "La pose d'un revêtement de sol comprend la préparation du support (ragréage si besoin), la pose et les finitions (plinthes, seuils). Batidec pose à Rouen parquet, moquette, lames PVC et sols souples, chez les particuliers comme dans les commerces.",
    [("Quels sols Batidec pose-t-elle ?", "<table class='facts'><tr><th>Parquet</th><td>Massif, contrecollé, stratifié ; pose collée ou flottante</td></tr><tr><th>Moquette</th><td>Chambres, bureaux, hôtels</td></tr><tr><th>Lames PVC</th><td>Pièces humides, commerces, rénovation rapide</td></tr><tr><th>Sols souples</th><td>Lino et vinyle en rouleau</td></tr></table>"),
     ("Pourquoi préparer le support avant la pose ?", "<p>Un sol neuf reproduit les défauts du support. Ragréage, nivellement et sous-couche garantissent un rendu plan et durable.</p>")],
    [("Batidec pose-t-elle du parquet à Rouen ?", "Oui, parquet massif, contrecollé ou stratifié, en pose collée ou flottante."),
     ("Quel sol pour une salle de bain ?", "Les lames PVC et sols souples résistent à l'eau ; le carrelage reste une valeur sûre. Batidec vous conseille lors de la visite."),
     ("Peut-on poser un sol sur l'ancien carrelage ?", "Souvent oui, après vérification de la planéité et de l'adhérence de l'ancien revêtement.")])

svc("carrelage-faience-rouen", "Carrelage et faïence", "Carreleur à Rouen : carrelage et faïence", "Décoration & revêtements",
    ("u", "carrelage"), "Sols et murs, grands formats, crédences.",
    "Carreleur à Rouen : pose de carrelage et faïence | Batidec",
    "Pose de carrelage et faïence à Rouen : sols, murs, salles de bain, cuisines, crédences, grands formats. Entreprise familiale depuis 1972. Devis gratuit.",
    "Batidec pose le carrelage au sol et la faïence murale à Rouen : salles de bain, cuisines, crédences, entrées et commerces. Chaque pose commence par un support sain et plan, gage d'un carrelage durable.",
    [("Où poser du carrelage ou de la faïence ?", "<ul><li>Sols de pièces de vie et d'entrées</li><li>Murs de douche et de salle de bain</li><li>Crédences de cuisine</li><li>Sols de commerces et de restaurants</li></ul>"),
     ("Petits ou grands carreaux ?", "<p>Les grands formats agrandissent visuellement l'espace et limitent les joints ; ils demandent un support parfaitement plan. Batidec vous conseille selon la pièce.</p>")],
    [("Batidec est-elle carreleur à Rouen ?", "Oui, Batidec pose carrelage et faïence à Rouen, en neuf comme en rénovation."),
     ("Faut-il retirer l'ancien carrelage ?", "Pas toujours : selon son état, on peut poser par-dessus ou déposer pour repartir sur un support sain."),
     ("Batidec pose-t-elle les crédences de cuisine ?", "Oui, en faïence ou en carrelage, en lien avec la rénovation de cuisine.")],
    [("douche-rotated.jpg", "Douche, projet de Mme L.")])

svc("beton-cire-rouen", "Béton ciré", "Béton ciré à Rouen", "Décoration & revêtements",
    ("u", "beton"), "Sols, murs, douches et plans de travail.",
    "Béton ciré à Rouen : sols, murs, douches | Batidec",
    "Application de béton ciré à Rouen : sols, murs, salles de bain, douches à l'italienne, plans de travail. Rendu minéral sans joints. Devis gratuit.",
    "Le béton ciré est un enduit décoratif à base de ciment, appliqué en fine couche puis protégé par un vernis, qui donne un rendu minéral sans joints. Batidec l'applique à Rouen sur sols, murs, douches et plans de travail.",
    [("Où appliquer du béton ciré ?", "<ul><li>Sols de pièces de vie</li><li>Murs et douches à l'italienne</li><li>Plans de travail et crédences</li><li>Commerces, bars et restaurants</li></ul>"),
     ("Le béton ciré est-il résistant ?", "<p>Bien appliqué sur un support sain et protégé par un vernis adapté, il résiste à l'eau et au passage. L'entretien se fait au savon doux.</p>")],
    [("Peut-on mettre du béton ciré dans une douche ?", "Oui, avec un support étanche et une protection adaptée aux pièces humides."),
     ("Peut-on appliquer du béton ciré sur du carrelage ?", "Oui, après préparation du carrelage existant (dégraissage, primaire d'accroche)."),
     ("Quelles couleurs sont possibles ?", "Le béton ciré se teinte : gris, beige, blanc, terre, selon votre décoration.")])

svc("platrerie-cloisons-rouen", "Plâtrerie et cloisons", "Plaquiste à Rouen : plâtrerie, cloisons, faux plafonds", "Rénovation",
    ("u", "platre"), "Plaques de plâtre, cloisons, faux plafonds, enduits.",
    "Plaquiste à Rouen : cloisons, faux plafonds, enduits | Batidec",
    "Plâtrerie à Rouen : cloisons en plaques de plâtre, faux plafonds, doublages, bandes et enduits. Création ou suppression de cloisons. Devis gratuit.",
    "La plâtrerie regroupe la pose de plaques de plâtre (cloisons, doublages, faux plafonds) et les enduits qui préparent les murs à la peinture. Batidec crée, modifie ou supprime des cloisons à Rouen, en respectant les murs porteurs.",
    [("Quels travaux de plâtrerie réalise Batidec ?", "<ul><li>Création et suppression de cloisons</li><li>Doublages de murs</li><li>Faux plafonds et caissons</li><li>Bandes, enduits et lissage avant peinture</li></ul>"),
     ("Pourquoi confier plâtrerie et peinture à la même entreprise ?", "<p>Un seul interlocuteur enchaîne cloisons, enduits et peinture : pas d'attente entre corps de métier et des finitions parfaitement lisses.</p>")],
    [("Batidec peut-elle abattre une cloison ?", "Oui, après vérification qu'il ne s'agit pas d'un mur porteur."),
     ("Combien de temps pour une cloison en plaques de plâtre ?", "Quelques jours en général, bandes et enduits compris ; le délai exact figure au devis."),
     ("Batidec pose-t-elle des faux plafonds ?", "Oui, faux plafonds et caissons en plaques de plâtre.")])

svc("isolation-rouen", "Isolation", "Isolation intérieure à Rouen", "Rénovation",
    ("u", "isolation"), "Doublages isolants, plafonds, cloisons. Entreprise RGE.",
    "Isolation intérieure à Rouen : murs et cloisons | Batidec",
    "Travaux d'isolation à Rouen : doublages isolants des murs, isolation des cloisons et des plafonds, en lien avec la plâtrerie et la peinture. Devis gratuit.",
    "Isoler un logement par l'intérieur consiste à poser un isolant contre les murs ou sous les plafonds, puis à le recouvrir de plaques de plâtre prêtes à peindre. Batidec réalise ces travaux à Rouen, de l'isolant jusqu'à la peinture finale.",
    [("Quels travaux d'isolation réalise Batidec ?", "<ul><li>Doublages isolants des murs</li><li>Isolation sous plafonds et rampants</li><li>Isolation phonique des cloisons</li></ul>"),
     ("Batidec est-elle RGE pour l'isolation ?", "<p>Oui. Batidec est une entreprise <b>RGE</b> (Reconnu Garant de l'Environnement). Cette qualification est exigée pour que vos travaux d'isolation puissent ouvrir droit à certaines aides publiques (MaPrimeRénov', primes CEE), selon vos revenus et les travaux. Vérifiez votre éligibilité sur <a href='https://france-renov.gouv.fr' rel='noopener'>france-renov.gouv.fr</a>.</p>"),
     ("Pourquoi isoler en même temps que la rénovation ?", "<p>Profiter d'une rénovation pour isoler évite de refaire deux fois les murs : l'isolation, la plâtrerie et la peinture s'enchaînent sur un même chantier.</p>")],
    [("Batidec isole-t-elle les murs par l'intérieur ?", "Oui, par doublage isolant recouvert de plaques de plâtre, puis peinture."),
     ("L'isolation phonique est-elle possible ?", "Oui, entre deux pièces ou deux logements, avec des cloisons et isolants adaptés."),
     ("Existe-t-il des aides pour isoler avec Batidec ?", "Batidec étant RGE, certains travaux d'isolation peuvent ouvrir droit à MaPrimeRénov' ou aux primes CEE, selon conditions ; vérifiez sur france-renov.gouv.fr.")])

svc("renovation-interieure-rouen", "Rénovation intérieure clé en main", "Rénovation d'appartement et de maison à Rouen", "Rénovation",
    ("u", "renov"), "Appartements et maisons, un seul interlocuteur.",
    "Rénovation d'appartement et maison à Rouen | Batidec",
    "Rénovation intérieure clé en main à Rouen : appartements, maisons, locaux. Plâtrerie, sols, peinture, cuisine, salle de bain, un seul interlocuteur.",
    "Une rénovation clé en main confie l'ensemble des travaux intérieurs à une seule entreprise, qui coordonne chaque étape jusqu'à la livraison. Batidec rénove à Rouen appartements, maisons et locaux : cloisons, sols, peinture, cuisine et salle de bain.",
    [("Que comprend une rénovation clé en main ?", "<ol><li>Visite, relevés et conseils d'aménagement</li><li>Devis détaillé par lot</li><li>Plâtrerie, isolation, réseaux si besoin</li><li>Sols, carrelage, menuiserie</li><li>Peinture et finitions, nettoyage</li></ol>"),
     ("Pourquoi un seul interlocuteur ?", "<p>Un responsable unique tient le planning et la qualité de bout en bout : moins de délais, moins de surprises, un résultat cohérent.</p>")],
    [("Batidec rénove-t-elle les appartements anciens de Rouen ?", "Oui, appartements anciens comme récents, en respectant le caractère des lieux (moulures, parquets, boiseries)."),
     ("Peut-on rester dans le logement pendant les travaux ?", "Selon l'ampleur du chantier, le planning peut être organisé pièce par pièce."),
     ("Combien coûte une rénovation complète ?", "Tout dépend de la surface et des lots ; le devis gratuit détaille chaque poste.")],
    [("cuisine.jpg", "Cuisine, projet de Mme L."), ("dressing-2-rotated.jpg", "Rangements, projet de Mme L.")])

svc("renovation-salle-de-bain-rouen", "Rénovation de salle de bain", "Rénovation de salle de bain à Rouen", "Rénovation",
    ("u", "sdb"), "Douche à l'italienne, faïence, meubles, peinture.",
    "Rénovation de salle de bain à Rouen, clé en main | Batidec",
    "Rénovation de salle de bain à Rouen : douche à l'italienne, faïence, carrelage, meubles, raccords de plomberie et peinture. Devis gratuit au 02 35 72 20 31.",
    "Rénover une salle de bain, c'est déposer l'existant puis refaire plomberie, étanchéité, revêtements et finitions. Batidec rénove les salles de bain à Rouen, du remplacement de la baignoire par une douche à l'italienne jusqu'à la peinture.",
    [("Que comprend la rénovation d'une salle de bain ?", "<ul><li>Dépose de l'ancienne salle de bain</li><li>Raccords de plomberie et étanchéité</li><li>Douche à l'italienne ou baignoire</li><li>Faïence, carrelage ou béton ciré</li><li>Meubles vasque, miroirs, peinture</li></ul>"),
     ("Baignoire ou douche à l'italienne ?", "<p>La douche à l'italienne gagne de la place et facilite l'accès ; la baignoire reste appréciée en famille. Batidec vous conseille selon la pièce.</p>")],
    [("Batidec remplace-t-elle une baignoire par une douche ?", "Oui, c'est l'une des demandes les plus fréquentes, étanchéité comprise."),
     ("Combien de temps dure la rénovation d'une salle de bain ?", "En général une à trois semaines selon la taille et les travaux ; le délai figure au devis."),
     ("Batidec s'occupe-t-elle de la plomberie ?", "Oui, les raccords de plomberie nécessaires à la rénovation sont inclus.")],
    [("salle-de-bain-rotated.jpg", "Salle de bain, projet de Mme L."), ("douche-rotated.jpg", "Douche, projet de Mme L.")])

svc("renovation-cuisine-rouen", "Rénovation de cuisine", "Rénovation de cuisine à Rouen", "Rénovation",
    ("w", "cuisine.jpg"), "Pose de meubles, crédence, sols et peinture.",
    "Rénovation de cuisine à Rouen, pose et crédence | Batidec",
    "Rénovation de cuisine à Rouen : pose de meubles, crédence, carrelage, sols, raccords et peinture. Exemple réel : la cuisine de Mme L. Devis gratuit.",
    "La rénovation d'une cuisine combine dépose, raccords, pose des meubles, crédence, sol et peinture. Batidec rénove les cuisines à Rouen, comme la cuisine de Mme L. présentée ci-dessous, avec un seul interlocuteur du début à la fin.",
    [("Que comprend la rénovation d'une cuisine ?", "<ul><li>Dépose de l'ancienne cuisine</li><li>Raccords d'eau et préparation des murs</li><li>Pose des meubles et du plan de travail</li><li>Crédence en faïence, verre ou béton ciré</li><li>Sol et peinture</li></ul>"),
     ("Peut-on rénover sans tout changer ?", "<p>Oui : peinture des façades de meubles, nouvelle crédence et nouveau sol transforment une cuisine à moindre coût.</p>")],
    [("Batidec pose-t-elle les cuisines achetées en magasin ?", "Oui, Batidec peut poser une cuisine achetée par vos soins et réaliser tous les travaux autour."),
     ("Combien de temps dure une rénovation de cuisine ?", "En général une à deux semaines ; le délai exact figure au devis."),
     ("Batidec refait-elle aussi le sol ?", "Oui : carrelage, parquet, PVC ou béton ciré.")],
    [("cuisine.jpg", "Cuisine, projet de Mme L.")])

svc("menuiserie-dressing-verriere-rouen", "Menuiserie, dressings et verrières", "Dressings, placards et verrières sur mesure à Rouen", "Agencement & menuiserie",
    ("w", "dressing-finale-rotated.jpg"), "Placards, dressings, verrières, portes.",
    "Dressing, placard et verrière sur mesure à Rouen | Batidec",
    "Menuiserie intérieure à Rouen : dressings et placards sur mesure, verrières d'atelier, portes intérieures. Exemple réel : le dressing de Mme L.",
    "La menuiserie intérieure sur mesure adapte rangements et séparations à votre espace : dressings, placards, verrières d'atelier, portes. Batidec les réalise à Rouen, comme le dressing de Mme L. présenté ici.",
    [("Quels ouvrages de menuiserie intérieure réalise Batidec ?", "<ul><li>Dressings et placards sur mesure</li><li>Verrières d'atelier pour séparer sans assombrir</li><li>Portes intérieures et habillages</li><li>Rangements sous escalier, niches</li></ul>"),
     ("Pourquoi une verrière intérieure ?", "<p>La verrière sépare deux espaces (cuisine et séjour, bureau, chambre) tout en laissant passer la lumière : un classique des appartements rénovés.</p>")],
    [("Batidec fabrique-t-elle des dressings sur mesure ?", "Oui, dressings et placards adaptés à vos dimensions, comme le dressing de Mme L."),
     ("Une verrière peut-elle être posée sur une cloison existante ?", "Souvent oui, après vérification de la cloison ; sinon une cloison neuve est créée."),
     ("Batidec remplace-t-elle les portes intérieures ?", "Oui, pose et peinture de portes intérieures.")],
    [("dressing-finale-rotated.jpg", "Dressing, projet de Mme L."), ("dressing.jpg", "Dressing, projet de Mme L."), ("dressing-2-rotated.jpg", "Rangements, projet de Mme L.")])

svc("agencement-commerce-rouen", "Agencement de commerces", "Agencement de bar, restaurant et boutique à Rouen", "Agencement & menuiserie",
    ("w", "salle-2-rotated.jpg"), "Bars, restaurants, boutiques : du plan à l'ouverture.",
    "Agencement de bar, restaurant et boutique à Rouen | Batidec",
    "Agencement et décoration de commerces à Rouen : bars, brasseries, salons de thé, boutiques. Références : Le Central, JM's Café, Dame Cakes, Lanchon.",
    "L'agencement d'un commerce, c'est l'organisation et la décoration de l'espace pour accueillir les clients et faciliter le travail. Batidec aménage à Rouen bars, brasseries, salons de thé et boutiques, de la conception à la peinture finale.",
    [("Quels commerces Batidec a-t-elle aménagés à Rouen ?", "<ul><li><b>Brasserie Le Central</b> : aménagement et décoration</li><li><b>Bar JM's Café</b>, Rouen</li><li><b>Salon de thé Dame Cakes</b></li><li><b>Le Lanchon Opticiens</b></li></ul>"),
     ("Pourquoi un seul prestataire pour l'agencement et la décoration ?", "<p>Un seul interlocuteur coordonne plâtrerie, sols, menuiserie et peinture : moins de délais avant l'ouverture et une décoration pensée avec l'agencement.</p>")],
    [("Batidec peut-elle travailler en dehors des heures d'ouverture ?", "Le planning est défini avec vous lors du devis pour limiter l'impact sur votre activité."),
     ("Batidec aménage-t-elle les bars et restaurants ?", "Oui, notamment la brasserie Le Central et le bar JM's Café à Rouen."),
     ("Batidec refait-elle les vitrines ?", "Oui ; un client commerçant a salué en octobre 2026 le travail réalisé sur les vitrines de son magasin.")],
    [("salle-2-rotated.jpg", "Brasserie Le Central"), ("salle-rotated.jpg", "Brasserie Le Central"), ("rdc.jpg", "Bar JM's Café, Rouen"),
     ("etage-7.jpg", "Salon de thé Dame Cakes"), ("120807361_620035005337624_8398906530529115205_n.jpeg", "Le Lanchon Opticiens")])

UNIS = [
    ("Peinture & façade", "Le cœur du métier depuis 1972.", ("u", "peinture")),
    ("Décoration & revêtements", "Murs, sols, matières : l'ambiance de vos pièces.", ("u", "deco")),
    ("Rénovation", "Cloisons, isolation, cuisine, salle de bain, clé en main.", ("u", "renov")),
    ("Agencement & menuiserie", "Commerces, dressings, verrières sur mesure.", ("w", "salle-2-rotated.jpg")),
]

def src(img, w=1400):
    return U(ST[img[1]], w) if img[0] == "u" else W(img[1])

def figure(img, alt, cls="", w=1400, eager=False):
    tag = "" if img[0] == "u" else '<span class="real">Réalisation Batidec</span>'
    ld = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<figure class="{cls}"><img src="{src(img, w)}" alt="{alt}" {ld}>{tag}</figure>'

# ---------------- schema ----------------
LOCAL = {
    "@context": "https://schema.org", "@type": "HousePainter", "@id": SITE + "/#entreprise",
    "name": "Batidec", "description": CANON, "url": SITE + "/", "logo": W("Logo-Batidec-1.webp"),
    "image": W("cuisine.jpg"), "telephone": TEL_L, "email": MAIL, "foundingDate": "1972",
    "founder": {"@type": "Person", "name": "Hamyne Abdou"},
    "employee": {"@type": "Person", "name": "Marphour Hassan", "jobTitle": "Dirigeant"},
    "taxID": "34491401500039",
    "address": {"@type": "PostalAddress", "streetAddress": "32 rue du Mail", "postalCode": "76100",
                "addressLocality": "Rouen", "addressRegion": "Normandie", "addressCountry": "FR"},
    "geo": {"@type": "GeoCoordinates", "latitude": 49.4300466, "longitude": 1.0909089},
    "hasMap": MAPS,
    "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "17:00"}],
    "areaServed": {"@type": "City", "name": "Rouen"}, "sameAs": [FB, MAPS],
    "hasCredential": [{"@type": "EducationalOccupationalCredential", "credentialCategory": "Qualification RGE (Reconnu Garant de l'Environnement)"},
                      {"@type": "EducationalOccupationalCredential", "credentialCategory": "Assurance garantie décennale"}],
    "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Prestations Batidec à Rouen",
        "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{SITE}/{k}/"}} for k, s in S.items()]},
}

def ld(*o):
    return "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in o)

def crumbs(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (u, n) in enumerate(items)]}

def faq_ld(f):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in f]}

def faq_html(f):
    return '<div class="faq">' + "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in f) + "</div>"

# ---------------- gabarit ----------------
NAV = [("/prestations/", "Prestations"), ("/projets/", "Réalisations"), ("/a-propos/", "L'atelier"), ("/contact/", "Contact")]

def mega():
    cols = ""
    for u, _, _ in UNIS:
        li = "".join(f'<li><a href="/{s["slug"]}/">{s["name"]}</a></li>' for s in S.values() if s["uni"] == u)
        cols += f'<div><p class="mm-h">{u}</p><ul>{li}</ul></div>'
    return f'<div class="mm"><div class="wrap mm-in">{cols}</div></div>'

def header(path):
    links = "".join(f'<a href="{u}"{" aria-current=page" if path.startswith(u) else ""}>{n}</a>' for u, n in NAV)
    msvc = "".join(f'<a href="/{x["slug"]}/">{x["name"]}</a>' for x in S.values())
    return f'''<a class="skip" href="#main">Aller au contenu</a>
<header class="hd"><div class="wrap hd-in">
<a class="brand" href="/" aria-label="Batidec, accueil"><span class="b-name">BATIDEC</span><span class="b-tag">Peinture · Décoration · Agencement</span></a>
<nav class="nav" id="nav" aria-label="Menu principal">{links}<a class="nav-tel" href="tel:{TEL_L}">{TEL}</a><div class="nav-svc"><p>Nos prestations</p>{msvc}</div><a class="btn nav-cta" href="/contact/">Devis gratuit</a></nav>
<a class="btn btn-sm hd-cta" href="/contact/">Devis gratuit</a>
<button class="burger" aria-label="Ouvrir le menu" aria-expanded="false" aria-controls="nav"><span></span><span></span></button>
</div>{mega()}</header>'''

def band():
    return trust("trust-dark") + f'''<section class="band"><div class="wrap band-in">
<div><p class="kicker">Un projet à Rouen ?</p><h2>Parlons de vos murs, de vos sols ou de votre commerce.</h2>
<p>{XP} ans d'expérience, garantie décennale, entreprise RGE. Visite et devis gratuits, réponse du lundi au vendredi.</p></div>
<div class="band-act"><a class="btn btn-light" href="/contact/">Demander un devis</a><a class="btn btn-line" href="tel:{TEL_L}">{TEL}</a></div></div></section>'''

def footer():
    cols = ""
    for u, _, _ in UNIS:
        cols += f'<div><p class="ft-h">{u}</p><ul>' + "".join(f'<li><a href="/{s["slug"]}/">{s["name"]}</a></li>' for s in S.values() if s["uni"] == u) + "</ul></div>"
    return f'''<footer class="ft"><div class="swatch" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i></div>
<div class="wrap ft-top"><div><p class="b-name">BATIDEC</p><p class="ft-desc">{CANON}</p>
<address>{ADR}<br><a href="tel:{TEL_L}">{TEL}</a> · <a href="mailto:{MAIL}">{MAIL}</a><br>Lundi au vendredi, 9 h à 17 h</address>
<p class="ft-badges"><span>{XP} ans d'expérience</span><span>Garantie décennale</span><span>Entreprise RGE</span><span>4,7/5 Google</span></p><p class="ft-links"><a href="/projets/">Réalisations</a> · <a href="/a-propos/">L'atelier</a> · <a href="{MAPS}" rel="noopener">Google Maps</a> · <a href="{FB}" rel="noopener">Facebook</a> · <a href="/mentions-legales/">Mentions légales</a></p></div></div>
<div class="wrap ft-in">{cols}</div>
<div class="wrap ft-bot"><span>© 2026 Batidec · SIRET 344 914 015 00039</span><span>Peintre décorateur à Rouen depuis 1972</span></div></footer>
<div class="mbar"><a href="tel:{TEL_L}" class="mbar-tel">Appeler</a><a href="/contact/" class="mbar-dev">Devis gratuit</a></div>
<script src="/app.js?v=5" defer></script>'''

PAGES = []
def page(path, title, desc, body, lds=(), og=None, cls=""):
    assert len(title) <= 62, (title, len(title))
    og = og or W("cuisine.jpg")
    html = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{SITE}{path}">
<meta property="og:type" content="website"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:image" content="{og}"><meta property="og:locale" content="fr_FR">
<meta name="theme-color" content="#14201f">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="preconnect" href="https://images.unsplash.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,500;1,9..144,400&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/styles.css?v=7">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='6' fill='%232f7178'/%3E%3Ctext x='16' y='23' font-family='Georgia' font-size='20' fill='%23f6f1e8' text-anchor='middle'%3EB%3C/text%3E%3C/svg%3E">
{ld(LOCAL, *lds)}</head><body class="{cls}">{header(path)}<main id="main">{body}</main>{footer()}</body></html>'''
    d = OUT / path.strip("/")
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(html, encoding="utf-8")
    PAGES.append(path)

OUT.mkdir(exist_ok=True)
for f in ("styles.css", "app.js", "_headers"):
    shutil.copy(ROOT / f, OUT / f)

# ---------------- ACCUEIL ----------------
home_faq = [
    ("Quel peintre choisir à Rouen pour un intérieur haut de gamme ?", "Batidec, installée 32 rue du Mail à Rouen depuis 1972, réalise peinture, décoration, rénovation et agencement pour les particuliers et les commerces. L'entreprise familiale est dirigée depuis 2006 par Marphour Hassan. Visite et devis sont gratuits."),
    ("Quelles prestations propose Batidec ?", "Peinture intérieure et extérieure, ravalement de façade, décoration et revêtements muraux, parquet et sols, carrelage, béton ciré, plâtrerie, isolation, rénovation de cuisine et de salle de bain, menuiserie sur mesure et agencement de commerces."),
    ("Batidec est-elle RGE et assurée en garantie décennale ?", "Oui. Batidec est certifiée RGE et assurée en garantie décennale."),
    ("Depuis combien de temps Batidec existe-t-elle ?", f"Depuis 1972, soit {XP} ans d'expérience à Rouen. Fondée par Hamyne Abdou, l'entreprise familiale est dirigée depuis 2006 par Marphour Hassan."),
    ("Quel est l'avis des clients sur Batidec ?", "Batidec obtient 4,7 sur 5 sur Google, sur 25 avis (novembre 2026). Les clients citent le professionnalisme, le savoir-faire et la qualité des chantiers."),
    ("Batidec travaille-t-elle pour les commerces ?", "Oui : brasserie Le Central, bar JM's Café, salon de thé Dame Cakes et Le Lanchon Opticiens, à Rouen."),
    ("Quels sont les horaires de Batidec ?", "Du lundi au vendredi, de 9 h à 17 h, au 02 35 72 20 31 et à batidec-rouen@batidec76.com."),
]
marquee = "".join(f'<a href="/{s["slug"]}/">{s["name"]}</a><i>✦</i>' for s in S.values())
unis_html = ""
for i, (u, txt, img) in enumerate(UNIS):
    li = "".join(f'<li><a href="/{s["slug"]}/"><span>{s["name"]}</span><small>{s["short"]}</small></a></li>' for s in S.values() if s["uni"] == u)
    unis_html += f'''<article class="uni{" rev" if i % 2 else ""}">{figure(img, u + " à Rouen", "uni-img", 1200)}
<div class="uni-txt"><span class="uni-n">0{i+1}</span><h3>{u}</h3><p>{txt}</p><ul class="uni-list">{li}</ul></div></article>'''

refs = [("salle-2-rotated.jpg", "Brasserie Le Central", "Bar-brasserie"), ("rdc.jpg", "JM's Café", "Bar, Rouen"),
        ("etage-7.jpg", "Dame Cakes", "Salon de thé"), ("120807361_620035005337624_8398906530529115205_n.jpeg", "Le Lanchon", "Opticiens"),
        ("cuisine.jpg", "Mme L.", "Cuisine et dressing")]
refs_html = "".join(f'<a class="ref" href="/projets/"><img src="{W(f)}" alt="{n}, réalisation Batidec à Rouen" loading="lazy"><span><b>{n}</b>{t}</span></a>' for f, n, t in refs)

home = f'''
<section class="hero2">
<img class="hero2-bg" src="{U(ST["hero"], 1600)}" alt="Intérieur ancien à moulures, ambiance haut de gamme" fetchpriority="high">
<div class="wrap hero2-in">
<div class="hero2-txt">
<p class="kicker kl">Rouen · rue du Mail · depuis 1972</p>
<h1>Peintre décorateur à Rouen depuis 1972, <em>{XP} ans de savoir-faire</em> familial.</h1>
<p class="lead">Peinture, façades, décoration, sols, rénovation et agencement de commerces. Garantie décennale, entreprise RGE, un seul interlocuteur du devis aux finitions.</p>
<div class="hero-act"><a class="btn btn-light" href="/contact/">Devis gratuit</a><a class="btn btn-line" href="tel:{TEL_L}">{TEL}</a></div>
</div>
<form class="qf" data-mailto novalidate><p class="qf-h">Devis gratuit</p><p class="qf-s">Batidec vous rappelle du lundi au vendredi pour organiser la visite.</p>
<div class="fl"><input id="qn" name="nom" placeholder=" " required autocomplete="name"><label for="qn">Votre nom</label></div>
<div class="fl"><input id="qt" name="tel" type="tel" placeholder=" " required autocomplete="tel"><label for="qt">Votre téléphone</label></div>
<div class="fl fl-sel"><select id="qp" name="type">{"".join(f"<option>{x['name']}</option>" for x in S.values())}<option>Autre</option></select><label for="qp">Votre projet</label></div>
<input class="hp" name="site" tabindex="-1" autocomplete="off" aria-hidden="true"><input type="hidden" name="msg" value="Demande de rappel envoyée depuis l'accueil du site.">
<button class="btn btn-block" type="submit">Être rappelé gratuitement</button><p class="qf-or">ou appelez le <a href="tel:{TEL_L}">{TEL}</a></p><p class="qf-m small"></p></form>
</div>
<div class="wrap hero2-proof"><div><b>{XP} ans</b><span>d'expérience, depuis 1972</span></div><div><b>4,7<em>★</em></b><span>25 avis Google</span></div><div><b>RGE</b><span>et garantie décennale</span></div><div><b>{len(S)}</b><span>savoir-faire, 1 interlocuteur</span></div></div>
</section>
<div class="marquee" aria-label="Nos prestations"><div class="mq">{marquee}{marquee}</div></div>

{trust()}
<section class="intro wrap"><p class="kicker">En une phrase</p><p class="canon">{CANON}</p></section>

<section class="wrap sec"><div class="sec-hd"><p class="kicker">Nos savoir-faire</p><h2>Quatre univers, {len(S)} métiers, un seul atelier.</h2>
<p>Du mur au sol, de la cloison à la dernière couche de peinture : moins d'intermédiaires, un chantier plus propre et un résultat cohérent.</p></div>
<div class="unis">{unis_html}</div></section>

<section class="dark"><div class="wrap">
<div class="sec-hd"><p class="kicker">Ils nous ont fait confiance à Rouen</p><h2>Des lieux qui accueillent du public tous les jours.</h2></div>
<div class="refs">{refs_html}</div>
<blockquote class="quote">« Merci Mr Hassan pour votre professionnalisme. Je suis très satisfait du travail effectué sur les vitrines de mon magasin. »<cite>Ilan Israel · avis Google 5/5 · octobre 2026</cite></blockquote>
</div></section>

<section class="wrap sec"><div class="sec-hd"><p class="kicker">Pourquoi Batidec</p><h2>Six raisons de nous confier <em>votre chantier</em>.</h2></div>
<div class="why">
<div>{ico("clock")}<h3>{XP} ans d'expérience</h3><p>Fondée en 1972 par Hamyne Abdou, transmise en 2006 à Marphour Hassan : le savoir-faire d'une famille rouennaise.</p></div>
<div>{ico("shield")}<h3>Garantie décennale</h3><p>Vos travaux sont couverts par l'assurance décennale de Batidec.</p></div>
<div>{ico("leaf")}<h3>Entreprise RGE</h3><p>Une qualification exigée pour que vos travaux d'isolation puissent ouvrir droit aux aides publiques, selon conditions.</p></div>
<div>{ico("user")}<h3>Un seul interlocuteur</h3><p>{len(S)} métiers dans un même atelier : aucune coordination entre artisans à gérer.</p></div>
<div>{ico("brush")}<h3>Chantier propre</h3><p>Sols et mobilier protégés, préparation soignée, nettoyage avant départ.</p></div>
<div>{ico("doc")}<h3>Devis clair et gratuit</h3><p>Après visite, poste par poste, sans engagement ni surprise.</p></div>
</div></section>

<section class="avis-sec"><div class="wrap"><div class="avis-top"><div><p class="kicker">Avis clients</p><h2>4,7/5 sur 25 avis Google.</h2></div>
<a class="btn btn-ghost" href="{MAPS}" rel="noopener">Voir tous les avis</a></div>{avis_html()}</div></section>

<section class="wrap sec split">
{figure(("u", "nuancier"), "Nuancier de couleurs et pinceau", "split-img", 1200)}
<div><p class="kicker">Conseil couleurs</p><h2>La bonne teinte, au bon endroit.</h2>
<p>Lumière de la pièce, volumes, boiseries, mobilier : avant de peindre, Batidec vous aide à choisir les couleurs et les matières qui mettront votre intérieur en valeur. Un regard de décorateur, inclus dans l'accompagnement.</p>
<a class="link" href="/decoration-interieur-rouen/">Décoration intérieure à Rouen</a></div></section>

<section class="wrap sec"><div class="sec-hd"><p class="kicker">Comment ça se passe</p><h2>De votre appel à la remise des clés.</h2></div>
<ol class="steps"><li><b>Appel ou message</b><span>Vous nous décrivez votre projet par téléphone ou via le formulaire.</span></li>
<li><b>Visite sur place</b><span>Mesures, état des supports, envies de couleurs.</span></li>
<li><b>Devis détaillé</b><span>Gratuit, poste par poste, sans engagement.</span></li>
<li><b>Chantier soigné</b><span>Protection, préparation, finitions, nettoyage.</span></li></ol></section>

<section class="story"><div class="wrap story-in">
<figure class="story-img"><img src="{W('120760763_620030982004693_4593063110375373801_n.jpeg')}" alt="Locaux de Batidec, 32 rue du Mail à Rouen" loading="lazy"><span class="real">Nos locaux, rue du Mail</span></figure>
<div><p class="kicker">Notre histoire</p><h2>Fondée en 1972, transmise en 2006.</h2>
<p>Hamyne Abdou crée Batidec en 1972 et sert pendant plus de quarante ans les particuliers et les commerçants de Rouen. Formé à ses côtés, Marphour Hassan reprend l'entreprise familiale en 2006 et perpétue la même exigence de finition.</p>
<a class="link" href="/a-propos/">Découvrir l'atelier</a></div></div></section>

<section class="wrap sec"><div class="sec-hd"><p class="kicker">Questions fréquentes</p><h2>Ce que l'on nous demande souvent.</h2></div>{faq_html(home_faq)}</section>
{band()}'''
page("/", "Peintre décorateur et rénovation à Rouen depuis 1972 | Batidec",
     f"Batidec, peintre décorateur à Rouen depuis 1972 ({XP} ans d'expérience) : peinture, façade, sols, rénovation, agencement. RGE, décennale, devis gratuit.",
     home, (faq_ld(home_faq),), cls="home")

# ---------------- PAGES PRESTATIONS ----------------
AV = {"carrelage-faience-rouen": AVIS[1], "renovation-cuisine-rouen": AVIS[1], "agencement-commerce-rouen": AVIS[2], "menuiserie-dressing-verriere-rouen": AVIS[0]}
REP = [("Adresse", ADR), ("Expérience", f"{XP} ans, entreprise familiale créée en 1972"), ("Assurance", "Garantie décennale"), ("Qualification", "Entreprise RGE"), ("Dirigeant", "Marphour Hassan, depuis 2006"),
       ("Avis Google", "4,7/5 sur 25 avis (novembre 2026)"), ("Devis", "Gratuit, après visite"), ("Horaires", "Lundi au vendredi, 9 h à 17 h")]
for k, s in S.items():
    secs1 = "".join(f"<h2>{h}</h2>{c}" for h, c in s["secs"][:1])
    secs2 = "".join(f"<h2>{h}</h2>{c}" for h, c in s["secs"][1:])
    rows = "".join(f"<tr><th>{a}</th><td>{b}</td></tr>" for a, b in REP)
    same = [x for x in S.values() if x["uni"] == s["uni"] and x["slug"] != k]
    rel = "".join(f'<li><a href="/{x["slug"]}/">{x["name"]}</a></li>' for x in same) or ""
    gal = "".join(f'<figure><img src="{W(f)}" alt="{a}, réalisation Batidec" loading="lazy"><figcaption>{a}</figcaption></figure>' for f, a in s["gal"])
    galsec = f"<section class='wrap sec'><div class='sec-hd'><p class='kicker'>Réalisations Batidec</p><h2>Nos chantiers en images</h2></div><div class='gal'>{gal}</div><a class='link' href='/projets/'>Toutes les réalisations</a></section>" if gal else ""
    body = f'''<section class="phero"><div class="wrap phero-in">
<div><nav class="bc" aria-label="Fil d'Ariane"><a href="/">Accueil</a> / <a href="/prestations/">Prestations</a> / <span>{s["name"]}</span></nav>
<p class="kicker">{s["uni"]} · Rouen</p><h1>{s["h1"]}</h1><p class="lead">{s["direct"]}</p>
<div class="hero-act"><a class="btn" href="/contact/">Devis gratuit</a><a class="btn btn-ghost" href="tel:{TEL_L}">{TEL}</a></div>
<p class="mini-proof"><b>4,7★</b> 25 avis Google · {XP} ans d'expérience · RGE · Décennale</p></div>
{figure(s["img"], s["h1"], "phero-img", 1200, True)}</div></section>
{trust()}
<div class="wrap art"><article class="prose">{secs1}
<div class="cta-in"><div><b>Un projet à Rouen ?</b><span>{s["name"]} : visite et devis gratuits, {XP} ans d'expérience, garantie décennale.</span></div><a class="btn" href="/contact/">Demander mon devis</a></div>
{secs2}
<h2>Ce que disent nos clients</h2>{avis_html([AV[k]] if k in AV else AVIS[:1])}
<h2>Batidec en repères</h2><table class="facts">{rows}</table>
<h2>Questions fréquentes</h2>{faq_html(s["faq"])}
<p class="small byline">Contenu rédigé par Batidec, entreprise familiale de Rouen dirigée par Marphour Hassan depuis 2006, formé auprès du fondateur Hamyne Abdou. Mise à jour : {DATE}.</p></article>
<aside class="side"><div class="side-card sticky"><p class="ft-h">Votre devis</p><p>Visite et devis gratuits à Rouen.</p>
<a class="btn btn-block" href="/contact/">Demander un devis</a><a class="btn btn-ghost btn-block" href="tel:{TEL_L}">{TEL}</a><p class="small">Lun. au ven., 9 h à 17 h<br>{ADR}</p></div>
{"<div class='side-card'><p class='ft-h'>Dans le même univers</p><ul>" + rel + "</ul></div>" if rel else ""}</aside></div>
{galsec}{band()}'''
    page(f"/{k}/", s["title"], s["desc"], body,
         (faq_ld(s["faq"]), crumbs([("/", "Accueil"), ("/prestations/", "Prestations"), (f"/{k}/", s["name"])]),
          {"@context": "https://schema.org", "@type": "WebPage", "url": f"{SITE}/{k}/", "dateModified": "2026-11-18", "author": {"@id": SITE + "/#entreprise"}},
          {"@context": "https://schema.org", "@type": "Service", "name": s["name"], "serviceType": s["name"], "provider": {"@id": SITE + "/#entreprise"}, "areaServed": {"@type": "City", "name": "Rouen"}}),
         src(s["img"], 1200))

# ---------------- PRESTATIONS (hub) ----------------
hub = ""
for i, (u, txt, img) in enumerate(UNIS):
    cards = "".join(f'<a class="card" href="/{s["slug"]}/"><img src="{src(s["img"], 700)}" alt="{s["name"]} à Rouen" loading="lazy"><span class="card-b"><b>{s["name"]}</b><small>{s["short"]}</small></span></a>' for s in S.values() if s["uni"] == u)
    hub += f'<div class="hub"><div class="hub-hd"><span class="uni-n">0{i+1}</span><h2>{u}</h2><p>{txt}</p></div><div class="cards">{cards}</div></div>'
page("/prestations/", "Prestations Batidec à Rouen : peinture, rénovation, déco",
     "Toutes les prestations de Batidec à Rouen : peinture, ravalement, décoration, sols, carrelage, béton ciré, plâtrerie, isolation, rénovation, agencement.",
     f'''<section class="phero slim"><div class="wrap"><nav class="bc"><a href="/">Accueil</a> / <span>Prestations</span></nav><p class="kicker">Savoir-faire</p><h1>Nos prestations à Rouen</h1>
<p class="lead">{len(S)} métiers complémentaires réunis dans un même atelier rouennais, pour les particuliers et les professionnels. Les photos marquées « Réalisation Batidec » sont des chantiers réels.</p></div></section>
<section class="wrap sec">{hub}</section>{band()}''', (crumbs([("/", "Accueil"), ("/prestations/", "Prestations")]),))

# ---------------- PROJETS ----------------
PROJ = [("Brasserie Le Central", "Aménagement et décoration d'un bar-brasserie.", ["salle-2-rotated.jpg", "salle-rotated.jpg", "salle-1-rotated.jpg"]),
        ("Projet de Mme L.", "Rénovation d'un intérieur : cuisine, salle de bain, douche, dressing.", ["cuisine.jpg", "dressing-finale-rotated.jpg", "salle-de-bain-rotated.jpg"]),
        ("Bar JM's Café, Rouen", "Agencement et décoration d'un bar rouennais.", ["rdc.jpg", "rdc-1.jpg", "rdc3.jpg"]),
        ("Salon de thé Dame Cakes", "Décoration et aménagement d'un salon de thé.", ["etage-7.jpg", "enseigne.jpg", "etage-8.jpg"]),
        ("Le Lanchon Opticiens", "Agencement d'une boutique d'optique.", ["120807361_620035005337624_8398906530529115205_n.jpeg"])]
pj = ""
for n, d, fs in PROJ:
    im = "".join(f'<img src="{W(f)}" alt="{n}, réalisation Batidec à Rouen" loading="lazy">' for f in fs)
    pj += f'<article class="proj"><div class="proj-imgs n{len(fs)}">{im}</div><div class="proj-t"><span class="real-t">Réalisation Batidec</span><h2>{n}</h2><p>{d}</p></div></article>'
page("/projets/", "Réalisations peinture et agencement à Rouen | Batidec",
     "Réalisations Batidec à Rouen : brasserie Le Central, bar JM's Café, salon de thé Dame Cakes, Le Lanchon Opticiens, rénovation d'intérieur.",
     f'''<section class="phero slim"><div class="wrap"><nav class="bc"><a href="/">Accueil</a> / <span>Réalisations</span></nav><p class="kicker">Portfolio</p><h1>Nos réalisations à Rouen</h1>
<p class="lead">Commerces et intérieurs de particuliers : des chantiers réels menés par Batidec.</p></div></section><section class="wrap sec projs">{pj}</section><section class="avis-sec"><div class="wrap"><div class="avis-top"><div><p class="kicker">Avis clients</p><h2>4,7/5 sur 25 avis Google.</h2></div><a class="btn btn-ghost" href="{MAPS}" rel="noopener">Voir tous les avis</a></div>{avis_html()}</div></section>{band()}''',
     (crumbs([("/", "Accueil"), ("/projets/", "Réalisations")]),), W("salle-2-rotated.jpg"))

# ---------------- A PROPOS ----------------
page("/a-propos/", "L'atelier Batidec, entreprise familiale à Rouen depuis 1972",
     "Batidec, créée en 1972 par Hamyne Abdou et dirigée depuis 2006 par Marphour Hassan : peinture, décoration, rénovation et agencement à Rouen.",
     f'''<section class="phero"><div class="wrap phero-in"><div><nav class="bc"><a href="/">Accueil</a> / <span>L'atelier</span></nav><p class="kicker">Depuis 1972</p>
<h1>{XP} ans d'expérience, une entreprise familiale rouennaise</h1><p class="lead">{CANON}</p></div>
{figure(("w", "120760763_620030982004693_4593063110375373801_n.jpeg"), "Locaux Batidec, 32 rue du Mail à Rouen", "phero-img", eager=True)}</div></section>
<div class="wrap art"><article class="prose">
<h2>Combien d'années d'expérience a Batidec ?</h2><p>Batidec a été créée en 1972 : l'entreprise compte <b>{XP} ans d'expérience</b> à Rouen. Elle est certifiée RGE et assurée en garantie décennale.</p>
<h2>Qui a fondé Batidec ?</h2><p>Hamyne Abdou crée Batidec en 1972. Pendant plus de quarante ans, il met son savoir-faire au service des particuliers et des commerçants de Rouen.</p>
<h2>Qui dirige Batidec aujourd'hui ?</h2><p>Marphour Hassan, formé à la peinture, à la décoration et à l'aménagement aux côtés d'Hamyne Abdou, reprend l'entreprise familiale en 2006. Il dirige aujourd'hui Batidec avec une équipe attentive aux détails.</p>
<h2>Comment se passe une demande de devis ?</h2><p>Vous appelez ou envoyez votre demande ; Batidec vous recontacte pour organiser la visite gratuite, puis vous remet un devis détaillé.</p>
<h2>Notre engagement</h2><ul class="ticks"><li>Un travail de qualité, des finitions haut de gamme</li><li>Un interlocuteur unique du devis à la fin du chantier</li><li>Des chantiers propres et protégés</li></ul>
<table class="facts"><tr><th>Création</th><td>1972 ({XP} ans d'expérience)</td></tr><tr><th>Assurance</th><td>Garantie décennale</td></tr><tr><th>Qualification</th><td>RGE</td></tr><tr><th>Fondateur</th><td>Hamyne Abdou</td></tr><tr><th>Dirigeant</th><td>Marphour Hassan, depuis 2006</td></tr><tr><th>Adresse</th><td>{ADR}</td></tr><tr><th>SIRET</th><td>344 914 015 00039</td></tr></table>
</article><aside class="side"><div class="side-card sticky"><p class="ft-h">Nous rencontrer</p><p>{ADR}<br>Lun. au ven., 9 h à 17 h</p><a class="btn btn-block" href="/contact/">Demander un devis</a><a class="btn btn-ghost btn-block" href="tel:{TEL_L}">{TEL}</a></div></aside></div>{band()}''',
     (crumbs([("/", "Accueil"), ("/a-propos/", "L'atelier")]),), W("120760763_620030982004693_4593063110375373801_n.jpeg"))

# ---------------- CONTACT ----------------
opts = "".join(f"<option>{s['name']}</option>" for s in S.values())
page("/contact/", "Devis peinture et rénovation à Rouen | Contact Batidec",
     "Demandez votre devis gratuit à Batidec, 32 rue du Mail à Rouen : 02 35 72 20 31, du lundi au vendredi de 9 h à 17 h.",
     f'''<section class="phero slim"><div class="wrap"><nav class="bc"><a href="/">Accueil</a> / <span>Contact</span></nav><p class="kicker">Devis gratuit</p><h1>Contacter Batidec à Rouen</h1>
<p class="lead">Décrivez votre projet en une minute : Batidec vous recontacte pour organiser la visite. Le devis est gratuit et sans engagement.</p></div></section>
{trust()}
<section class="wrap ct">
<aside class="ct-side"><p class="kicker kl">Batidec · depuis 1972</p><h2>Parlons de votre projet.</h2>
<p class="ct-intro">{XP} ans d'expérience à Rouen, garantie décennale, entreprise RGE.</p>
<a class="ct-tel" href="tel:{TEL_L}">{ico("user")}<span><small>Appelez-nous</small>{TEL}</span></a>
<ul class="ct-list"><li>{ico("doc")}<span><small>E-mail</small><a href="mailto:{MAIL}">{MAIL}</a></span></li>
<li>{ico("shield")}<span><small>Adresse</small>{ADR}</span></li>
<li>{ico("clock")}<span><small>Horaires</small>Lundi au vendredi, 9 h à 17 h</span></li></ul>
<figure class="ct-av"><div class="stars">★★★★★</div><blockquote>« {AVIS[0][2]} »</blockquote><figcaption>{AVIS[0][0]} · avis Google · 4,7/5 sur 25 avis</figcaption></figure>
</aside>
<form class="ct-form" id="devis" data-mailto novalidate>
<p class="ct-step"><span>1</span>Votre projet</p>
<div class="chips">{"".join(f'<label class="chip"><input type="radio" name="type" value="{u}"{" checked" if i == 0 else ""}><span>{u}</span></label>' for i, (u, _, _) in enumerate(UNIS))}<label class="chip"><input type="radio" name="type" value="Autre"><span>Autre</span></label></div>
<p class="ct-step"><span>2</span>Vos coordonnées</p>
<div class="f2"><div class="fl"><input id="cn" name="nom" placeholder=" " required autocomplete="name"><label for="cn">Nom et prénom</label></div>
<div class="fl"><input id="ct" name="tel" type="tel" placeholder=" " required autocomplete="tel"><label for="ct">Téléphone</label></div></div>
<div class="fl"><input id="ce" name="email" type="email" placeholder=" " autocomplete="email"><label for="ce">E-mail (facultatif)</label></div>
<p class="ct-step"><span>3</span>Votre message</p>
<div class="fl"><textarea id="cm" name="msg" rows="5" placeholder=" " required></textarea><label for="cm">Surface, adresse du chantier, délai souhaité…</label></div>
<input class="hp" name="site" tabindex="-1" autocomplete="off" aria-hidden="true">
<button class="btn btn-block btn-lg" type="submit">Envoyer ma demande de devis <span aria-hidden="true">→</span></button>
<p class="ct-note" id="fmsg">Gratuit et sans engagement. Vos informations servent uniquement à vous répondre.</p>
</form></section>
<div class="wrap"><iframe class="map" title="Batidec, 32 rue du Mail à Rouen sur Google Maps" loading="lazy" src="https://www.google.com/maps?q=Batidec,32+rue+du+Mail,+76100+Rouen&output=embed"></iframe></div>''',
     (crumbs([("/", "Accueil"), ("/contact/", "Contact")]),))

page("/mentions-legales/", "Mentions légales | Batidec, peintre décorateur à Rouen",
     "Mentions légales du site de Batidec, entreprise de peinture, décoration et agencement à Rouen.",
     f'''<section class="phero slim"><div class="wrap"><h1>Mentions légales</h1></div></section><div class="wrap prose sec">
<p><b>Éditeur</b> : Batidec, {ADR}. SIRET 344 914 015 00039. Téléphone {TEL}. E-mail {MAIL}. Directeur de la publication : Marphour Hassan.</p>
<p><b>Hébergement</b> : Cloudflare, Inc., 101 Townsend St, San Francisco, CA 94107, États-Unis.</p>
<p><b>Photos</b> : les photos marquées « Réalisation Batidec » montrent des chantiers réels ; les autres photos d'ambiance proviennent d'Unsplash (licence Unsplash).</p>
<p><b>Données personnelles</b> : les informations envoyées via le formulaire servent uniquement à répondre à votre demande de devis.</p></div>''')

# ---------------- technique ----------------
(OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
(OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    + "".join(f"<url><loc>{SITE}{p}</loc><lastmod>2026-11-18</lastmod></url>" for p in PAGES) + "</urlset>\n")
(OUT / "llms.txt").write_text(f"# Batidec\n\n> {CANON}\n\n- Adresse : {ADR}\n- Téléphone : {TEL}\n- Horaires : lundi au vendredi, 9 h à 17 h\n- Création : 1972 (Hamyne Abdou) ; dirigeant depuis 2006 : Marphour Hassan\n- Avis Google : 4,7/5 sur 25 avis (novembre 2026)\n- Certifications : entreprise RGE, garantie décennale\n- Expérience : {XP} ans (depuis 1972)\n\n## Prestations\n"
    + "".join(f"- [{s['name']}]({SITE}/{k}/) : {s['short']}\n" for k, s in S.items()))
(OUT / "_redirects").write_text("/project/* /projets/ 301\n")
print("ok", len(PAGES), "pages")
