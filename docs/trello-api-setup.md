# Obtenir une clé API et un token Trello

Nécessaire pour utiliser `trello_client` en réel (les tests unitaires du
module, eux, n'en ont pas besoin — ils mockent les réponses HTTP).

1. **Clé API** : se connecter sur https://trello.com/power-ups/admin, créer
   un Power-Up (ou réutiliser un existant), onglet « API key » → copier la
   clé.
2. **Token** : sur la même page, lien « Token » à côté de la clé (ou
   directement `https://trello.com/1/authorize?expiration=never&scope=read&response_type=token&name=<nom-du-power-up>&key=<clé-api>`
   dans le navigateur) → autoriser → copier le token affiché. Portée `read`
   seule suffit ici (le client ne fait que lire).
3. **Board ID** : ouvrir le board visé dans le navigateur, ajouter `.json` à
   l'URL (`https://trello.com/b/<shortId>/<nom>.json`) → champ `id` en tête
   du JSON.
4. Copier `.env.example` en `.env` (déjà dans `.gitignore`, jamais commité) et
   renseigner `TRELLO_API_KEY`, `TRELLO_TOKEN`, `TRELLO_BOARD_ID`.

Ni la clé ni le token ne doivent jamais être écrits en dur dans le code ou
committés — `TrelloClient.from_env()` les lit depuis l'environnement.
