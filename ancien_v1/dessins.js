/* Dessins Medadom Professionnel (20/10/2026) : personnages et objets en SVG plat, avec
   des ombres douces, faits pour etre animes. Chaque fonction rend une chaine SVG ; les pieces
   animables portent une classe (tete, paupieres, bouche-*, sourcils-*, bras, respire...),
   prefixee par l'identifiant du personnage pour que plusieurs dessins cohabitent. */
(function () {
  const NAVY = "#1F1650";
  const PEAUX = {
    claire: { p: "#F7CDB0", o: "#E9AD8B", j: "#F29A9A" },
    mate: { p: "#D9A07A", o: "#C2805A", j: "#E07F72" },
    foncee: { p: "#8D5A3B", o: "#744629", j: "#B5624E" },
  };

  /* ------------------------------------------------------------ visage commun */
  function visage(id, peau, opts) {
    const P = PEAUX[peau];
    const cils = opts.cils
      ? `<path d="M254,256 l-9,-7 M262,252 l-6,-9 M338,256 l9,-7 M330,252 l6,-9" stroke="#2A2140" stroke-width="4" stroke-linecap="round"/>`
      : "";
    return `
    <ellipse cx="234" cy="270" rx="17" ry="24" fill="${P.p}"/>
    <path d="M232,258 q-8,12 2,24" stroke="${P.o}" stroke-width="5" fill="none" stroke-linecap="round"/>
    <ellipse cx="366" cy="270" rx="17" ry="24" fill="${P.p}"/>
    <path d="M368,258 q8,12 -2,24" stroke="${P.o}" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M300,168 C360,168 386,214 384,272 C382,334 346,378 300,380 C254,378 218,334 216,272 C214,214 240,168 300,168 Z" fill="${P.p}"/>
    <path d="M226,300 C236,350 268,376 300,380 C262,368 238,338 226,300 Z" fill="${P.o}" opacity=".45"/>
    <ellipse cx="252" cy="312" rx="20" ry="12" fill="${P.j}" opacity=".35"/>
    <ellipse cx="348" cy="312" rx="20" ry="12" fill="${P.j}" opacity=".35"/>
    <g class="${id}-yeux">
      <ellipse cx="266" cy="272" rx="9" ry="11.5" fill="#2A2140"/>
      <ellipse cx="334" cy="272" rx="9" ry="11.5" fill="#2A2140"/>
      <circle cx="269" cy="267" r="3.2" fill="#fff"/><circle cx="337" cy="267" r="3.2" fill="#fff"/>
      ${cils}
    </g>
    <g class="${id}-paupieres" style="transform-origin:300px 258px; transform:scaleY(0)">
      <rect x="252" y="257" width="30" height="28" rx="12" fill="${P.p}"/>
      <rect x="320" y="257" width="30" height="28" rx="12" fill="${P.p}"/>
      <path d="M254,280 q12,6 24,0 M322,280 q12,6 24,0" stroke="#2A2140" stroke-width="4" fill="none" stroke-linecap="round"/>
    </g>
    <g class="${id}-sourcils-calmes">
      <path d="M250,238 Q266,229 282,236" stroke="${opts.sourcils}" stroke-width="7" fill="none" stroke-linecap="round"/>
      <path d="M318,236 Q334,229 350,238" stroke="${opts.sourcils}" stroke-width="7" fill="none" stroke-linecap="round"/>
    </g>
    <g class="${id}-sourcils-inquiets" style="opacity:0">
      <path d="M250,240 Q266,236 282,228" stroke="${opts.sourcils}" stroke-width="7" fill="none" stroke-linecap="round"/>
      <path d="M318,228 Q334,236 350,240" stroke="${opts.sourcils}" stroke-width="7" fill="none" stroke-linecap="round"/>
    </g>
    <path d="M300,288 Q290,312 306,318" stroke="${P.o}" stroke-width="6" fill="none" stroke-linecap="round"/>
    <g class="${id}-bouche-sourire">
      <path d="M272,334 Q300,364 328,334 Q300,346 272,334 Z" fill="#A23E3A"/>
      <path d="M284,348 Q300,358 316,348 Q300,352 284,348 Z" fill="#E77F79"/>
    </g>
    <g class="${id}-bouche-ouverte" style="opacity:0">
      <ellipse cx="300" cy="342" rx="17" ry="14" fill="#A23E3A"/>
      <ellipse cx="300" cy="350" rx="10" ry="5" fill="#E77F79"/>
    </g>
    <g class="${id}-bouche-inquiete" style="opacity:0">
      <path d="M282,344 Q300,334 318,344" stroke="#A23E3A" stroke-width="6" fill="none" stroke-linecap="round"/>
    </g>`;
  }

  /* --------------------------------------------- medecin en teleconsultation */
  function medecin(id, o) {
    o = Object.assign({ peau: "claire", cheveux: "#5B3423", reflet: "#7E4C33", tenue: "#7FB8E8",
                        accent: "#E4579A", femme: true, casque: true }, o || {});
    const P = PEAUX[o.peau];
    const cheveuxDos = o.femme
      ? `<path d="M196,300 C184,186 238,124 300,122 C374,124 422,186 408,300 C416,352 426,402 394,434
           C384,392 380,358 370,334 L230,334 C220,358 216,392 206,434 C174,402 184,352 196,300 Z" fill="${o.cheveux}"/>`
      : "";
    const meche = o.femme
      ? `<path d="M220,268 C216,190 262,146 310,148 C362,150 392,192 386,256 C366,214 334,196 302,198
           C266,200 238,226 220,268 Z" fill="${o.cheveux}"/>
         <path d="M300,166 C326,160 356,172 370,196" stroke="${o.reflet}" stroke-width="7" fill="none" stroke-linecap="round"/>
         <path d="M246,196 C260,176 280,168 300,168" stroke="${o.reflet}" stroke-width="5" fill="none" stroke-linecap="round" opacity=".7"/>`
      : `<path d="M216,250 C206,170 260,128 310,130 C366,132 400,174 386,248 C380,222 368,206 352,198
           C330,212 290,214 262,204 C240,214 224,232 216,250 Z" fill="${o.cheveux}"/>
         <path d="M262,204 C286,196 318,198 352,198" stroke="${o.reflet}" stroke-width="6" fill="none" stroke-linecap="round"/>`;
    const casque = o.casque
      ? `<path d="M222,262 C214,150 386,150 378,262" stroke="${NAVY}" stroke-width="13" fill="none" stroke-linecap="round"/>
         <rect x="200" y="238" width="34" height="62" rx="15" fill="${NAVY}"/>
         <rect x="366" y="238" width="34" height="62" rx="15" fill="${NAVY}"/>
         <rect x="206" y="252" width="8" height="34" rx="4" fill="${o.accent}"/>
         <path d="M218,296 C226,332 246,350 272,354" stroke="${NAVY}" stroke-width="8" fill="none" stroke-linecap="round"/>
         <ellipse cx="276" cy="354" rx="9" ry="7" fill="${o.accent}"/>`
      : "";
    return `<svg viewBox="0 0 600 760" xmlns="http://www.w3.org/2000/svg" overflow="visible">
  <g class="${id}-respire" style="transform-origin:300px 760px">
    ${cheveuxDos}
    <path d="M118,760 L124,566 Q128,472 214,448 L268,426 Q300,448 332,426 L386,448 Q472,472 476,566 L482,760 Z" fill="#FFFFFF"/>
    <path d="M118,760 L124,566 Q128,500 172,470 Q150,572 162,760 Z" fill="#E7EBF3"/>
    <path d="M482,760 L476,566 Q472,500 428,470 Q450,572 438,760 Z" fill="#E7EBF3"/>
    <path d="M268,426 L300,516 L332,426 Q300,448 268,426 Z" fill="${o.tenue}"/>
    <path d="M268,426 L300,516 L262,606 L222,454 Z" fill="#FFFFFF"/>
    <path d="M300,516 L262,606 L250,560 Z" fill="#E7EBF3"/>
    <path d="M332,426 L300,516 L338,606 L378,454 Z" fill="#FFFFFF"/>
    <path d="M300,516 L338,606 L350,560 Z" fill="#E7EBF3"/>
    <rect x="182" y="584" width="66" height="10" rx="5" fill="#E1E5EE"/>
    <rect x="194" y="556" width="9" height="34" rx="4.5" fill="${o.accent}"/>
    <rect x="208" y="560" width="9" height="30" rx="4.5" fill="${NAVY}"/>
    <rect x="364" y="532" width="62" height="80" rx="10" fill="#FFFFFF" stroke="#DDE2EC" stroke-width="3"/>
    <rect x="374" y="544" width="42" height="28" rx="6" fill="${o.accent}" opacity=".85"/>
    <rect x="374" y="580" width="42" height="7" rx="3.5" fill="#DDE2EC"/>
    <rect x="374" y="592" width="28" height="7" rx="3.5" fill="#DDE2EC"/>
    <path d="M262,434 C236,504 238,566 264,610" stroke="#3B3D5C" stroke-width="9" fill="none" stroke-linecap="round"/>
    <path d="M338,434 C364,504 362,566 336,610" stroke="#3B3D5C" stroke-width="9" fill="none" stroke-linecap="round"/>
    <path d="M264,610 Q300,644 336,610" stroke="#3B3D5C" stroke-width="9" fill="none"/>
    <path d="M300,628 C300,660 282,690 256,700" stroke="#3B3D5C" stroke-width="9" fill="none" stroke-linecap="round"/>
    <circle cx="242" cy="708" r="27" fill="#CDD2DF" stroke="#3B3D5C" stroke-width="7"/>
    <circle cx="242" cy="708" r="12" fill="#F4F6FA"/>
    <path d="M272,362 L328,362 L334,432 Q300,456 266,432 Z" fill="${P.p}"/>
    <path d="M272,362 L328,362 L330,394 Q300,412 270,394 Z" fill="${P.o}"/>
    <g class="${id}-tete" style="transform-origin:300px 390px">
      ${visage(id, o.peau, { cils: o.femme, sourcils: o.femme ? "#4A2A1A" : "#3A2418" })}
      ${meche}
      ${casque}
    </g>
  </g>
  <g class="${id}-bras" style="transform-origin:440px 480px">
    <path d="M440,480 C486,540 512,610 506,668" stroke="#E1E5EE" stroke-width="82" fill="none" stroke-linecap="round"/>
    <path d="M440,480 C486,540 512,610 506,668" stroke="#FFFFFF" stroke-width="72" fill="none" stroke-linecap="round"/>
    <path d="M506,668 C500,618 482,580 462,552" stroke="#E1E5EE" stroke-width="72" fill="none" stroke-linecap="round"/>
    <path d="M506,668 C500,618 482,580 462,552" stroke="#FFFFFF" stroke-width="64" fill="none" stroke-linecap="round"/>
    <path d="M478,566 L446,540" stroke="${o.tenue}" stroke-width="20" stroke-linecap="round"/>
    <g transform="translate(452 498) rotate(-14)">
      <ellipse cx="0" cy="0" rx="36" ry="42" fill="${P.p}"/>
      <rect x="-32" y="-82" width="16" height="50" rx="8" fill="${P.p}"/>
      <rect x="-14" y="-92" width="16" height="58" rx="8" fill="${P.p}"/>
      <rect x="4" y="-88" width="16" height="54" rx="8" fill="${P.p}"/>
      <rect x="20" y="-74" width="15" height="44" rx="7.5" fill="${P.p}"/>
      <path d="M-30,6 C-56,-6 -62,-30 -52,-40" stroke="${P.p}" stroke-width="17" fill="none" stroke-linecap="round"/>
      <path d="M-20,20 C-6,30 14,30 28,18" stroke="${P.o}" stroke-width="4" fill="none" stroke-linecap="round"/>
    </g>
  </g>
</svg>`;
  }

  /* -------------------------------------------------- patiente a la maison */
  function patiente(id, o) {
    o = Object.assign({ peau: "mate", cheveux: "#2B2233", reflet: "#4A3A55", pull: "#F7B6D2",
                        pullOmbre: "#EE97BE", canape: "#B9C3E8", canapeOmbre: "#A3AEDB" }, o || {});
    const P = PEAUX[o.peau];
    return `<svg viewBox="0 0 640 760" xmlns="http://www.w3.org/2000/svg" overflow="visible">
  <rect x="20" y="430" width="600" height="300" rx="70" fill="${o.canape}"/>
  <rect x="20" y="600" width="600" height="130" rx="50" fill="${o.canapeOmbre}"/>
  <rect x="0" y="470" width="110" height="260" rx="55" fill="${o.canapeOmbre}"/>
  <rect x="530" y="470" width="110" height="260" rx="55" fill="${o.canapeOmbre}"/>
  <rect x="60" y="360" width="150" height="150" rx="40" fill="#FFFFFF" opacity=".85" transform="rotate(-10 135 435)"/>
  <g class="${id}-respire" style="transform-origin:320px 740px">
    <path d="M196,320 C186,214 246,156 320,154 C398,156 452,214 442,320 C448,384 436,440 404,470 L236,470 C206,440 190,384 196,320 Z" fill="${o.cheveux}"/>
    <path d="M150,740 L158,560 Q164,474 252,452 L296,438 Q320,456 344,438 L388,452 Q476,474 482,560 L490,740 Z" fill="${o.pull}"/>
    <path d="M150,740 L158,560 Q164,500 206,476 Q186,580 196,740 Z" fill="${o.pullOmbre}"/>
    <path d="M296,438 Q320,470 344,438" stroke="${o.pullOmbre}" stroke-width="10" fill="none"/>
    <path d="M292,380 L348,380 L352,444 Q320,464 288,444 Z" fill="${P.p}"/>
    <path d="M292,380 L348,380 L350,408 Q320,424 290,408 Z" fill="${P.o}"/>
    <g class="${id}-tete" style="transform-origin:320px 410px">
      <g transform="translate(20 0)">${visage(id, o.peau, { cils: true, sourcils: "#1E1626" })}</g>
      <path d="M240,258 C236,190 278,150 330,152 C386,154 418,198 410,252 C392,220 358,202 320,204 C286,206 258,226 240,258 Z" fill="${o.cheveux}"/>
      <path d="M300,170 C330,162 368,176 386,204" stroke="${o.reflet}" stroke-width="7" fill="none" stroke-linecap="round"/>
      <circle cx="320" cy="140" r="44" fill="${o.cheveux}"/>
      <path d="M296,124 C306,108 328,104 344,114" stroke="${o.reflet}" stroke-width="6" fill="none" stroke-linecap="round"/>
    </g>
    <g class="${id}-mains">
      <path d="M210,560 C230,640 300,660 330,600" stroke="${o.pullOmbre}" stroke-width="66" fill="none" stroke-linecap="round"/>
      <path d="M430,560 C410,640 350,660 330,600" stroke="${o.pull}" stroke-width="66" fill="none" stroke-linecap="round"/>
      <g transform="translate(330 560) rotate(-6)">
        <rect x="-50" y="-96" width="100" height="176" rx="20" fill="${NAVY}"/>
        <rect x="-38" y="-84" width="76" height="152" rx="12" fill="#3B3070"/>
        <circle cx="0" cy="-70" r="5" fill="#6F67A3"/>
        <ellipse cx="-38" cy="40" rx="30" ry="26" fill="${P.p}"/>
        <ellipse cx="38" cy="40" rx="30" ry="26" fill="${P.p}"/>
        <path d="M-56,30 q8,-14 22,-10 M56,30 q-8,-14 -22,-10" stroke="${P.o}" stroke-width="4" fill="none" stroke-linecap="round"/>
      </g>
    </g>
  </g>
</svg>`;
  }

  /* ------------------------------------------------------------ objets */
  function etoile(cx, cy, r1, r2, n) {
    const pts = [];
    for (let i = 0; i < 2 * n; i++) {
      const r = i % 2 ? r2 : r1, a = Math.PI * i / n - Math.PI / 2;
      pts.push((cx + r * Math.cos(a)).toFixed(1) + "," + (cy + r * Math.sin(a)).toFixed(1));
    }
    return pts.join(" ");
  }

  function bulleValidee(id, accent) {
    return `<svg viewBox="0 0 240 230" xmlns="http://www.w3.org/2000/svg" overflow="visible">
  <path d="M20,80 C20,40 50,18 92,18 L150,18 C192,18 222,40 222,80 L222,122 C222,164 192,186 150,186
           L96,186 L46,222 L58,180 C34,170 20,148 20,122 Z" fill="#FFFFFF" filter="url(#${id}-ombre)"/>
  <defs><filter id="${id}-ombre" x="-20%" y="-20%" width="140%" height="150%">
    <feDropShadow dx="0" dy="10" stdDeviation="10" flood-color="#1F1650" flood-opacity=".12"/></filter></defs>
  <g class="${id}-sceau" style="transform-origin:121px 102px">
    <polygon points="${etoile(121, 102, 54, 46, 12)}" fill="${accent}" stroke="${accent}" stroke-width="8" stroke-linejoin="round"/>
    <path class="${id}-coche" d="M96,104 L114,122 L148,86" stroke="#FFFFFF" stroke-width="13" fill="none"
          stroke-linecap="round" stroke-linejoin="round" pathLength="1" style="stroke-dasharray:1;stroke-dashoffset:1"/>
  </g>
</svg>`;
  }

  function bulleQuestion(id, accent) {
    return `<svg viewBox="0 0 200 190" xmlns="http://www.w3.org/2000/svg" overflow="visible">
  <defs><filter id="${id}-ombre" x="-20%" y="-20%" width="140%" height="150%">
    <feDropShadow dx="0" dy="10" stdDeviation="10" flood-color="#1F1650" flood-opacity=".12"/></filter></defs>
  <circle cx="100" cy="86" r="76" fill="#FFFFFF" filter="url(#${id}-ombre)"/>
  <circle cx="40" cy="168" r="14" fill="#FFFFFF"/><circle cx="18" cy="186" r="8" fill="#FFFFFF"/>
  <text x="100" y="118" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="96" fill="${accent}">?</text>
</svg>`;
  }

  function ruban(id, clair, fonce) {
    return `<svg viewBox="0 0 200 260" xmlns="http://www.w3.org/2000/svg" overflow="visible">
  <path class="${id}-trait" d="M44,236 L100,116 C130,70 130,24 100,24 C70,24 70,70 100,116 L156,236"
        stroke="${fonce}" stroke-width="36" fill="none" stroke-linejoin="round" pathLength="1"
        style="stroke-dasharray:1;stroke-dashoffset:1"/>
  <path class="${id}-dessus" d="M100,116 L156,236" stroke="${clair}" stroke-width="36" fill="none" style="opacity:0"/>
</svg>`;
  }

  function appel(id, o) {
    /* ecran de teleconsultation : le medecin y apparait, en direct */
    o = Object.assign({ clair: "#FCE3EF", accent: "#E4579A" }, o || {});
    return `<svg viewBox="0 0 420 560" xmlns="http://www.w3.org/2000/svg" overflow="visible">
  <defs>
    <clipPath id="${id}-clip"><rect x="20" y="20" width="380" height="520" rx="34"/></clipPath>
    <filter id="${id}-ombre" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="18" stdDeviation="18" flood-color="#1F1650" flood-opacity=".18"/></filter>
  </defs>
  <rect x="0" y="0" width="420" height="560" rx="46" fill="${NAVY}" filter="url(#${id}-ombre)"/>
  <rect x="20" y="20" width="380" height="520" rx="34" fill="${o.clair}"/>
  <g clip-path="url(#${id}-clip)">
    <circle cx="210" cy="250" r="190" fill="#FFFFFF" opacity=".55"/>
    <g class="${id}-onde">
      <circle cx="210" cy="270" r="60" fill="none" stroke="${o.accent}" stroke-width="6" opacity=".6"/>
      <circle cx="210" cy="270" r="60" fill="none" stroke="${o.accent}" stroke-width="6" opacity=".6"/>
    </g>
    <g class="${id}-portrait" style="opacity:0">${o.portrait || ""}</g>
  </g>
  <rect x="38" y="40" width="224" height="42" rx="21" fill="${NAVY}"/>
  <circle class="${id}-direct" cx="62" cy="60" r="8" fill="#4ADE80"/>
  <text x="80" y="68" font-family="Poppins" font-weight="600" font-size="19" fill="#FFFFFF">Téléconsultation</text>
  <rect x="318" y="98" width="66" height="88" rx="14" fill="#FFFFFF"/>
  <circle cx="351" cy="130" r="14" fill="#E3E6EF"/><rect x="331" y="150" width="40" height="24" rx="12" fill="#E3E6EF"/>
</svg>`;
  }

  function eclat(couleur) {
    return `<svg viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg" overflow="visible">
  <path d="M30,0 C32,20 40,28 60,30 C40,32 32,40 30,60 C28,40 20,32 0,30 C20,28 28,20 30,0 Z" fill="${couleur}"/></svg>`;
  }

  window.D = { NAVY, medecin, patiente, bulleValidee, bulleQuestion, ruban, appel, etoile, eclat };
})();
