"""Reel Medadom Professionnel (29/10/2026) : l'infection urinaire de l'homme en teleconsultation, en 9:16
(Instagram, Facebook) et en carre (LinkedIn). Moteur version 2 : moteur_reel2.js, reel2.css.

    python reel_iu.py [--essai] [--format 9x16|1x1]

Sources, chaque ecran et chaque phrase lue :
- SPILF, « Infections urinaires masculines aigues communautaires de l'adulte (IUMACA) », mise a jour des
  recommandations, jeu de diapositives du comite des referentiels du 20/06/2026
  (infectiologie.com, spilf-groupe-recos-ium.pptx) : BU non recommandee, ECBU avant toute antibiotherapie
  (diapo 6) ; cystite : diagnostic, attente de l'ECBU si bonne tolerance ou diagnostic douteux,
  fosfomycine-trometamol J1-J3-J5, nitrofurantoine, pivmecillinam, 7 jours sauf fosfomycine 3 doses
  (diapos 8, 9, 11) ; prostatite aigue en ambulatoire : ceftriaxone IV, IM ou SC 1 g/j, ou ciprofloxacine
  ou levofloxacine en l'absence de prise de fluoroquinolones dans les 6 mois, nausees, vomissements,
  malabsorption, observance incertaine (diapo 14), 14 jours (diapo 18) ; orientation vers l'hopital,
  score de risque de sepsis a 6 variables, 3 ou plus : 40 % de risque (diapos 26, 27) ; epididymite et
  orchite : torsion du cordon spermatique (urgence), ECBU systematique, PCR C. trachomatis et
  N. gonorrhoeae sur le 1er jet chez l'homme sexuellement actif (diapo 30) ;
- Info-antibio n° 109 (SPILF, juin 2026), memes molecules et durees ;
- JNI 2026, R. Calin, « Les infections urinaires, actualites 2026 » : « Homme et IU : la fin du "tout
  prostatite" » ;
- compte rendu de la classe virtuelle Medadom du 25/02/2026 : ECBU au laboratoire ou avec un infirmier,
  ordonnance infirmiere pour la ceftriaxone, courrier d'adressage mentionnant la demarche et la conduite a
  tenir transmise au patient. Ses autres points (bandelette, hemoculture si fievre, 10 jours) sont
  anterieurs aux recommandations de juin 2026 et ne sont pas repris."""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ICI = Path(__file__).resolve().parent
R = Path(r"C:\Users\NR SMART\tools\lcdg-reel")
sys.path.insert(0, str(R))
from dotenv import load_dotenv
load_dotenv(R / ".env")
from lcdg import voix

EMILIE = "d3AXX0BlgJHYFCuH9X88"   # femme_agee du catalogue LCDG : Emilie (« vraiment tres pro », 28/10/2026)
TEMPO = 1.05                # rythme des voix v3 des reels (charte LCDG)
DEBUT_VOIX = 0.6            # s : la voix commence apres l'apparition du premier ecran
AVANCE = 0.12               # s : un texte apparait juste avant d'etre dit
TENUE = 0.9                 # s : apres la derniere phrase, avant la carte de fin
FIN = 3.2                   # s : carte de fin (logo, « Le lien est en bio »)
ECART_PRISES = 1.0          # s : blanc entre la prise du contenu et celle de la fin
# ancienne fin, toujours lue dans la 1re prise (cache de la prise approuvee le 29/10) puis coupee au montage
PRISE1_SUITE = "[cheerful] Vous êtes médecin généraliste ? Rejoignez Médadom."
MUSIQUE = Path(r"C:\Users\NR SMART\Downloads\Caleb Arredondo - Echo Sax No.4.mp3")
SORTIE = Path(r"C:\Users\NR SMART\Downloads\Medadom_reel_infection_urinaire_homme")
NOM = "iu"
NB = "\u00a0"
THEME = {"fond": "#A7CCED", "encre": "#1F1650", "accent": "#1C5FAE", "accent-pale": "rgba(28,95,174,.20)",
         "clair": "#D2E6F8", "ombre-fond": "rgba(30,70,140,.22)", "rouge": "#E0393E"}
COUVERTURE = {"etiquette": "Téléconsultation",
              "titre": f"Infection urinaire<br><span class='surligne'>chez l’homme</span>",
              "sous": "Ce qui change en 2026", "dessin": "iu_01_medecin_teleconsultation"}


