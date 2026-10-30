"""Rendu d'une scene animee Medadom (page HTML + GSAP) en video 1080x1920, image par image.

    python rendu.py <scene.html> <sortie.mp4> [--fps 30] [--audio son.wav] [--debut 0] [--fin T]

La page expose window.TL (frise GSAP en pause), window.seek(t), window.verifier() et
window.PRET. Chrome (celui du poste, sans telechargement) est pilote par Playwright : on
place la frise a chaque instant, on capture, et ffmpeg encode. Avant tout, la zone sure
est controlee a la fin de la frise (tout est alors a l'ecran) : un texte ou un dessin cle
hors des marges arrete le rendu."""
import argparse
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ap = argparse.ArgumentParser()
ap.add_argument("scene")
ap.add_argument("sortie")
ap.add_argument("--fps", type=int, default=30)
ap.add_argument("--audio")
ap.add_argument("--debut", type=float, default=0.0)
ap.add_argument("--fin", type=float)
ap.add_argument("--controles", default="", help="instants supplementaires du controle des marges, ex. 3.5,7")
ap.add_argument("--hauteur", type=int, default=1920, help="1080 pour la version carree (LinkedIn)")
a = ap.parse_args()

scene = Path(a.scene).resolve()
with sync_playwright() as p:
    nav = p.chromium.launch(channel="chrome", args=["--allow-file-access-from-files", "--disable-gpu"])
    page = nav.new_page(viewport={"width": 1080, "height": a.hauteur}, device_scale_factor=1)
    page.goto(scene.as_uri() + "?rendu=1")
    page.wait_for_function("window.PRET === true", timeout=60000)
    duree = page.evaluate("window.TL.duration()")
    fin = min(a.fin or duree, duree)
    instants = [fin] + [float(x) for x in a.controles.split(",") if x]
    ecarts = []
    for t in instants:
        page.evaluate(f"window.seek({t})")
        ecarts += [f"t={t:.2f} s  {e}" for e in page.evaluate("window.verifier()")]
    if ecarts:
        print("[!] hors des marges :\n    " + "\n    ".join(ecarts))
        sys.exit(1)
    print(f"marges : OK ; {fin - a.debut:.2f} s a {a.fps} images/s")
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "image2pipe", "-framerate", str(a.fps), "-c:v", "png", "-i", "-"]
    if a.audio:
        cmd += ["-ss", str(a.debut), "-i", a.audio, "-c:a", "aac", "-b:a", "192k", "-shortest"]
    cmd += ["-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            a.sortie]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = int(round((fin - a.debut) * a.fps))
    for i in range(n):
        page.evaluate(f"window.seek({a.debut + i / a.fps})")
        ff.stdin.write(page.screenshot(type="png"))
        if i % (a.fps * 2) == 0:
            print(f"  {i}/{n}", flush=True)
    ff.stdin.close()
    code = ff.wait()
    nav.close()
if code:
    sys.exit(f"[!] ffmpeg a echoue (code {code}) : {a.sortie} est absent ou incomplet")
print(a.sortie)
