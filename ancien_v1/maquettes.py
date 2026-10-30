"""Maquettes fixes (1080x1920) des reels Medadom Professionnel, 20/10/2026 : une image
d'ouverture et une image de contenu par theme, avec une couleur par theme et des dessins
originaux (medecins, icones) faits ici en SVG. Rendu par Chrome sans interface.

    python maquettes.py"""
import math
import subprocess
from pathlib import Path

ICI = Path(__file__).resolve().parent
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
NAVY = "#1F1650"

THEMES = {
    "rose": {"fond": "#FFF5F9", "points": "#F1C3DA", "accent": "#E4579A", "doux": "#F7B6D2",
             "clair": "#FCE3EF", "second": "#E4579A"},
    "dt2": {"fond": "#FFF6F2", "points": "#F5CBBE", "accent": "#E2574C", "doux": "#F6A291",
            "clair": "#FDE4DB", "second": "#2FA36B"},
}


# ------------------------------------------------------------------ dessins
def visage(peau="#F6C9A8", joues="#F29A9A"):
    return f"""
  <ellipse cx="142" cy="212" rx="12" ry="16" fill="#EDB898"/>
  <ellipse cx="258" cy="212" rx="12" ry="16" fill="#EDB898"/>
  <ellipse cx="200" cy="200" rx="60" ry="72" fill="{peau}"/>
  <ellipse cx="178" cy="206" rx="5.5" ry="7" fill="#2A2140"/>
  <ellipse cx="222" cy="206" rx="5.5" ry="7" fill="#2A2140"/>
  <circle cx="180" cy="203" r="1.8" fill="#fff"/><circle cx="224" cy="203" r="1.8" fill="#fff"/>
  <path d="M200,214 Q194,228 203,231" stroke="#D99A78" stroke-width="3.5" fill="none" stroke-linecap="round"/>
  <circle cx="161" cy="232" r="11" fill="{joues}" opacity=".42"/>
  <circle cx="239" cy="232" r="11" fill="{joues}" opacity=".42"/>
  <path d="M184,246 Q200,260 216,246" stroke="#B5524A" stroke-width="4.5" fill="none" stroke-linecap="round"/>"""


def blouse(chemise, stylo):
    return f"""
  <path d="M178,268 L222,268 L226,318 Q200,334 174,318 Z" fill="#E9AF8E"/>
  <path d="M56,560 L60,420 Q62,350 130,330 L172,312 Q200,330 228,312 L270,330 Q338,350 340,420 L344,560 Z"
        fill="#FFFFFF" stroke="#E2E5EE" stroke-width="3"/>
  <path d="M172,312 L200,382 L228,312 Q200,330 172,312 Z" fill="{chemise}"/>
  <path d="M172,312 L200,382 L170,448 L138,338 Z" fill="#FFFFFF" stroke="#E2E5EE" stroke-width="3" stroke-linejoin="round"/>
  <path d="M228,312 L200,382 L230,448 L262,338 Z" fill="#FFFFFF" stroke="#E2E5EE" stroke-width="3" stroke-linejoin="round"/>
  <rect x="262" y="446" width="48" height="9" rx="4.5" fill="#E2E5EE"/>
  <rect x="274" y="424" width="7" height="28" rx="3.5" fill="{stylo}"/>
  <path d="M168,322 C148,382 152,432 178,472" stroke="#3B3D5C" stroke-width="8" fill="none" stroke-linecap="round"/>
  <path d="M232,322 C252,382 248,432 222,472" stroke="#3B3D5C" stroke-width="8" fill="none" stroke-linecap="round"/>
  <path d="M178,472 Q200,494 222,472" stroke="#3B3D5C" stroke-width="8" fill="none"/>
  <path d="M200,488 L200,514" stroke="#3B3D5C" stroke-width="8"/>
  <circle cx="200" cy="530" r="18" fill="#D7DAE5" stroke="#3B3D5C" stroke-width="6"/>"""


