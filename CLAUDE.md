# VScode6-learning-sprintIA

Module Python `trello_client` : client lecture seule pour l'API Trello (cartes,
labels/tags, custom fields résolus, commentaires d'un board donné).

## Commandes

```bash
pip install -r requirements.txt
pytest -q                                    # toute la suite
pytest -q tests/test_trello_client.py::test_get_board_cards_resolves_labels_custom_fields_and_comments  # un seul test
```

Credentials Trello (`TRELLO_API_KEY`/`TRELLO_TOKEN`/`TRELLO_BOARD_ID`) : voir
`docs/trello-api-setup.md`. Les tests unitaires ne les requièrent pas (réponses
HTTP mockées).

## Claude Code — configuration du projet

- `.claude/settings.json` (versionné) : garde-fou git destructif, rappel de vérif
  réelle avant commit (adapter `_WATCHED_PREFIXES`/`_VERIF_BASH` dans
  `.claude/hooks/warn_verif_before_commit.py` au canal de CE projet), gate
  orchestrateur, scan supervision en SessionStart, deny rules secrets.
- `.claude/skills/` : orchestrateur (compose et exécute les plans multi-étapes),
  superviseur (diagnostic étage 2), revue-increment (definition of done),
  veille-agentic (état de l'art), audit-technique.
- `.claude/agents/` : les sous-agents porteurs que l'orchestrateur dispatche.
- `.claude/supervision/` + `.claude/orchestration/` : dispositif de supervision.
  Journal des orchestrations : `log_run.py` (`--solde` pour requalifier un run en
  attente). Arbitrages humains : `arbitrages.json`.

Le dispositif vient du hub de supervision : **corriger là-bas puis régénérer
l'export**, jamais localement — les copies locales divergent (leçon P1).

## Discipline de gestion des tokens

Le contexte est un cache actif facturé à chaque tour, pas une mémoire gratuite.

- **Ne pas parcourir** `_bmad/`, `_bmad-output/`, `.claude/skills/bmad-*` sauf demande
  explicite.
- **Lire avant d'écrire**, grep les appelants avant de modifier une fonction partagée
  du client Trello.
- **Sous-agent pour toute sortie volumineuse.**
- **`/compact` dès ~40 %** de fenêtre utilisée si la session doit continuer longtemps.
- **`/clear` (pas une 3e rustine) après deux corrections ratées consécutives** sur le
  même problème — repartir à froid avec un meilleur prompt bat l'insistance.

## Règles de travail

- Propose → arbitre → applique : aucun correctif auto-appliqué sans arbitrage humain.
- Jamais `succes` au journal sur un livrable que l'utilisateur doit encore valider.
- Tout chiffre écrit s'appuie sur la commande qui l'a produit.
