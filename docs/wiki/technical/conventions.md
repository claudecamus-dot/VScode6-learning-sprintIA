# Conventions du projet

Conventions constatées dans le code ou déjà écrites dans le dépôt — aucune règle
inventée pour ce document. Chaque entrée cite son fichier source.

## Commandes

```bash
pip install -r requirements.txt
pytest -q                                    # toute la suite
pytest -q tests/test_trello_client.py::test_get_board_cards_resolves_labels_custom_fields_and_comments  # un seul test
```
Source : `CLAUDE.md`, `README.md`.

Vérifié le 2026-09-24 : le test unique ci-dessus passe seul (`1 passed in 0.37s`).

## Linter

`ruff.toml` (racine) déclare `select = ["E", "F", "I"]`, `line-length = 100`, et
exclut `_bmad`, `_bmad-output`, `.claude` (fournisseurs tiers / copies
synchronisées du canon du hub de supervision VScode5, bannière « GÉNÉRÉ — NE
PAS ÉDITER LOCALEMENT » : leur qualité se corrige au hub, pas ici) — source :
`ruff.toml`.

Commande : `ruff check .`

État réel vérifié le 2026-09-24 : **la commande passe** — `All checks passed!`,
0 erreur. Historique : 88 erreurs initiales, ramenées à 79 par un correctif
mécanique ciblé (`ruff check . --select I001,F401 --fix`, imports non triés et
imports inutilisés), puis les 66 `E501`/13 `E741` restantes soldées le même
jour à la main (jamais de reformatage global) — sauf celles portées par
`.claude` (copies canon), sorties du périmètre lint plutôt que corrigées
localement, une correction locale y étant écrasée à la prochaine propagation.
Suite de tests rejouée après le fix : 45 passed. Plafonnée par
`tests/test_lint_baseline.py` (modèle `VsCode4/tests/test_lint_baseline.py`,
baseline désormais vide) : toute régression barre.

## Dépendances épinglées

`requirements.txt` épingle chaque version exacte (constats d'audit 4 et 6) :
« sans épinglage, rien ne fige ce qui est installé et aucune confrontation CVE
n'est possible ». Les valeurs sont relevées par `py -m pip freeze` sur un poste
où la suite est verte ; toute montée de version se fait suite verte à l'appui.
Source : commentaire en tête de `requirements.txt`.

## CI

`.github/workflows/tests.yml` : install épinglée (`pip install -r
requirements.txt`) puis suite complète avec couverture :

```bash
python -m pytest tests/ -q --cov=trello_client --cov="docs/run-ia" --cov-report=term-missing
```

Le gabarit OCTO nécessaire à `test_generation_decks` est récupéré par
sparse-checkout depuis le dépôt public `claudecamus-dot/VsCode2`
(`app/assets/template-octo.pptx`), exposé via la variable d'environnement
`TEMPLATE_OCTO_PATH` — jamais copié dans ce dépôt. Sans ce gabarit,
`test_generation_decks` est explicitement SAUTÉ (constat d'audit 7) plutôt que
tu. Source : `.github/workflows/tests.yml`.

Déclaratif seulement : ce workflow n'a jamais été exécuté sur le compte GitHub
associé à ce dépôt (Actions désactivé — `gh api ... /actions/workflows/tests.yml/dispatches`
retourne HTTP 422, vérifié le 2026-09-24, hors périmètre de correction ici).

## Secrets et configuration

`TrelloClient.from_env()` lit les identifiants dans les variables d'environnement
`TRELLO_API_KEY` / `TRELLO_TOKEN` (et `TRELLO_BOARD_ID` pour le board), jamais en
dur dans le code. Voir `docs/trello-api-setup.md` pour les obtenir. Source :
docstring de `trello_client/client.py` (lignes 1-8) et `CLAUDE.md`.

Les tests unitaires ne requièrent aucun credential réel : les réponses HTTP sont
mockées (`tests/test_trello_client.py`, `tests/test_trello_secrets.py`). Un test
dédié (`tests/test_trello_secrets.py`) vérifie qu'une clé/un token ne fuient pas
dans un message d'exception. Source : commentaires du workflow CI et des tests.

`TEMPLATE_OCTO_PATH` : variable d'environnement pointant vers le gabarit PPTX
OCTO utilisé par les générateurs de `docs/run-ia/` — voir `.github/workflows/tests.yml`
et `tests/test_generer_deck_template_env_hub.py`.

## Nommage

- Le module applicatif principal est `trello_client/` (paquet Python avec
  `__init__.py` et `client.py`) — source : `git ls-files`.
- Les scripts de génération de decks vivent sous `docs/run-ia/` (`generer_deck.py`,
  `contenu_deck.py`), y compris une variante `docs/run-ia/atelier-agentic-run/`
  avec ses propres `generer_deck.py`/`contenu_deck.py` — source : `git ls-files`.
- Classes exposées : `TrelloClient`, `Card`, `Comment`, exceptions
  `TrelloAuthError` et `TrelloSchemaError` (remplace un `KeyError` brut porté par
  le champ manquant et l'identifiant de la carte/action en cause) — source :
  `trello_client/client.py`.
- Tests nommés par ce qu'ils prouvent plutôt que par la fonction testée
  (`test_generer_deck_repli_image_hub.py`,
  `test_generer_deck_repli_prime_pas_sur_cache_hub.py`,
  `test_trello_robustesse_hub.py`) — source : `git ls-files tests/`.

## Dépendance au kit agentic

`tests/test_contrat_kit_pptx.py` déclare et vérifie en CI que les générateurs de
`docs/run-ia/` dépendent par `sys.path` (jamais par copie) des modules
`pptx_deck` (skill `pptx-deck`) et `framed_image` / `nature_images` /
`stock_images` (skill `pptx-framed-image`) installés sous `.claude/skills/`. Le
test extrait les noms réellement utilisés par les générateurs et exige leur
présence dans le kit installé, pour qu'une régénération du kit depuis le hub ne
casse pas silencieusement un générateur. Source :
`tests/test_contrat_kit_pptx.py` (docstring, constat d'audit « risque_technique »
du 2026-09-23).

## Dispositif agentic

Le dispositif de pilotage (`.claude/settings.json`, hooks, skills, orchestration)
provient du hub de supervision (`VScode5 - Supervision projets`) : « corriger
là-bas puis régénérer l'export, jamais localement — les copies locales
divergent ». Source : `CLAUDE.md`.
