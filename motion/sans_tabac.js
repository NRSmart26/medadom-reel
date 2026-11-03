/* Mois sans tabac (novembre 2026), direction artistique « respiration » : fond clair et aere, encre Medadom,
   vert frais. La cigarette se consume, s'eteint, puis se defait en 30 segments qui forment l'anneau des 30
   jours ; un compteur les allume un a un. Deux versions : « marque » (le symbole et le nom) et « info »
   (trois faits sources : 55 % des fumeurs quotidiens veulent arreter, 30 jours = 5 fois plus de chances,
   substituts nicotiniques, la plupart rembourses a 65 % par l'Assurance maladie, sur prescription).
   Sources : Sante publique France, communique du 1er octobre 2026 (Barometre 2024 ; 30 jours sans tabac
   multiplient par 5 les chances d'arret a long terme) ; ameli.fr, espace medecin, prise en charge du sevrage
   tabagique (04/12/2025). */
Motion.demarrer(function (M) {
  const { D, CARRE, tl, noeud, decouper, compteur } = M;
  const MES = D.mesure, INFO = D.version !== "marque", V = D.temps;
  const R = document.documentElement.style;
  R.setProperty("--fond", "#EAF2EE");
  R.setProperty("--encre", "#1F1650");
  R.setProperty("--logo", "#1F1650");
  R.setProperty("--pro-texte", "#1F1650");
  R.setProperty("--pro-fond", "rgba(255,255,255,.75)");
  R.setProperty("--grain", ".05");
  const VERT = "#2E9E7A", GRIS = "#CFDAD5";

  // geometrie : anneau de 30 segments autour du centre (cx, cy), cigarette horizontale au meme centre
  const G = CARRE
    ? { cx: 540, cy: 450, r: 205, sw: 15, sh: 36, long: 450, epais: 32, titre: 735 }
    : { cx: 540, cy: 870, r: 300, sw: 21, sh: 52, long: 640, epais: 46, titre: 1255 };
  const N = 30, part = G.long / N, x0 = G.cx - G.long / 2;

  noeud(`<style>
    #ciel { background: linear-gradient(180deg, #F7FBF9 0%, #EAF2EE 55%, #DDEBE5 100%); }
    #souffle-l { background: radial-gradient(circle at 50% ${CARRE ? 39 : 43}%, rgba(255,255,255,.95) 0%, rgba(255,255,255,0) 46%); }
    .seg { position: absolute; left: 0; top: 0; border-radius: 3px; will-change: transform; }
    #contour { position: absolute; border: 2px solid #CFC8BD; border-radius: 6px; }
    #braise { position: absolute; border-radius: 4px; background: radial-gradient(circle at 30% 50%, #FFD2A1 0%, #F58A3C 45%, #C9471E 100%);
      box-shadow: 0 0 26px 8px rgba(245,122,58,.55); }
    #fumee { position: absolute; overflow: visible; }
    .chiffre-anneau { position: absolute; left: 0; right: 0; text-align: center; font: 800 210px/1 Poppins; color: #1F1650;
      letter-spacing: -.04em; font-variant-numeric: tabular-nums; }
    html.carre .chiffre-anneau { font-size: 142px; }
    .jours { position: absolute; left: 0; right: 0; text-align: center; font: 600 46px/1 Poppins; color: ${VERT}; }
    html.carre .jours { font-size: 32px; }
    .titre { position: absolute; left: 0; right: 0; text-align: center; font: 800 98px/1.02 Poppins; color: #1F1650; letter-spacing: -.02em; }
    html.carre .titre { font-size: 74px; }
    .dates { position: absolute; left: 0; right: 0; text-align: center; font: 600 40px/1 Poppins; color: ${VERT}; }
    html.carre .dates { font-size: 30px; }
    .dates sup { font-size: .58em; vertical-align: .62em; line-height: 0; }
    .plan { position: absolute; left: 100px; right: 100px; top: 760px; height: 820px; display: flex; flex-direction: column;
      justify-content: center; align-items: center; text-align: center; color: #1F1650; }
    html.carre .plan { left: 60px; right: 60px; top: 300px; height: 740px; }
    .gros { font: 800 230px/1 Poppins; color: ${VERT}; letter-spacing: -.04em; }
    html.carre .gros { font-size: 168px; }
    .phrase { font: 600 64px/1.18 Poppins; letter-spacing: -.01em; }
    html.carre .seul-916 { display: none; }
    html.carre .phrase { font-size: 50px; }
    .etiquette { display: inline-block; font: 600 30px/1 Poppins; letter-spacing: .1em; text-transform: uppercase; color: #fff;
      background: ${VERT}; border-radius: 999px; padding: 16px 28px 14px; }
    html.carre .etiquette { font-size: 24px; padding: 12px 22px 10px; }
    .source { font: 400 26px/1.3 Poppins; color: rgba(31,22,80,.55); }
    html.carre .source { font-size: 21px; }
  </style>`, document.head);

  noeud('<div id="ciel" class="calque"></div>');
  const lumiere = noeud('<div id="souffle-l" class="calque"></div>');
  const entete = noeud('<div class="entete" data-zone="texte"><div class="logo"></div><div class="pro">Professionnel</div></div>');
  const embleme = noeud('<div id="embleme" class="calque"></div>');

  // la cigarette : 30 tranches cote a cote (la braise a gauche, le filtre a droite sur 6 tranches)
  const y0 = G.cy - G.epais / 2;
  const contour = noeud(`<div id="contour" style="left:${x0 - 2}px;top:${y0 - 2}px;width:${G.long + 4}px;height:${G.epais + 4}px"></div>`, embleme);
  const segs = [];
  for (let i = 0; i < N; i++) {
    const filtre = i >= N - 6;
    const s = noeud(`<div class="seg" style="width:${part + .6}px;height:${G.epais}px;background:${filtre ? "#E2C08F" : "#FFFFFF"}"></div>`, embleme);
    gsap.set(s, { x: x0 + i * part, y: y0, borderRadius: 0 });
    segs.push(s);
  }
  // la bague doree entre papier et filtre
  const bague = noeud(`<div class="seg" style="width:3px;height:${G.epais}px;background:#C9A86A"></div>`, embleme);
  gsap.set(bague, { x: x0 + (N - 6) * part - 1.5, y: y0 });
  const braise = noeud(`<div id="braise" style="left:${x0 - 6}px;top:${y0}px;width:16px;height:${G.epais}px"></div>`, embleme);
  // la fumee : une volute qui monte de la braise
  const fx = x0, fy = y0 - 6, H = CARRE ? 230 : 360;
  const fumee = noeud(`<svg id="fumee" style="left:${fx - 150}px;top:${fy - H}px" width="300" height="${H}" viewBox="0 0 300 ${H}">
    <path d="M150,${H} C110,${H * .82} 190,${H * .66} 150,${H * .5} C112,${H * .35} 186,${H * .2} 160,0" fill="none"
      stroke="#B9B3AA" stroke-width="${CARRE ? 7 : 10}" stroke-linecap="round" opacity=".75"/></svg>`, embleme);
  const volute = fumee.querySelector("path");
  M.trait(volute);

  // au centre de l'anneau : le compteur des jours
  const chiffre = noeud(`<div class="chiffre-anneau" data-zone="texte" style="top:${G.cy - (CARRE ? 92 : 132)}px">0</div>`, embleme);
  const jours = noeud(`<div class="jours" data-zone="texte" style="top:${G.cy + (CARRE ? 58 : 86)}px">jours</div>`, embleme);
  const titre = noeud(`<div class="titre" data-zone="texte" style="top:${G.titre}px">Mois sans tabac</div>`, embleme);
  const dates = noeud(`<div class="dates" data-zone="texte" style="top:${G.titre + (CARRE ? 96 : 128)}px">Du 1<sup>er</sup> au 30 novembre</div>`, embleme);
  const motsTitre = decouper(titre, "m");
  gsap.set(motsTitre, { yPercent: 110 });
  gsap.set([chiffre, jours, dates], { opacity: 0 });
  gsap.set(entete, { opacity: 0, y: -16 });
  gsap.set([contour, ...segs, bague], { opacity: 0 });
  gsap.set(braise, { opacity: 0 });

  // 1. la cigarette apparait, la braise rougeoie, la fumee monte
  tl.to(entete, { opacity: 1, y: 0, duration: 1.0, ease: "power3.out" }, .2)
    .to([contour, ...segs, bague], { opacity: 1, duration: .7, ease: "power2.out" }, .15)
    .fromTo(embleme, { scale: .97 }, { scale: 1, duration: 1.4, ease: "power3.out" }, .15)
    .to(braise, { opacity: 1, duration: .5 }, .35)
    .to(braise, { boxShadow: "0 0 34px 12px rgba(245,122,58,.7)", duration: .45, yoyo: true, repeat: 1, ease: "sine.inOut" }, .8)
    .to(volute, { strokeDashoffset: 0, duration: 1.6, ease: "power1.inOut" }, .55)
    .to(fumee, { y: -50, opacity: 0, duration: 1.5, ease: "power1.in" }, 1.7);
  // 2. elle s'eteint : la braise s'eteint en fondu sur une pointe de cendre
  tl.to(segs[0], { backgroundColor: "#B3ADA4", duration: .5 }, 1.9)
    .to(braise, { opacity: 0, duration: .7, ease: "power2.inOut" }, 1.9);
  // 3. les 30 tranches s'envolent vers l'anneau (la 1re en haut, puis dans le sens des aiguilles d'une montre) ;
  // le contour tient jusqu'a l'envol : sans lui, le papier blanc se perd dans le fond clair
  const T3 = MES - .5;
  tl.to(contour, { opacity: 0, duration: .25 }, T3)
    .to(bague, { opacity: 0, duration: .25 }, T3);
  segs.forEach((s, i) => {
    const a = (-90 + i * 360 / N) * Math.PI / 180;
    const x = G.cx + G.r * Math.cos(a) - G.sw / 2, y = G.cy + G.r * Math.sin(a) - G.sh / 2;
    const t = T3 + i * .028;
    // le gris d'abord : une tranche de papier blanc en vol se perdrait dans le fond clair
    tl.to(s, { backgroundColor: GRIS, duration: .3 }, t)
      .to(s, { x, duration: 1.15, ease: "power2.inOut" }, t)
      .to(s, { y, duration: 1.15, ease: "power3.inOut" }, t)
      .to(s, { width: G.sw, height: G.sh, rotation: -90 + i * 360 / N + 90, borderRadius: G.sw / 2,
        duration: 1.0, ease: "power2.inOut" }, t + .1);
  });
  // 4. le compteur : chaque jour allume son segment
  const T4 = T3 + 1.15 + N * .028 + .05;
  tl.to([chiffre, jours], { opacity: 1, duration: .4 }, T4 - .2);
  compteur(chiffre, 0, 30, 1.7, T4, 0, "power1.inOut");
  segs.forEach((s, i) => tl.to(s, { backgroundColor: VERT, boxShadow: "0 0 14px rgba(46,158,122,.45)", duration: .18 },
    T4 + 1.7 * Math.pow((i + 1) / N, 1.05) - .05));
  // a 30 : une onde part de l'anneau, l'anneau respire une fois
  const onde = noeud(`<div style="position:absolute;left:${G.cx - G.r - G.sh / 2}px;top:${G.cy - G.r - G.sh / 2}px;
    width:${2 * G.r + G.sh}px;height:${2 * G.r + G.sh}px;border-radius:50%;border:3px solid ${VERT}"></div>`, embleme);
  gsap.set(onde, { opacity: 0 });
  // set puis to (et non fromTo, qui poserait l'onde des la construction, visible des le premier plan)
  tl.set(onde, { opacity: .7, scale: 1 }, T4 + 1.72)
    .to(onde, { opacity: 0, scale: 1.28, duration: 1.1, ease: "power2.out" }, T4 + 1.72)
    .to(segs, { scale: 1.12, duration: .22, yoyo: true, repeat: 1, ease: "sine.inOut", stagger: { each: .006 } }, T4 + 1.7);
  // 5. le nom et les dates
  const T5 = T4 + 1.5;
  tl.to(motsTitre, { yPercent: 0, duration: .9, stagger: .07, ease: "power4.out" }, T5)
    .fromTo(dates, { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: .8, ease: "power3.out" }, T5 + .45);
  // la lumiere respire
  tl.fromTo(lumiere, { opacity: .7 }, { opacity: 1, duration: D.duree / 4, yoyo: true, repeat: 3, ease: "sine.inOut" }, 0);

  // la composition s'efface a S, la carte de fin Medadom occupe les 3 dernieres secondes
  const S = V ? V.signature - .55 : D.duree - 3.3;
  if (!INFO) {
    fin();
    return;
  }

  // version info : l'anneau se range en badge sous l'entete, le nom s'efface, les plans defilent dessous
  const TI = V ? V.p1 - 1.0 : T5 + 2.2;
  const haut = CARRE ? -250 : -340, petit = CARRE ? .34 : .36;
  gsap.set(embleme, { transformOrigin: `${G.cx}px ${G.cy}px` });
  tl.to([titre, dates], { opacity: 0, duration: .4 }, TI - .1)
    .to(embleme, { y: haut, scale: petit, duration: 1.0, ease: "power3.inOut" }, TI);

  function plan(html, debut, fin) {
    const p = noeud(`<div class="plan">${html}</div>`);
    p.querySelectorAll(".phrase, .gros, .etiquette, .source").forEach(e => e.dataset.zone = "texte");
    gsap.set(p, { opacity: 0 });
    tl.set(p, { opacity: 1 }, debut).to(p, { opacity: 0, y: -24, duration: .4, ease: "power2.in" }, fin - .45);
    return p;
  }
  function entrer(el, t) {
    const mots = decouper(el, "m");
    gsap.set(mots, { yPercent: 110 });
    tl.to(mots, { yPercent: 0, duration: .85, stagger: .045, ease: "power4.out" }, t);
  }
  function apparaitre(el, t) {
    gsap.set(el, { opacity: 0, y: 24 });
    tl.to(el, { opacity: 1, y: 0, duration: .7, ease: "power3.out" }, t);
  }

  // trois plans de meme duree ; le retour final (1 s) se termine 0,6 s avant que la composition s'efface
  const L = (S - 1.6 - (TI + .5)) / 3;
  // les plans se calent sur la voix quand il y en a une (version « voix », D.temps)
  const t1 = V ? V.p1 - .25 : TI + .5, t2 = V ? V.p2 - .25 : t1 + L, t3 = V ? V.p3 - .25 : t2 + L, t4 = V ? S : t3 + L;
  const p1 = plan(`<div class="gros">55 %</div>
    <div class="phrase" style="margin-top:18px">des fumeurs quotidiens<br>souhaitent arrêter <br class="seul-916">de fumer</div>
    <div class="source" style="margin-top:40px">Source : Santé publique France, Baromètre 2024</div>`, t1, t2);
  const g1 = p1.querySelector(".gros");
  apparaitre(g1, t1 + .05); compteur(g1, 0, 55, 1.2, t1 + .05, 0, "power2.out", 0, " %");
  entrer(p1.querySelector(".phrase"), V ? V.p1b - .12 : t1 + .45);
  apparaitre(p1.querySelector(".source"), V ? V.p1b + .8 : t1 + 1.3);

  const p2 = plan(`<div class="phrase">30 jours sans tabac :</div>
    <div class="gros" style="margin-top:6px">× 5</div>
    <div class="phrase">les chances d’arrêter<br>à long terme</div>
    <div class="source" style="margin-top:40px">Source : Santé publique France, 2026,<br>d’après West et Stapleton, 2008</div>`, t2, t3);
  const [ph2a, ph2b] = p2.querySelectorAll(".phrase");
  entrer(ph2a, t2 + .05);
  gsap.set(p2.querySelector(".gros"), { opacity: 0, scale: .6 });
  tl.to(p2.querySelector(".gros"), { opacity: 1, scale: 1, duration: .8, ease: "back.out(2.2)" }, V ? V.p2b - .1 : t2 + .5);
  entrer(ph2b, V ? V.p2c - .12 : t2 + .95);
  apparaitre(p2.querySelector(".source"), V ? V.p2c + .6 : t2 + 1.6);

  // ameli : « la grande majorite des substituts nicotiniques est remboursee a 65 % » (pas tous : prix libres)
  const p3 = plan(`<div class="etiquette">Substituts nicotiniques</div>
    <div class="phrase" style="margin-top:30px">La plupart remboursés à</div>
    <div class="gros">65 %</div>
    <div class="phrase">par l’Assurance maladie,<br>sur prescription</div>
    <div class="source" style="margin-top:40px">Source : ameli.fr</div>`, t3, t4);
  const [ph3a, ph3b] = p3.querySelectorAll(".phrase"), g3 = p3.querySelector(".gros");
  apparaitre(p3.querySelector(".etiquette"), t3 + .05);
  entrer(ph3a, V ? V.p3a - .12 : t3 + .3);
  const tg3 = V ? V.p3b - .12 : t3 + .6;
  apparaitre(g3, tg3); compteur(g3, 0, 65, 1.2, tg3, 0, "power2.out", 0, " %");
  entrer(ph3b, V ? V.p3c - .12 : t3 + 1.1);
  apparaitre(p3.querySelector(".source"), V ? V.p3c + .3 : t3 + 1.6);

  // retour : l'anneau revient au centre avec son nom, puis la fin
  if (!V) tl.to(embleme, { y: 0, scale: 1, duration: 1.0, ease: "power3.inOut" }, t4 - .1)
    .to([titre, dates], { opacity: 1, duration: .5 }, t4 + .5);
  fin();

  // la composition s'efface en montant et en se brouillant, la carte de fin Medadom prend sa place, puis
  // s'efface a son tour jusqu'au fond nu du premier plan (la boucle)
  function fin() {
    tl.to([embleme, entete], { opacity: 0, y: "-=16", filter: "blur(10px)", duration: .9, ease: "power2.in" }, S);
    M.carteFin(S + .35);
  }
});
