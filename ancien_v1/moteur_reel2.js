/* Moteur des reels Medadom, version 2 (29/10/2026), sur la base de moteur_reel.js : construit les scenes a
   partir de window.DONNEES (ecrites par le generateur, avec les instants tires de la voix) et une frise GSAP
   en pause. Ajouts de la version 2 :
   - texte ajuste : chaque scene recoit l'echelle --k la plus grande ou son texte tient, le dessin gardant
     sa place (Romain, 29/10/2026 : « le texte doit etre gros quand on a la place, ils vont voir ca sur un
     mobile ») ;
   - pastilles barrees (un trait rouge raye ce qui n'est plus recommande) et grilles de criteres qui se
     cochent une a une ;
   - une barre de progression, une graduation par scene ;
   - le format carre de LinkedIn (DONNEES.format.carre) : texte a gauche, dessin a droite. */
(function () {
  const D = window.DONNEES, racine = document.body, tl = gsap.timeline({ paused: true });
  const CARRE = !!(D.format && D.format.carre), H = CARRE ? 1080 : 1920;
  if (CARRE) document.body.classList.add("carre");
  const fmt = (v, dec) => Number(v).toFixed(dec || 0).replace(".", ",").replace(/\B(?=(\d{3})+(?!\d))/g, " ");
  Object.entries(D.theme).forEach(([k, v]) => document.documentElement.style.setProperty("--" + k, v));
  const couleur = nom => getComputedStyle(document.documentElement).getPropertyValue("--" + nom).trim();

  function telephone(src, position) {
    return `<div class="tel">
      <span class="bouton" style="left:-5px;top:150px;height:46px"></span>
      <span class="bouton" style="left:-5px;top:220px;height:80px"></span>
      <span class="bouton" style="left:-5px;top:312px;height:80px"></span>
      <span class="bouton" style="right:-5px;top:240px;height:120px"></span>
      <div class="ecran">
        <img src="${src}" style="object-position:${position || "50% 50%"}">
        <div class="ile"></div>
        <div class="barre"><i></i>Téléconsultation</div>
        <div class="commandes">
          <span><svg width="30" height="30" viewBox="0 0 24 24"><rect x="9" y="3" width="6" height="11" rx="3" fill="#1F1650"/><path d="M6 11a6 6 0 0 0 12 0M12 17v4" stroke="#1F1650" stroke-width="2" fill="none" stroke-linecap="round"/></svg></span>
          <span class="raccrocher"><svg width="34" height="34" viewBox="0 0 24 24"><path d="M3 13c5-4 13-4 18 0l-2 3-4-1v-2c-2-.6-4-.6-6 0v2l-4 1z" fill="#fff"/></svg></span>
          <span><svg width="32" height="32" viewBox="0 0 24 24"><rect x="3" y="7" width="12" height="10" rx="2" fill="#1F1650"/><path d="M15 11l6-3v8l-6-3z" fill="#1F1650"/></svg></span>
        </div>
      </div>
      <div class="reflet"></div>
    </div>`;
  }

  // decoupe en mots : les noeuds texte mot par mot, les balises (surligne, souligne, b) en bloc
  function enMots(el) {
    const morceaux = [];
    [...el.childNodes].forEach(n => {
      if (n.nodeType === 3) {
        n.textContent.split(/(\s+)/).forEach(m => { if (m) morceaux.push(m.trim() ? Object.assign(document.createElement("span"), { className: "mot", textContent: m }) : document.createTextNode(m)); });
      } else if (n.nodeName === "BR") {
        morceaux.push(n.cloneNode());
      } else {
        const s = document.createElement("span"); s.className = "mot"; s.appendChild(n.cloneNode(true)); morceaux.push(s);
      }
    });
    el.innerHTML = "";
    morceaux.forEach(m => el.appendChild(m));
  }

  const CROIX = `<svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18" stroke="#fff" stroke-width="3.6" stroke-linecap="round"/></svg>`;
  const COCHE = `<svg viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>`;

  function element(e) {
    const n = document.createElement("div");
    n.dataset.etape = e.etape || 0;
    n.dataset.zone = "texte";
    switch (e.genre) {
      case "etiquette": n.className = "etiquette"; n.innerHTML = e.texte; break;
      case "pastille":
        n.className = "pastille" + (e.alerte ? " alerte" : "") + (e.barree ? " barree" : "");
        // le texte dans un seul span : sinon un <b> devient une colonne a part de la pastille (flex)
        n.innerHTML = e.barree ? `<span class="croix">${CROIX}</span><span class="libelle">${e.texte}<i class="trait"></i></span>`
          : `<span>${e.texte}</span>`;
        break;
      case "criteres": n.className = "criteres"; n.dataset.pas = e.pas || .3;
        n.innerHTML = e.items.map(it => `<div class="critere${it.large ? " large" : ""}"><span class="case">${COCHE}</span><span>${it.texte}</span></div>`).join("");
        break;
      case "chiffre": n.className = "chiffre";
        n.innerHTML = `${e.prefixe || ""}<span class="valeur">${fmt(e.valeur, e.dec)}</span><span class="unite">${e.suffixe || ""}</span>`; break;
      default: n.className = e.genre; n.innerHTML = e.html; enMots(n);
    }
    return n;
  }

  const scenes = D.scenes.map((s, i) => {
    const sc = document.createElement("section");
    sc.className = "scene"; sc.id = "scene" + i;
    const col = document.createElement("div"); col.className = "colonne";
    let visuel = null;
    s.elements.forEach(e => {
      if (e.genre === "dessin") {
        visuel = document.createElement("div"); visuel.className = "dessin";
        visuel.innerHTML = `<img src="${e.src}">`;
        visuel.dataset.bas = e.bas ? 1 : 0; visuel.dataset.etape = e.etape || 0;
        visuel.dataset.ratio = e.ratio;
      } else if (e.genre === "telephone") {
        visuel = document.createElement("div"); visuel.className = "telbloc";
        visuel.innerHTML = telephone(e.src, e.position);
        visuel.dataset.etape = e.etape || 0;
      } else col.appendChild(element(e));
    });
    sc.appendChild(col);
    let sol = null;
    if (visuel) {
      if (visuel.className === "dessin" && visuel.dataset.bas === "0") { sol = document.createElement("div"); sol.className = "sol"; sc.appendChild(sol); }
      sc.appendChild(visuel);
    }
    racine.appendChild(sc);
    return { s, sc, col, visuel, sol };
  });
  const prog = document.createElement("div"); prog.className = "progression";
  prog.innerHTML = scenes.map(() => "<i><b></b></i>").join("");
  racine.appendChild(prog);
  const fin = document.createElement("section");
  fin.className = "scene"; fin.id = "fin";
  fin.innerHTML = `<div class="fin"><div class="carte" data-zone="texte"><img class="logo" src="${D.logo}">
    <div class="pro">Professionnel</div></div><div class="bio" data-zone="texte">${D.bio || "Le lien est en bio"}</div></div>`;
  racine.appendChild(fin);

  // le texte : la plus grande echelle ou il tient (hauteur et largeur) ; le dessin garde sa place
  const P = CARRE
    ? { kmax: 1.0, kmax_seul: 1.25, kmin: .5, bas: 1032, reserve: 0 }
    : { kmax: 1.36, kmax_seul: 1.7, kmin: .7, bas: 1600, reserve: 430 };   // le texte d'abord, le dessin s'adapte
  function ajuster(sc, col, visuel) {
    const limite = P.bas - (visuel && !CARRE ? P.reserve : 0);
    // sans dessin, le texte prend toute la place : plus grand, et toute la largeur en carre
    if (!visuel && CARRE) col.style.width = "968px";
    if (visuel && CARRE) col.classList.add("etroite");
    let k = visuel ? P.kmax : P.kmax_seul;
    for (; k > P.kmin; k -= .02) {
      col.style.setProperty("--k", k.toFixed(3));
      const r = col.getBoundingClientRect();
      const deborde = [...col.querySelectorAll("*")].some(el => el.getBoundingClientRect().right > r.right + 1);
      if (r.bottom <= limite && !deborde) break;
    }
    return k;
  }

  function mettreEnPage() {
    scenes.forEach(({ sc, col, visuel, sol }) => {
      sc.style.opacity = 1;
      ajuster(sc, col, visuel);
      if (!visuel) {                      // sans dessin : le texte se centre dans la zone, un peu au-dessus du milieu
        const haut0 = CARRE ? 150 : 300, h = col.getBoundingClientRect().height;
        col.style.top = (haut0 + Math.max(0, (P.bas - haut0 - h) * .42)) + "px";
        sc.style.opacity = 0; return;
      }
      const haut = col.getBoundingClientRect().bottom + 56;
      if (visuel.className === "telbloc") {
        let k, left, top;
        if (CARRE) { k = Math.min(1, (H - 150 - 40) / 764); left = 640 + (420 - 372 * k) / 2; top = 150; }
        else { k = Math.min(1, (1600 - haut) / 764); left = 540 - 186 * k; top = haut; }
        Object.assign(visuel.style, { left: left + "px", top: top + "px", width: 372 * k + "px", height: 764 * k + "px" });
        visuel.firstElementChild.style.transform = `scale(${k})`; visuel.firstElementChild.style.transformOrigin = "0 0";
        visuel.dataset.zone = "cle";
      } else {
        const r = +visuel.dataset.ratio, bas = visuel.dataset.bas === "1";
        let w, h, left, top;
        if (CARRE) {
          const zw = 420, bord = bas ? H + 20 : H - 70, zh = bord - 160;
          h = zh; w = h * r;
          if (w > zw) { w = zw; h = w / r; }
          left = 640 + (zw - w) / 2; top = bord - h;
        } else {
          const bord = bas ? H + 26 : 1580;
          h = Math.min(bord - haut, bas ? 1100 : 760); w = h * r;
          if (w > 980) { w = 980; h = w / r; }
          top = bord - h; left = 540 - w / 2;
        }
        Object.assign(visuel.style, { left: left + "px", top: top + "px", width: w + "px", height: h + "px" });
        visuel.dataset.zone = bas ? "bas" : "cle";
        if (sol) Object.assign(sol.style, { left: (left + w * .14) + "px", top: (top + h - 34) + "px", width: w * .72 + "px", height: "46px" });
      }
      sc.style.opacity = 0;
    });
  }

  function frise() {
    const accent = couleur("accent");
    // decor vivant
    tl.to(".forme.a", { x: 120, y: -80, duration: D.duree, ease: "sine.inOut" }, 0)
      .to(".forme.b", { x: -100, y: 90, duration: D.duree, ease: "sine.inOut" }, 0)
      .from(".entete", { opacity: 0, y: -20, duration: .6, ease: "power3.out" }, 0)
      .from(".progression", { opacity: 0, duration: .6 }, .2);
    const graduations = prog.querySelectorAll("b");
    scenes.forEach(({ s }, i) => tl.to(graduations[i], { scaleX: 1, duration: Math.max(.1, s.fin - s.debut), ease: "none" }, s.debut));
    tl.to(prog, { opacity: 0, duration: .3 }, D.fin - .3);

    scenes.forEach(({ s, sc, col, visuel, sol }) => {
      tl.set(sc, { opacity: 1 }, s.debut);
      tl.set(sc, { opacity: 0 }, s.fin);
      const parEtape = {};
      col.querySelectorAll(":scope > [data-etape]").forEach(el => {
        const k = +el.dataset.etape, t = s.etapes[Math.min(k, s.etapes.length - 1)];
        const rang = parEtape[k] = (parEtape[k] || 0) + 1, dt = t + (rang - 1) * 0.16;
        if (el.classList.contains("etiquette")) {
          tl.from(el, { x: -60, opacity: 0, duration: .6, ease: "back.out(1.8)" }, dt);
        } else if (el.classList.contains("pastille")) {
          tl.from(el, { x: -90, opacity: 0, scale: .94, transformOrigin: "left center", duration: .65, ease: "back.out(1.5)" }, dt);
          if (el.classList.contains("barree")) {
            tl.from(el.querySelector(".croix"), { scale: 0, rotation: -90, duration: .45, ease: "back.out(2.4)" }, dt + .55)
              .to(el.querySelector(".trait"), { scaleX: 1, duration: .45, ease: "power2.inOut" }, dt + .6)
              .to(el.querySelector(".libelle"), { opacity: .55, duration: .4 }, dt + .9);
          }
          if (el.classList.contains("alerte"))
            tl.to(el, { scale: 1.045, duration: .22, yoyo: true, repeat: 1, ease: "sine.inOut", transformOrigin: "left center" }, dt + .75);
        } else if (el.classList.contains("criteres")) {
          const pas = +el.dataset.pas;
          el.querySelectorAll(".critere").forEach((c, j) => {
            const tj = dt + j * pas;
            tl.from(c, { y: 34, scale: .86, opacity: 0, duration: .5, ease: "back.out(1.7)" }, tj)
              .to(c.querySelector(".case"), { backgroundColor: accent, borderColor: accent, duration: .2 }, tj + .28)
              .to(c.querySelector("path"), { strokeDashoffset: 0, duration: .3, ease: "power2.out" }, tj + .32)
              .from(c.querySelector(".case"), { scale: .6, duration: .35, ease: "back.out(3)" }, tj + .28);
          });
        } else if (el.classList.contains("chiffre")) {
          tl.from(el, { scale: .78, opacity: 0, transformOrigin: "left bottom", duration: .7, ease: "back.out(2)" }, dt);
          const v = el.querySelector(".valeur"), e = s.elements.find(x => x.genre === "chiffre"), o = { v: 0 };
          tl.to(o, { v: e.valeur, duration: 1.1, ease: "power2.out", onUpdate: () => v.textContent = fmt(o.v, e.dec) }, dt);
        } else {
          const mots = el.querySelectorAll(".mot");
          tl.from(mots, { y: 54, opacity: 0, duration: .6, stagger: .045, ease: "power4.out" }, dt);
        }
        el.querySelectorAll(".surligne").forEach(h => { gsap.set(h, { "--trace": 0 }); tl.to(h, { "--trace": 1, duration: .5, ease: "power2.inOut" }, dt + .2); });
        el.querySelectorAll(".souligne").forEach(h => { gsap.set(h, { "--trait": 0 }); tl.to(h, { "--trait": 1, duration: .5, ease: "power2.inOut" }, dt + .3); });
      });
      if (visuel) {
        const t = s.etapes[Math.min(+visuel.dataset.etape, s.etapes.length - 1)] + .1;
        tl.from(visuel, { y: 150, opacity: 0, scale: .9, transformOrigin: "50% 100%", duration: 1.0, ease: "power3.out" }, t);
        if (sol) tl.from(sol, { opacity: 0, scaleX: .5, duration: 1.0, ease: "power3.out" }, t);
        const flotte = Math.max(0, s.fin - .45 - (t + 1.0));
        if (flotte > 1) tl.to(visuel, { y: -12, duration: Math.min(2.4, flotte / 2), yoyo: true,
          repeat: Math.max(1, Math.floor(flotte / Math.min(2.4, flotte / 2)) - 1), ease: "sine.inOut" }, t + 1.0);
        tl.to(visuel, { opacity: 0, y: 40, duration: .35, ease: "power2.in" }, s.fin - .38);
        if (sol) tl.to(sol, { opacity: 0, duration: .35 }, s.fin - .38);
      }
      tl.to(col.children, { opacity: 0, y: -36, duration: .35, stagger: .03, ease: "power2.in" }, s.fin - .42);
    });
    tl.set(fin, { opacity: 1 }, D.fin);
    tl.from("#fin .carte", { scale: .82, opacity: 0, duration: .8, ease: "back.out(1.6)" }, D.fin)
      .from("#fin .logo", { y: 24, opacity: 0, duration: .6, ease: "power3.out" }, D.fin + .25)
      .from("#fin .pro", { y: 18, opacity: 0, duration: .5, ease: "power3.out" }, D.fin + .45)
      .from("#fin .bio", { y: 30, opacity: 0, duration: .6, ease: "power3.out" }, D.fin + .7);
    tl.to({}, { duration: .01 }, D.duree - .01);
  }

  window.TL = tl;
  window.seek = t => { tl.seek(t, false); };
  window.verifier = () => {
    const zones = CARRE
      ? { texte: [40, 40, 1040, 1040], cle: [20, 20, 1060, 1060], bas: [20, 20, 1060, 1110] }
      : { texte: [94, 298, 964, 1600], cle: [30, 290, 1050, 1610], bas: [30, 290, 1050, 1990] }, ecarts = [];
    document.querySelectorAll(".scene").forEach(sc => {
      if (+getComputedStyle(sc).opacity < 0.5) return;
      sc.querySelectorAll("[data-zone]").forEach(el => {
        if (+getComputedStyle(el).opacity < 0.5) return;
        const [x0, y0, x1, y1] = zones[el.dataset.zone], r = el.getBoundingClientRect();
        if (r.left < x0 || r.top < y0 || r.right > x1 || r.bottom > y1)
          ecarts.push(`${sc.id} ${el.className} : ${Math.round(r.left)},${Math.round(r.top)} -> ${Math.round(r.right)},${Math.round(r.bottom)}`);
      });
    });
    return ecarts;
  };
  // echelle de texte retenue par scene, pour le controle
  window.echelles = () => scenes.map(({ col }) => +col.style.getPropertyValue("--k"));
  document.fonts.ready.then(() => {
    const imgs = [...document.images].map(i => i.complete ? null : new Promise(r => { i.onload = i.onerror = r; }));
    Promise.all(imgs).then(() => { mettreEnPage(); frise(); window.PRET = true;
      if (!location.search.includes("rendu")) tl.play(); });
  });
})();