def d(nom):
    """Dessin detoure (sans fond) : chemin, rapport largeur/hauteur, ancre en bas ou non."""
    f = ICI / "dessins_canva" / "detoures" / f"{nom}.png"
    im = Image.open(f)
    bas = im.getchannel("A").crop((0, im.height - 3, im.width, im.height)).getextrema()[1] > 200
    return {"src": f"dessins_canva/detoures/{nom}.png", "ratio": im.width / im.height, "bas": bas}


def orig(nom):
    """Dessin entier (avec son fond) : pour l'ecran du telephone."""
    return f"dessins_canva/{nom}.png"


def c(texte, large=False):
    return {"texte": texte, "large": large}


SCENES = [
    # SPILF 2026 (IUMACA) : infection urinaire aigue communautaire de l'homme adulte (diapos 1, 3) ; quatre entites
    # cliniques ; « la fin du "tout prostatite" » : JNI 2026 ; le public nomme des la premiere phrase (conseil du 28/10)
    {"voix": "[serious] Médecins généralistes : la Spilf a mis à jour ses recommandations sur l’infection urinaire "
             "aiguë communautaire de l’homme. | [curious] Fini le « tout prostatite » ! | Quatre tableaux à "
             "distinguer.",
     "el": [("etiquette", f"SPILF 2026{NB}: IU aiguë communautaire", 0),
            ("titre", f"Fini le «{NB}tout prostatite{NB}»", 1),
            ("criteres", [c("Cystite"), c("Prostatite aiguë"), c("Pyélonéphrite aiguë"), c("Épididymite, orchite")], 2, .28),
            ("dessin", d("iu_02_patient_visio"), 0)]},
    # diapo 6 : BU non recommandee ; ECBU avant toute antibiotherapie. Labo ou infirmier : CR Medadom 25/02/2026
    {"voix": "[matter-of-fact] La bandelette urinaire ? Elle n’est plus recommandée. | Un E.C.B.U. avant toute "
             "antibiothérapie : | au laboratoire, ou avec un infirmier.",
     "el": [("etiquette", "Le diagnostic", 0), ("barree", "Bandelette urinaire", 0),
            ("texte", "Un <span class='surligne'>ECBU</span> avant toute antibiothérapie", 1),
            ("pastille", "Au laboratoire ou avec un infirmier", 2),
            ("dessin", d("iu_03_ecbu"), 1)]},
    # diapos 8, 9, 11 : signes locaux d'apparition aigue, sans fievre ; attendre l'ECBU si bonne tolerance ou
    # diagnostic douteux ; sinon trois molecules ; 7 jours, sauf fosfomycine-trometamol (3 doses J1-J3-J5)
    {"voix": "[warm] Des signes urinaires aigus, sans fièvre : c’est une cystite. | Bien tolérée, ou douteuse ? "
             "Attendez l’E.C.B.U.",
     "el": [("etiquette", "Signes urinaires aigus, sans fièvre", 0), ("titre", "Cystite", 0),
            ("pastille", f"Bien tolérée ou douteuse{NB}: <b>attendre l’ECBU</b>", 1)]},
    # AMM : Monuril et Selexid (femme), nitrofurantoine « pas indiquee chez l'homme » (courrier ANSM 2023) ;
    # la SPILF 2026 les recommande quand meme : mention a l'ecran seulement
    {"voix": "Sinon : fosfomycine-trométamol, nitrofurantoïne, ou pivmécilinam. | Sept jours… ou trois doses de "
             "fosfomycine.",
     "el": [("etiquette", "Cystite, si on ne peut pas attendre", 0),
            ("pastille", "Fosfomycine-trométamol, nitrofurantoïne ou pivmécillinam", 0),
            ("note", "Hors AMM chez l’homme, recommandées par la SPILF", 0),
            ("pastille!", f"7{NB}jours · fosfomycine{NB}: J1,{NB}J3,{NB}J5", 1),
            ("dessin", d("iu_04_comprimes"), 0)]},
    # diapos 12, 14 : signes de cystite + fievre ou manifestations systemiques ; sans signe de gravite, traitement
    # initie en ambulatoire : ceftriaxone IV, IM ou SC 1 g/jour. Ordonnance infirmiere : CR Medadom
    {"voix": "[serious] Signes de cystite, avec fièvre ou signes systémiques : c’est une prostatite aiguë. | En "
             "ambulatoire, sans signe de gravité : ceftriaxone, un gramme par jour, en intraveineuse, intramusculaire "
             "ou sous-cutanée… avec une ordonnance infirmière.",
     "el": [("etiquette", "Signes de cystite + fièvre ou signes systémiques", 0), ("titre", "Prostatite aiguë", 0),
            ("pastille", f"En ambulatoire, sans gravité{NB}: <b>ceftriaxone 1{NB}g/j</b>, IV, IM ou SC", 1),
            ("pastille", "Avec une ordonnance infirmière", 1),
            ("dessin", d("iu_05_infirmiere"), 1)]},
    # diapos 14, 16, 18 : cipro ou levofloxacine en l'absence de FQ dans les 6 mois et si la voie orale n'est pas
    # compromise ; relais selon l'antibiogramme, sulfamethoxazole-trimethoprime en premier ; prostatite : 14 jours
    {"voix": "Ou ciprofloxacine, ou lévofloxacine… si aucune fluoroquinolone depuis six mois, et si la voie orale "
             "n’est pas compromise. | Le relais, selon l’antibiogramme : cotrimoxazole en premier. | Pour la "
             "prostatite : quatorze jours, au total.",
     "el": [("etiquette", "Ou cipro- ou lévofloxacine", 0),
            ("criteres", [c("Pas de fluoroquinolone depuis 6&nbsp;mois", True), c("Voie orale non compromise", True)],
             0, .9),
            ("pastille", f"Relais selon l’antibiogramme{NB}: <b>cotrimoxazole en 1er</b>", 1),
            ("chiffre", 14, 2, "", f"{NB}jours"), ("legende", "au total, pour la <b>prostatite aiguë</b>", 2)]},
    # diapos 19, 20, 38 : douleurs lombaires + fievre ou manifestations systemiques, +/- signes de cystite ;
    # scanner injecte systematique dans les 48-72 h ; consultation d'urologie recommandee
    {"voix": "Douleur lombaire, avec fièvre ou signes systémiques, avec ou sans signes de cystite : c’est une "
             "pyélonéphrite. | Un scanner injecté, systématique, sous quarante-huit à soixante-douze heures. | Et "
             "une consultation d’urologie.",
     "el": [("etiquette", "Douleur lombaire + fièvre ou signes systémiques", 0), ("titre", "Pyélonéphrite aiguë", 0),
            ("pastille", f"Scanner injecté systématique, <b>sous 48 à 72{NB}h</b>", 1),
            ("pastille", "Consultation d’urologie", 2),
            ("dessin", d("iu_10_lombaire"), 0)]},
    # diapo 26 : score de risque de sepsis a 6 variables ; 3 ou plus : 40 % de risque de progression
    {"voix": "[serious] Prostatite ou pyélonéphrite : quand adresser à l’hôpital ? | Comptez ces six critères. | "
             "[emphatic] À partir de trois : quarante pour cent de risque d’évoluer vers un sepsis.",
     "el": [("etiquette", "Prostatite, pyélonéphrite", 0), ("titre", f"L’hôpital{NB}?", 0),
            ("criteres", [c(f"Âge &gt; 65{NB}ans"), c(f"T &gt; 38{NB}°C"), c(f"PAS ≤ 110{NB}mmHg"),
                          c("FC &gt; 110/min"), c(f"SpO<sub>2</sub> ≤ 95{NB}%"),
                          c("Troubles récents des fonctions supérieures", True)], 1, .3),
            ("pastille!", f"≥{NB}3 critères{NB}: <b>40{NB}% de risque d’évoluer vers un sepsis</b>", 2)]},
    # diapos 26, 27 : sepsis ou choc septique -> soins intensifs ; les autres criteres d'orientation vers l'hopital
    # « pause » : 3,5 s de silence apres la phrase, le temps que les cinq cases se cochent et se lisent
    {"voix": "[serious] Un sepsis ? Soins intensifs. | Et l’hôpital, aussi, dans ces cinq situations.", "pause": 3.5,
     "el": [("pastille!", f"Sepsis ou choc septique{NB}: <b>soins intensifs</b>", 0),
            ("etiquette", "L’hôpital aussi si", 1),
            ("criteres", [c("Obstruction urinaire suspectée ou confirmée", True),
                          c("Prise orale impossible (vomissements, confusion…)", True),
                          c("Déclin fonctionnel empêchant le maintien à domicile", True),
                          c("Comorbidité décompensée nécessitant l’hôpital", True),
                          c("Douleur non contrôlée", True)], 1, .45)]},
    # CR Medadom : courrier d'adressage mentionnant la demarche et la conduite a tenir transmise au patient
    {"voix": "Et adressez avec un courrier : | votre démarche, | et la conduite à tenir donnée au patient.",
     "el": [("etiquette", "Le courrier d’adressage", 0),
            ("pastille", "Votre démarche", 1), ("pastille", "La conduite à tenir donnée au patient", 2),
            ("dessin", d("iu_07_hopital"), 0)]},
    # diapo 30 : tumefaction, douleur de l'epididyme ou du testicule d'apparition aigue ; diagnostic differentiel :
    # torsion du cordon spermatique (urgence) ; ECBU systematique ; homme sexuellement actif, quel que soit son age :
    # PCR C. trachomatis et N. gonorrhoeae sur 1er jet d'urine
    {"voix": "[serious] Une bourse douloureuse, d’apparition aiguë ? D’abord, la torsion du cordon : c’est une "
             "urgence. | Sinon, épididymite ou orchite : un E.C.B.U.… | et chez l’homme sexuellement actif, quel que "
             "soit son âge, une P.C.R. Klamydia et gonocoque, sur le premier jet.",
     "el": [("etiquette", "Bourse douloureuse aiguë", 0),
            ("pastille!", f"Torsion du cordon{NB}: <b>urgence</b>", 0),
            ("pastille", f"Épididymite, orchite{NB}: <b>ECBU</b>", 1),
            ("pastille", f"Sexuellement actif, quel que soit l’âge{NB}: PCR Chlamydia et gonocoque, 1er{NB}jet", 2),
            ("dessin", d("iu_08_chrono"), 0)]},
    # diapos 36, 37 : bilan systematique des le 1er episode : IPSS, echographie des voies urinaires avec RPM,
    # toucher rectal « a distance de l'episode infectieux » (dit : une fois l'infection passee, car « a distance »
    # se comprendrait « en teleconsultation ») ; PSA non systematique, si necessaire au moins 3 mois apres l'infection
    {"voix": "[warm] Dès le premier épisode, un bilan : | le score I.P.S.S., une échographie des voies urinaires avec "
             "le résidu post-mictionnel… | et un toucher rectal, une fois l’infection passée. | Le P.S.A. ? Pas systématique ; si "
             "besoin, au moins trois mois après l’infection.",
     "el": [("etiquette", "Dès le 1er épisode", 0), ("titre", "Le bilan", 0),
            ("pastille", "Score IPSS, écho des voies urinaires + résidu post-mictionnel", 1),
            ("pastille", "Toucher rectal, une fois l’infection passée", 2),
            ("pastille!", f"PSA non systématique{NB}: si besoin, ≥{NB}3{NB}mois après l’infection", 3),
            ("dessin", d("iu_09_echographie"), 0)]},
    # la fin, dans une 2e prise (Romain, 30/10/2026 : « la dernière slide doit inciter à nous rejoindre, la voix
    # doit donner envie »). Arguments repris mot pour mot de la page de recrutement MEDADOM validée par MEDADOM
    # (LP-MEDADOM-comparatif-final, 28/10/2026) : contrat salarié de 5 à 10 h par semaine en complément de votre
    # activité, depuis chez vous, sur les créneaux de votre choix, 7 j/7 de 6 h à 23 h, facturation et tiers
    # payant gérés, support médical en temps réel ; « postuler en 2 minutes », « réponse sous 48 h ». Les classes
    # virtuelles : le compte rendu de la classe virtuelle MEDADOM du 25/02/2026, source de ce reel
    {"voix": "[warm] Et si vous téléconsultiez… depuis chez vous ? | Avec Médadom : un contrat salarié, de cinq à "
             "dix heures par semaine, en complément de votre activité. | Vos créneaux, sept jours sur sept, de six "
             "heures à vingt-trois heures. | La facturation et le tiers payant ? Gérés pour vous. | Et vous n’êtes "
             "jamais seul : un support médical en temps réel… et des classes virtuelles, comme celle d’où vient "
             "cette vidéo.",
     "prise": 2,
     "el": [("etiquette", "Rejoindre Medadom", 0),
            ("titre", f"Téléconsultez depuis <span class='surligne'>chez vous</span>", 0),
            ("criteres", [c(f"Contrat salarié, 5 à 10{NB}h par semaine, en complément de votre activité", True)], 1, .3),
            ("criteres", [c(f"Vos créneaux, 7{NB}j/7, de 6{NB}h à 23{NB}h", True)], 2, .3),
            ("criteres", [c("Facturation et tiers payant gérés pour vous", True)], 3, .3),
            ("criteres", [c("Support médical en temps réel", True), c("Classes virtuelles de formation", True)],
             4, 1.6)]},
    {"voix": "[excited] Vous êtes médecin généraliste ? | Rejoignez Médadom ! | Postulez en deux minutes… réponse "
             "sous quarante-huit heures.",
     "prise": 2,
     "el": [("titre", f"Vous êtes médecin généraliste{NB}?", 0),
            ("fort", "<span class='surligne'>Rejoignez Medadom</span>", 1),
            ("pastille!", f"Postulez en 2{NB}minutes · <b>réponse sous 48{NB}h</b>", 2),
            ("telephone", orig("iu_01_medecin_teleconsultation"), 0, "38% 50%")]},
]

