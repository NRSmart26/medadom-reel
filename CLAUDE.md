# Reels Medadom Professionnel (Med Academy) — instructions pour Claude Code

Cet outil fabrique les reels du compte « Medadom Professionnel » : des fiches pratiques animées pour les médecins
généralistes, tirées des classes virtuelles Medadom (Med Academy), qui finissent sur « Rejoignez Medadom ».
**Il n'a rien à voir avec les reels LCDG** (dépôt `lcdg-reel`, autre charte, autre méthode) : ne rien y mélanger.

Référence de qualité : le reel « Infection urinaire de l'homme en téléconsultation » (`reels/iu_homme.py`, 29-30
octobre 2026), jugé « magnifique » par Romain. Chaque nouveau reel part de ce fichier.

## La méthode, dans l'ordre

1. **Lire la source en entier** (compte rendu de classe virtuelle Medadom, PDF). Puis **vérifier que chaque fait est
   à jour, à la source officielle du jour** : la classe virtuelle peut dater de plusieurs mois et les
   recommandations changer entre-temps (cas réel : la classe de février 2026 recommandait la bandelette urinaire,
   la SPILF de juin 2026 ne la recommande plus). Chercher la version la plus récente sur le site de la société
   savante (ex. recospilf.infectiologie.com, fiches datées), la HAS, l'ANSM (ruptures, restrictions), et l'AMM des
   molécules citées (base-donnees-publique.medicaments.gouv.fr). Une recommandation hors AMM se signale à l'écran
   (« Hors AMM chez l'homme, recommandées par la SPILF »). Garder les sources dans `sources/<reel>/` et les citer
   en tête du fichier du reel, scène par scène.
2. **Écrire le fichier du reel** (`reels/<reel>.py`, copie de `iu_homme.py`) : THEME (une couleur par sujet),
   COUVERTURE, SCENES. Voir « Écrire les scènes ».
3. **Dessins** (voir « Dessins ») : 8 à 10 dessins Canva, détourés.
4. **Mise en page sans voix, sans crédit** :
   `python fabrique.py reels/<reel>.py --sans-voix --essai`, puis `python planche.py reel_<nom>_9x16.html` et
   `python planche.py reel_<nom>_1x1.html`. Lire les échelles de texte : au moins 1,0 en 9:16 sur chaque scène
   (0,85 en carré), sinon alléger la scène ou la couper en deux. Seule exception : la scène d'appel en carré,
   dont le titre part de 90 px et partage la largeur avec le téléphone (0,72 sur le reel de référence, soit un
   titre de 65 px, lisible). Marges : OK. Regarder les planches.
5. **Relecture indépendante, avant toute voix** : un agent relit écran, voix et libellés contre les sources (voir
   « Relecture »). Corriger, puis refaire l'étape 4.
6. **Voix, son, rendu** : `python fabrique.py reels/<reel>.py` (9:16 puis carré, environ 25 min ; la voix
   coûte environ 1 crédit ElevenLabs par caractère lu, 500 environ pour 2 min). Les prises sont en cache : un
   nouveau rendu ne coûte rien.
7. **Contrôles du rendu** : `python controle_voix.py reels/<reel>.py "passage à risque" ...` (transcription,
   extrait sonore des DCI, sigles et mots longs, à faire écouter à Romain) ; planche d'images de chaque vidéo
   (ffmpeg, une image toutes les 3 s) regardée en entier ; son à -14 LUFS ; pas de coupure de mot.
8. **Livrables** dans SORTIE : les deux vidéos et les deux couvertures (faites par `fabrique.py`), l'extrait sonore
   (`controle_voix.py`), et `legendes.txt`, écrit par Claude à partir du modèle `reels/iu_homme_legendes.txt`
   (Instagram et LinkedIn, champ de la recommandation, sources, mention hors AMM). Garder une copie des légendes
   dans `reels/<reel>_legendes.txt`. Envoyer les vidéos et l'extrait à Romain.

## Écrire les scènes

- **Le public nommé dans la première phrase** : « Médecins généralistes : … » (conseil reçu par Romain, 28/10/2026),
  puis directement un fait (« la Spilf a mis à jour ses recommandations »). La couverture porte le titre.
- **Une scène = une idée**, 2 à 4 éléments à l'écran. Le texte d'abord : il doit être gros, ils regardent sur un
  téléphone (Romain, 29/10/2026). Trop d'éléments ? Couper la scène en deux (cystite : « attendre l'ECBU », puis
  « si on ne peut pas attendre »).
