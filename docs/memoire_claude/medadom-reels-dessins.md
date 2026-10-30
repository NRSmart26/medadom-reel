---
name: medadom-reels-dessins
description: "Reels Medadom Professionnel en dessins : style des vignettes Medadom, générés dans Canva, jamais dessinés à la main ni animés"
metadata:
  node_type: memory
  type: feedback
  originSessionId: c52333eb-2092-4068-8d6a-41bf40843acc
  modified: 2026-10-30T12:44:37.013Z
---

Pour les reels du compte Instagram Medadom Professionnel (médecins généralistes), Romain veut
des dessins « flat » dans le style exact des vignettes Medadom qu'il fournit (médecins en blouse,
visages simples, fond uni de la couleur du thème), une couleur par thème, des marges strictes.

**Why:** le 20/10/2026, mes personnages dessinés en SVG à la main ont été jugés « ultra mal
faits » ; « fais de vrais dessins », « je ne te demande pas d'inventer », « si tu n'y arrives
pas, laisse juste les dessins et n'anime rien du tout ». Il a refusé aussi les photos réelles
(« je t'ai demandé des dessins ») et les personnages en surpoids pour le diabète (« cliché »).
« Le téléphone doit être un vrai téléphone » : un appareil réaliste (cadre, îlot, reflet),
l'écran montrant le dessin.

Le 29/10/2026 (reel infection urinaire de l'homme), Romain : « le motion design doit être ultra quali », « le
texte doit être gros quand on a la place, ils vont voir ça sur un mobile », et une voix « au même niveau que les reels
LCDG », plus une version LinkedIn. Fait : moteur version 2 (moteur_reel2.js, reel2.css, reel_iu.py, planche_reel2.py)
— échelle de texte ajustée par scène (le texte d'abord, le dessin s'adapte), pastilles barrées, critères qui se
cochent, barre de progression, version carrée (texte à gauche, dessin à droite). Tout doit être sourcé : sources
gardées dans `medadom/sources_iu/`. Les reels Medadom avec voix (migraine, obésité) font environ 2 min.

Le 30/10/2026 : la voix d'Emilie sur ce reel « vraiment parfait, bravo », mais la fin doit « inciter à nous
rejoindre » et la voix y « donner envie ». Fait : fin en 2 scènes (bénéfices cochés un à un, puis appel), voix de fin
en prise séparée, plus enthousiaste, raccordée après un blanc (la prise principale reste en cache). Arguments de
recrutement : uniquement ceux de la page de recrutement validée par MEDADOM (LP-MEDADOM-comparatif-final,
28/10/2026). Une coupure insérée dans la voix se pose sur le blanc mesuré dans le son, jamais sur l'horodatage seul
(il avançait de 0,3 s et a tranché un mot). Une formulation comme « à distance » se lit « en téléconsultation » dans
ce contexte : à bannir (« toucher rectal, à distance »). Version carrée : « Le lien est dans le post ».

Depuis le 30/10/2026, **l'outil des reels Medadom est `C:\Users\NR SMART\tools\medadom-reel`** (dépôt git local,
séparé des reels LCDG à la demande de Romain : « il ne faut pas tout mélanger ») : lire son CLAUDE.md avant tout
reel Medadom ; un fichier de contenu par reel dans `reels/`, modèle `reels/iu_homme.py`.

**How to apply:** générer les dessins dans Canva (generate-image avec la vignette de Romain en
référence, fond uni, sans texte), les exporter en pleine définition via une page du design
`DAHYkUMJaDM` (add_page + insert_fill, commit, export PNG). Dessins fixes ; seuls les textes
s'animent. Outillage : `C:\Users\NR SMART\tools\medadom-reel` (dépôt privé GitHub
`NRSmart26/medadom-reel` depuis le 30/10/2026 ; l'ancien `lcdg-reel-atelier\medadom\` est
remplacé, archivé dans `ancien_v1/`). Voir [[son-et-voix-des-reels]] et
[[visuels-reference-pertinence]].

Le 30/10/2026, « + ECBU positif » ajouté à l'écran pour la prostatite et la pyélonéphrite (définitions
SPILF), pas pour la cystite : diagnostic clinique, et « attendre l'ECBU » serait devenu contradictoire.
