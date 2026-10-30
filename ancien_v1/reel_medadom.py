"""Reels Medadom Professionnel (20/10/2026) : Octobre rose et diabete de type 2.

    python reel_medadom.py <rose|dt2> [--essai]

1. Voix d'Emilie (ElevenLabs v3, d'une seule prise, en cache) ; les instants de chaque
   texte a l'ecran sont tires de l'horodatage de la voix (separateur « | » dans le texte lu).
   La couverture n'est pas lue : c'est une image a part (couverture_<nom>.png), le reel
   commence directement sur le contenu (Romain, 20/10/2026).
2. Page HTML (moteur_reel.js + reel.css) avec ces instants, rendue image par image (rendu.py).
3. Son : voix + musique des reels Medadom (« Echo Sax No.4 »), qui s'efface sous la voix,
   puis -14 LUFS.
--essai : voix, instants, page et couverture, sans le rendu video.

Textes : comptes rendus de classe virtuelle Medadom (29/10/2025, 26/11/2025), valides par
Romain le 20/10/2026 ; chiffres tels que dans les comptes rendus."""
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image

ICI = Path(__file__).resolve().parent
R = Path(r"C:\Users\NR SMART\tools\lcdg-reel")
sys.path.insert(0, str(R))
from dotenv import load_dotenv
load_dotenv(R / ".env")
from lcdg import voix

EMILIE = "d3AXX0BlgJHYFCuH9X88"   # femme_agee du catalogue : Emilie, voix choisie par Romain
TEMPO = 1.05                # rythme des voix v3 des reels (charte LCDG)
DEBUT_VOIX = 0.6            # s : la voix commence apres l'apparition du premier ecran
AVANCE = 0.12               # s : un texte apparait juste avant d'etre dit
TENUE = 0.9                 # s : apres la derniere phrase, avant la carte de fin
FIN = 3.2                   # s : carte de fin (logo, « Le lien est en bio »)
MUSIQUE = Path(r"C:\Users\NR SMART\Downloads\Caleb Arredondo - Echo Sax No.4.mp3")
SORTIE = Path(r"C:\Users\NR SMART\Downloads\Medadom_reels_Octobre_rose_DT2")
NB = "\u00a0"


def d(nom):
    """Dessin detoure (sans fond) : chemin, rapport largeur/hauteur, ancre en bas ou non."""
    f = ICI / "dessins_canva" / "detoures" / f"{nom}.png"
    im = Image.open(f)
    bas = im.getchannel("A").crop((0, im.height - 3, im.width, im.height)).getextrema()[1] > 200
    return {"src": f"dessins_canva/detoures/{nom}.png", "ratio": im.width / im.height, "bas": bas}


def orig(nom):
    """Dessin entier (avec son fond) : pour l'ecran du telephone."""
    return f"dessins_canva/{nom}.png"


