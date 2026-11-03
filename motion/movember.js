/* Movember (novembre 2026), direction artistique « nuit et ivoire » : fond nuit profond, typographie
   editoriale (Bodoni MT), une moustache qui se trace d'un trait puis se remplit d'ivoire, au rythme du saxo
   (Echo Sax No.4, une mesure = 3,157 s). Deux versions : « marque » (3 mesures, le symbole et le nom) et
   « info » (7 mesures : les trois causes de Movember, un fait INCa, l'ouverture vers la pratique).
   Sources : movember.com/about-us ; CIRC-OMS, GLOBOCAN 2024 (France metropolitaine : 55 250 nouveaux cas
   estimes en 2024, 1er cancer de l'homme) ; INCa, Panorama des cancers en France 2026 (9 002 deces en 2023). */
Motion.exiger("Bodoni MT");
Motion.demarrer(function (M) {
  const { D, CARRE, tl, noeud, decouper, compteur, trait } = M;
  const MES = 3.157, INFO = D.version !== "marque", V = D.temps;
  const R = document.documentElement.style;
  R.setProperty("--fond", "#0B0918");
  R.setProperty("--encre", "#F2EADB");
  R.setProperty("--logo", "#F2EADB");
  R.setProperty("--pro-texte", "#F2EADB");
  R.setProperty("--pro-bord", "rgba(242,234,219,.55)");
  R.setProperty("--grain", ".09");

  noeud(`<style>
    #lueur { background: radial-gradient(ellipse 70% 42% at 50% 40%, rgba(52,38,128,.9) 0%, rgba(28,21,74,.55) 42%, rgba(11,9,24,0) 75%); }
    html.carre #lueur { background: radial-gradient(ellipse 70% 60% at 50% 44%, rgba(52,38,128,.9) 0%, rgba(28,21,74,.55) 42%, rgba(11,9,24,0) 78%); }
    #vignette { background: radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 52%, rgba(0,0,0,.6) 100%); }
    #embleme { position: absolute; left: 0; right: 0; top: 700px; height: 760px; }
    html.carre #embleme { top: 345px; height: 620px; }
    #moustache { position: absolute; left: 130px; width: 820px; top: 0; overflow: visible;
      filter: drop-shadow(0 0 34px rgba(242,234,219,.18)); }
    html.carre #moustache { left: 250px; width: 580px; }
    .titre { position: absolute; left: 0; right: 0; top: 262px; text-align: center; font: 400 184px/1 "Bodoni MT", serif;
      letter-spacing: -.01em; color: #F2EADB; }
    html.carre .titre { top: 170px; font-size: 148px; }
    .filet { position: absolute; left: 480px; width: 120px; height: 2px; top: 520px; background: #C9A86A; }
    html.carre .filet { top: 360px; }
    .sous { position: absolute; left: 0; right: 0; top: 552px; text-align: center; font: 500 30px/1 Poppins;
      letter-spacing: .32em; text-transform: uppercase; color: rgba(242,234,219,.86); }
    html.carre .sous { top: 388px; font-size: 25px; }
    .causes { position: absolute; left: 0; right: 0; top: 650px; text-align: center; font: 500 36px/1 Poppins;
      color: #F2EADB; letter-spacing: .02em; }
    html.carre .causes { top: 470px; font-size: 30px; }
    .causes i { font-style: normal; color: #C9A86A; margin: 0 .55em; }
    .plan { position: absolute; left: 110px; right: 110px; top: 760px; height: 820px; display: flex;
      flex-direction: column; justify-content: center; align-items: center; text-align: center; color: #F2EADB; }
    html.carre .plan { left: 60px; right: 60px; top: 300px; height: 740px; }
    .phrase { font: 600 66px/1.18 Poppins; letter-spacing: -.01em; }
    html.carre .phrase { font-size: 52px; }
    .serif { font: italic 400 92px/1.1 "Bodoni MT", serif; color: #D9BD86; letter-spacing: 0; }
    html.carre .serif { font-size: 74px; }
    .etiquette { display: inline-block; font: 600 30px/1 Poppins; letter-spacing: .14em; text-transform: uppercase;
      color: #D9BD86; border: 2px solid rgba(201,168,106,.7); border-radius: 999px; padding: 16px 28px 14px; }
    html.carre .etiquette { font-size: 24px; padding: 12px 22px 10px; }
    .chiffre { font: 400 230px/1 "Bodoni MT", serif; color: #F2EADB; letter-spacing: -.02em; }
    html.carre .chiffre { font-size: 170px; }
    .avant { font: 500 42px/1.2 Poppins; color: rgba(242,234,219,.86); }
    html.carre .seul-916 { display: none; }
    html.carre .avant { font-size: 34px; }
    .source { font: 400 26px/1.3 Poppins; color: rgba(242,234,219,.6); }
    html.carre .source { font-size: 21px; }
  </style>`, document.head);

  noeud('<div id="lueur" class="calque"></div>');
  noeud('<div id="vignette" class="calque"></div>');
  const entete = noeud('<div class="entete"><div class="logo"></div><div class="pro">Professionnel</div></div>');
  entete.dataset.zone = "texte";

  // la moustache : une demi-forme dessinee a droite, la gauche en miroir (x -> 1000 - x)
  const DROITE = "M500,152 C532,104 598,88 668,96 C752,106 812,156 868,164 C916,170 948,138 960,92 " +
    "C964,74 984,66 992,80 C999,94 986,140 952,178 C905,222 820,238 730,226 C640,212 565,214 500,236";
  const miroir = d => d.replace(/(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)/g, (_, x, y) => `${1000 - +x},${y}`);
  const GAUCHE = miroir(DROITE);
  // forme pleine : contour droit, puis contour gauche parcouru a l'envers
  const inverse = d => {
    const pts = d.replace(/[MC]/g, " ").trim().split(/\s+/);
    const r = pts.reverse();
    let out = `M${r[0]}`;
    for (let i = 1; i < r.length; i += 3) out += ` C${r[i]} ${r[i + 1]} ${r[i + 2]}`;
    return out;
  };
  const PLEINE = DROITE + " " + inverse(GAUCHE).replace(/^M[^ ]+/, "") + " Z";

  const embleme = noeud('<div id="embleme"></div>');
  const svg = noeud(`<svg id="moustache" viewBox="0 50 1000 200" data-zone="cle">
    <defs>
      <linearGradient id="ivoire" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="#FBF6EC"/><stop offset="1" stop-color="#E4D8C1"/>
      </linearGradient>
      <linearGradient id="reflet" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".75"/>
        <stop offset="1" stop-color="#fff" stop-opacity="0"/>
      </linearGradient>
      <clipPath id="forme"><path d="${PLEINE}"/></clipPath>
      <clipPath id="revele"><rect id="revele-r" x="500" y="0" width="0" height="320"/></clipPath>
      <!-- gravure : des hachures fines, inclinees vers l'exterieur de chaque cote, plus marquees en bas -->
      <pattern id="hach-d" width="11" height="11" patternUnits="userSpaceOnUse" patternTransform="rotate(-38)">
        <line x1="0" y1="0" x2="0" y2="11" stroke="#B9A47E" stroke-width="1.5"/></pattern>
      <pattern id="hach-g" width="11" height="11" patternUnits="userSpaceOnUse" patternTransform="rotate(38)">
        <line x1="0" y1="0" x2="0" y2="11" stroke="#B9A47E" stroke-width="1.5"/></pattern>
      <linearGradient id="fondu-g" x1="0" y1="0" x2="0" y2="1">
        <stop offset=".35" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff" stop-opacity=".9"/></linearGradient>
      <mask id="bas"><rect x="0" y="50" width="1000" height="200" fill="url(#fondu-g)"/></mask>
    </defs>
    <g clip-path="url(#revele)"><path d="${PLEINE}" fill="url(#ivoire)"/>
      <g clip-path="url(#forme)" mask="url(#bas)" opacity=".9">
        <rect x="500" y="50" width="500" height="200" fill="url(#hach-d)"/>
        <rect x="0" y="50" width="500" height="200" fill="url(#hach-g)"/>
      </g></g>
    <g clip-path="url(#forme)"><rect id="reflet-r" x="-260" y="40" width="200" height="240" fill="url(#reflet)" transform="skewX(-18)"/></g>
    <path class="contour" d="${DROITE}" fill="none" stroke="#F2EADB" stroke-width="3" stroke-linecap="round"/>
    <path class="contour" d="${GAUCHE}" fill="none" stroke="#F2EADB" stroke-width="3" stroke-linecap="round"/>
  </svg>`, embleme);
  const titre = noeud('<div class="titre" data-zone="texte">Movember</div>', embleme);
  const filet = noeud('<div class="filet"></div>', embleme);
  const sous = noeud('<div class="sous" data-zone="texte">Novembre · la santé des hommes</div>', embleme);

  const contours = [...svg.querySelectorAll(".contour")];
  contours.forEach(trait);
  const lettres = decouper(titre, "l");
  gsap.set(lettres, { yPercent: 105 });
  gsap.set(filet, { scaleX: 0 });
  // depart a 0,4 em : a 0,45 em, la ligne debordait de la zone sure pendant son fondu (review Codex, 30/10/2026)
  gsap.set(sous, { opacity: 0, letterSpacing: "0.4em" });
  gsap.set(entete, { opacity: 0, y: -16 });

  // 1re mesure : le trait, puis l'ivoire qui se repand depuis le centre, puis un reflet
  tl.to(entete, { opacity: 1, y: 0, duration: 1.0, ease: "power3.out" }, 0.2)
    .to(contours, { strokeDashoffset: 0, duration: 1.5, ease: "power2.inOut" }, 0.15)
    .to("#revele-r", { attr: { x: 0, width: 1000 }, duration: 1.1, ease: "power3.inOut" }, 1.15)
    .to(contours, { opacity: 0, duration: .6 }, 2.0)
    .to("#reflet-r", { attr: { x: 1150 }, duration: 1.3, ease: "power2.inOut" }, 2.15);
  // 2e mesure : le nom, lettre a lettre, le filet d'or, la ligne de sous-titre
  tl.to(lettres, { yPercent: 0, duration: 1.0, stagger: .055, ease: "power4.out" }, MES)
    .to(filet, { scaleX: 1, duration: .8, ease: "power3.inOut" }, MES + .75)
    .to(sous, { opacity: 1, letterSpacing: "0.32em", duration: 1.4, ease: "power3.out" }, MES + .95);
  // la lueur respire, la moustache flotte a peine
  tl.fromTo("#lueur", { opacity: .75 }, { opacity: 1, duration: D.duree / 2, yoyo: true, repeat: 1, ease: "sine.inOut" }, 0);

  if (!INFO) {
    const causes = noeud('<div class="causes" data-zone="texte">Prostate<i>·</i>Testicules<i>·</i>Santé mentale</div>', embleme);
    const mots = decouper(causes, "m");
    gsap.set(mots, { yPercent: 110 });
    tl.to(mots, { yPercent: 0, duration: .9, stagger: .09, ease: "power4.out" }, 2 * MES)
      .to(svg, { y: -8, duration: 1.6, yoyo: true, repeat: 1, ease: "sine.inOut" }, 2 * MES - .3);
    fin();
    return;
  }

  // version info : l'embleme monte se ranger sous l'entete, les plans defilent dessous
  const haut = CARRE ? -200 : -265, petit = CARRE ? .46 : .56;
  gsap.set(embleme, { transformOrigin: "50% 0%" });
  // les temps des plans : sur les mesures de la musique, ou sur la voix (version « voix », D.temps)
  const Q = V
    ? { haut: V.p1 - 1.25, p1: V.p1 - .25, p1b: V.p1b - .12, p2: V.p2 - .3, p2a: V.p2a - .12, av: V.p2b - .2,
        p2b: V.p2b - .1, p2c: V.p2c - .1, p2d: V.p2d - .1, p3: V.p3 - .3, p3b: V.p3b - .12, fin: V.signature - .55 }
    : { haut: 2 * MES, p1: 2 * MES + .5, p1b: 2 * MES + 1.35, p2: 3 * MES + .75, p2a: 3 * MES + 1.1, av: 4 * MES - .3,
        p2b: 4 * MES - .2, p2c: 4 * MES + .5, p2d: 4 * MES + 1.0, p3: 5 * MES, p3b: 5 * MES + .85, fin: 6 * MES + .4 };
  tl.to(sous, { opacity: 0, duration: .4 }, Q.haut - .1)
    .to(filet, { opacity: 0, duration: .4 }, Q.haut - .1)
    .to(embleme, { y: haut, scale: petit, duration: 1.1, ease: "power3.inOut" }, Q.haut);

  const plans = [];
  function plan(html, debut, fin) {
    const p = noeud(`<div class="plan">${html}</div>`);
    p.querySelectorAll(".phrase, .serif, .etiquette, .chiffre, .avant, .source").forEach(e => e.dataset.zone = "texte");
    plans.push(p);
    tl.set(p, { opacity: 1 }, debut).to(p, { opacity: 0, y: -24, duration: .4, ease: "power2.in" }, fin - .45);
    gsap.set(p, { opacity: 0 });
    return p;
  }
  function entrer(el, t, unite) {
    const morceaux = decouper(el, unite || "m");
    gsap.set(morceaux, { yPercent: 110 });
    tl.to(morceaux, { yPercent: 0, duration: .85, stagger: .05, ease: "power4.out" }, t);
  }

  // 3e mesure : les trois causes de Movember
  const p1 = plan(`<div class="phrase">Cancer de la prostate,<br>cancer du testicule,<br>santé mentale et<br>prévention du suicide :</div>
    <div class="serif" style="margin-top:22px">novembre, on en parle.</div>`, Q.p1, Q.p2);
  entrer(p1.querySelector(".phrase"), Q.p1 + .05);
  entrer(p1.querySelector(".serif"), Q.p1b);

  // 4e et 5e mesures : le fait, source INCa ; le compteur part sur la 5e mesure
  const p2 = plan(`<div class="etiquette">Cancer de la prostate</div>
    <div class="phrase" style="margin-top:34px">Le plus fréquent<br>chez l’homme</div>
    <div class="avant" style="margin-top:46px">plus de</div>
    <div class="chiffre" style="margin-top:6px">55 000</div>
    <div class="avant" style="margin-top:4px">nouveaux cas estimés <br class="seul-916">en France en 2024,</div>
    <div class="avant" style="margin-top:12px">et 9 002 décès en 2023</div>
    <div class="source" style="margin-top:34px">Sources : CIRC-OMS, GLOBOCAN 2024 (France métropolitaine) ;<br>INCa, Panorama des cancers en France 2026</div>`, Q.p2, Q.p3);
  gsap.set(p2.querySelector(".etiquette"), { opacity: 0, y: 20 });
  tl.to(p2.querySelector(".etiquette"), { opacity: 1, y: 0, duration: .7, ease: "power3.out" }, Q.p2 + .05);
  entrer(p2.querySelector(".phrase"), Q.p2a);
  const [av1, av2, av3] = p2.querySelectorAll(".avant"), ch = p2.querySelector(".chiffre"), src = p2.querySelector(".source");
  gsap.set([av1, av2, av3, ch, src], { opacity: 0 });
  tl.to(av1, { opacity: 1, duration: .5 }, Q.av)
    .fromTo(ch, { opacity: 0, scale: .92 }, { opacity: 1, scale: 1, duration: .9, ease: "power3.out" }, Q.p2b)
    .to(av2, { opacity: 1, duration: .6 }, Q.p2c)
    .to(av3, { opacity: 1, duration: .6 }, Q.p2d)
    .to(src, { opacity: 1, duration: .6 }, Q.p2d + .5);
  compteur(ch, 0, 550, 1.6, Q.p2b, 0, "power2.out", 100);

  // 6e mesure : l'ouverture vers la pratique
  const p3 = plan(`<div class="phrase">En consultation comme<br>en téléconsultation :</div>
    <div class="serif" style="margin-top:26px">parlons-en.</div>`, Q.p3, Q.fin);
  entrer(p3.querySelector(".phrase"), Q.p3 + .05);
  entrer(p3.querySelector(".serif"), Q.p3b, "l");

  // 7e mesure : l'embleme revient au centre ; 8e : la carte de fin
  if (!V) tl.to(embleme, { y: 0, scale: 1, duration: 1.1, ease: "power3.inOut" }, 6 * MES + .2)
    .to([sous, filet], { opacity: 1, duration: .6 }, 6 * MES + 1.0);
  fin();

  // derniere mesure : la composition s'efface en montant et en se brouillant, la carte de fin Medadom prend sa
  // place, puis s'efface a son tour jusqu'au fond nu du premier plan (la boucle)
  function fin() {
    const t = V ? V.signature - .55 : D.duree - MES - .3;
    tl.to([embleme, entete], { opacity: 0, y: "-=16", filter: "blur(10px)", duration: .9, ease: "power2.in" }, t);
    M.carteFin(t + .35);
  }
});
