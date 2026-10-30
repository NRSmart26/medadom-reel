"""Motion design Medadom : reels courts sans voix, en musique (novembre 2026). Une piece = un fichier
motion/<piece>.js (sa direction artistique), deux versions (« marque » : le symbole et le nom ; « info » : un
fait source et une ouverture vers la pratique), deux formats (9:16 et carre LinkedIn).

    python motion.py <piece> --essai      pages et controle des marges a chaque demi-seconde, sans rendu
    python motion.py <piece> --planche    idem, plus une planche d'images par version et par format
    python motion.py <piece>              son, rendu des 4 videos et couvertures, dans SORTIE
    options : --version marque|info, --format 9x16|1x1

Rien d'autre dans le dossier pendant un rendu (voir CLAUDE.md, « Format et rendu »)."""
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

ICI = Path(__file__).resolve().parent
SORTIE = Path.home() / "Downloads" / "Medadom_novembre_2026"
TRAVAIL = ICI / "travail" / "motion"
MES_SAX = 3.157  # Echo Sax No.4 : une mesure (4 temps a ~76 BPM), mesuree sur le fichier
PIECES = {
    # la musique d'Octobre rose (Romain, 30/10/2026) ; la section rythmique entre a 2,68 s du fichier
    "movember": {"musique": ICI / "musique" / "echo_sax_no4.mp3", "debut": 2.68, "mesure": MES_SAX,
                 "durees": {"marque": 4 * MES_SAX, "info": 8 * MES_SAX}, "couverture": 7.7},
    # « aucune » : video muette, Romain ajoute la musique a la publication (30/10/2026)
    "sans_tabac": {"musique": "aucune", "debut": 0.0, "mesure": 3.0,
                   "durees": {"marque": 12.5, "info": 25.5}, "couverture": 8.6},
}
FORMATS = {"9x16": 1920, "1x1": 1080}


def ff(*args):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args], check=True)