REELS = {
    "rose": {
        "theme": {"fond": "#ED9FCC", "encre": "#1F1650", "accent": "#C2337E", "accent-pale": "rgba(194,51,126,.20)",
                  "clair": "#F7C6E2", "ombre-fond": "rgba(150,40,110,.22)"},
        "couverture": {"etiquette": "Octobre rose",
                       "titre": f"Inquiétudes<br>à la palpation{NB}:<br><span class='surligne'>gérer le stress</span>",
                       "sous": "en téléconsultation",
                       "dessin": "rose_01_medecin_teleconsultation"},
        "scenes": [
            {"voix": "Le cancer du sein reste le cancer le plus fréquent chez la femme : soixante et un mille deux "
                     "cent quatorze nouveaux cas en deux mille vingt-trois. | C’est la première cause de décès par "
                     "cancer chez la femme.",
             "el": [("etiquette", "Octobre rose", 0), ("texte", "Le cancer le plus fréquent chez la femme", 0),
                    ("chiffre", 61214, 0), ("legende", "nouveaux cas de cancer du sein <b>en 2023</b>", 0),
                    ("pastille!", "1re cause de décès par cancer chez la femme", 1),
                    ("dessin", d("rose_07_ruban"), 0)]},
            {"voix": "D’abord, l’écoute active. | Laissez-la décrire la boule, la douleur, l’écoulement, | et leur "
                     "contexte d’apparition.",
             "el": [("etiquette", "1. L’écoute active", 0), ("pastille", "La boule", 1), ("pastille", "La douleur", 1),
                    ("pastille", "L’écoulement", 1), ("pastille", "Leur contexte d’apparition", 2),
                    ("dessin", d("rose_03_ecoute"), 0)]},
            {"voix": "Ensuite, les bonnes questions. | Ses antécédents personnels et familiaux de cancer du sein. | "
                     "Son contexte gynécologique. | Et ses traitements : contraception hormonale, ou traitement "
                     "hormonal de la ménopause.",
             "el": [("etiquette", "2. Les bonnes questions", 0),
                    ("pastille", "Antécédents personnels et familiaux de cancer du sein", 1),
                    ("pastille", "Contexte gynécologique : grossesses, allaitement, règles, ménopause", 2),
                    ("pastille", "Traitements : contraception hormonale, THM", 3),
                    ("dessin", d("rose_04_questions"), 0)]},
            {"voix": "Rassurez-la, sans rien exclure. | Les symptômes bénins sont fréquents. | Mais n’employez pas "
                     "le mot cancer sans preuve histologique.",
             "el": [("etiquette", "3. Rassurer, sans exclure", 0),
                    ("texte", "Les symptômes bénins sont <span class='souligne'>fréquents</span>.", 1),
                    ("pastille!", "Pas de mot « cancer » sans preuve histologique", 2),
                    ("dessin", d("rose_02_patiente_appel"), 0)]},
            {"voix": "Expliquez les limites de la téléconsultation : un examen en présentiel peut être nécessaire. | "
                     "Un examen des seins a-t-il été fait il y a moins d’un an ? | La Haute Autorité de santé le "
                     "recommande chaque année, dès vingt-cinq ans.",
             "el": [("etiquette", "Les limites de la téléconsultation", 0),
                    ("texte", "Un examen en présentiel peut être <span class='souligne'>nécessaire</span>.", 0),
                    ("pastille", "Examen des seins de moins d’un an ?", 1),
                    ("pastille", "HAS : chaque année dès 25 ans", 2),
                    ("telephone", orig("rose_01_medecin_teleconsultation"), 0, "30% 50%")]},
            {"voix": "Une masse, un écoulement pathologique ou un doute ? | Prescrivez une imagerie diagnostique : "
                     "mammographie et échographie. | Et si la suspicion est forte, orientez rapidement vers un "
                     "circuit de sénologie.",
             "el": [("etiquette", "4. Orienter", 0), ("texte", "Masse, écoulement pathologique ou doute ?", 0),
                    ("pastille", "Mammographie et échographie diagnostiques", 1),
                    ("pastille!", "Suspicion forte : circuit de sénologie rapide", 2),
                    ("dessin", d("rose_06_imagerie"), 0)]},
            {"voix": "[cheerful] Vous êtes médecin généraliste ? | Rejoignez Médadom.",
             "el": [("titre", "Vous êtes médecin généraliste ?", 0),
                    ("fort", "<span class='surligne'>Rejoignez Medadom</span>", 1),
                    ("telephone", orig("rose_01_medecin_teleconsultation"), 0, "30% 50%")]},
        ],
    },
    "dt2": {
        "theme": {"fond": "#F69F91", "encre": "#1F1650", "accent": "#2FA36B", "accent-pale": "rgba(47,163,107,.22)",
                  "clair": "#FBC8BE", "ombre-fond": "rgba(190,70,50,.20)"},
        "couverture": {"etiquette": "Diabète de type 2",
                       "titre": f"Prévenir<br><span class='surligne'>par la nutrition</span>",
                       "sous": "en téléconsultation",
                       "dessin": "dt2_01_medecin_teleconsultation"},
        "scenes": [
            {"voix": "Face au diabète de type deux, votre rôle : dépister et prévenir, chez les patients à risque. | "
                     "Puis orienter vers la nutrition, l’activité physique et l’éducation thérapeutique.",
             "el": [("etiquette", "Diabète de type 2", 0), ("titre", "Votre rôle", 0),
                    ("pastille", "Dépister et prévenir chez les patients à risque", 0),
                    ("pastille", "Orienter : nutrition, activité physique, éducation thérapeutique", 1),
                    ("dessin", d("dt2_02_glycemie"), 0)]},
            {"voix": "À chaque consultation, surveillez le poids. | Une perte d’au moins cinq pour cent apporte une "
                     "amélioration métabolique significative.",
             "el": [("etiquette", "Le poids, à chaque consultation", 0), ("chiffre", 5, 1, "≥ ", f"{NB}%"),
                    ("legende", "de poids perdu : une amélioration métabolique <span class='souligne'>significative</span>", 1),
                    ("dessin", d("dt2_06_balance"), 0)]},
            {"voix": "Côté alimentation, la méditerranéenne reste la référence. | Aucun aliment n’est interdit : "
                     "seules les quantités varient. | Et les régimes restrictifs sont contre-productifs.",
             "el": [("etiquette", "L’alimentation", 0), ("pastille", "Méditerranéenne : la référence", 0),
                    ("pastille", "Aucun aliment interdit, seules les quantités varient", 1),
                    ("pastille!", "Régimes restrictifs : contre\u2011productifs", 2),
                    ("dessin", d("dt2_03_assiette"), 0)]},
            {"voix": "Préférez le fait maison. | Orientez vers un nutritionniste, | avec un suivi psychologique en "
                     "cas de troubles du comportement alimentaire.",
             "el": [("etiquette", "Accompagner", 0), ("pastille", "Préférer le fait maison", 0),
                    ("pastille", "Orienter vers un nutritionniste", 1),
                    ("pastille", "Suivi psychologique si troubles du comportement alimentaire", 2),
                    ("dessin", d("dt2_04_cuisine"), 0)]},
            {"voix": "Côté activité physique : en prédiabète, elle réduit de cinquante pour cent le risque de "
                     "progression, sur environ trois ans. | Et une activité physique adaptée peut être prescrite.",
             "el": [("etiquette", "L’activité physique", 0), ("chiffre", 50, 0, "−", f"{NB}%"),
                    ("legende", "de risque de progression du prédiabète, sur environ 3 ans", 0),
                    ("pastille", "Activité physique adaptée : sur prescription", 1),
                    ("dessin", d("dt2_05_marche"), 0)]},
            {"voix": "Une prise en charge pluriprofessionnelle, dont vous êtes le chef d’orchestre. | N’hésitez pas "
                     "à déléguer.",
             "el": [("etiquette", "Le généraliste, chef d’orchestre", 0),
                    ("texte", "Une prise en charge <span class='souligne'>pluriprofessionnelle</span>", 0),
                    ("fort", "<span class='surligne'>N’hésitez pas à déléguer</span>", 1),
                    ("dessin", d("dt2_07_equipe"), 0)]},
            {"voix": "[cheerful] Vous êtes médecin généraliste ? | Rejoignez Médadom.",
             "el": [("titre", "Vous êtes médecin généraliste ?", 0),
                    ("fort", "<span class='surligne'>Rejoignez Medadom</span>", 1),
                    ("telephone", orig("dt2_01_medecin_teleconsultation"), 0, "68% 50%")]},
        ],
    },
}