def medecin_femme(stylo):
    cheveux = "#6B3A22"
    return f"""<svg viewBox="0 0 400 560" xmlns="http://www.w3.org/2000/svg">
  <path d="M116,215 C102,118 160,76 205,78 C264,80 302,124 292,215 C298,262 304,302 272,322
           C262,288 258,252 252,232 L150,232 C142,256 140,292 130,322 C98,302 106,262 116,215 Z" fill="{cheveux}"/>
  {blouse("#A8D0F2", stylo)}
  {visage()}
  <path d="M136,192 C138,126 182,106 214,108 C254,110 274,148 266,190 C248,160 222,150 196,154
           C170,158 152,172 136,192 Z" fill="{cheveux}"/>
  <path d="M198,152 C214,138 240,136 254,150" stroke="#87492B" stroke-width="4" fill="none" stroke-linecap="round"/>
  <path d="M166,188 Q178,181 190,187" stroke="#4A2A1A" stroke-width="4" fill="none" stroke-linecap="round"/>
  <path d="M210,187 Q222,181 234,188" stroke="#4A2A1A" stroke-width="4" fill="none" stroke-linecap="round"/>
</svg>"""


def medecin_homme(stylo):
    cheveux = "#8B4A2B"
    boucles = [(146, 158, 28), (168, 130, 30), (200, 120, 31), (232, 128, 30), (258, 154, 27),
               (140, 186, 20), (262, 184, 19), (184, 112, 18), (218, 110, 18)]
    rond = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{cheveux}"/>' for x, y, r in boucles)
    reflets = "".join(f'<path d="M{x - r * .45:.0f},{y - r * .2:.0f} q{r * .35:.0f},-{r * .45:.0f} {r * .8:.0f},-{r * .1:.0f}" '
                      f'stroke="#A9603C" stroke-width="4" fill="none" stroke-linecap="round"/>'
                      for x, y, r in boucles[:5])
    return f"""<svg viewBox="0 0 400 560" xmlns="http://www.w3.org/2000/svg">
  {blouse("#9CC7EE", stylo)}
  {visage("#F3C4A2")}
  {rond}{reflets}
  <path d="M166,186 Q178,180 190,186" stroke="#5A3020" stroke-width="5" fill="none" stroke-linecap="round"/>
  <path d="M210,186 Q222,180 234,186" stroke="#5A3020" stroke-width="5" fill="none" stroke-linecap="round"/>
</svg>"""


def etoile(cx, cy, r1, r2, n=12):
    pts = []
    for i in range(2 * n):
        r = r1 if i % 2 == 0 else r2
        a = math.pi * i / n - math.pi / 2
        pts.append(f"{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}")
    return " ".join(pts)


def bulle_validee(accent):
    return f"""<svg viewBox="0 0 220 210" xmlns="http://www.w3.org/2000/svg">
  <path d="M10,70 C10,30 40,10 80,10 L140,10 C180,10 210,30 210,70 L210,110 C210,150 180,170 140,170
           L82,170 L36,204 L48,164 C24,156 10,136 10,110 Z" fill="#FFFFFF" stroke="#ECE6EF" stroke-width="3"/>
  <polygon points="{etoile(110, 90, 50, 43)}" fill="{accent}" stroke="{accent}" stroke-width="6" stroke-linejoin="round"/>
  <path d="M88,92 L104,108 L134,76" stroke="#FFFFFF" stroke-width="11" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""


def ruban(accent, fonce):
    return f"""<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <path d="M100,104 L158,222" stroke="{accent}" stroke-width="34" fill="none"/>
  <path d="M42,222 L100,104 C128,62 128,18 100,18 C72,18 72,62 100,104" stroke="{fonce}" stroke-width="34"
        fill="none" stroke-linejoin="round"/>
  <path d="M100,104 L130,165" stroke="{accent}" stroke-width="34" fill="none"/>
