"""Planche de controle d'un reel Medadom version 2 (9:16 ou carre) : pour chaque scene, une image a mi-chemin
et une image une fois tous ses textes poses, puis la carte de fin ; marges verifiees a chaque image, et
l'echelle de texte retenue par scene.

    python planche_reel2.py reel_iu_9x16.html"""
import io
import json
import re
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

page_html = Path(sys.argv[1]).resolve()
donnees = json.loads(re.search(r"window\.DONNEES = (\{.*?\});</script>", page_html.read_text(encoding="utf-8"), re.S).group(1))
carre = donnees.get("format", {}).get("carre")
h = 1080 if carre else 1920
instants = []
for s in donnees["scenes"]:
    instants += [s["etapes"][-1] + 0.25, s["fin"] - 0.55]
instants.append(donnees["duree"] - 0.5)
ims, ecarts = [], []
with sync_playwright() as p:
    nav = p.chromium.launch(channel="chrome", args=["--allow-file-access-from-files"])
    page = nav.new_page(viewport={"width": 1080, "height": h})
    page.goto(page_html.as_uri() + "?rendu=1", wait_until="domcontentloaded")
    page.wait_for_function("window.PRET === true", timeout=60000)
    print("echelles de texte :", page.evaluate("window.echelles()"))
    for i, t in enumerate(instants):
        page.evaluate(f"window.seek({t})")
        if i % 2 or i == len(instants) - 1:          # marges une fois les entrees finies (pas en plein glissement)
            ecarts += [f"t={t:.2f}  {e}" for e in page.evaluate("window.verifier()")]
        ims.append(Image.open(io.BytesIO(page.screenshot())).convert("RGB").resize((360, h // 3)))
    nav.close()
cols = 6
lignes = (len(ims) + cols - 1) // cols
pl = Image.new("RGB", (cols * 370, lignes * (h // 3 + 10)), "white")
for i, im in enumerate(ims):
    pl.paste(im, ((i % cols) * 370, (i // cols) * (h // 3 + 10)))
sortie = page_html.with_name(page_html.stem + "_planche.png")
pl.save(sortie)
print(sortie)
print("marges : " + ("OK" if not ecarts else "\n  " + "\n  ".join(ecarts)))