DECOR = """<div class="lumiere"></div><div class="trame"></div>
<div class="forme a" style="left:-280px;top:1180px;width:760px;height:760px"></div>
<div class="forme b" style="left:640px;top:-120px;width:620px;height:620px"></div>
<div class="entete"><img src="photos/medadom/logo_net.png"><span>Professionnel</span></div>"""


def elements(liste):
    out = []
    for e in liste:
        genre, contenu, etape = e[0], e[1], e[2]
        if genre == "etiquette":
            out.append({"genre": "etiquette", "texte": contenu, "etape": etape})
        elif genre in ("pastille", "pastille!", "barree"):
            out.append({"genre": "pastille", "texte": contenu, "etape": etape, "alerte": genre == "pastille!",
                        "barree": genre == "barree"})
        elif genre == "criteres":
            out.append({"genre": "criteres", "items": contenu, "etape": etape, "pas": e[3]})
        elif genre == "chiffre":
            out.append({"genre": "chiffre", "valeur": contenu, "etape": etape,
                        "prefixe": e[3] if len(e) > 3 else "", "suffixe": e[4] if len(e) > 4 else ""})
        elif genre == "dessin":
            out.append({"genre": "dessin", "etape": etape, **contenu})
        elif genre == "telephone":
            out.append({"genre": "telephone", "src": contenu, "etape": etape, "position": e[3]})
        else:
            out.append({"genre": genre, "html": contenu, "etape": etape})
    return out