DECOR = """<div class="lumiere"></div><div class="trame"></div>
<div class="forme a" style="left:-280px;top:1180px;width:760px;height:760px"></div>
<div class="forme b" style="left:640px;top:-120px;width:620px;height:620px"></div>
<div class="entete"><img src="photos/medadom/logo_net.png"><span>Professionnel</span></div>"""


def elements(liste):
    out = []
    for e in liste:
        genre, contenu, etape = e[0], e[1], e[2]
        if genre in ("etiquette", "pastille", "pastille!"):
            out.append({"genre": "pastille" if genre.startswith("pastille") else genre, "texte": contenu,
                        "etape": etape, "alerte": genre == "pastille!"})
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


def couverture(nom, cfg):
    """Couverture du reel (image a part, non lue) : 1080 x 1920, contenu dans le recadrage 4:5."""
    c, dess = cfg["couverture"], d(cfg["couverture"]["dessin"])
    page = ICI / f"couverture_{nom}.html"
    page.write_text(f"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<link rel="stylesheet" href="reel.css"><style>
:root {{ {variables(cfg["theme"])} }}
.entete {{ left: 0; right: 0; top: 330px; justify-content: center; }}
.entete img {{ height: 52px; }} .entete span {{ font-size: 30px; padding: 6px 16px 8px; }}
.bloc {{ position: absolute; left: 80px; right: 80px; top: 450px; display: flex; flex-direction: column;
  align-items: center; text-align: center; gap: 34px; }}
.etiquette {{ font-size: 44px; }}
.titre {{ font-size: 100px; line-height: 1.05; letter-spacing: -2px; }}
.sous {{ font-weight: 700; font-size: 60px; line-height: 1.1; margin-top: -6px; }}
.titre .surligne {{ margin: 10px 0 14px; }}
.dessin {{ position: absolute; }}
</style></head><body>{DECOR}
<div class="bloc"><div class="etiquette">{c["etiquette"]}</div><div class="titre">{c["titre"]}</div><div class="sous">{c["sous"]}</div></div>
<div class="dessin" id="d"><img src="{dess["src"]}"></div>
<script>
document.fonts.ready.then(() => {{
  const b = document.querySelector('.bloc').getBoundingClientRect(), r = {dess["ratio"]};
  let h = 1946 - (b.bottom + 30), w = h * r;
  if (w > 1000) {{ w = 1000; h = w / r; }}
  Object.assign(document.getElementById('d').style, {{ left: (540 - w / 2) + 'px', top: (1946 - h) + 'px', width: w + 'px', height: h + 'px' }});
  window.BLOC = [b.left, b.top, b.right, b.bottom];
  window.PRET = true;
}});
</script></body></html>""", encoding="utf-8")
    from playwright.sync_api import sync_playwright
    SORTIE.mkdir(parents=True, exist_ok=True)
    sortie = SORTIE / f"couverture_{nom}.png"
    with sync_playwright() as p:
        nav = p.chromium.launch(channel="chrome", args=["--allow-file-access-from-files"])
        pg = nav.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto(page.as_uri(), wait_until="domcontentloaded")
        pg.wait_for_function("window.PRET === true", timeout=60000)
        pg.wait_for_timeout(300)
        bloc = pg.evaluate("window.BLOC")
        pg.screenshot(path=str(sortie))
        nav.close()
    if bloc[1] < 285 or bloc[3] > 1635 or bloc[0] < 60 or bloc[2] > 1020:
        raise SystemExit(f"[!] couverture : texte hors du recadrage 4:5 {bloc}")
    print(sortie, "texte", [round(x) for x in bloc])


def ff(*a):
    r = subprocess.run(["ffmpeg", "-v", "error", "-y", *a], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit("ffmpeg : " + r.stderr[-1200:])


def duree(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                 str(f)], capture_output=True, text=True).stdout)


def main():
    nom = sys.argv[1]
    essai = "--essai" in sys.argv
    cfg = REELS[nom]
    travail = ICI / "travail" / nom
    travail.mkdir(parents=True, exist_ok=True)
    couverture(nom, cfg)

    # 1. voix d'une seule prise ; position de chaque temps dans le texte lu
    textes, debuts = [], []          # debuts[i] = positions (dans le texte complet) des temps de la scene i
    pos = 0
    for s in cfg["scenes"]:
        morceaux = [m.strip() for m in s["voix"].split("|")]
        p, starts = pos, []
        for m in morceaux:
            starts.append(p)
            p += len(m) + 1
        textes.append(" ".join(morceaux))
        debuts.append(starts)
        pos += len(textes[-1]) + 1
    texte = " ".join(textes)
    mp3, al = voix.synthese(texte, EMILIE, travail / "voix_emilie", "eleven_v3", None)
    al = al.get("alignment", al)
    assert "".join(al["characters"]) == texte, "horodatage et texte ne correspondent pas"
    car, t0s, t1s = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]

    def instant(i):
        """Debut de la premiere lettre prononcee a partir de la position i (hors indications)."""
        dans = False
        for j in range(i, len(car)):
            c = car[j]
            if c == "[":
                dans = True
            elif c == "]":
                dans = False
            elif not dans and c.isalnum():
                return t0s[j] / TEMPO + DEBUT_VOIX
        raise ValueError(i)

    fin_voix = max(t1s) / TEMPO + DEBUT_VOIX
    scenes = []
    for k, s in enumerate(cfg["scenes"]):
        etapes = [max(0.15, instant(p) - AVANCE) for p in debuts[k]]
        scenes.append({"debut": 0.0 if k == 0 else etapes[0] - 0.25, "etapes": etapes,
                       "elements": elements(s["el"])})
    for k in range(len(scenes) - 1):
        scenes[k]["fin"] = scenes[k + 1]["debut"]
    scenes[-1]["fin"] = fin_voix + TENUE
    total = scenes[-1]["fin"] + FIN
    for k, s in enumerate(scenes):
        print(f"scene {k + 1} : {s['debut']:6.2f} -> {s['fin']:6.2f} s, temps " +
              ", ".join(f"{t:.2f}" for t in s["etapes"]))
    print(f"voix : {fin_voix - DEBUT_VOIX:.1f} s ; reel : {total:.1f} s ; {len(texte)} caracteres")

    # 2. page (controlable avec planche_reel.py des l'essai), puis rendu image par image
    donnees = {"theme": cfg["theme"], "scenes": scenes, "fin": scenes[-1]["fin"], "duree": total,
               "logo": "photos/medadom/logo_net.png"}
    page = ICI / f"reel_{nom}.html"
    page.write_text(f"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<link rel="stylesheet" href="reel.css"></head><body>{DECOR}
<script>window.DONNEES = {json.dumps(donnees, ensure_ascii=False)};</script>
<script src="node_modules/gsap/dist/gsap.min.js"></script>
<script src="moteur_reel.js"></script></body></html>""", encoding="utf-8")
    if essai:
        print(page)
        return

    # 3. son : voix posee, musique effacee sous la voix, -14 LUFS
    voix_wav = travail / "voix_posee.wav"
    ff("-i", str(mp3), "-af", f"atempo={TEMPO},loudnorm=I=-16:TP=-2,aresample=48000,"
       f"adelay={int(DEBUT_VOIX * 1000)}:all=1,apad=whole_dur={total:.3f},atrim=0:{total:.3f}",
       "-ac", "2", str(voix_wav))
    musique_wav = travail / "musique.wav"
    ff("-i", str(MUSIQUE), "-t", f"{total:.3f}", "-af",
       f"loudnorm=I=-26:TP=-3,aresample=48000,afade=t=in:d=0.8,afade=t=out:st={total - 2.2:.3f}:d=2.2",
       "-ac", "2", str(musique_wav))
    if duree(musique_wav) < total - 0.05:
        raise SystemExit("[!] musique plus courte que le reel")
    melange = travail / "melange.wav"
    ff("-i", str(musique_wav), "-i", str(voix_wav), "-filter_complex",
       "[1:a]asplit=2[v][sc];[0:a][sc]sidechaincompress=threshold=0.015:ratio=10:attack=25:release=450[m];"
       "[m][v]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5,aresample=48000[out]",
       "-map", "[out]", "-t", f"{total:.3f}", str(melange))
    SORTIE.mkdir(parents=True, exist_ok=True)
    final = SORTIE / f"medadom_{nom}.mp4"
    controles = ",".join(f"{s['fin'] - 0.5:.2f}" for s in scenes) + f",{total - 0.5:.2f}"
    r = subprocess.run([sys.executable, str(ICI / "rendu.py"), str(page), str(final), "--audio", str(melange),
                        "--controles", controles])
    if r.returncode:
        raise SystemExit("[!] rendu interrompu")
    print(final, f"{duree(final):.1f} s")


if __name__ == "__main__":
    main()
