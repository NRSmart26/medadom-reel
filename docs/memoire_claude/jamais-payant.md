---
name: jamais-payant
description: "Romain refuse tout abonnement ou outil payant (« on ne paiera pas du tout, jamais ») — ne proposer que des solutions gratuites"
metadata:
  node_type: memory
  type: feedback
  originSessionId: c52333eb-2092-4068-8d6a-41bf40843acc
  modified: 2026-10-05T17:40:59.570Z
---

Romain ne paiera aucun abonnement ni outil pour les reels LCDG : « on ne paiera pas du
tout, jamais ok ? » (02/10/2026, en réponse à la recommandation de l'offre Starter
d'ElevenLabs).

**Why:** décision de principe de Romain sur les coûts de LCDG ; il l'a dite sèchement
après que je l'ai recommandée deux fois.

**How to apply:** chercher d'abord la solution gratuite (offre gratuite, bibliothèque,
contournement technique). Ne plus proposer d'offre payante, de banque d'images payante ni
d'abonnement. Si une limite de l'offre gratuite a une conséquence réelle (licence,
quota, emplacements), la signaler une fois, factuellement, sans revenir à la charge.
Exemple : les 3 emplacements de voix ElevenLabs gratuits se gèrent en supprimant une voix
(Romain le fait lui-même). Voir [[son-et-voix-des-reels]].

ElevenLabs vérifié le 05/10/2026 via /v1/user/subscription : offre « payg » plafonnée à
10 000 caractères par mois, sans dépassement possible (`can_extend_character_limit` false,
pas de facture). Au-delà, l'API refuse au lieu de facturer. Relire ce compteur avant une
grosse génération. Pour corriger une phrase d'un reel, `scripts/revoix.py` ne relit que les
blocs modifiés (566 caractères au lieu de 1 020 pour le désogestrel).