def variables(theme):
    return ";".join(f"--{k}:{v}" for k, v in theme.items())


def couverture(carre):
    """Couverture (image a part, non lue). 9:16 : texte centre, dessin en bas, dans le recadrage 4:5.
    Carre (LinkedIn) : texte a gauche, dessin a droite."""
    c_, dess = COUVERTURE, d(COUVERTURE["dessin"])
    h = 1080 if carre else 1920
    if carre:
        style = """.entete { left: 64px; top: 64px; } .entete img { height: 46px; }
.bloc { position: absolute; left: 64px; width: 560px; top: 0; bottom: 0; display: flex; flex-direction: column;
  justify-content: center; align-items: flex-start; gap: 26px; }
.etiquette { font-size: 36px; } .titre { font-size: 74px; line-height: 1.06; letter-spacing: -1.4px; }
.sous { font-weight: 700; font-size: 42px; line-height: 1.15; }"""
        place = f"""let h = 820, w = h * r; if (w > 540) {{ w = 540; h = w / r; }}
  const bas = {str(dess["bas"]).lower()};
  Object.assign(document.getElementById('d').style, {{ left: (1080 - w) + 'px', top: (bas ? 1100 - h : 540 - h / 2) + 'px', width: w + 'px', height: h + 'px' }});"""
    else:
        style = """.entete { left: 0; right: 0; top: 330px; justify-content: center; }
.entete img { height: 52px; } .entete span { font-size: 30px; padding: 6px 16px 8px; }
.bloc { position: absolute; left: 80px; right: 80px; top: 450px; display: flex; flex-direction: column;
  align-items: center; text-align: center; gap: 34px; }
.etiquette { font-size: 44px; } .titre { font-size: 100px; line-height: 1.05; letter-spacing: -2px; }
.sous { font-weight: 700; font-size: 60px; line-height: 1.1; margin-top: -6px; }"""
        place = """const haut = document.querySelector('.bloc').getBoundingClientRect().bottom;
  let h = 1946 - (haut + 30), w = h * r; if (w > 1000) { w = 1000; h = w / r; }
  Object.assign(document.getElementById('d').style, { left: (540 - w / 2) + 'px', top: (1946 - h) + 'px', width: w + 'px', height: h + 'px' });"""
    page = ICI / f"couverture_{NOM}{'_carre' if carre else ''}.html"
    page.write_text(f"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<link rel="stylesheet" href="reel2.css"><style>
:root {{ {variables(THEME)} }}
html, body {{ height: {h}px; }}
{style}
.titre .surligne {{ margin: 10px 0 14px; }}
.dessin {{ position: absolute; }}
</style></head><body>{DECOR}
<div class="bloc"><div class="etiquette">{c_["etiquette"]}</div><div class="titre">{c_["titre"]}</div><div class="sous">{c_["sous"]}</div></div>
<div class="dessin" id="d"><img src="{dess["src"]}"></div>
<script>
document.fonts.ready.then(() => {{
  const r = {dess["ratio"]};
  {place}
  const rs = [...document.querySelector('.bloc').children].map(e => e.getBoundingClientRect());
  window.BLOC = [Math.min(...rs.map(x => x.left)), Math.min(...rs.map(x => x.top)),
                 Math.max(...rs.map(x => x.right)), Math.max(...rs.map(x => x.bottom))];
  window.PRET = true;
}});
</script></body></html>""", encoding="utf-8")
    from playwright.sync_api import sync_playwright
    SORTIE.mkdir(parents=True, exist_ok=True)
    sortie = SORTIE / f"couverture_{'1x1_linkedin' if carre else '9x16_instagram_facebook'}.png"
    with sync_playwright() as p:
        nav = p.chromium.launch(channel="chrome", args=["--allow-file-access-from-files"])
        pg = nav.new_page(viewport={"width": 1080, "height": h})
        pg.goto(page.as_uri(), wait_until="domcontentloaded")
        pg.wait_for_function("window.PRET === true", timeout=60000)
        pg.wait_for_timeout(300)
        bloc = pg.evaluate("window.BLOC")
        pg.screenshot(path=str(sortie))
        nav.close()
    zone = (40, 40, 1040, 1040) if carre else (60, 285, 1020, 1635)
    if bloc[0] < zone[0] or bloc[1] < zone[1] or bloc[2] > zone[2] or bloc[3] > zone[3]:
        raise SystemExit(f"[!] couverture : texte hors zone {bloc}")
    print(sortie, "texte", [round(x) for x in bloc])


def ff(*a):
    r = subprocess.run(["ffmpeg", "-v", "error", "-y", *a], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit("ffmpeg : " + r.stderr[-1200:])


TAUX_ANALYSE = 16000


def pcm_mono(f):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(f), "-f", "f32le", "-ac", "1", "-ar", str(TAUX_ANALYSE), "-"],
                       capture_output=True, check=True)
    return np.frombuffer(r.stdout, dtype="<f4")


def blanc_proche(son, t, avant=0.4, apres=1.0, pas=0.03):
    """Milieu de la fenetre de pas s la plus silencieuse dans [t - avant, t + apres]."""
    n = int(pas * TAUX_ANALYSE)
    i0, i1 = int(max(0, t - avant) * TAUX_ANALYSE), int(min(len(son) / TAUX_ANALYSE, t + apres) * TAUX_ANALYSE)
    f = son[i0:i1 - (i1 - i0) % n].reshape(-1, n)
    k = int(np.argmin((f ** 2).mean(axis=1)))
    return (i0 + k * n + n / 2) / TAUX_ANALYSE


def duree(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                 str(f)], capture_output=True, text=True).stdout)


def main():
    essai = "--essai" in sys.argv
    formats = [sys.argv[sys.argv.index("--format") + 1]] if "--format" in sys.argv else ["9x16", "1x1"]
    travail = ICI / "travail" / NOM
    travail.mkdir(parents=True, exist_ok=True)
    for f in formats:
        couverture(f == "1x1")

    # 1. voix : deux prises lues chacune d'une traite. La 1re porte le contenu ; la 2e, la fin (scenes
    # "prise": 2), d'un autre ton (Romain, 30/10/2026 : « elle doit donner envie »). La 1re garde dans son
    # texte l'ancienne fin (PRISE1_SUITE) : son cache reste valable (prise approuvee, aucun credit), et
    # le son est coupe avant cette ancienne fin.
    groupes = [[k for k, s in enumerate(SCENES) if s.get("prise", 1) == g] for g in (1, 2)]
    groupes = [g for g in groupes if g]
    prises = []
    for n, g in enumerate(groupes):
        textes, debuts = [], []
        pos = 0
        for k in g:
            morceaux = [m.strip() for m in SCENES[k]["voix"].split("|")]
            p, starts = pos, []
            for m in morceaux:
                starts.append(p)
                p += len(m) + 1
            textes.append(" ".join(morceaux))
            debuts.append(starts)
            pos += len(textes[-1]) + 1
        texte = " ".join(textes)
        lu = texte + (" " + PRISE1_SUITE if n == 0 and len(groupes) > 1 else "")
        if "--sans-voix" in sys.argv:        # mise en page seule : instants estimes, aucun credit ElevenLabs
            mp3, car = None, list(lu)
            t0s = [i / 15.0 for i in range(len(lu))]
            t1s = [t + 1 / 15.0 for t in t0s]
        else:
            mp3, al = voix.synthese(lu, EMILIE, travail / "voix_emilie", "eleven_v3", None)
            al = al.get("alignment", al)
            assert "".join(al["characters"]) == lu, "horodatage et texte ne correspondent pas"
            car, t0s, t1s = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
        fin_texte = max(t1s[:len(texte)])
        # fin de la prise : au milieu du blanc qui suit son texte (avant l'ancienne fin, s'il y en a une)
        if len(lu) > len(texte):
            suite = next(j for j in range(len(texte) + 1, len(lu)) if lu[j].isalnum())
            coupe = (fin_texte + t0s[suite]) / 2
        else:
            coupe = (duree(mp3) if mp3 else fin_texte + 0.5)
        prises.append({"mp3": mp3, "car": car, "t0s": t0s, "debuts": debuts, "fin_texte": fin_texte,
                       "coupe": coupe})

    def instant(pr, i, decalage):
        """Debut de la premiere lettre prononcee a partir de la position i (hors indications)."""
        dans = False
        for j in range(i, len(pr["car"])):
            ch = pr["car"][j]
            if ch == "[":
                dans = True
            elif ch == "]":
                dans = False
            elif not dans and ch.isalnum():
                return pr["t0s"][j] / TEMPO + decalage
        raise ValueError(i)

    decalages, t = [], DEBUT_VOIX            # debut de chaque prise dans le reel
    for pr in prises:
        decalages.append(t)
        t += pr["coupe"] / TEMPO + ECART_PRISES
    fin_voix = decalages[-1] + prises[-1]["fin_texte"] / TEMPO
    etapes_de = {}
    for g, pr, dec in zip(groupes, prises, decalages):
        for k, starts in zip(g, pr["debuts"]):
            etapes_de[k] = [max(0.15, instant(pr, p, dec) - AVANCE) for p in starts]
    scenes = []
    for k, s in enumerate(SCENES):
        etapes = etapes_de[k]
        scenes.append({"debut": 0.0 if k == 0 else etapes[0] - 0.25, "etapes": etapes,
                       "elements": elements(s["el"])})
    for k in range(len(scenes) - 1):
        scenes[k]["fin"] = scenes[k + 1]["debut"]
    scenes[-1]["fin"] = fin_voix + TENUE
    # pauses : un silence insere dans la voix a la fin d'une scene, qui decale toutes les suivantes
    pauses = []
    for k, s in enumerate(SCENES[:-1]):
        p = s.get("pause", 0)
        if not p:
            continue
        pauses.append((scenes[k]["fin"], p))
        scenes[k]["fin"] += p
        for sc in scenes[k + 1:]:
            sc["debut"] += p
            sc["fin"] += p
            sc["etapes"] = [t + p for t in sc["etapes"]]
    fin_voix += sum(p for _, p in pauses)
    total = scenes[-1]["fin"] + FIN
    for k, s in enumerate(scenes):
        print(f"scene {k + 1} : {s['debut']:6.2f} -> {s['fin']:6.2f} s, temps " +
              ", ".join(f"{t:.2f}" for t in s["etapes"]))
    print(f"voix : {fin_voix - DEBUT_VOIX:.1f} s ; reel : {total:.1f} s ; {len(prises)} prise(s)")

    # 2. pages (controlables avec planche_reel.py), puis rendu image par image
    pages = {}
    for f in formats:
        donnees = {"theme": THEME, "scenes": scenes, "fin": scenes[-1]["fin"], "duree": total,
                   "logo": "photos/medadom/logo_net.png", "format": {"carre": f == "1x1"},
                   # LinkedIn n'a pas de lien en bio : le lien est dans la publication
                   "bio": "Le lien est dans le post" if f == "1x1" else "Le lien est en bio"}
        page = ICI / f"reel_{NOM}_{f}.html"
        page.write_text(f"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<link rel="stylesheet" href="reel2.css"><style>sub {{ font-size: .62em; vertical-align: -.18em; }}</style></head><body>{DECOR}
<script>window.DONNEES = {json.dumps(donnees, ensure_ascii=False)};</script>
<script src="node_modules/gsap/dist/gsap.min.js"></script>
<script src="moteur_reel2.js"></script></body></html>""", encoding="utf-8")
        pages[f] = page
        print(page)
    if essai:
        return

    # 3. son : voix posee, musique effacee sous la voix, -14 LUFS
    # les prises bout a bout (chacune coupee a sa fin), separees par ECART_PRISES, apres DEBUT_VOIX
    voix_brute = travail / "voix_brute.wav"
    entrees, filtres = [], []
    for i, pr in enumerate(prises):
        entrees += ["-i", str(pr["mp3"])]
        pad = f",apad=pad_dur={ECART_PRISES:.3f}" if i < len(prises) - 1 else ""
        filtres.append(f"[{i}:a]atrim=0:{pr['coupe']:.3f},asetpts=PTS-STARTPTS,atempo={TEMPO},"
                       f"loudnorm=I=-16:TP=-2,aresample=48000,aformat=channel_layouts=stereo{pad}[p{i}]")
    filtres.append("".join(f"[p{i}]" for i in range(len(prises))) +
                   f"concat=n={len(prises)}:v=0:a=1,adelay={int(DEBUT_VOIX * 1000)}:all=1[v]")
    ff(*entrees, "-filter_complex", ";".join(filtres), "-map", "[v]", "-ac", "2", str(voix_brute))
    # une pause se pose dans le vrai blanc le plus proche : l'horodatage de la voix avance parfois de
    # 0,3 s sur le son, et une coupe a l'instant calcule tranchait la fin d'un mot (Romain, 30/10/2026)
    son = pcm_mono(voix_brute)
    pauses = [(blanc_proche(son, t), p) for t, p in pauses]
    voix_wav = travail / "voix_posee.wav"
    coupes = [0.0] + [t for t, _ in pauses] + [None]
    filtres, noms = [], []
    for i in range(len(coupes) - 1):
        fin_seg = f":{coupes[i + 1]:.3f}" if coupes[i + 1] is not None else ""
        pad = f",apad=pad_dur={pauses[i][1]:.3f}" if i < len(pauses) else ""
        filtres.append(f"[0:a]atrim={coupes[i]:.3f}{fin_seg},asetpts=PTS-STARTPTS{pad}[s{i}]")
        noms.append(f"[s{i}]")
    filtres.append(f"{''.join(noms)}concat=n={len(noms)}:v=0:a=1,apad=whole_dur={total:.3f},atrim=0:{total:.3f}[v]")
    ff("-i", str(voix_brute), "-filter_complex", ";".join(filtres), "-map", "[v]", "-ac", "2", str(voix_wav))
    musique_wav = travail / "musique.wav"
    # la musique (101 s) est plus courte que le reel : elle s'enchaine sur elle-meme, fondu de 4 s au raccord
    ff("-i", str(MUSIQUE), "-i", str(MUSIQUE), "-filter_complex",
       "[0:a][1:a]acrossfade=d=4:c1=tri:c2=tri,"
       f"atrim=0:{total:.3f},loudnorm=I=-26:TP=-3,aresample=48000,afade=t=in:d=0.8,"
       f"afade=t=out:st={total - 2.2:.3f}:d=2.2", "-ac", "2", str(musique_wav))
    if duree(musique_wav) < total - 0.05:
        raise SystemExit("[!] musique plus courte que le reel")
    melange = travail / "melange.wav"
    ff("-i", str(musique_wav), "-i", str(voix_wav), "-filter_complex",
       "[1:a]asplit=2[v][sc];[0:a][sc]sidechaincompress=threshold=0.015:ratio=10:attack=25:release=450[m];"
       "[m][v]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5,aresample=48000[out]",
       "-map", "[out]", "-t", f"{total:.3f}", str(melange))
    SORTIE.mkdir(parents=True, exist_ok=True)
    controles = ",".join(f"{s['fin'] - 0.5:.2f}" for s in scenes) + f",{total - 0.5:.2f}"
    for f, page in pages.items():
        final = SORTIE / f"medadom_iu_{f}{'_instagram_facebook' if f == '9x16' else '_linkedin'}.mp4"
        r = subprocess.run([sys.executable, str(ICI / "rendu.py"), str(page), str(final), "--audio", str(melange),
                            "--controles", controles, "--hauteur", "1080" if f == "1x1" else "1920"])
        if r.returncode:
            raise SystemExit(f"[!] rendu {f} interrompu")
        print(final, f"{duree(final):.1f} s")


if __name__ == "__main__":
    main()
