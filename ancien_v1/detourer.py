"""Detoure les dessins Canva (fond uni rose ou saumon) : le fond relie aux bords devient
transparent, avec un bord adouci, puis l'image est recadree sur le sujet. Romain, 20/10/2026 :
« elles ne doivent pas avoir cet arriere-plan rose, il doit juste y avoir le medecin ».

    python detourer.py           -> dessins_canva/detoures/*.png + fonds.json (couleur de fond par theme)"""
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

ICI = Path(__file__).resolve().parent
SRC = ICI / "dessins_canva"
DST = SRC / "detoures"
DST.mkdir(exist_ok=True)
TOL_DUR, TOL_DOUX = 9.0, 19.0     # distance couleur au fond : en dessous, fond ; au-dela, sujet

fonds = {}
for f in sorted(SRC.glob("*.png")):
    if f.name.startswith("planche"):
        continue
    im = Image.open(f).convert("RGB")
    a = np.asarray(im).astype(float)
    h, w, _ = a.shape
    bord = np.concatenate([a[0, :], a[:, 0], a[:, -1]])
    fond = np.median(bord, axis=0)
    fonds.setdefault(f.name.split("_")[0], []).append(fond)
    d = np.sqrt(((a - fond) ** 2).sum(axis=2))
    proche = d < TOL_DOUX
    lab, n = ndimage.label(proche)
    touche = set(np.unique(np.concatenate([lab[0, :], lab[:, 0], lab[:, -1]]))) - {0}
    zone = np.isin(lab, list(touche))
    # alpha : 0 dans le fond, montee douce entre les deux seuils, 1 dans le sujet
    alpha = np.clip((d - TOL_DUR) / (TOL_DOUX - TOL_DUR), 0, 1)
    alpha = np.where(zone, alpha, 1.0)
    # petites taches isolees du fond (bruit) retirees
    sujet = alpha > 0.5
    lab2, n2 = ndimage.label(sujet)
    if n2:
        tailles = ndimage.sum(sujet, lab2, range(1, n2 + 1))
        petits = np.isin(lab2, [i + 1 for i, t in enumerate(tailles) if t < 400])
        alpha[petits] = 0
    a_img = Image.fromarray((alpha * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
    rgba = im.copy()
    rgba.putalpha(a_img)
    boite = rgba.getbbox()
    rgba = rgba.crop(boite)
    touche_bas = boite[3] >= h - 2
    rgba.save(DST / f.name, optimize=True)
    print(f"{f.name:40} {rgba.size}  bas touche : {touche_bas}")
moy = {k: [int(round(x)) for x in np.median(np.array(v), axis=0)] for k, v in fonds.items()}
(DST / "fonds.json").write_text(json.dumps(moy), encoding="utf-8")
print(moy)