- **Toujours une scène « quand adresser »** : la limite de la téléconsultation (hôpital, autre professionnel,
  présentiel) et comment adresser (courrier : démarche et conduite à tenir). Romain : « le rôle du
  téléconsultant c'est de traiter, mais d'adresser vers d'autres professionnels ou l'hôpital dans les cas
  impossibles en téléconsultation, c'est très bien ».
- **Exactitude médicale** : une définition ou une indication garde sa condition entière (« signes de cystite,
  avec fièvre **ou signes systémiques** » ; « **en ambulatoire, sans signe de gravité** : ceftriaxone ») ; un
  tableau clinique ne se résume jamais à un signe qui en définirait un autre ; une opinion s'attribue. Quand la
  définition officielle comprend un examen (« … + ECBU positif »), le dire aussi, au moins à l'écran (relevé par
  la review Codex du 30/10/2026 sur le reel de référence : ajouté à la prostatite et à la pyélonéphrite). Mais
  seulement là où la source l'écrit : la cystite est un diagnostic clinique que l'ECBU confirme, et « + ECBU
  positif » y aurait contredit « attendre l'ECBU » (erreur faite puis retirée le même jour).
- **Des mots qu'on dit, et jamais d'ambiguïté avec la téléconsultation** : « toucher rectal à distance » (sens :
  après l'épisode) se lisait « toucher rectal en téléconsultation » ; écrire « une fois l'infection passée ».
- **La fin, deux scènes, dans une 2e prise de voix** (`"prise": 2`, ton `[warm]` puis `[excited]`) :
  1. les avantages, cochés un à un pendant que la voix les dit (un élément `criteres` par temps) ;
  2. l'appel : « Vous êtes médecin généraliste ? », « Rejoignez Medadom », « Postulez en 2 minutes · réponse sous
     48 h », le téléphone en visio.
  **Arguments de recrutement : seulement ceux validés par Medadom**, mot pour mot, dans la page de recrutement
  (`Downloads\LP-MEDADOM-comparatif-final`, 28/10/2026) : contrat salarié de 5 à 10 h par semaine en complément
  de votre activité ; depuis chez vous, vos créneaux 7 j/7 de 6 h à 23 h ; facturation et tiers payant gérés ;
  support médical en temps réel ; RCP, congés payés et retraite inclus ; postuler en 2 minutes, réponse sous
  48 h. Les classes virtuelles : le reel en vient lui-même (« comme celle d'où vient cette vidéo »).
- **Scène dense à lire** (une liste de critères) : `"pause": 3.5`, un silence le temps que les cases se cochent.
- **Genres d'éléments** (en-tête de `fabrique.py`) : `barree` pour ce qui n'est plus recommandé, `criteres`
  pour une liste à cocher, `chiffre` pour un nombre qui compte, `note` pour une mention discrète (hors AMM),
  `pastille!` pour l'alerte de la scène.

## Voix

- **Emilie** (bibliothèque ElevenLabs, `voix.EMILIE`), modèle v3 : « vraiment très pro » (28/10/2026), « vraiment
  parfait, bravo » sur ce reel (30/10/2026). Indications de jeu entre crochets : `[serious]`, `[warm]`,
  `[curious]`, `[matter-of-fact]`, `[emphatic]` ; `[excited]` pour la fin.
- Sigles épelés avec des points (« E.C.B.U. », « P.C.R. »), « Spilf » écrit comme un mot, « Médadom » accentué
  dans la voix, nombres en toutes lettres. Une DCI qui pourrait être mal lue s'écrit dans la voix comme elle se
  prononce (« pivmécilinam », « Klamydia ») ; l'écran garde l'orthographe exacte.
- Corriger une phrase de la 1re prise la régénère entière (environ 500 crédits) : pour ne changer que la fin,
  passer par la 2e prise. `PRISE1_SUITE` permet de garder une prise déjà payée dont le texte finissait autrement.
- **Une pause se pose dans le vrai blanc mesuré dans le son**, jamais sur l'horodatage seul : il avance parfois de
  0,3 s et a tranché la fin d'un mot (« situations », 30/10/2026). `fabrique.son` le fait.
- Compte ElevenLabs gratuit (10 000 crédits par mois, renouvelés le 27) ; Romain ne paiera jamais d'abonnement.
  La clé est dans `.env`, jamais affichée.

## Dessins

- Style exact des vignettes Medadom : « flat », visages simples aux yeux en points, fond uni de la couleur du sujet,
  aucun texte. Jamais de dessin fait à la main ni de photo ; pas de cliché (surpoids pour le diabète).
- Canva, outil `generate-image` avec la vignette de référence en image (`dessins/` : un dessin d'un reel
  précédent, téléversé par `create-upload-url`). Prompt qui marche : « Flat vector illustration in exactly the
  same style as the reference image (simple flat shapes, no outlines, soft shading, friendly simple face with dot
  eyes). <sujet>. Plain uniform light blue background (#A6CCEA), no gradient, no text, no letters, no numbers, no
  logo. » Un objet ou un écran : « blank screen, without digits ».
- Pleine définition : dans le design de travail `DAHYkUMJaDM`, `add_page` 1264 x 1264, `insert_fill` du dessin,
  commit, `export-design` PNG des nouvelles pages ; puis `python dessins.py telecharger nom=url ...`,
  `python dessins.py detourer`, `python dessins.py planche <prefixe>`.
- Un dessin dit ce que dit la scène (douleur lombaire : un homme qui se tient le bas du dos, thermomètre en main).
  Un dessin qui réduit trop le texte d'une scène s'enlève : le texte passe avant.

## Format et rendu

- 9:16 pour Instagram et Facebook, carré 1:1 pour LinkedIn (texte à gauche, dessin à droite ; carte de fin « Le
  lien est dans le post »). Zones sûres contrôlées par le moteur (`window.verifier`), rendu image par image
  (`rendu.py`, Chrome piloté par Playwright, 30 i/s).
- Musique : « Echo Sax No.4 » (`musique/`, 101 s), bouclée avec un fondu quand le reel est plus long, effacée sous
  la voix ; mixage à -14 LUFS.
- Durée : 2 min à 2 min 45 pour une fiche complète (les reels Medadom migraine et obésité font environ 2 min).

## Relecture indépendante (avant la voix)

Lancer un agent (outil Agent, `general-purpose`) qui lit le fichier du reel et toutes les sources, sans rien
modifier, et vérifie : chaque fait (écran et voix) avec ses bornes et sa source ; aucune condition coupée ; des
mots qu'on dit, aucune ambiguïté avec la téléconsultation ; écran et voix dans le même ordre ; prononciation des
DCI et sigles ; contradictions avec le compte rendu Medadom (à expliquer, pas à cacher). Il rend une liste
d'erreurs et de suggestions, chacune avec la citation, la source et une correction. Sur le reel de référence :
8 erreurs, toutes des conditions coupées ou des nuances.

## Fichiers

- `fabrique.py` : le moteur (voix en deux prises, calage, pauses, couvertures, son, rendu des deux formats).
- `moteur.js`, `reel.css` : l'animation (GSAP) et la charte ; texte ajusté par scène, pastilles barrées, cases qui
  se cochent, barre de progression, version carrée.
- `rendu.py` (vidéo), `planche.py` (contrôle des pages), `dessins.py`, `controle_voix.py`, `voix.py`.
- `reels/` : un fichier par reel. `sources/<reel>/` : les sources. `dessins/` et `dessins/detoures/`.
- `references/` : les vignettes Medadom de référence (style des dessins, à donner à Canva).
- `sauvegarde/voix/<reel>/` : les prises de voix déjà payées, copiées hors du cache (voir « Sur un autre PC »).
- `docs/memoire_claude/` : les règles apprises avec Romain (préférences, refus, voix), copie de la mémoire de
  Claude Code du PC de travail, à relire au début d'un nouveau reel.
- `ancien_v1/` : le premier moteur (reels Octobre rose et diabète de type 2, 20/10/2026), gardé pour mémoire.
- Non versionnés : `travail/` (voix en cache, sons), `node_modules/` (`npm install`), `.env`.
- Installation : `pip install -r requirements.txt`, `npm install`, ffmpeg dans le PATH, Chrome installé (rendu
  piloté par Playwright), `.env` avec `ELEVENLABS_API_KEY=`.

## Sur un autre PC

1. `git clone`, puis l'installation ci-dessus, et le `.env` (la clé ElevenLabs n'est jamais sur GitHub).
2. Reprendre les voix payées : copier `sauvegarde/voix/<reel>/*` dans `travail/<reel>/voix/` (le reel `iu`
   devient `travail/iu/voix/`). Sinon `fabrique.py` régénère la voix et consomme des crédits.
3. Les livrables (vidéos, couvertures, légendes) s'écrivent dans `~/Downloads/<dossier du reel>` (SORTIE).
4. Après une nouvelle voix, la copier aussi dans `sauvegarde/voix/<reel>/` et committer.
- Ancien moteur (reels Octobre rose et diabète, 20/10/2026) : `C:\Users\NR SMART\tools\lcdg-reel-atelier\medadom`.
