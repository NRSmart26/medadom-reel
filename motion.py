"""Motion design Medadom : reels courts sans voix, en musique (novembre 2026). Une piece = un fichier
motion/<piece>.js (sa direction artistique), deux versions (« marque » : le symbole et le nom ; « info » : un
fait source et une ouverture vers la pratique), deux formats (9:16 et carre LinkedIn).

    python motion.py <piece> --essai      pages et controle des marges a chaque demi-seconde, sans rendu
    python motion.py <piece> --planche    idem, plus une planche d'images par version et par format
    python motion.py <piece>              son, rendu des 4 videos et couvertures, dans SORTIE
    options : --version marque|info, --format 9x16|1x1
    python motion.py <piece> --voix       la version info avec voix, en carre LinkedIn (--format 9x16 : Instagram) ;
                                          avec --essai ou --planche : temps estimes si la voix n'est pas en cache,
                                          aucun credit

Rien d'autre dans le dossier pendant un rendu (voir CLAUDE.md, « Format et rendu »)."""
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
import fabrique
import voix

SORTIE = Path.home() / "Downloads" / "Medadom_novembre_2026"
TRAVAIL = ICI / "travail" / "motion"
MES_SAX = 3.157  # Echo Sax No.4 : une mesure (4 temps a ~76 BPM), mesuree sur le fichier
PIECES = {
    # la musique d'Octobre rose (Romain, 30/10/2026) ; la section rythmique entre a 2,68 s du fichier
    "movember": {"musique": ICI / "musique" / "echo_sax_no4.mp3", "debut": 2.68, "mesure": MES_SAX,
                 "durees": {"marque": 4 * MES_SAX, "info": 8 * MES_SAX}, "couverture": 7.7,
                 # voix (Romain, 03/11/2026 : « sur les reels linkedin info, pas marque ») : (repere, texte lu,
                 # pause apres) ; « nom » tombe sur l'entree du titre, chaque repere declenche un element
                 "voix": {"id": voix.EMILIE, "cale_nom": MES_SAX + .1, "segments": [
                     ("intro", "[warm] Médecins généralistes : novembre, c’est", 0),
                     ("nom", "Movember, le mois de la santé des hommes.", 1.0),
                     ("p1", "Le cancer de la prostate, le cancer du testicule, la santé mentale et la prévention du suicide :", 0),
                     ("p1b", "novembre, on en parle.", .6),
                     ("p2", "[serious] Le cancer de la prostate est", 0),
                     ("p2a", "le plus fréquent chez l’homme :", 0),
                     ("p2b", "plus de cinquante-cinq mille", 0),
                     ("p2c", "nouveaux cas estimés en France en deux mille vingt-quatre,", 0),
                     ("p2d", "et plus de neuf mille décès en deux mille vingt-trois.", 1.0),
                     ("p3", "[warm] En consultation comme en téléconsultation :", 0),
                     ("p3b", "parlons-en.", 1.3),
                     ("signature", "Médadom Professionnel.", 0)]}},
    # « aucune » : video muette, possible pour une piece. Ici, la musique fournie par Romain (03/11/2026), jouee de
    # 8,75 s a 29,6 s du fichier (silence avant, arret net apres), bouclee en fondu ; mesure : le rythme de l'animation
    "sans_tabac": {"musique": ICI / "musique" / "sans_tabac_recording-00_32.mp3", "debut": 8.75, "fin": 29.6, "mesure": 3.0,
                   "durees": {"marque": 12.5, "info": 25.5}, "couverture": 8.6,
                   "voix": {"id": voix.EMILIE, "cale_nom": 6.15, "segments": [
                       ("intro", "[warm] Médecins généralistes : du premier au trente novembre, c’est le", 0),
                       ("nom", "Mois sans tabac.", 1.2),
                       ("p1", "[matter-of-fact] Cinquante-cinq pour cent", 0),
                       ("p1b", "des fumeurs quotidiens souhaitent arrêter de fumer.", .9),
                       ("p2", "Arrêter de fumer pendant trente jours", 0),
                       ("p2b", "multiplie par cinq", 0),
                       ("p2c", "les chances d’arrêter à long terme.", .9),
                       ("p3", "[serious] Les substituts nicotiniques :", 0),
                       ("p3a", "la plupart sont remboursés à", 0),
                       ("p3b", "soixante-cinq pour cent", 0),
                       ("p3c", "par l’Assurance maladie, sur prescription.", 1.4),
                       ("signature", "[warm] Médadom Professionnel.", 0)]}},
}
FORMATS = {"9x16": 1920, "1x1": 1080}
FIN_VOIX = 3.0  # s : la carte de fin, depuis le debut de la signature dite


