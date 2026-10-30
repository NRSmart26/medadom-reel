"""Planche de controle d'un reel Medadom : une image par scene, une fois ses textes poses,
et la carte de fin ; marges verifiees a chaque image.  python planche_reel.py reel_rose.html"""
import io
import json
import re
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

page_html = Path(sys.argv[1]).resolve()
donnees = json.loads(re.search(r"window\.DONNEES = (\{.*?\});</script>", page_html.read_text(encoding="utf-8"), re.S).group(1))
instants = [s["fin"] - 0.55 for s in donnees["scenes"]] + [donnees["duree"] - 0.5]
ims, ecarts = [], []
with sync_playwright() as p:
    nav = p.chromium.launch(channel="chrome", args=["--allow-file-access-from-files"])
    page = nav.new_page(viewport={"width": 1080, "height": 1920})
    page.goto(page_html.as_uri() + "?rendu=1", wait_until="domcontentloaded")
    page.wait_for_function("window.PRET === true", timeout=60000)
    for t in instants:
        page.evaluate(f"window.seek({t})")
        ecarts += [f"t={t:.2f}  {e}" for e in page.evaluate("window.verifier()")]
        ims.append(Image.open(io.BytesIO(page.screenshot())).convert("RGB").resize((360, 640)))
    nav.close()
pl = Image.new("RGB", (len(ims) * 370, 640), "white")
for i, im in enumerate(ims):
    pl.paste(im, (i * 370, 0))
sortie = page_html.with_name(page_html.stem + "_planche.png")
pl.save(sortie)
print(sortie, "| marges :", ecarts or "OK")
