"""Reel Medadom Professionnel : l'infection urinaire de l'homme en teleconsultation (29-30/10/2026), en 9:16
(Instagram, Facebook) et en carre (LinkedIn). Le modele des prochains reels : voir CLAUDE.md.

    python fabrique.py reels/iu_homme.py

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
  anterieurs aux recommandations de juin 2026 et ne sont pas repris.
Verifie le 29/10/2026 sur les fiches recospilf.infectiologie.com actualisees les 22-23/09/2026 ; AMM : Monuril,
Selexid (femme), nitrofurantoine « pas indiquee chez l'homme » (courrier ANSM 2023) : mention a l'ecran."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from fabrique import NB, c, d, orig

NOM = "iu"
SORTIE = Path.home() / "Downloads" / "Medadom_reel_infection_urinaire_homme"   # livrables
THEME = {"fond": "#A7CCED", "encre": "#1F1650", "accent": "#1C5FAE", "accent-pale": "rgba(28,95,174,.20)",
         "clair": "#D2E6F8", "ombre-fond": "rgba(30,70,140,.22)", "rouge": "#E0393E"}
COUVERTURE = {"etiquette": "Téléconsultation",
              "titre": f"Infection urinaire<br><span class='surligne'>chez l’homme</span>",
              "sous": "Ce qui change en 2026", "dessin": "iu_01_medecin_teleconsultation"}
# ancienne fin, toujours lue dans la 1re prise (cache de la prise approuvee le 29/10) puis coupee au montage
PRISE1_SUITE = "[cheerful] Vous êtes médecin généraliste ? Rejoignez Médadom."

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