def ff(*args):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args], check=True)


def page(piece, version, f, duree=None, temps=None):
    p = PIECES[piece]
    donnees = {"piece": piece, "version": version, "format": f, "mesure": p["mesure"],
               "duree": round(duree if duree else p["durees"][version], 4)}
    if temps:
        donnees["temps"] = temps
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


def source_musique(piece, duree):
    """(fichier, debut) de la musique ; si la piece borne sa musique (« fin ») et qu'elle est plus courte que le
    reel, elle s'enchaine une fois sur elle-meme, en fondu de 1,5 s au raccord."""
    p = PIECES[piece]
    if "fin" not in p or p["fin"] - p["debut"] >= duree:
        return p["musique"], p["debut"]
    long = p["fin"] - p["debut"]
    if 2 * long - 1.5 < duree:
        raise SystemExit(f"[!] {piece} : musique plus courte que le reel ({duree:.1f} s), meme bouclee une fois")
    boucle = TRAVAIL / f"{piece}_boucle.wav"
    entree = ["-ss", f"{p['debut']:.3f}", "-t", f"{long:.3f}", "-i", str(p["musique"])]
    ff(*entree, *entree, "-filter_complex", "[0:a][1:a]acrossfade=d=1.5:c1=tri:c2=tri", str(boucle))
    return boucle, 0.0


def son(piece, version):
    """Extrait de la musique a la duree exacte du reel : entree nette, fondu de sortie, -14 LUFS."""
    p = PIECES[piece]
    duree = p["durees"][version]
    wav = TRAVAIL / f"{piece}_{version}.wav"
    fichier, debut = source_musique(piece, duree)
    ff("-ss", f"{debut:.3f}", "-i", str(fichier), "-af",
       f"afade=t=in:d=0.04,afade=t=out:st={duree - 1.4:.3f}:d=1.4,loudnorm=I=-14:TP=-1.5,aresample=48000,"
       f"apad=whole_dur={duree:.3f}", "-t", f"{duree:.3f}", "-ac", "2", str(wav))
    return wav


def calage_voix(piece, payer):
    """Instants des reperes, tires de l'horodatage de la voix (estimes sans credit si elle n'est pas en cache et
    que payer est faux). La voix demarre pour que « nom » tombe sur l'entree du titre."""
    v = PIECES[piece]["voix"]
    segments = v["segments"]
    texte = " ".join(s[1] for s in segments)
    dossier = TRAVAIL / "voix"
    mp3, js = voix.chemins(texte, v["id"], dossier)
    if payer or (mp3.exists() and js.exists()):
        mp3, al = voix.synthese(texte, v["id"], dossier)
        al = al.get("alignment", al)
        assert "".join(al["characters"]) == texte, "horodatage et texte ne correspondent pas"
        t0s, t1s = al["character_start_times_seconds"], al["character_end_times_seconds"]
    else:
        mp3, t0s = None, [i / 15.0 for i in range(len(texte))]
        t1s = [t + 1 / 15.0 for t in t0s]

    def premier(i):   # premier caractere lu d'un segment : ni indication [entre crochets], ni ponctuation
        dans = False
        for j in range(i, len(texte)):
            if texte[j] == "[":
                dans = True
            elif texte[j] == "]":
                dans = False
            elif not dans and texte[j].isalnum():
                return t0s[j] / fabrique.TEMPO
        raise ValueError(i)

    bruts, fins, pos = {}, {}, 0
    for nom, t, _ in segments:
        bruts[nom] = premier(pos)
        fins[nom] = max(t1s[pos:pos + len(t)]) / fabrique.TEMPO
        pos += len(t) + 1
    debut = max(.3, v["cale_nom"] - bruts["nom"])
    temps, deja, pauses = {}, 0.0, []
    for nom, _, p in segments:
        temps[nom] = round(debut + bruts[nom] + deja, 3)
        if p:
            pauses.append((debut + fins[nom], p))   # instant dans la voix brute, sans les pauses precedentes
            deja += p
    return {"mp3": mp3, "debut": debut, "temps": temps, "pauses": pauses, "total": temps["signature"] + FIN_VOIX}