</svg>"""


def telephone(clair, portrait):
    return f"""<svg viewBox="0 0 300 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="300" height="600" rx="46" fill="{NAVY}"/>
  <rect x="12" y="12" width="276" height="576" rx="36" fill="#FFFFFF"/>
  <rect x="110" y="24" width="80" height="16" rx="8" fill="{NAVY}"/>
  <clipPath id="ecran"><rect x="28" y="58" width="244" height="388" rx="24"/></clipPath>
  <rect x="28" y="58" width="244" height="388" rx="24" fill="{clair}"/>
  <g clip-path="url(#ecran)">{portrait.replace("<svg ", '<svg x="-10" y="120" width="320" height="448" ', 1)}</g>
  <rect x="42" y="72" width="164" height="32" rx="16" fill="{NAVY}"/>
  <circle cx="60" cy="88" r="6" fill="#4ADE80"/>
  <text x="72" y="94" font-family="Poppins" font-weight="600" font-size="16" fill="#fff">Téléconsultation</text>
  <rect x="196" y="352" width="62" height="80" rx="14" fill="#FFFFFF" stroke="{clair}" stroke-width="3"/>
  <circle cx="227" cy="380" r="13" fill="#E3E6EF"/><rect x="209" y="398" width="36" height="22" rx="11" fill="#E3E6EF"/>
  <circle cx="92" cy="506" r="27" fill="#EEF0F6"/><circle cx="150" cy="506" r="27" fill="#EEF0F6"/>
  <circle cx="208" cy="506" r="27" fill="#E5484D"/>
  <path d="M196,508 q12,-10 24,0" stroke="#fff" stroke-width="6" fill="none" stroke-linecap="round"/>
  <rect x="84" y="494" width="16" height="22" rx="8" fill="#9AA0B8"/>
  <rect x="139" y="497" width="22" height="16" rx="4" fill="#9AA0B8"/>
</svg>"""


def goutte(couleur, reflet):
    return f"""<svg viewBox="0 0 100 150" xmlns="http://www.w3.org/2000/svg">
  <path d="M50,2 C50,2 2,62 2,97 C2,127 24,148 50,148 C76,148 98,127 98,97 C98,62 50,2 50,2 Z" fill="{couleur}"/>
  <path d="M26,96 C26,80 34,66 40,58" stroke="{reflet}" stroke-width="7" fill="none" stroke-linecap="round" opacity=".7"/>
</svg>"""


def sucre():
    return """<svg viewBox="0 0 90 96" xmlns="http://www.w3.org/2000/svg">
  <polygon points="4,24 45,4 86,24 45,44" fill="#FFFFFF" stroke="#D9DCE6" stroke-width="2"/>
  <polygon points="4,24 45,44 45,92 4,72" fill="#E6E8F0" stroke="#D9DCE6" stroke-width="2"/>
  <polygon points="45,44 86,24 86,72 45,92" fill="#CED2DE" stroke="#D9DCE6" stroke-width="2"/>
</svg>"""


def assiette(vert):
    return f"""<svg viewBox="0 0 300 220" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="150" cy="150" rx="140" ry="58" fill="#FFFFFF" stroke="#E6E1E6" stroke-width="4"/>
  <ellipse cx="150" cy="142" rx="100" ry="38" fill="#F4F1F4"/>
  <circle cx="112" cy="128" r="26" fill="{vert}"/><circle cx="140" cy="116" r="24" fill="#4CC38A"/>
  <circle cx="168" cy="126" r="25" fill="{vert}"/><circle cx="96" cy="140" r="18" fill="#7AD3A6"/>
  <circle cx="190" cy="140" r="16" fill="#E2574C"/><circle cx="206" cy="128" r="13" fill="#F07A6F"/>
  <ellipse cx="150" cy="148" rx="34" ry="12" fill="#F5C26B"/>
  <path d="M266,60 L266,170" stroke="#B7BCCB" stroke-width="8" stroke-linecap="round"/>
  <path d="M34,60 L34,170" stroke="#B7BCCB" stroke-width="8" stroke-linecap="round"/>
  <path d="M24,60 L24,92 Q34,104 44,92 L44,60" stroke="#B7BCCB" stroke-width="5" fill="none"/>
