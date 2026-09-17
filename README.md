# VScode6-learning-sprintIA

Module Python `trello_client` : client lecture seule pour l'API Trello — cartes
d'un board, leurs labels ("tags"), leurs custom fields résolus et leurs
commentaires.

## Démarrage

```bash
pip install -r requirements.txt
pytest -q
```

Pour un usage réel (au-delà des tests, qui mockent les réponses HTTP), voir
`docs/trello-api-setup.md` pour obtenir une clé API et un token Trello, puis :

```python
from trello_client import TrelloClient

client = TrelloClient.from_env()  # lit TRELLO_API_KEY / TRELLO_TOKEN
cards = client.get_board_cards(board_id="...")
for card in cards:
    print(card.name, card.labels, card.custom_fields, [c.text for c in card.comments])
```

## Dispositif agentic

Le dispositif de pilotage (orchestrateur, superviseur, hooks garde-fou) et
BMAD-METHOD sont installés — voir `CLAUDE.md` et `AGENTS.md`.
