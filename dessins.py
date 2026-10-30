"""Dessins Canva des reels Medadom : telechargement des exports, puis detourage (fond uni retire).

    python dessins.py telecharger <nom>=<url d'export Canva> [<nom>=<url> ...]
    python dessins.py detourer [<nom> ...]          (sans nom : tous les dessins pas encore detoures)
    python dessins.py planche <prefixe>             (planche de controle des dessins detoures, ex. iu_)

Les dessins se generent dans Canva (outil generate-image, la vignette de reference en image) puis s'exportent
en pleine definition par une page 1264 x 1264 du design de travail DAHYkUMJaDM (add_page + insert_fill, commit,
export PNG) : voir CLAUDE.md. dessins/<nom>.png garde le fond (ecran du telephone) ; dessins/detoures/<nom>.png
est le sujet seul, recadre, pour les scenes."""
import json
import sys
import urllib.request
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

ICI = Path(__file__).resolve().parent
SRC = ICI / "dessins"
DST = SRC / "detoures"
TOL_DUR, TOL_DOUX = 9.0, 19.0     # distance de couleur au fond : en dessous, fond ; au-dela, sujet


def telecharger(paires):
    SRC.mkdir(exist_ok=True)
    for paire in paires:
        nom, url = paire.split("=", 1)
        cible = SRC / f"{nom}.png"
        with urllib.request.urlopen(url, timeout=120) as r:
            cible.write_bytes(r.read())
        print(cible.name, cible.stat().st_size // 1024, "Ko")


def detourer_un(f):
    """Le fond relie aux bords devient transparent, bord adouci ; l'image est recadree sur le sujet."""
    im = Image.open(f).convert("RGB")
    a = np.asarray(im).astype(float)
    h, w, _ = a.shape
    fond = np.median(np.concatenate([a[0, :], a[:, 0], a[:, -1]]), axis=0)
    dist = np.sqrt(((a - fond) ** 2).sum(axis=2))
    lab, _ = ndimage.label(dist < TOL_DOUX)
    touche = set(np.unique(np.concatenate([lab[0, :], lab[:, 0], lab[:, -1]]))) - {0}
    zone = np.isin(lab, list(touche))
    alpha = np.where(zone, np.clip((dist - TOL_DUR) / (TOL_DOUX - TOL_DUR), 0, 1), 1.0)
    sujet = alpha > 0.5                       # petites taches isolees du fond (bruit) retirees
    lab2, n2 = ndimage.label(sujet)
    if n2:
        tailles = ndimage.sum(sujet, lab2, range(1, n2 + 1))
        alpha[np.isin(lab2, [i + 1 for i, t in enumerate(tailles) if t < 400])] = 0
    rgba = im.copy()
    rgba.putalpha(Image.fromarray((alpha * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8)))
    boite = rgba.getbbox()
    DST.mkdir(exist_ok=True)
    rgba.crop(boite).save(DST / f.name, optimize=True)
    print(f"{f.name:40} {rgba.crop(boite).size}  touche le bas : {boite[3] >= h - 2}  fond : "
          f"{[int(round(x)) for x in fond]}")


def planche(prefixe):
    ims = [Image.open(f).convert("RGBA") for f in sorted(DST.glob(f"{prefixe}*.png"))]
    cote = 300
    pl = Image.new("RGB", (len(ims) * (cote + 10) + 10, cote + 20), (200, 220, 240))
    for i, im in enumerate(ims):
        im.thumbnail((cote, cote))
        pl.paste(im, (10 + i * (cote + 10) + (cote - im.width) // 2, 10 + cote - im.height), im)
    sortie = DST / f"planche_{prefixe}.png"
    pl.save(sortie)
    print(sortie)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    action, args = sys.argv[1], sys.argv[2:]
    if action == "telecharger":
        telecharger(args)
    elif action == "detourer":
        fichiers = [SRC / f"{n}.png" for n in args] if args else \
            [f for f in sorted(SRC.glob("*.png")) if not f.name.startswith("planche") and not (DST / f.name).exists()]
        for f in fichiers:
            detourer_un(f)
    elif action == "planche":
        planche(args[0] if args else "")
    else:
        raise SystemExit(__doc__)
