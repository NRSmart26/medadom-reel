# Préférences globales (tous projets) — NR Smart

## Review de code par Codex avant commit (cross-model)
AVANT chaque commit/push portant un changement **substantiel** (nouvelle logique,
refactor non trivial, fix non évident, nouveau script/module), lancer une review du
diff par **Codex CLI** — un modèle différent (GPT) qui attrape mes angles morts.

- **Commande** (review staged + unstaged + untracked, non-interactif) :
  `codex review --uncommitted`
  **Aucun `-c model=…` ici** : le modèle et l'effort viennent de `~/.codex/config.toml`,
  réglé sur `gpt-5.6-luna` à l'effort `high`. Une option `-c` écrase cette
  configuration, donc un changement de défaut n'y prendrait jamais effet.
  Variantes : `--base main` (vs branche), `--commit <sha>` (review a posteriori,
  quand le working tree a déjà bougé).
  **Pourquoi Luna à `high`** (bascule du 2026-10-02) : mesuré sur deux diffs dont les
  défauts étaient connus d'avance, Luna à `high` a retrouvé les trois mécanismes du
  premier cas et trois défauts sur cinq du second, pour un seul constat faux sur dix ;
  Terra à `high`, sur les mêmes diffs, n'a retrouvé qu'un mécanisme sur trois au
  premier cas. C'est le palier le moins cher du catalogue.
- **Le réglage fort ne s'emploie que si l'utilisateur l'écrit dans le prompt du lot.**
  Claude Code ne décide JAMAIS seul qu'un lot est à risque :
  `codex -p risque review --uncommitted`
  **Aucun `-c` de modèle ni d'effort** : le réglage fort vit en UN seul endroit,
  `C:\Users\NR SMART\.codex\risque.config.toml`, réglé sur `gpt-6.1-sol` à l'effort
  `high` (bascule du 2026-10-02 ; lancement du modèle le 2026-09-29). Le `-p` se place
  **AVANT** la sous-commande — `codex review -p risque` est refusé, et `-p` n'apparaît
  pas dans `codex review --help` tout en y fonctionnant.
  Il reste utile parce que Luna n'a pas vu deux défauts que le réglage fort avait
  trouvés : la recherche d'un fragment par sous-chaîne, et une comparaison insensible
  à la casse.
  ⚠️ **Un profil inexistant est accepté EN SILENCE** et la passe tourne sur le défaut :
  d'où la règle ci-dessous de relever `model:` à chaque passe.
- **Repli si Luna est refusé** : `gpt-5.6-terra` à l'effort `high`, par `-c`, et
  **jamais Sol en repli** — Sol ne s'emploie que sur demande explicite :
  `codex review --uncommitted -c 'model="gpt-5.6-terra"' -c 'model_reasoning_effort="high"'`
  Le repli est **signalé dans le compte rendu**. Une review qui échoue n'est jamais
  sautée. Si aucune passe n'aboutit, le dire et le tracer dans le commit — jamais
  committer en silence.
- **LIRE LE MODÈLE ANNONCÉ, À CHAQUE PASSE.** La sortie imprime `model:` et
  `reasoning effort:` : les relever et les **écrire dans le compte rendu**. Une passe
  qui a tourné sur un autre modèle que celui attendu **ne compte pas** : elle est
  relancée. Mesuré le 2026-10-02 : un réglage absent ou mal nommé est accepté en
  silence et la passe tourne sur le défaut, sans un mot.
- ⚠️ **Spark est RETIRÉ** — annonce OpenAI du 2026-09-11, effective la semaine du 15.
  `gpt-5.3-codex-spark` a disparu du catalogue `codex debug models` et l'appel rend
  `400 invalid_request_error : not supported when using Codex with a ChatGPT account`.
  Ne plus l'utiliser. Si Codex change à nouveau, revérifier le slug dans
  `codex debug models` et **redater cette note**.
- **Luna n'est pas interdit.** La règle « jamais Luna, ça vide les quotas » n'était
  écrite dans aucun fichier, et aucun incident consigné ne l'étaye : relevé le
  2026-10-02 dans la configuration, les règles globales, les règles de chaque projet et
  toutes les mémoires automatiques. La mesure du même jour en fait le réglage par défaut.
- **Déclencheur** : changements substantiels, juste avant commit. **PAS** les renames /
  typos / bumps de version / docs triviales — inutile, lent et bruyant.
- **Workflow** : (1) coder → (2) la commande ci-dessus → (3) présenter les
  retours de Codex à l'utilisateur → (4) corriger ce qui est pertinent → (5) committer.
- **Préférence souple** : l'utilisateur peut dire « skip la review » (hotfix urgent).
  Si je l'oublie de façon répétée → durcir en hook `settings.json` (à rediscuter).
- **Auth** (une fois, par l'utilisateur) : `codex login` (compte OpenAI) ou
  `OPENAI_API_KEY`. Si la review échoue pour cause d'auth, le **signaler** — ne jamais
  committer en silence en sautant la review.

## Écriture de fichiers
- Un contenu de fichier qui contient des backquotes, des antislashs ou des guillemets ne
  passe jamais par une commande shell (heredoc, `echo`, `python -c`) : il s'écrit avec
  l'outil Write ou Edit. Deux fichiers corrompus en deux jours : un `\b` devenu l'octet
  0x08 dans une regex le 01/10/2026, des backquotes évaluées par bash dans
  `simsar/AGENTS.md` le 02/10/2026.

## Posture générale
- Faire des **retours francs et des recommandations argumentées** ; ne pas me contenter
  d'exécuter quand je vois un risque, un coût caché ou une meilleure approche.
  L'utilisateur veut un avis critique, pas un « oui-oui ».
