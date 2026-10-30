---
name: son-et-voix-des-reels
description: "Reels LCDG — voix de synthèse ElevenLabs (4 voix : homme/femme, jeune/plus âgé), musique de Romain, bruitages sur le motion ; jamais de bruitage à l'ouverture"
metadata:
  node_type: memory
  type: feedback
  originSessionId: c52333eb-2092-4068-8d6a-41bf40843acc
  modified: 2026-10-28T12:35:45.731Z
---

Depuis le 01/10/2026, les reels LCDG ont une **voix off de synthèse** (ElevenLabs, modèle
v3 avec indications de jeu entre crochets), **la musique choisie par Romain** sous la voix
(atténuée quand la voix parle) et des **bruitages calés sur le motion**. Cela annule sa
consigne du 21/09/2026 (« ni musique ni bruitage, je l'intègre moi-même »).

**Why:** Romain veut un reel « humain » qui donne envie d'écouter (« si c'est humain c'est
que c'est bon ») ; il a changé d'avis sur la musique après la vidéo motion de son associé.
Il a rejeté les voix aux respirations audibles (sa propre voix clonée, supprimée depuis),
les voix de bibliothèque trop « annonce » et une voix avec de la réverbération (F40_1).

**How to apply:**
- Quatre voix fixées le 02/10/2026, dans `VOIX_CATALOGUE` (charte du dépôt lcdg-reel) :
  `homme_age` (Guillaume, bibliothèque, sans emplacement), `homme_jeune` (voix créée,
  « ça fait jeune »), `femme_agee` (F40_3) et `femme_jeune` (F23_1), toutes enregistrées.
  Choix selon le thème, la gravité, l'urgence ; on alterne d'un reel à l'autre.
- femme_agee (F40_3) : Romain y entend « de la résonance, comme dans un bocal en verre »
  (05/10/2026). Mesuré : une zone qui sonne à 2,8-3,1 kHz ; corrigée dans l'outil par un
  filtre (champ "traitement" du catalogue). S'il l'entend encore : remix ElevenLabs de la
  voix (« studio sec, sans réverbération »), qui demande de libérer un emplacement.
- Jamais de bruitage à l'ouverture du reel (« tu as rajouté du bruit en entrée, il ne faut
  pas faire ça du tout », 02/10/2026) ; la musique finit par un fondu audible.
- Comparer des voix en mesurant le bruit des pauses. La durée du reel n'est pas une
  contrainte.
- Compte ElevenLabs gratuit (Romain ne paiera jamais, voir [[jamais-payant]]) : 10 000
  crédits par mois (renouvellement le 27 du mois), 3 emplacements de voix, tous pris.
  Une narration complète (environ 1 250 caractères, modèle v3) a coûté environ 290
  crédits (mesuré deux fois le 02/10/2026). Étiquette « Info IA » à la
  publication.
- 20/10/2026 : les deux voix de femme créées (F40_3, F23_1) sont remplacées. Romain entendait
  encore la résonance (« on entend de la raisonance en fond ») ; mesuré : pic fixe vers 3 kHz
  sur toute la narration, que le filtre ne rattrape pas quand des prises sont recollées.
  Choisies à l'écoute parmi les voix « professionnelles » françaises de la bibliothèque
  ElevenLabs (gratuites, sans emplacement) : `femme_jeune` = Jeanne (« plus jeune donc plus
  punchy »), `femme_agee` = Emilie (« plus sérieux, genre 42 ans »). Les anciennes restent
  sous `femme_*_creee` pour les reels déjà rendus. Méthode qui a marché : 4 voix lisant le même
  passage, un fichier bout à bout, Romain choisit. Ne jamais recoller des prises d'une voix
  qui résonne.
- Le clonage de la voix de l'associé a été bloqué le 01/10/2026 : ne pas le retenter.
- Reels à booster en publicité (16/10/2026, reel « minimum de patients ») : Romain veut un
  hook réactif, une voix qui réagit, interrogative et surprise, « un peu choquée » (« pardon ?!
  non mais ça va pas du tout ! »), et ce jour-là une femme (femme_agee). Fait : des indications
  [incredulous], [surprised], [shocked]… sur les phrases. Le « Pardon ?! » mis en ouverture a été
  retiré à l'écoute (« enlève le pardon au début, sinon c'est top ») : le reel s'ouvre sur le
  fait, dit sur un ton incrédule, sans interjection devant. La surprise porte
  sur l'obligation et sur ce qui n'est pas dit, jamais sur un chiffre qu'elle exagérerait, et
  aucun jugement ne passe pour un fait (« ça va pas du tout » n'a pas été lu). Narration
  d'environ 1 470 caractères : 322 crédits.
- 28/10/2026 : Emilie (femme_agee) sur le reel cumul emploi-retraite : « vraiment très pro !
  bravo ! ». homme_jeune (« LCDG homme 2 », voix créée) refusée sur le reel vaccins : « pas assez
  d'intonation et de rythme humain », et elle a prononcé « consulpation » pour « consultation ».
  Ne plus la choisir ; les voix de bibliothèque (Guillaume, Jeanne, Emilie) d'abord.
- On ne peut pas écouter : la transcription ElevenLabs (Scribe, gratuite,
  controle_prononciation.py dans l'atelier) ne repère que les erreurs grossières (elle a
  « corrigé » consulpation en consultation, confiance parfaite). Envoyer à Romain un extrait
  sonore des phrases à risque (mots longs, noms de médicaments) avec chaque nouvelle voix.

Voir [[format-reel-v2]], [[reel-porte-entree]] et [[broll-revue-exigeante]].
