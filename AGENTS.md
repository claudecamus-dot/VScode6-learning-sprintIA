<!-- bmad:context -->
<!-- Verified 2026-09-20 against ac3f879. Managed by bmad-project-context; edits inside this block are replaced on refresh. Keep anything you want preserved outside the markers. -->

## VScode6-learning-sprintIA

Module Python `trello_client` : client **lecture seule** de l'API Trello — cartes
d'un board, labels, custom fields résolus en valeur lisible, commentaires.
Le dépôt porte aussi des supports d'atelier générés (`docs/run-ia/`, decks pptx).

## Where things are

- Code applicatif : `trello_client/client.py` (client, pagination, redaction des
  secrets), `trello_client/__init__.py` (API publique)
- Tests : `tests/` — 5 fichiers, aucun n'ouvre de socket ni ne lit de credential
  (session HTTP doublée)
- CI : `.github/workflows/tests.yml` — rejoue `pytest tests/` avec couverture sur
  push/PR, dépendances épinglées par `requirements.txt`
- Credentials réels (usage hors tests) : `docs/trello-api-setup.md`, `.env.example`
- Dispositif agentic : `.claude/skills/`, `.claude/agents/` ; BMAD : `_bmad/`,
  `_bmad-output/` — ne pas parcourir, grep ciblé

## Running and verifying

Commandes exécutées le 2026-09-20 sur ac3f879 :

```bash
py -m pytest -q                       # 24 passed en 12 s
py -m pytest -q tests/test_trello_client.py::test_get_board_cards_resolves_labels_custom_fields_and_comments   # un seul test
py -m py_compile trello_client/client.py
```

Sous Windows, ajouter `--basetemp=C:/tmp/<court>` : le scratchpad pytest par
défaut dépasse MAX_PATH et fabrique de faux échecs.

## Pitfalls

- **Ne jamais laisser une `requests.HTTPError` remonter brute** : l'URL Trello
  porte `key=` et `token=` en query string. Tout chemin d'erreur passe par
  `_redacted_http_error` / `redact_secrets` (régression déjà corrigée en 62ccf97,
  gardée par `tests/test_trello_secrets.py`).
- **Pas de N+1 sur les cartes** : `_iter_raw_cards` pagine (`limit`) et rapatrie
  les commentaires dans la même requête. Appeler `get_card_comments` en boucle sur
  un board réintroduit le défaut corrigé en 17c4043 — et le quota (100 req / 10 s
  par token) est atteint avant la fin.
- **Un champ absent de la réponse n'est pas une valeur vide** : `_champ` lève
  `TrelloSchemaError` avec le contexte. Ne pas le remplacer par un `.get(..., "")`,
  un schéma Trello qui change deviendrait silencieux.
- `pptx_deck.py` a **une seule source**, la skill du kit ; une copie locale est
  interdite et `tests/test_pptx_deck_non_duplique.py` échoue si elle réapparaît.
- Le dispositif sous `.claude/` vient du hub VScode5 : corriger là-bas puis
  régénérer l'export, jamais localement.

<!-- /bmad:context -->