</svg>"""


def pomme(rouge, vert):
    return f"""<svg viewBox="0 0 120 130" xmlns="http://www.w3.org/2000/svg">
  <path d="M60,34 C40,20 6,28 8,66 C10,104 36,126 52,122 C56,121 64,121 68,122 C84,126 110,104 112,66
           C114,28 80,20 60,34 Z" fill="{rouge}"/>
  <path d="M60,34 C60,22 64,12 70,6" stroke="#6B4226" stroke-width="5" fill="none" stroke-linecap="round"/>
  <path d="M66,22 C78,6 98,8 102,14 C92,26 76,28 66,22 Z" fill="{vert}"/>
  <path d="M28,58 C30,48 36,42 44,40" stroke="#FFFFFF" stroke-width="6" fill="none" stroke-linecap="round" opacity=".5"/>
</svg>"""


def data(svg):
    """Un SVG en image : l'encodage URL garde les accents et les guillemets."""
    from urllib.parse import quote
    return "data:image/svg+xml;utf8," + quote(svg)


# ------------------------------------------------------------------ pages
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=block');
* { margin: 0; padding: 0; box-sizing: border-box; }
body { width: 1080px; height: 1920px; overflow: hidden; font-family: 'Poppins', sans-serif; color: NAVY;
  background-color: FOND;
  background-image: radial-gradient(POINTS 2.6px, transparent 2.8px);
  background-size: 44px 44px; background-position: 22px 22px; position: relative; }
.halo { position: absolute; border-radius: 50%; filter: blur(60px); opacity: .55; }
.logo { position: absolute; left: 50%; top: 300px; transform: translateX(-50%); height: 46px; opacity: .95; }
.bloc { position: absolute; left: 90px; right: 90px; top: 420px; }
.etiquette { display: inline-block; background: NAVY; color: #fff; font-weight: 700; font-size: 40px;
  padding: 6px 24px 8px; border-radius: 12px; }
h1 { font-weight: 800; font-size: 100px; line-height: 1.04; margin-top: 30px; letter-spacing: -1px; }
.surligne { display: inline-block; background: ACCENT; color: #fff; padding: 0 22px 8px; border-radius: 16px;
  margin-top: 10px; transform: rotate(-1.5deg); }
.sous { font-weight: 500; font-size: 46px; line-height: 1.3; margin-top: 34px; }
.sous b { font-weight: 700; border-bottom: 7px solid ACCENT; }
.pastilles { margin-top: 40px; display: flex; flex-direction: column; gap: 20px; align-items: flex-start; }
.pastille { background: #fff; border: 3px solid CLAIR; border-radius: 40px; padding: 14px 30px 16px 26px;
  font-size: 34px; font-weight: 500; line-height: 1.25; display: flex; align-items: center; gap: 16px;
  box-shadow: 0 6px 18px rgba(31,22,80,.06); }
.pastille::before { content: ''; flex: 0 0 18px; height: 18px; border-radius: 50%; background: SECOND; }
.chiffre { font-weight: 800; font-size: 210px; line-height: 1; color: ACCENT; margin-top: 30px; letter-spacing: -4px; }
.legende { font-weight: 500; font-size: 44px; line-height: 1.3; margin-top: 8px; }
.dessin { position: absolute; }
"""


def page(theme, corps, halos):
    t = THEMES[theme]
    css = (CSS.replace("NAVY", NAVY).replace("FOND", t["fond"]).replace("POINTS", t["points"])
           .replace("ACCENT", t["accent"]).replace("CLAIR", t["clair"]).replace("SECOND", t["second"]))
    h = "".join(f'<div class="halo" style="left:{x}px;top:{y}px;width:{r}px;height:{r}px;background:{c}"></div>'
                for x, y, r, c in halos)
    logo = (ICI / "logo_medadom.png").as_uri()
    return (f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>{css}</style></head>'
            f'<body>{h}<img class="logo" src="{logo}">{corps}</body></html>')


def img(svg, x, y, w, rot=0):
    """Dessin en SVG en ligne : la police de la page s'y applique (pas dans une <img>)."""
    svg = svg.replace("<svg ", '<svg width="100%" ', 1)
    return (f'<div class="dessin" style="left:{x}px;top:{y}px;width:{w}px;'
            f'transform:rotate({rot}deg)">{svg}</div>')