def page(piece, version, f):
    p = PIECES[piece]
    donnees = {"piece": piece, "version": version, "format": f, "duree": round(p["durees"][version], 4),
               "mesure": p["mesure"]}
    chemin = ICI / f"motion_{piece}_{version}_{f}.html"
    chemin.write_text(f"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<link rel="stylesheet" href="motion/motion.css"></head><body>
<script>window.DONNEES = {json.dumps(donnees)};</script>
<script src="node_modules/gsap/dist/gsap.min.js"></script>
<script src="motion/commun.js"></script>
<script src="motion/{piece}.js"></script></body></html>""", encoding="utf-8")
    return chemin


def ouvrir(nav, chemin, f):
    pg = nav.new_page(viewport={"width": 1080, "height": FORMATS[f]}, device_scale_factor=1)
    pg.goto(chemin.as_uri() + "?rendu=1")
    pg.wait_for_function("window.PRET === true", timeout=60000)
    return pg


def controler(pg, duree, fps=30):
    """Marges a chaque image (un debord de 0,1 s passait entre deux controles a la demi-seconde, review Codex du
    30/10/2026) ; la frise doit durer exactement la duree prevue."""
    tl = pg.evaluate("window.TL.duration()")
    ecarts = [] if abs(tl - duree) < 0.02 else [f"frise de {tl:.2f} s pour {duree:.2f} s prevues"]
    ecarts += pg.evaluate(f"""() => {{ const e = [];
        for (let i = 0; i < {int(round(duree * fps))}; i++) {{ window.seek(i / {fps});
          window.verifier().forEach(x => e.push(`t=${{(i / {fps}).toFixed(2)}} s  ${{x}}`)); }}
        return e; }}""")
    return ecarts


def planche(pg, duree, sortie, n=15):
    vignettes = []
    for i in range(n):
        t = duree * (i + 0.5) / n
        pg.evaluate(f"window.seek({t})")
        png = TRAVAIL / "_v.png"
        pg.screenshot(path=str(png))
        im = Image.open(png).convert("RGB")
        vignettes.append((t, im.resize((im.width // 3, im.height // 3), Image.LANCZOS)))
    cols = 5
    w, h = vignettes[0][1].size
    feuille = Image.new("RGB", (cols * w + (cols + 1) * 8, ((n + cols - 1) // cols) * (h + 8) + 8), (40, 40, 40))
    for i, (t, v) in enumerate(vignettes):
        feuille.paste(v, (8 + (i % cols) * (w + 8), 8 + (i // cols) * (h + 8)))
    feuille.save(sortie)
    (TRAVAIL / "_v.png").unlink(missing_ok=True)


def couverture(pg, t, sortie):
    pg.evaluate(f"window.seek({t})")
    pg.screenshot(path=str(sortie))


def son(piece, version):
    """Extrait de la musique a la duree exacte du reel : entree nette, fondu de sortie, -14 LUFS."""
    p = PIECES[piece]
    duree = p["durees"][version]
    wav = TRAVAIL / f"{piece}_{version}.wav"
    ff("-ss", f"{p['debut']:.3f}", "-i", str(p["musique"]), "-af",
       f"afade=t=in:d=0.04,afade=t=out:st={duree - 1.4:.3f}:d=1.4,loudnorm=I=-14:TP=-1.5,aresample=48000,"
       f"apad=whole_dur={duree:.3f}", "-t", f"{duree:.3f}", "-ac", "2", str(wav))
    return wav


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in PIECES:
        raise SystemExit(__doc__ + f"\npieces : {', '.join(PIECES)}")
    piece = sys.argv[1]
    choix = lambda opt, tous: [sys.argv[sys.argv.index(opt) + 1]] if opt in sys.argv else tous
    versions, formats = choix("--version", ["marque", "info"]), choix("--format", list(FORMATS))
    essai, avec_planche = "--essai" in sys.argv, "--planche" in sys.argv
    TRAVAIL.mkdir(parents=True, exist_ok=True)
    p = PIECES[piece]
    # avant tout : une musique introuvable n'ecrit rien dans SORTIE (ni couverture, ni video) ;
    # « aucune » est un choix (video muette, musique ajoutee a la publication)
    muette = p["musique"] == "aucune"
    if not (essai or avec_planche or muette) and not (p["musique"] and Path(p["musique"]).exists()):
        raise SystemExit(f"[!] {piece} : pas de musique ({p['musique']}). La choisir avec Romain (gratuite, libre "
                         "d'usage commercial, sans Content ID), la poser dans musique/, puis renseigner musique, "
                         "debut et mesure dans PIECES ; ou « aucune » pour une video muette.")
    pages = {(v, f): page(piece, v, f) for v in versions for f in formats}
    with sync_playwright() as pw:
        nav = pw.chromium.launch(channel="chrome", args=["--allow-file-access-from-files", "--disable-gpu"])
        for (v, f), chemin in pages.items():
            pg = ouvrir(nav, chemin, f)
            ecarts = controler(pg, p["durees"][v])
            print(f"{piece} {v} {f} : " + ("marges OK" if not ecarts else "\n    " + "\n    ".join(ecarts[:12])))
            if avec_planche:
                feuille = TRAVAIL / f"{piece}_{v}_{f}_planche.png"
                planche(pg, p["durees"][v], feuille)
                print("  ", feuille)
            if not essai and not avec_planche and v == "marque":
                SORTIE.mkdir(parents=True, exist_ok=True)
                nom = "9x16_instagram_facebook" if f == "9x16" else "1x1_linkedin"
                couverture(pg, p["couverture"], SORTIE / f"couverture_{piece}_{nom}.png")
            pg.close()
            if ecarts and not essai and not avec_planche:
                raise SystemExit("[!] marges : rendu arrete")
        nav.close()
    if essai or avec_planche:
        return
    for v in versions:
        wav = None if muette else son(piece, v)
        for f in formats:
            nom = "9x16_instagram_facebook" if f == "9x16" else "1x1_linkedin"
            final = SORTIE / f"medadom_{piece}_{v}_{nom}{'_muette' if muette else ''}.mp4"
            r = subprocess.run([sys.executable, str(ICI / "rendu.py"), str(pages[(v, f)]), str(final),
                                "--hauteur", str(FORMATS[f])] + (["--audio", str(wav)] if wav else []))
            if r.returncode:
                raise SystemExit(f"[!] rendu {piece} {v} {f} interrompu")


if __name__ == "__main__":
    main()
