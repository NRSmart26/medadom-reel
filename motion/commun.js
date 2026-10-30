/* Socle des pieces de motion design : lit window.DONNEES (piece, version, format, duree, ecrites par
   motion.py), fournit la frise GSAP en pause et l'interface que rendu.py attend : window.PRET, window.TL,
   window.seek(t), window.verifier(). Une piece appelle Motion.demarrer(construire), ou construire(M) pose
   le DOM et remplit M.tl. */
window.Motion = (function () {
  const D = window.DONNEES, CARRE = D.format === "1x1", H = CARRE ? 1080 : 1920;
  if (CARRE) { document.documentElement.classList.add("carre"); document.body.classList.add("carre"); }
  const tl = gsap.timeline({ paused: true });

  // zones sures : les memes que le moteur des reels (moteur.js) ; « cle » tolere un peu plus large pour un symbole
  const ZONES = CARRE
    ? { texte: [40, 40, 1040, 1040], cle: [20, 20, 1060, 1060] }
    : { texte: [94, 298, 964, 1600], cle: [30, 290, 1050, 1610] };

  function noeud(html, parent) {
    const t = document.createElement("template");
    t.innerHTML = html.trim();
    const n = t.content.firstElementChild;
    (parent || document.body).appendChild(n);
    return n;
  }

  // decoupe un texte en lettres (.l) ou en mots (.m), chacun dans un masque ; les <br> et balises restent
  function decouper(el, unite) {
    const sortie = [];
    const parcourir = (n, cible) => {
      [...n.childNodes].forEach(c => {
        if (c.nodeType === 3) {
          const morceaux = unite === "l" ? [...c.textContent] : c.textContent.split(/(\s+)/);
          morceaux.forEach(m => {
            if (!m) return;
            if (!m.trim()) { cible.appendChild(document.createTextNode(m)); return; }
            const masque = document.createElement("span"); masque.className = "masque";
            const s = document.createElement("span"); s.className = unite; s.textContent = m;
            masque.appendChild(s); cible.appendChild(masque); sortie.push(s);
          });
        } else if (c.nodeName === "BR") {
          cible.appendChild(c.cloneNode());
        } else {
          const copie = c.cloneNode(false); cible.appendChild(copie); parcourir(c, copie);
        }
      });
    };
    const source = el.cloneNode(true); el.innerHTML = ""; parcourir(source, el);
    return sortie;
  }

  // compteur anime : la valeur s'ecrit a la francaise (espace fine des milliers, virgule)
  const fmt = (v, dec) => Number(v).toFixed(dec || 0).replace(".", ",").replace(/\B(?=(\d{3})+(?!\d))/g, " ");
  // pas : 100 compte de cent en cent (60 000 defile en 0, 100, 200... sans chiffres parasites) ;
  // suffixe : ce qui suit le nombre (« % »)
  function compteur(el, de, a, duree, t, dec, ease, pas, suffixe) {
    const o = { v: de }, ecrire = () => { el.textContent = fmt(pas ? Math.round(o.v) * pas : o.v, dec) + (suffixe || ""); };
    ecrire();
    tl.to(o, { v: a, duration: duree, ease: ease || "power3.out", onUpdate: ecrire }, t);
  }

  // carte de fin : le logo se devoile de gauche a droite, la pastille monte, puis tout s'efface pour reboucler
  // sur le fond nu du premier plan. La piece efface sa composition juste avant « debut ».
  function carteFin(debut) {
    const c = noeud('<div class="fin"><div class="logo" data-zone="texte"></div><div class="pro" data-zone="texte">Professionnel</div></div>');
    const [logo, pro] = c.children;
    gsap.set(c, { opacity: 0 });
    gsap.set(logo, { clipPath: "inset(0% 100% 0% 0%)" });
    gsap.set(pro, { opacity: 0, y: 18 });
    tl.set(c, { opacity: 1 }, debut)
      .to(logo, { clipPath: "inset(0% 0% 0% 0%)", duration: 1.0, ease: "power3.inOut" }, debut)
      .to(pro, { opacity: 1, y: 0, duration: .7, ease: "power3.out" }, debut + .6)
      .to(c, { opacity: 0, filter: "blur(8px)", duration: .6, ease: "power2.in" }, D.duree - .7);
    return c;
  }

  // longueur d'un trace SVG, pour le dessiner au trait (strokeDashoffset)
  function trait(path) {
    const L = path.getTotalLength();
    gsap.set(path, { strokeDasharray: L, strokeDashoffset: L });
    return L;
  }

  const grain = noeud('<div id="grain" class="calque"></div>');
  function seek(t) {
    tl.seek(t, false);
    // grain de pellicule : 12 tirages par seconde, toujours les memes pour un instant donne
    const k = Math.floor(t * 12), x = (k * 7919) % 512, y = (k * 104729) % 512;
    grain.style.backgroundPosition = `${x}px ${y}px`;
  }

  // polices du systeme exigees par une piece (Bodoni MT vient d'Office) : absente, Chrome en prendrait une
  // autre sans rien dire. Detection par la largeur d'un texte avec deux polices de repli differentes.
  const exigees = [];
  function exiger(nom) { exigees.push(nom); }
  function presente(nom) {
    const c = document.createElement("canvas").getContext("2d"), t = "Movember Mois sans tabac 0123456789";
    c.font = `72px "${nom}", monospace`; const a = c.measureText(t).width;
    c.font = `72px "${nom}", sans-serif`; const b = c.measureText(t).width;
    return Math.abs(a - b) < .5;
  }

  function verifier() {
    const ecarts = exigees.filter(n => !presente(n)).map(n => `police absente : ${n}`);
    document.querySelectorAll("[data-zone]").forEach(el => {
      let n = el, visible = true;
      while (n && n !== document.body) { if (+getComputedStyle(n).opacity < 0.5) { visible = false; break; } n = n.parentElement; }
      if (!visible) return;
      // un texte se mesure a son contenu (les blocs de texte prennent toute la largeur), un SVG a sa boite
      let r = el.getBoundingClientRect();
      if (!(el instanceof SVGElement)) { const g = document.createRange(); g.selectNodeContents(el); r = g.getBoundingClientRect(); }
      const [x0, y0, x1, y1] = ZONES[el.dataset.zone];
      if (r.width === 0) return;
      if (r.left < x0 || r.top < y0 || r.right > x1 || r.bottom > y1)
        ecarts.push(`${el.id || el.className} : ${Math.round(r.left)},${Math.round(r.top)} -> ${Math.round(r.right)},${Math.round(r.bottom)}`);
    });
    return ecarts;
  }

  function demarrer(construire) {
    document.fonts.ready.then(() => {
      const imgs = [...document.images].map(i => i.complete ? null : new Promise(r => { i.onload = i.onerror = r; }));
      Promise.all(imgs).then(() => {
        construire(M);
        document.body.appendChild(grain);   // le grain passe au-dessus de tout ce que la piece a pose
        // la frise dure exactement la duree prevue (rendu.py la compare au son)
        tl.set({}, {}, D.duree);
        window.TL = tl; window.seek = seek; window.verifier = verifier; window.PRET = true;
        seek(0);
        if (!location.search.includes("rendu")) tl.play();
      });
    });
  }

  const M = { D, CARRE, H, tl, noeud, decouper, compteur, trait, fmt, demarrer, exiger, carteFin };
  return M;
})();
