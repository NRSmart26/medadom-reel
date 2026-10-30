"""Fabrique des reels Medadom Professionnel (Med Academy) : un fichier de contenu par reel, dans reels/.

    python fabrique.py reels/<reel>.py --sans-voix --essai    mise en page seule (aucun credit), pages + couvertures
    python planche.py reel_<nom>_9x16.html                     controle des pages (idem pour _1x1)
    python fabrique.py reels/<reel>.py --essai                 + la voix (credits ElevenLabs), sans rendu video
    python fabrique.py reels/<reel>.py [--format 9x16|1x1]     voix, son et rendu des deux formats
    --sortie <dossier> : livrables ailleurs que dans SORTIE (un essai qui n'ecrase rien)

Le fichier de contenu (voir reels/iu_homme.py, le modele) definit : NOM, SORTIE (dossier des livrables), THEME,
COUVERTURE, SCENES ; et au besoin VOIX (Emilie par defaut), MUSIQUE, PRISE1_SUITE. Il importe d'ici les aides de
redaction : NB, c(), d(), orig().

Une scene : {"voix": "texte lu | temps suivant | ...", "el": [(genre, contenu, temps, ...), ...]}, et au besoin
"pause" (s de silence apres la scene, le temps de lire), "prise": 2 (la fin, lue a part d'un autre ton).
Genres : etiquette, titre, texte, fort, legende, note (petite mention), pastille, pastille! (alerte), barree
(ce qui n'est plus recommande), criteres (cases qui se cochent : [c(...), ...], temps, pas), chiffre (valeur,
temps, prefixe, suffixe), dessin (d("nom")), telephone (orig("nom"), temps, cadrage). Le temps d'un element est
le numero du « | » de la voix ou il arrive (0 = debut de la scene).

Le moteur (moteur.js, reel.css) ajuste le texte de chaque scene a la plus grande taille ou il tient : le texte
d'abord, le dessin s'adapte (Romain, 29/10/2026 : « ils vont voir ca sur un mobile »)."""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
import voix

NB = " "
TEMPO = 1.05                # rythme des voix v3 (meme reglage que les reels LCDG)
DEBUT_VOIX = 0.6            # s : la voix commence apres l'apparition du premier ecran
AVANCE = 0.12               # s : un texte apparait juste avant d'etre dit
TENUE = 0.9                 # s : apres la derniere phrase, avant la carte de fin
FIN = 3.2                   # s : carte de fin (logo, lien)
ECART_PRISES = 1.0          # s : blanc entre la prise du contenu et celle de la fin
MUSIQUE = ICI / "musique" / "echo_sax_no4.mp3"   # la musique des reels Medadom (101 s, bouclee au besoin)
TAUX_ANALYSE = 16000
DECOR = """<div class="lumiere"></div><div class="trame"></div>
<div class="forme a" style="left:-280px;top:1180px;width:760px;height:760px"></div>
<div class="forme b" style="left:640px;top:-120px;width:620px;height:620px"></div>
<div class="entete"><img src="photos/medadom/logo_net.png"><span>Professionnel</span></div>"""


# ------------------------------------------------------------------ aides de redaction (fichiers de reels/)
def d(nom):
    """Dessin detoure (sans fond) : chemin, rapport largeur/hauteur, ancre en bas ou non."""
    im = Image.open(ICI / "dessins" / "detoures" / f"{nom}.png")
    bas = im.getchannel("A").crop((0, im.height - 3, im.width, im.height)).getextrema()[1] > 200
    return {"src": f"dessins/detoures/{nom}.png", "ratio": im.width / im.height, "bas": bas}


def orig(nom):
    """Dessin entier (avec son fond) : pour l'ecran du telephone."""
    return f"dessins/{nom}.png"


def c(texte, large=False):
    """Une case de criteres ; large : sur toute la largeur."""
    return {"texte": texte, "large": large}


# ------------------------------------------------------------------ moteur
def charger(chemin):
    spec = importlib.util.spec_from_file_location("reel", chemin)
    reel = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(reel)
    return reel


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