def son_voix(piece, c):
    """Voix posee (pauses dans le vrai blanc, comme fabrique.son), musique effacee sous la voix s'il y en a une,
    -14 LUFS, a la duree exacte du reel."""
    p, total = PIECES[piece], c["total"]
    brute, posee = TRAVAIL / f"{piece}_voix_brute.wav", TRAVAIL / f"{piece}_voix_posee.wav"
    melange = TRAVAIL / f"{piece}_voix.wav"
    ff("-i", str(c["mp3"]), "-af", f"atempo={fabrique.TEMPO},loudnorm=I=-16:TP=-2,aresample=48000,"
       f"aformat=channel_layouts=stereo,adelay={int(c['debut'] * 1000)}:all=1", str(brute))
    analyse = fabrique.pcm_mono(brute)
    pauses = [(fabrique.blanc_proche(analyse, t), d) for t, d in c["pauses"]]
    coupes = [0.0] + [t for t, _ in pauses] + [None]
    filtres, noms = [], []
    for i in range(len(coupes) - 1):
        fin = f":{coupes[i + 1]:.3f}" if coupes[i + 1] is not None else ""
        pad = f",apad=pad_dur={pauses[i][1]:.3f}" if i < len(pauses) else ""
        filtres.append(f"[0:a]atrim={coupes[i]:.3f}{fin},asetpts=PTS-STARTPTS{pad}[s{i}]")
        noms.append(f"[s{i}]")
    filtres.append(f"{''.join(noms)}concat=n={len(noms)}:v=0:a=1,apad=whole_dur={total:.3f},atrim=0:{total:.3f}[v]")
    ff("-i", str(brute), "-filter_complex", ";".join(filtres), "-map", "[v]", "-ac", "2", str(posee))
    if p["musique"] == "aucune":
        ff("-i", str(posee), "-af", "loudnorm=I=-14:TP=-1.5,aresample=48000", "-t", f"{total:.3f}", str(melange))
        return melange
    musique = TRAVAIL / f"{piece}_voix_musique.wav"
    fichier, debut = source_musique(piece, total)
    ff("-ss", f"{debut:.3f}", "-i", str(fichier), "-af",
       f"atrim=0:{total:.3f},loudnorm=I=-26:TP=-3,aresample=48000,afade=t=in:d=0.04,"
       f"afade=t=out:st={total - 2.2:.3f}:d=2.2", "-ac", "2", str(musique))
    ff("-i", str(musique), "-i", str(posee), "-filter_complex",
       "[1:a]asplit=2[v][sc];[0:a][sc]sidechaincompress=threshold=0.015:ratio=10:attack=25:release=450[m];"
       "[m][v]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5,aresample=48000[out]",
       "-map", "[out]", "-t", f"{total:.3f}", str(melange))
    return melange


def main_voix(piece, essai, avec_planche, f="1x1"):
    """La version info avec voix, en carre LinkedIn ou en 9:16 : la voix commande les plans."""
    TRAVAIL.mkdir(parents=True, exist_ok=True)
    payer = not (essai or avec_planche)
    c = calage_voix(piece, payer)
    print("voix en cache" if c["mp3"] else "temps estimes (aucun credit)", f"; {c['total']:.2f} s ;", c["temps"])
    chemin = page(piece, "voix", f, duree=c["total"], temps=c["temps"])
    with sync_playwright() as pw:
        nav = pw.chromium.launch(channel="chrome", args=["--allow-file-access-from-files", "--disable-gpu"])
        pg = ouvrir(nav, chemin, f)
        ecarts = controler(pg, c["total"])
        print(f"{piece} voix {f} : " + ("marges OK" if not ecarts else "\n    " + "\n    ".join(ecarts[:12])))
        if avec_planche:
            feuille = TRAVAIL / f"{piece}_voix_{f}_planche.png"
            planche(pg, c["total"], feuille, n=20)
            print("  ", feuille)
        nav.close()
    if not payer:
        return
    if ecarts:
        raise SystemExit("[!] marges : rendu arrete")
    SORTIE.mkdir(parents=True, exist_ok=True)
    wav = son_voix(piece, c)
    nom = "9x16_instagram_facebook" if f == "9x16" else "1x1_linkedin"
    final = SORTIE / f"medadom_{piece}_info_voix_{nom}.mp4"
    r = subprocess.run([sys.executable, str(ICI / "rendu.py"), str(chemin), str(final), "--audio", str(wav),
                        "--hauteur", str(FORMATS[f])])
    if r.returncode:
        raise SystemExit(f"[!] rendu {piece} voix interrompu")


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in PIECES:
        raise SystemExit(__doc__ + f"\npieces : {', '.join(PIECES)}")
    piece = sys.argv[1]
    if "--voix" in sys.argv:
        f = sys.argv[sys.argv.index("--format") + 1] if "--format" in sys.argv else "1x1"
        return main_voix(piece, "--essai" in sys.argv, "--planche" in sys.argv, f)
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
