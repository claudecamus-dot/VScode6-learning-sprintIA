# Notes — ce qu'on propose en phase RUN, côté design

Complément versé le 2026-09-18, en réponse à une question posée la veille : « que
proposer en phase de run d'un point de vue design ? ». Brut, pas encore mis en slide —
à reprendre si un chapitre design s'ouvre dans `AGENTIC-PRODUCT-RUN-offre-octo.pptx`
(le deck constate aujourd'hui que « le design system dérive sans que personne le voie »,
`contenu_deck.py:47`, mais ne détaille pas encore la réponse).

Six briques, dans l'ordre où l'utilisateur les a données :

1. **Boucle de mesure (analytics)** — analytics, verbatims, remontées support, logs
   techniques. Suppose une infra de collecte (automatisable, OCTO sait faire) et de
   stockage (research system / BDD sécurisée). C'est ce qui permet au client de savoir
   où est le problème sans nous le demander — sinon il pilote à l'aveugle.

2. **Kit de production** — le design system, mais surtout son mode d'emploi : quand
   utiliser quel composant, les cas où il ne faut pas, les checklists (accessibilité,
   messages d'erreur, cas limites — champ vide, réseau coupé). Une bibliothèque de
   composants seule ne rend personne autonome ; ce sont les règles d'usage qui font la
   différence.

3. **Formation** — le cœur du transfert : former leurs équipes à utiliser le kit, à lire
   les données de la boucle de mesure, à faire une revue de design entre elles. Pas
   seulement les designers : PO et devs aussi, souvent eux qui décident sur le terrain.
   Idéalement identifier 2-3 personnes référentes chez le client, montées plus loin, pour
   qu'elles prennent le relais en interne.

4. **Gouvernance** — qui a le droit de créer un nouveau composant, comment il entre dans
   le système, qui tranche quand deux équipes ne sont pas d'accord. Le point qu'on oublie
   presque toujours, et par où les design systems / plans de taggage / BDD se délitent en
   quelques mois (lien direct avec le REX en cours sur MES sur ce point précis — c'est
   là que l'apport est le plus net).

5. **Rituels** — design review régulière, office hours où les équipes client viennent
   avec leurs questions, comité pour les sujets structurants. Peu de jours au total, mais
   du rythme : c'est ce qui maintient le niveau dans le temps.

6. **Audit périodique** — retour ponctuel (2x/an par ex.) pour vérifier l'état réel du
   design system, les écarts installés, l'accessibilité, ce que disent les données.
   Débouche sur un plan de correction priorisé que le client exécute (ou nous fait
   intervenir pour l'exécuter). Charge faible, effet rassurant.

## Statut

Note brute non arbitrée, pas encore reprise dans le deck ni dans une offre. À qualifier
au prochain chantier sur `docs/run-ia` : soit un nouveau chapitre/slide (via
`bmad-agent-ux-designer` ou `bmad-ux` en régime proposé — écrit un fichier réel), soit un
enrichissement de la slide « le design system dérive ».
