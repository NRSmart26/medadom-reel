/* Moteur des reels Medadom, version premium : construit les scenes a partir de
   window.DONNEES (ecrites par reel_medadom.py, avec les instants tires de la voix) et une frise
   GSAP en pause. Les mots entrent quand la voix les dit ; les dessins detoures arrivent avec
   leur ombre puis flottent doucement ; chaque scene sort proprement avant la suivante. */
(function () {
  const D = window.DONNEES, racine = document.body, tl = gsap.timeline({ paused: true });
  const fmt = (v, dec) => Number(v).toFixed(dec || 0).replace(".", ",").replace(/\B(?=(\d{3})+(?!\d))/g, " ");
  Object.entries(D.theme).forEach(([k, v]) => document.documentElement.style.setProperty("--" + k, v));

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

  function element(e) {
    const n = document.createElement("div");
    n.dataset.etape = e.etape || 0;
    n.dataset.zone = "texte";
    switch (e.genre) {
      case "etiquette": n.className = "etiquette"; n.textContent = e.texte; break;
      case "pastille": n.className = "pastille" + (e.alerte ? " alerte" : ""); n.textContent = e.texte; break;
      case "chiffre": n.className = "chiffre";
        n.innerHTML = `${e.prefixe || ""}<span class="valeur">${fmt(e.valeur, e.dec)}</span>${e.suffixe || ""}`; break;
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
  const fin = document.createElement("section");
  fin.className = "scene"; fin.id = "fin";
  fin.innerHTML = `<div class="fin"><div class="carte" data-zone="texte"><img class="logo" src="${D.logo}">
    <div class="pro">Professionnel</div></div><div class="bio" data-zone="texte">Le lien est en bio</div></div>`;
  racine.appendChild(fin);

  // le visuel prend la place qui reste sous les textes
  function mettreEnPage() {
    scenes.forEach(({ sc, col, visuel, sol }) => {
      if (!visuel) return;
      sc.style.opacity = 1;
      const haut = col.getBoundingClientRect().bottom + 56;
      if (visuel.className === "telbloc") {
        const dispo = 1600 - haut, k = Math.min(1, dispo / 764);
        visuel.style.left = (540 - 186 * k) + "px"; visuel.style.top = haut + "px";
        visuel.style.width = 372 * k + "px"; visuel.style.height = 764 * k + "px";
        visuel.firstElementChild.style.transform = `scale(${k})`; visuel.firstElementChild.style.transformOrigin = "0 0";
        visuel.dataset.zone = "cle";
      } else {
        const r = +visuel.dataset.ratio, bas = visuel.dataset.bas === "1";
        const bord = bas ? 1920 + 26 : 1580;
        let h = Math.min(bord - haut, bas ? 1100 : 720), w = h * r;
        if (w > 980) { w = 980; h = w / r; }
        const top = bord - h, left = 540 - w / 2;
        Object.assign(visuel.style, { left: left + "px", top: top + "px", width: w + "px", height: h + "px" });
        visuel.dataset.zone = bas ? "bas" : "cle";
        if (sol) Object.assign(sol.style, { left: (540 - w * .36) + "px", top: (top + h - 34) + "px", width: w * .72 + "px", height: "46px" });
      }
      sc.style.opacity = 0;
    });
  }

  function frise() {
    // decor vivant
    tl.to(".forme.a", { x: 120, y: -80, duration: D.duree, ease: "sine.inOut" }, 0)
      .to(".forme.b", { x: -100, y: 90, duration: D.duree, ease: "sine.inOut" }, 0)
      .from(".entete", { opacity: 0, y: -20, duration: .6, ease: "power3.out" }, 0);

    scenes.forEach(({ s, sc, col, visuel, sol }) => {
      tl.set(sc, { opacity: 1 }, s.debut);
      tl.set(sc, { opacity: 0 }, s.fin);
      const parEtape = {};
      col.querySelectorAll("[data-etape]").forEach(el => {
        const k = +el.dataset.etape, t = s.etapes[Math.min(k, s.etapes.length - 1)];
        const rang = parEtape[k] = (parEtape[k] || 0) + 1, dt = t + (rang - 1) * 0.14;
        if (el.classList.contains("etiquette")) {
          tl.from(el, { x: -60, opacity: 0, duration: .6, ease: "back.out(1.8)" }, dt);
        } else if (el.classList.contains("pastille")) {
          tl.from(el, { x: -90, opacity: 0, scale: .94, transformOrigin: "left center", duration: .65, ease: "back.out(1.5)" }, dt);
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
    const zones = { texte: [96, 300, 964, 1600], cle: [30, 290, 1050, 1610], bas: [30, 290, 1050, 1990] }, ecarts = [];
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
  document.fonts.ready.then(() => {
    const imgs = [...document.images].map(i => i.complete ? null : new Promise(r => { i.onload = i.onerror = r; }));
    Promise.all(imgs).then(() => { mettreEnPage(); frise(); window.PRET = true;
      if (!location.search.includes("rendu")) tl.play(); });
  });
})();