R, D = THEMES["rose"], THEMES["dt2"]
femme, homme = medecin_femme(R["accent"]), medecin_homme(D["accent"])
pages = {
    "A1_rose_ouverture": page("rose", f"""
<div class="bloc">
  <span class="etiquette">Octobre rose</span>
  <h1 style="font-size:88px">Une patiente<br>inquiète après<br><span class="surligne">l’autopalpation</span> ?</h1>
  <p class="sous">Les bons réflexes <b>en téléconsultation</b></p>
</div>
{img(femme, 60, 1060, 560)}
{img(bulle_validee(R["accent"]), 500, 1110, 220, -4)}
{img(telephone(R["clair"], medecin_homme(R["accent"])), 710, 1200, 280, 6)}
{img(ruban(R["doux"], R["accent"]), 860, 400, 120, 12)}
""", [(-200, 1100, 700, R["clair"]), (700, 900, 600, R["clair"])]),
    "A2_rose_contenu": page("rose", f"""
<div class="bloc">
  <span class="etiquette">En téléconsultation</span>
  <h1 style="font-size:84px">Écouter,<br>rassurer, <span class="surligne">orienter</span></h1>
  <div class="pastilles">
    <div class="pastille">Laisser décrire : boule, douleur, écoulement</div>
    <div class="pastille">Rassurer : les symptômes bénins sont fréquents</div>
    <div class="pastille">Pas le mot « cancer » sans preuve histologique</div>
    <div class="pastille">Un doute ? Imagerie diagnostique</div>
  </div>
</div>
{img(telephone(R["clair"], femme), 660, 1240, 300, -5)}
{img(ruban(R["doux"], R["accent"]), 120, 1380, 150, -10)}
""", [(-150, 1300, 650, R["clair"]), (600, 300, 500, R["clair"])]),
    "B1_dt2_ouverture": page("dt2", f"""
<div class="bloc">
  <span class="etiquette">Diabète de type 2</span>
  <h1>Le prévenir<br><span class="surligne">dans l’assiette</span></h1>
  <p class="sous">Le rôle du médecin généraliste, <b>en téléconsultation</b></p>
</div>
{img(homme, 470, 1060, 560)}
{img(bulle_validee(D["accent"]), 330, 1010, 220, 4)}
{img(goutte(D["accent"], "#FFFFFF"), 110, 1150, 120, -8)}
{img(goutte(D["doux"], "#FFFFFF"), 200, 1250, 90, 10)}
{img(sucre(), 90, 1400, 120, 0)}
{img(sucre(), 200, 1440, 100, 8)}
{img(sucre(), 140, 1500, 110, -6)}
""", [(-200, 1100, 700, D["clair"]), (650, 900, 600, D["clair"])]),
    "B2_dt2_contenu": page("dt2", f"""
<div class="bloc">
  <span class="etiquette">Prise en charge nutritionnelle</span>
  <div class="chiffre">≥ 5 %</div>
  <p class="legende">de poids perdu : une amélioration <b style="border-bottom:7px solid {D["accent"]}">métabolique significative</b></p>
  <div class="pastilles">
    <div class="pastille">Alimentation méditerranéenne : la référence</div>
    <div class="pastille">Aucun aliment interdit, seules les quantités varient</div>
    <div class="pastille">Régimes restrictifs : contre-productifs</div>
  </div>
</div>
{img(assiette(D["second"]), 470, 1380, 520)}
{img(pomme(D["accent"], D["second"]), 150, 1420, 170, -8)}
""", [(-150, 1250, 650, D["clair"]), (650, 350, 500, D["clair"])]),
}

sortie = ICI / "maquettes"
sortie.mkdir(exist_ok=True)
for nom, html in pages.items():
    f = sortie / f"{nom}.html"
    f.write_text(html, encoding="utf-8")
    png = sortie / f"{nom}.png"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
                    "--window-size=1080,1920", "--virtual-time-budget=9000", "--allow-file-access-from-files",
                    f"--screenshot={png}", f.as_uri()], capture_output=True, timeout=180)
    print(png, png.exists())