def couverture(reel, carre):
    """Couverture (image a part, non lue). 9:16 : texte centre, dessin en bas, dans le recadrage 4:5.
    Carre (LinkedIn) : texte a gauche, dessin a droite."""
    c_, dess = reel.COUVERTURE, d(reel.COUVERTURE["dessin"])
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
    page = ICI / f"couverture_{reel.NOM}{'_carre' if carre else ''}.html"
    page.write_text(f"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<link rel="stylesheet" href="reel.css"><style>
:root {{ {variables(reel.THEME)} }}
html, body {{ height: {h}px; }}
{style}
.titre .surligne {{ margin: 10px 0 14px; }}
.dessin {{ position: absolute; }}
</style></head><body>{DECOR}
<div class="bloc"><div class="etiquette">{c_["etiquette"]}</div><div class="titre">{c_["titre"]}</div><div class="sous">{c_["sous"]}</div></div>
<div class="dessin" id="d"><img src="{dess["src"]}"></div>
<script>
// polices et dessin charges avant de placer et de capturer : sinon la couverture peut sortir sans son dessin
Promise.all([document.fonts.ready, document.querySelector('#d img').decode()]).then(() => {{
  const r = {dess["ratio"]};
  {place}
  const rs = [...document.querySelector('.bloc').children].map(e => e.getBoundingClientRect());
  window.BLOC = [Math.min(...rs.map(x => x.left)), Math.min(...rs.map(x => x.top)),
                 Math.max(...rs.map(x => x.right)), Math.max(...rs.map(x => x.bottom))];
  window.PRET = true;
}});
</script></body></html>""", encoding="utf-8")
    from playwright.sync_api import sync_playwright
    Path(reel.SORTIE).mkdir(parents=True, exist_ok=True)
    sortie = Path(reel.SORTIE) / f"couverture_{'1x1_linkedin' if carre else '9x16_instagram_facebook'}.png"
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


def duree(f):
    sortie = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                             str(f)], capture_output=True, text=True).stdout.strip()
    return float(sortie) if sortie else 0.0


def pcm_mono(f):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(f), "-f", "f32le", "-ac", "1", "-ar", str(TAUX_ANALYSE),
                        "-"], capture_output=True, check=True)
    return np.frombuffer(r.stdout, dtype="<f4")


def blanc_proche(son, t, avant=0.4, apres=1.0, pas=0.03):
    """Milieu de la fenetre de pas s la plus silencieuse dans [t - avant, t + apres]."""
    n = int(pas * TAUX_ANALYSE)
    i0, i1 = int(max(0, t - avant) * TAUX_ANALYSE), int(min(len(son) / TAUX_ANALYSE, t + apres) * TAUX_ANALYSE)
    f = son[i0:i1 - (i1 - i0) % n].reshape(-1, n)
    k = int(np.argmin((f ** 2).mean(axis=1)))
    return (i0 + k * n + n / 2) / TAUX_ANALYSE


def prises_de(reel, sans_voix, dossier_voix):
    """Les prises de voix : la 1re porte le contenu, la 2e (scenes "prise": 2) la fin, d'un autre ton. La 1re
    peut garder dans son texte une ancienne fin (PRISE1_SUITE) pour reprendre une prise deja payee : le son est
    alors coupe avant elle."""
    voix_id = getattr(reel, "VOIX", voix.EMILIE)
    suite_1 = getattr(reel, "PRISE1_SUITE", "")
    groupes = [[k for k, s in enumerate(reel.SCENES) if s.get("prise", 1) == g] for g in (1, 2)]
    groupes = [g for g in groupes if g]
    prises = []
    for n, g in enumerate(groupes):
        textes, debuts = [], []
        pos = 0
        for k in g:
            morceaux = [m.strip() for m in reel.SCENES[k]["voix"].split("|")]
            p, starts = pos, []
            for m in morceaux:
                starts.append(p)
                p += len(m) + 1
            textes.append(" ".join(morceaux))
            debuts.append(starts)
            pos += len(textes[-1]) + 1
        texte = " ".join(textes)
        lu = texte + (" " + suite_1 if n == 0 and suite_1 else "")
        if sans_voix:                        # mise en page seule : instants estimes, aucun credit
            mp3, car = None, list(lu)
            t0s = [i / 15.0 for i in range(len(lu))]
            t1s = [t + 1 / 15.0 for t in t0s]
        else:
            mp3, al = voix.synthese(lu, voix_id, dossier_voix)
            al = al.get("alignment", al)
            assert "".join(al["characters"]) == lu, "horodatage et texte ne correspondent pas"
            car, t0s, t1s = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
        fin_texte = max(t1s[:len(texte)])
        if len(lu) > len(texte):             # fin de la prise : au milieu du blanc avant l'ancienne fin
            suite = next(j for j in range(len(texte) + 1, len(lu)) if lu[j].isalnum())
            coupe = (fin_texte + t0s[suite]) / 2
        else:
            coupe = duree(mp3) if mp3 else fin_texte + 0.5
        prises.append({"mp3": mp3, "car": car, "t0s": t0s, "debuts": debuts, "groupe": g, "fin_texte": fin_texte,
                       "coupe": coupe, "texte": texte})
    return prises


def calage(reel, prises):
    """Instants de chaque scene et de chaque temps, tires de l'horodatage des prises ; pauses inserees."""
    def instant(pr, i, decalage):
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

    decalages, t = [], DEBUT_VOIX
    for pr in prises:
        decalages.append(t)
        t += pr["coupe"] / TEMPO + ECART_PRISES
    fin_voix = decalages[-1] + prises[-1]["fin_texte"] / TEMPO
    etapes_de = {}
    for pr, dec in zip(prises, decalages):
        for k, starts in zip(pr["groupe"], pr["debuts"]):
            etapes_de[k] = [max(0.15, instant(pr, p, dec) - AVANCE) for p in starts]
    scenes = []
    for k, s in enumerate(reel.SCENES):
        etapes = etapes_de[k]
        scenes.append({"debut": 0.0 if k == 0 else etapes[0] - 0.25, "etapes": etapes,
                       "elements": elements(s["el"])})
    for k in range(len(scenes) - 1):
        scenes[k]["fin"] = scenes[k + 1]["debut"]
    scenes[-1]["fin"] = fin_voix + TENUE
    # pause : un silence insere dans la voix a la fin d'une scene, qui decale toutes les suivantes
    # chaque pause garde son instant dans la voix brute (sans les pauses precedentes), ou son() la pose
    pauses, deja = [], 0.0
    for k, s in enumerate(reel.SCENES[:-1]):
        p = s.get("pause", 0)
        if not p:
            continue
        pauses.append((scenes[k]["fin"] - deja, p))
        deja += p
        scenes[k]["fin"] += p
        for sc in scenes[k + 1:]:
            sc["debut"] += p
            sc["fin"] += p
            sc["etapes"] = [x + p for x in sc["etapes"]]
    fin_voix += sum(p for _, p in pauses)
    return scenes, pauses, fin_voix, scenes[-1]["fin"] + FIN


def pages(reel, scenes, total, formats):
    out = {}
    for f in formats:
        donnees = {"theme": reel.THEME, "scenes": scenes, "fin": scenes[-1]["fin"], "duree": total,
                   "logo": "photos/medadom/logo_net.png", "format": {"carre": f == "1x1"},
                   # LinkedIn n'a pas de lien en bio : le lien est dans la publication
                   "bio": "Le lien est dans le post" if f == "1x1" else "Le lien est en bio"}
        page = ICI / f"reel_{reel.NOM}_{f}.html"
        page.write_text(f"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<link rel="stylesheet" href="reel.css"><style>sub {{ font-size: .62em; vertical-align: -.18em; }}</style></head><body>{DECOR}
<script>window.DONNEES = {json.dumps(donnees, ensure_ascii=False)};</script>
<script src="node_modules/gsap/dist/gsap.min.js"></script>
<script src="moteur.js"></script></body></html>""", encoding="utf-8")
        out[f] = page
        print(page)
    return out


def son(reel, prises, pauses, total, travail):
    """Voix posee (prises bout a bout, pauses dans le vrai blanc), musique effacee sous la voix, -14 LUFS."""
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
    # une pause se pose dans le vrai blanc le plus proche : l'horodatage avance parfois de 0,3 s sur le son, et
    # une coupe a l'instant calcule a tranche la fin d'un mot (reel infection urinaire, 30/10/2026)
    analyse = pcm_mono(voix_brute)
    pauses = [(blanc_proche(analyse, t), p) for t, p in pauses]
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
    musique = Path(getattr(reel, "MUSIQUE", MUSIQUE))
    musique_wav = travail / "musique.wav"
    # la musique est plus courte que le reel : elle s'enchaine sur elle-meme, fondu de 4 s au raccord
    ff("-i", str(musique), "-i", str(musique), "-filter_complex",
       "[0:a][1:a]acrossfade=d=4:c1=tri:c2=tri,"
       f"atrim=0:{total:.3f},loudnorm=I=-26:TP=-3,aresample=48000,afade=t=in:d=0.8,"
       f"afade=t=out:st={total - 2.2:.3f}:d=2.2", "-ac", "2", str(musique_wav))
    if duree(musique_wav) < total - 0.05:
        raise SystemExit("[!] musique plus courte que le reel, meme bouclee une fois")
    melange = travail / "melange.wav"
    ff("-i", str(musique_wav), "-i", str(voix_wav), "-filter_complex",
       "[1:a]asplit=2[v][sc];[0:a][sc]sidechaincompress=threshold=0.015:ratio=10:attack=25:release=450[m];"
       "[m][v]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5,aresample=48000[out]",
       "-map", "[out]", "-t", f"{total:.3f}", str(melange))
    return melange


def main():
    if len(sys.argv) < 2 or not sys.argv[1].endswith(".py"):
        raise SystemExit(__doc__)
    reel = charger(sys.argv[1])
    if "--sortie" in sys.argv:                # livrables ailleurs (un essai sans ecraser ceux du reel)
        reel.SORTIE = Path(sys.argv[sys.argv.index("--sortie") + 1])
    essai, sans_voix = "--essai" in sys.argv, "--sans-voix" in sys.argv
    formats = [sys.argv[sys.argv.index("--format") + 1]] if "--format" in sys.argv else ["9x16", "1x1"]
    travail = ICI / "travail" / reel.NOM
    travail.mkdir(parents=True, exist_ok=True)
    for f in formats:
        couverture(reel, f == "1x1")
    prises = prises_de(reel, sans_voix, travail / "voix")
    scenes, pauses, fin_voix, total = calage(reel, prises)
    for k, s in enumerate(scenes):
        print(f"scene {k + 1} : {s['debut']:6.2f} -> {s['fin']:6.2f} s, temps " +
              ", ".join(f"{t:.2f}" for t in s["etapes"]))
    print(f"voix : {fin_voix - DEBUT_VOIX:.1f} s ; reel : {total:.1f} s ; {len(prises)} prise(s)" +
          ("" if sans_voix else "".join(f"\n  prise {i + 1} : {pr['mp3'].name}" for i, pr in enumerate(prises))))
    les_pages = pages(reel, scenes, total, formats)
    if essai:
        return
    melange = son(reel, prises, pauses, total, travail)
    controles = ",".join(f"{s['fin'] - 0.5:.2f}" for s in scenes) + f",{total - 0.5:.2f}"
    for f, page in les_pages.items():
        final = Path(reel.SORTIE) / f"medadom_{reel.NOM}_{f}{'_instagram_facebook' if f == '9x16' else '_linkedin'}.mp4"
        r = subprocess.run([sys.executable, str(ICI / "rendu.py"), str(page), str(final), "--audio", str(melange),
                            "--controles", controles, "--hauteur", "1080" if f == "1x1" else "1920"])
        if r.returncode:
            raise SystemExit(f"[!] rendu {f} interrompu")
        print(final, f"{duree(final):.1f} s")


if __name__ == "__main__":
    main()
