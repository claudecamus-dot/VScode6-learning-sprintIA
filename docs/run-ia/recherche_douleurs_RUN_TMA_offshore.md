---
title: "Recherche exploratoire — Douleurs de gestion du RUN, avec ou sans TMA, onshore, nearshore ou offshore"
date: 2026-09-18
language: fr
status: "Desk research — version 1.0"
---

# Recherche exploratoire — Douleurs de gestion du RUN, avec ou sans TMA, onshore, nearshore ou offshore

**Date de recherche :** 18 septembre 2026  
**Périmètre :** RUN applicatif, support et maintenance, gestion des incidents et problèmes, TMA/infogérance, centres de services, nearshore/offshore, connaissance, documentation, dette technique et pilotage fournisseur.  
**Objectif :** identifier les douleurs récurrentes, leurs mécanismes, leurs variations selon le modèle opératoire, ainsi que les opportunités potentielles pour une offre « RUN IA ».

> **Note méthodologique** — Ce document est une recherche exploratoire sur sources publiques, et non une étude de marché représentative du seul marché français. Les enquêtes éditeurs sont utiles pour repérer des tendances, mais peuvent comporter un biais commercial. Les travaux académiques décrivent mieux les mécanismes, parfois à partir d'échantillons restreints ou plus anciens. Les verbatims communautaires sont anecdotiques et ne doivent pas être généralisés à un pays, un prestataire ou une population.

---

## 1. Synthèse exécutive

La douleur centrale du RUN n'est pas seulement « trop de tickets ». Elle tient surtout à la **rupture de continuité du contexte** entre l'utilisateur, le support, l'exploitation, l'équipe de développement, les fournisseurs, le code, les changements, les incidents précédents et la documentation.

Cette rupture produit un système dans lequel chaque nouveau signal doit être requalifié presque depuis zéro : retrouver le bon propriétaire, comprendre l'architecture, rassembler les preuves, distinguer symptôme et cause, évaluer l'impact utilisateur, puis reconstruire l'historique. La TMA et l'offshore ne créent pas nécessairement ce problème, mais ils peuvent ajouter des interfaces organisationnelles, contractuelles, temporelles et informationnelles qui l'amplifient.

### Les neuf constats les plus structurants

1. **Le RUN absorbe une part croissante du temps disponible.** Dans le SRE Report 2025 de Catchpoint, la médiane du temps consacré aux activités d'exploitation atteint 30 %, contre 25 % l'année précédente. La médiane du « toil », c'est-à-dire du travail répétitif à faible valeur durable, atteint 20 %.[^1]

2. **La pression de livraison concurrence explicitement la fiabilité.** Dans la même enquête, 41 % des répondants déclarent ressentir « souvent » ou « toujours » une pression pour privilégier les calendriers ou échéances de release plutôt que la fiabilité.[^1]

3. **Le problème n'est pas l'absence d'outils, mais l'absence de vue exploitable.** Toujours selon Catchpoint, 61 % des répondants utilisent entre deux et cinq outils de monitoring/observabilité et 25 % entre six et dix, tandis que 51 % jugent leur instrumentation d'observabilité inférieure au niveau nécessaire.[^1]

4. **Le contexte d'incident reste incomplet.** L'enquête Atlassian 2024, menée auprès de plus de 500 professionnels et décideurs IT américains d'organisations pratiquant DevOps, place en tête des douleurs le manque de visibilité complète sur l'infrastructure. Seuls 55 % déclarent accéder à l'état de santé en temps réel des services pendant un incident.[^2]

5. **La collaboration et la compréhension causale restent des chantiers prioritaires.** Dans cette même enquête, 37 % citent la collaboration interne et 33 % la compréhension de la cause racine parmi les domaines nécessitant une amélioration immédiate. La création du post-mortem demeure l'un des processus les moins automatisés.[^2]

6. **L'externalisation ne supprime pas le besoin d'une organisation cliente forte.** Deloitte rapporte en 2024 que 70 % des dirigeants interrogés ont réinternalisé sélectivement, au cours des cinq années précédentes, certains périmètres auparavant confiés à des tiers ; dans le même temps, 80 % prévoient de maintenir ou d'augmenter leurs investissements dans l'externalisation. Le mouvement observé est donc celui d'un rééquilibrage, pas d'un retour uniforme au « tout interne ».[^3]

7. **La gouvernance de l'écosystème fournisseur est elle-même une faiblesse.** Dans l'enquête Deloitte 2024, 70 % des dirigeants considèrent que leur fonction de Vendor Management Office n'est pas pleinement mature, alors que les modèles combinent de plus en plus équipes internes, fournisseurs, centres captifs et travailleurs numériques.[^3]

8. **L'offshore amplifie surtout des frictions connues : délai de feedback, coordination, partage de connaissance et contrôle.** Une revue systématique de 86 études empiriques sur le développement logiciel distribué identifie les distances géographique, temporelle et socioculturelle comme des facteurs affectant la communication, la coordination et le contrôle, avec un effort supplémentaire de gestion de projet.[^4] Cela ne signifie pas que l'offshore échoue par nature : les résultats dépendent fortement de la modularité du travail, de l'autonomie locale, du chevauchement horaire, de la qualité du transfert et du modèle de gouvernance.

9. **L'IA a le meilleur potentiel lorsqu'elle reconstruit et entretient le contexte, pas lorsqu'elle automatise aveuglément la remédiation.** Une offre « RUN IA » paraît particulièrement pertinente pour réunir les preuves, qualifier et dédupliquer les signaux, produire un dossier d'incident, maintenir une documentation sourcée, sécuriser les transmissions et relier les incidents récurrents à la dette technique. L'autonomie d'action devrait venir plus tard, dans des périmètres réversibles et contrôlés.

### Thèse de travail

> **Le vrai gisement de valeur du RUN IA est la réduction du coût de reconstruction du contexte et du coût de coordination, avant même la réduction du coût d'exécution technique.**

---

## 2. Périmètre et définitions utiles

### RUN

Dans ce document, le RUN désigne l'ensemble des activités nécessaires pour maintenir un service numérique utilisable, fiable, sécurisé et évolutif après sa mise en production : surveillance, support, gestion des incidents et problèmes, changements, maintenance corrective/adaptative/évolutive, communication, capitalisation, gestion de la connaissance et pilotage de la qualité de service.

### TMA

Dans la définition historique du CIGREF et de Syntec, la TMA prend en charge la maintenance et l'évolution de tout ou partie du système applicatif. Elle couvre notamment l'assistance applicative, la maintenance curative et la maintenance évolutive ; elle ne se confond pas nécessairement avec l'exploitation de production.[^5]

Cette distinction reste utile : une entreprise peut externaliser la maintenance applicative sans externaliser la production, ou inversement. Les douleurs apparaissent souvent précisément **aux interfaces** entre ces responsabilités.

### Modèles opératoires considérés

- **Interne / sans TMA** : les équipes de l'entreprise assurent directement le RUN.
- **TMA onshore** : maintenance confiée à un prestataire dans le même pays ou avec une forte proximité opérationnelle.
- **Nearshore** : centre de services dans une zone proche, avec un décalage horaire, linguistique ou juridique limité.
- **Offshore lointain** : centre de services plus éloigné, souvent choisi notamment pour la capacité ou le coût.
- **Centre captif / GIC** : entité appartenant au groupe, située dans une autre région ou un autre pays.
- **Multi-fournisseurs** : plusieurs acteurs interviennent sur des couches ou applications différentes.
- **Hybride** : combinaison d'équipes internes, prestataires, centres captifs et automatisations.

---

## 3. Signaux quantitatifs disponibles

| Signal | Résultat public | Lecture pour le RUN | Limites |
|---|---:|---|---|
| Charge d'exploitation | Médiane de 30 % du temps en activités d'exploitation dans le SRE Report 2025, contre 25 % en 2024[^1] | Le RUN réactif peut évincer l'ingénierie préventive | Enquête orientée SRE/fiabilité, échantillon auto-sélectionné |
| Toil | Médiane de 20 % du temps[^1] | Une part importante du travail ne produit pas d'amélioration durable | La définition et l'auto-évaluation peuvent varier |
| Arbitrage vitesse/fiabilité | 41 % « souvent » ou « toujours » sous pression pour privilégier la release à la fiabilité[^1] | La dette et les problèmes récurrents restent repoussés | Perception déclarative |
| Dispersion des outils | 61 % utilisent 2 à 5 outils d'observabilité, 25 % en utilisent 6 à 10[^1] | Multiplication des sources et difficulté à corréler les preuves | Nombre d'outils ≠ mauvaise qualité en soi |
| Instrumentation | 51 % estiment l'instrumentation inférieure au besoin[^1] | L'IA ne peut pas compenser des preuves absentes ou de mauvaise qualité | Perception déclarative |
| Visibilité d'incident | 55 % seulement ont accès à l'état de santé live des services[^2] | Le commandement d'incident opère avec une image partielle | Échantillon américain, organisations DevOps de 101+ employés |
| Douleur principale d'incident | 22 % citent le manque de visibilité complète ; 17 % la coordination inter-départements ; 13 % le manque de contexte[^2] | Visibilité, coordination et contexte forment un même nœud de douleur | Une seule « plus grande douleur » par répondant |
| Amélioration urgente | Collaboration interne : 37 % ; cause racine : 33 % ; résolution, compréhension des changements et détection : environ 31 % chacun[^2] | Les difficultés sont autant organisationnelles que techniques | Enquête éditeur |
| Volume d'incidents | 40 % des répondants Catchpoint ont géré 1 à 5 incidents sur les 30 jours précédents ; 23 % en ont géré 6 à 10[^1] | Le coût de qualification se répète fréquemment | N'indique pas la gravité ni la taille des organisations |
| Pression croissante | PagerDuty rapporte une hausse annuelle de 13 % des incidents impliquant les clients dans son enquête 2024 auprès de 350 dirigeants[^6] | La capacité de réponse doit absorber une complexité croissante | Étude sponsorisée par un fournisseur de gestion d'incidents |
| Rééquilibrage du sourcing | 70 % ont sélectivement réinternalisé un périmètre ; 80 % maintiennent ou augmentent l'externalisation[^3] | Les entreprises cherchent un portefeuille de modèles plutôt qu'une réponse unique | Enquête de dirigeants, non spécifique au RUN applicatif |
| Maturité du pilotage fournisseur | 70 % indiquent un VMO non pleinement mature[^3] | Le coût de coordination et la responsabilité de bout en bout restent mal maîtrisés | « Maturité » auto-déclarée |
| Bénéfices de l'IA dans l'outsourcing | 83 % utilisent l'IA dans des services externalisés, mais 25 % seulement constatent une baisse des coûts fournisseur ou une amélioration de qualité[^3] | L'adoption technique ne garantit pas un résultat opérationnel | Données agrégées sur plusieurs types d'outsourcing |
| Talents des centres globaux | Deloitte cite les déficits de compétences, le turnover et la hausse des coûts du travail parmi les défis persistants ; 50 % prévoient d'étendre leur empreinte GBS[^7] | L'offshore n'élimine pas le risque de capacité et de rétention | Périmètre GBS plus large que la TMA IT |

---

## 4. Carte des douleurs du RUN

## 4.1 Le RUN devient une « usine à tickets »

### Manifestations

- pilotage par volumes entrants, ancienneté du backlog et respect des délais contractuels ;
- clôture rapide de tickets sans élimination de la cause ;
- même incident revenant sous plusieurs libellés ;
- niveau 1 servant d'aiguillage plus que de résolution ;
- multiplication des statuts, catégories et files d'attente ;
- équipes techniques recevant des demandes pauvres en preuves ;
- utilisateur obligé de reformuler plusieurs fois son problème.

### Mécanisme

Le ticket devient l'unité de travail et de facturation, alors que le véritable objet à piloter est le **problème de service** et son impact. Lorsque les systèmes de mesure récompensent la prise en charge, le délai de réponse ou la clôture, ils peuvent sous-valoriser la prévention, la documentation et la suppression des causes récurrentes.

### Conséquences

- augmentation du coût par problème réellement résolu ;
- illusion de performance malgré une expérience utilisateur dégradée ;
- backlog de problèmes permanents masqué par un bon respect des SLA ;
- difficulté à justifier les investissements de fiabilisation.

### Mesures à observer

- taux de réouverture ;
- taux de récurrence à 30/90 jours ;
- ratio incidents/problèmes ;
- nombre de tickets par cause racine ;
- taux de résolution définitive ;
- effort de qualification avant assignation utile ;
- satisfaction utilisateur après résolution, pas seulement après clôture.

---

## 4.2 Les équipes reconstruisent le contexte à chaque incident

### Manifestations

- recherche manuelle du dernier déploiement ;
- difficulté à savoir quels composants et utilisateurs sont touchés ;
- dépendances non cartographiées ;
- historique dispersé entre ITSM, chat, logs, dashboards, Git et documents ;
- lancement de plusieurs investigations parallèles ;
- escalades tardives parce que le propriétaire n'est pas connu.

Atlassian rapporte que le manque de visibilité complète sur l'infrastructure reste la première douleur déclarée dans son enquête 2024, et que seuls 55 % des répondants accèdent à l'état de santé live des services pendant un incident.[^2]

### Conséquences

- temps de diagnostic supérieur au temps de correction ;
- mobilisation excessive de profils seniors ;
- décisions prises à partir d'informations incomplètes ;
- communication utilisateur incertaine ;
- difficulté à comparer l'incident à des précédents.

### Opportunité RUN IA

Créer automatiquement un **dossier de contexte** contenant : symptômes, chronologie, services affectés, utilisateurs ou segments touchés, changements récents, incidents similaires, logs pertinents, propriétaire probable, runbook et niveau de confiance.

---

## 4.3 Le toil et le travail réactif évinceraient le préventif

Le SRE Report 2025 indique une hausse de la médiane du travail opérationnel à 30 %, tandis que le temps d'ingénierie reste stable à 50 % ; le rapport interprète cette évolution comme un risque d'empiètement des tâches routinières sur les efforts proactifs.[^1]

### Manifestations

- enrichissement manuel des tickets ;
- copier-coller entre outils ;
- relances de propriétaires ;
- création répétitive de rapports ;
- mêmes requêtes de diagnostic ;
- traitements de données ponctuels non industrialisés ;
- réunions de synchronisation destinées à compenser un manque de visibilité.

### Cercle vicieux

1. Les incidents consomment le temps disponible.
2. Les travaux de fiabilisation sont repoussés.
3. La dette, l'observabilité et la documentation se dégradent.
4. Les incidents deviennent plus difficiles à résoudre.
5. Le RUN consomme encore davantage de capacité.

Une automatisation pertinente doit donc supprimer le toil **et** convertir le temps gagné en réduction durable des causes. Sans gouvernance de cette capacité, l'automatisation peut simplement permettre d'absorber plus de flux sans améliorer le système.

---

## 4.4 L'observabilité est fragmentée ou insuffisante

Le nombre d'outils n'est pas un bon proxy de maturité. Une entreprise peut disposer de nombreux dashboards tout en manquant de données corrélables, de conventions de nommage, de propagation d'identifiants ou de cartographie des dépendances.

### Manifestations

- métriques, traces et logs sans identifiant commun ;
- alertes sans contexte métier ;
- seuils statiques et bruit important ;
- informations différentes selon l'outil consulté ;
- dépendance à un expert capable d'interpréter les signaux ;
- monitoring technique déconnecté des parcours utilisateurs.

### Point clé

L'IA ne crée pas une preuve qui n'existe pas. Une couche RUN IA doit donc mesurer la **qualité de l'évidence** : fraîcheur, complétude, cohérence, traçabilité et couverture des parcours critiques.

---

## 4.5 La recherche de cause racine reste lente et inconstante

Dans l'enquête Atlassian, 33 % des répondants citent la compréhension de la cause racine comme un domaine exigeant une amélioration immédiate.[^2]

### Manifestations

- confusion entre symptôme, déclencheur et cause systémique ;
- diagnostic orienté par le premier signal disponible ;
- hypothèses non consignées ;
- difficulté à reproduire ;
- correctif local sans test de non-régression ;
- post-mortem produit tardivement ou jamais transformé en actions.

### Risque

Une « cause racine » générée trop tôt par une IA peut donner une fausse assurance. Le produit devrait plutôt gérer un ensemble d'hypothèses, chacune reliée à des preuves, à des contradictions et à un niveau de confiance.

---

## 4.6 La connaissance est tribale, périssable et mal transférée

La documentation est souvent pensée comme un livrable statique, alors que la connaissance opérationnelle vit dans les décisions, les incidents, les changements, les échanges et les gestes de diagnostic.

Une étude de cinq transferts de maintenance logicielle dans une banque suisse conclut que la connaissance la plus critique concerne le logiciel lui-même — sa structure, ses fonctions et son comportement — et qu'elle se transmet efficacement par des tâches de maintenance réelles ou réalistes, guidées par des experts.[^8]

### Manifestations

- documentation descriptive mais inutilisable en incident ;
- informations non datées ou contradictoires ;
- vidéos longues sans indexation ;
- dépendance à une ou deux personnes ;
- onboarding mesuré en mois ;
- transfert limité à des présentations ;
- perte de connaissance lors du turnover ou d'un changement de fournisseur.

### Ce que cela implique

Un transfert ne peut pas être validé uniquement par la livraison de documents. Il doit être testé par la capacité de la nouvelle équipe à diagnostiquer et résoudre des cas réels avec une autonomie croissante.

---

## 4.7 Le post-incident ne ferme pas réellement la boucle

Atlassian observe que la création du post-mortem reste parmi les processus les moins automatisés.[^2] Catchpoint constate également un niveau de soutien perçu plus faible après l'incident que pendant celui-ci, ce qui suggère un risque de perte d'énergie une fois le service restauré.[^1]

### Manifestations

- retour à la normale considéré comme la fin du travail ;
- actions correctives sans propriétaire ou date ;
- enseignements non propagés aux autres équipes ;
- runbook non mis à jour ;
- absence de vérification de l'efficacité du correctif ;
- dette technique créée par le contournement d'urgence.

### Indicateurs utiles

- taux d'actions post-incident closes dans le délai ;
- taux d'incidents avec runbook/documentation mis à jour ;
- récurrence de la classe d'incident ;
- nombre d'autres services ayant appliqué la mesure préventive ;
- délai entre restauration et capitalisation validée.

---

## 4.8 Le BUILD et le RUN ont des objectifs et des horizons différents

Le conflit entre release et fiabilité apparaît explicitement dans le SRE Report 2025.[^1]

### Manifestations

- équipe projet dissoute juste après la mise en production ;
- documentation de passage au RUN incomplète ;
- critères d'acceptation centrés sur la fonctionnalité ;
- absence de budget d'observabilité ou de support ;
- dette créée pendant le build transférée silencieusement au RUN ;
- maintien de production sans accès aux décisions d'architecture.

### Douleur particulière après un build agentique ou très accéléré

- code produit plus vite que sa compréhension ;
- décisions dispersées dans des conversations avec des agents ;
- tests et documentation de qualité variable ;
- ownership ambigu ;
- dépendances ajoutées sans inventaire complet ;
- difficulté à reproduire pourquoi une implémentation a été choisie.

### Opportunité

Un **RUN readiness check** devrait être une étape de livraison : cartographie, ownership, traces, tests critiques, rollback, runbooks, dépendances, secrets, SLO et backlog de dette connu.

---

## 4.9 La voix utilisateur est séparée du diagnostic technique

### Manifestations

- feedback dans Intercom ou Zendesk, incidents dans l'ITSM, usage dans l'analytics et défauts dans Jira ;
- impossibilité de savoir combien d'utilisateurs sont réellement touchés ;
- demandes de fonctionnalités masquant des problèmes de compréhension ;
- correctif déployé sans fermeture de boucle auprès des utilisateurs ;
- priorité dictée par le volume de tickets plutôt que par le segment, la criticité ou l'abandon.

### Conséquence

Le RUN optimise la disponibilité technique tandis que le produit mesure l'adoption, sans représentation commune du problème vécu.

### Opportunité RUN IA

Relier un verbatim utilisateur à un parcours, une version, un événement, un composant, un changement et une classe d'incident, avec conservation des preuves et respect des contraintes de données personnelles.

---

## 4.10 Les SLA contractuels peuvent être atteints sans produire le résultat attendu

### Manifestations

- délai de réponse respecté, mais diagnostic peu utile ;
- ticket fermé puis rouvert ;
- contournement accepté comme résolution ;
- priorité contractuelle différente de l'impact utilisateur ;
- optimisation locale par fournisseur ;
- exclusions de périmètre déclenchant des renvois de responsabilité.

### Tension structurelle

Les contrats historiques sont souvent adaptés à une logique de service mesurable, mais peuvent encourager une lecture transactionnelle : volumes, délais et pénalités. Deloitte constate une progression des modèles orientés résultats et valeur, ce qui traduit la recherche d'un meilleur alignement entre prestation et impact.[^3]

### Évolution possible

Compléter les SLA par :

- SLO orientés service ou parcours ;
- récurrence et taux de résolution définitive ;
- coût d'inaction de la dette ;
- satisfaction et effort utilisateur ;
- fraîcheur documentaire ;
- capacité de reprise et de réversibilité ;
- réduction du toil ;
- amélioration de la détectabilité.

---

## 4.11 Le pilotage multi-fournisseurs dilue la responsabilité de bout en bout

### Manifestations

- « ticket ping-pong » entre application, infrastructure, éditeur et réseau ;
- chaque prestataire respecte son SLA local ;
- personne ne possède le parcours complet ;
- données et tableaux de bord non partagés ;
- escalade commerciale utilisée pour résoudre un problème technique ;
- RCA négociée plutôt que construite collectivement.

Le CIGREF recommandait déjà historiquement de clarifier les responsabilités vis-à-vis des autres prestataires et de préparer une véritable réversibilité opérationnelle, pas seulement contractuelle.[^5]

### Opportunité

Créer une couche de preuve et de chronologie commune, indépendante des frontières fournisseur, sans supprimer la source de vérité contractuelle de chaque acteur.

---

## 4.12 La dette technique est visible comme opinion, rarement comme coût du RUN

### Manifestations

- backlog de dette séparé des incidents ;
- priorisation par ancienneté ou influence de l'équipe ;
- absence de lien entre composant fragile et coût opérationnel ;
- dette documentaire non comptabilisée ;
- dépendances obsolètes traitées uniquement lors d'une alerte de sécurité ;
- modules à forte fréquence de changement mais faible couverture de tests.

### Mesure plus utile : les « intérêts » de la dette

Pour chaque dette, mesurer :

- incidents et tickets associés ;
- heures de diagnostic et de contournement ;
- délai ajouté aux évolutions ;
- risque de sécurité ou de conformité ;
- coût d'infrastructure ;
- dépendance à une personne ou un fournisseur ;
- effet sur le temps d'onboarding ;
- fréquence de rollback.

Une capacité RUN IA pourrait transformer la dette d'un inventaire statique en **portefeuille de risques et de coûts observés**.

---

## 4.13 Talents, astreinte, turnover et fatigue opérationnelle

Les modèles internes et externalisés partagent une même difficulté : conserver les compétences rares et maintenir une connaissance suffisante du système. Deloitte cite les écarts de compétences, le turnover et la hausse des coûts du travail parmi les défis persistants des organisations globales de services.[^7]

### Manifestations

- experts sollicités sur toutes les escalades ;
- équipes de nuit ou d'astreinte sous tension ;
- prestataires remplaçant des profils sans continuité suffisante ;
- CV ou séniorité contractuels ne reflétant pas toujours l'équipe effective ;
- coût invisible de mentorat et de contrôle côté client ;
- baisse de qualité lors des rotations.

### Point de vigilance

L'origine géographique ne détermine pas la qualité d'une équipe. Les variables les plus utiles à mesurer sont la stabilité, l'expérience du système, le niveau d'autonomie, la qualité du leadership local, la capacité à signaler les risques et la transparence du staffing.

---

## 4.14 Sécurité, accès de production et chaîne de sous-traitance

La CNIL rappelle que le responsable de traitement doit connaître les mesures de sécurité du sous-traitant, définir contractuellement les responsabilités, l'authentification, la restitution/destruction des données et la notification des incidents, et considérer toute la chaîne de sous-traitance.[^9]

### Douleurs opérationnelles

- habilitations trop larges pour faciliter le support ;
- comptes partagés ou mal attribués ;
- accès d'urgence non révoqués ;
- sous-traitants ultérieurs peu visibles ;
- transferts de données hors zone mal compris ;
- tension entre vitesse de diagnostic et moindre privilège ;
- auditabilité incomplète des actions humaines et automatisées.

### Implication RUN IA

Toute action automatisée doit être soumise à un moteur de politique : périmètre autorisé, identité, justification, preuve, approbation, réversibilité et journal d'audit.

---

## 4.15 Réversibilité et dépendance fournisseur

La réversibilité est souvent bien décrite juridiquement mais rarement exercée comme une capacité opérationnelle continue. Le CIGREF recommandait de vérifier régulièrement qu'elle pouvait effectivement être engagée.[^5]

### Manifestations

- documentation produite à la fin du contrat ;
- données exportables mais non exploitables ;
- scripts et outils appartenant au fournisseur ;
- connaissance concentrée dans l'équipe sortante ;
- inventaire incomplet des accès, exceptions et tâches planifiées ;
- coûts de transition sous-estimés ;
- maintien d'un fournisseur par incapacité pratique à changer.

### Test de réversibilité plus réaliste

Demander périodiquement à une équipe indépendante de :

1. retrouver la cartographie du service ;
2. traiter un incident simulé ;
3. exécuter un déploiement et un rollback ;
4. identifier les dépendances et secrets ;
5. reprendre un ticket complexe ;
6. produire le reporting attendu.

---

## 5. Ce qui change selon le modèle opératoire

| Modèle | Douleurs dominantes | Ce qu'il peut améliorer | Conditions de réussite |
|---|---|---|---|
| **RUN interne** | connaissance tribale, surcharge d'astreinte, arbitrage roadmap/fiabilité, difficulté à industrialiser les tâches rares | proximité métier, responsabilité directe, boucle de feedback plus courte | ownership explicite, capacité réservée au préventif, observabilité et documentation intégrées au travail |
| **TMA onshore** | contractualisation du flux, frontière client/prestataire, dépendance au key account, mesure par SLA plutôt que résultat | capacité, standardisation, spécialisation, continuité de service | gouvernance conjointe, transparence du staffing, métriques de résultat, réversibilité testée |
| **Nearshore** | transfert de connaissance, différence linguistique ou culturelle modérée, coordination intersite | couverture élargie, proximité horaire, bassin de compétences | chevauchement suffisant, équipes stables, ownership de composants, leadership local |
| **Offshore lointain** | latence de feedback, handovers, faible temps de recouvrement, transfert tacite, contrôle et sécurité | couverture 24/7, capacité importante, spécialisation, coûts unitaires potentiellement inférieurs | travail modularisé, autonomie locale, standards explicites, passation structurée, gouvernance et accès rigoureux |
| **Centre captif/GIC** | recrutement, turnover, distance organisationnelle, duplication de management | plus de contrôle, alignement d'incitations, capitalisation interne | carrière locale, mandat clair, leadership global, produits ou domaines possédés de bout en bout |
| **Multi-fournisseurs** | renvoi de responsabilité, données cloisonnées, incohérence de processus, RCA conflictuelle | concurrence, spécialisation, réduction de dépendance unique | intégration de service, RACI de bout en bout, chronologie et preuves partagées, gouvernance commune |
| **Hybride** | complexité du portefeuille de modèles, frontières mouvantes, difficulté à comparer la performance | souplesse, résilience, choix du meilleur modèle par type de travail | architecture de gouvernance, taxonomie commune, données homogènes et arbitrage central |

### Conclusion comparative

Il n'existe pas de modèle universellement supérieur. Le modèle le plus adapté dépend notamment de quatre dimensions :

- **couplage métier** : le travail exige-t-il des échanges fréquents avec les utilisateurs ou décideurs ?
- **spécificité de la connaissance** : l'application et son histoire sont-elles difficiles à apprendre ?
- **modularité technique** : le périmètre peut-il être possédé et testé indépendamment ?
- **urgence et ambiguïté** : le travail demande-t-il des décisions rapides avec des informations incomplètes ?

Plus le travail est ambigu, fortement couplé au métier, spécifique et urgent, plus la distance et le nombre d'interfaces deviennent coûteux. À l'inverse, un domaine bien délimité, observable, documenté et doté d'une équipe autonome peut être opéré efficacement à distance.

---

## 6. Focus : mécanismes spécifiques de l'offshore

## 6.1 La latence n'est pas seulement une question de réunions

Un faible chevauchement horaire transforme une question bloquante de cinq minutes en cycle de 24 heures. Il ralentit également les revues de code, les validations fonctionnelles, les changements urgents et la clarification d'une alerte.

Une étude portant sur 80 clients et six entretiens conclut, dans son échantillon, que le nearshore obtient de meilleurs résultats que le far offshore sur le succès global, la qualité, l'effort de gestion, le respect du planning et les problèmes de communication ; les auteurs le recommandent particulièrement pour les projets agiles ou intensifs en communication.[^10] Ce résultat est directionnel et ne doit pas être transformé en règle générale.

### Contre-mesures

- heures de recouvrement garanties ;
- lead local habilité à décider ;
- lots de travail indépendants ;
- seuil clair entre question asynchrone et appel immédiat ;
- dossier de passation standardisé ;
- rotation ponctuelle ou colocalisation lors des phases critiques.

## 6.2 Le handover peut créer une « perte par compression »

Une passation résume nécessairement la situation. Si le format est faible, les hypothèses, les doutes, les signaux faibles et les raisons d'une décision disparaissent. L'équipe suivante reçoit une conclusion sans le raisonnement ni les preuves.

### Opportunité RUN IA

Générer un **handover actif** : état courant, actions tentées, résultats, hypothèses rejetées, risques, prochaines décisions, personnes à joindre et preuves liées. La nouvelle équipe doit pouvoir poser des questions à ce dossier, avec retour aux sources.

## 6.3 Le transfert de connaissance est un apprentissage, pas une livraison documentaire

Les travaux sur la maintenance externalisée montrent l'importance de tâches guidées et réalistes.[^8] Les difficultés augmentent lorsque le système possède beaucoup de connaissances implicites, d'exceptions et d'histoire non documentée.

### Contre-mesures

- progression « observation → résolution guidée → autonomie » ;
- cas réels sélectionnés par complexité croissante ;
- tests de reprise ;
- mesure de l'autonomie, pas seulement de la présence aux sessions ;
- documentation créée à partir du travail réel ;
- maintien d'une période de coexistence suffisante.

## 6.4 Le coût unitaire peut masquer le coût client retenu

Le coût complet inclut aussi :

- spécification supplémentaire ;
- contrôle qualité ;
- coordination ;
- gouvernance fournisseur ;
- gestion des accès ;
- répétition des explications ;
- correction et rework ;
- transition et réversibilité ;
- coût de la latence de décision.

La bonne comparaison n'est donc pas « taux journalier local contre taux offshore », mais **coût par résultat durable**, incluant le travail conservé côté client et les effets sur la qualité ou le délai.

## 6.5 Le « follow-the-sun » est une capacité exigeante

Le modèle peut réduire le temps de restauration si :

- chaque équipe a un périmètre d'autorité clair ;
- les environnements et outils sont cohérents ;
- la preuve est partagée ;
- le handover est testé ;
- le niveau de compétence est comparable ;
- un incident commander conserve la continuité.

Sans ces conditions, il peut devenir un enchaînement de requalifications et de pertes de contexte.

## 6.6 Les différences culturelles doivent être traitées comme des variables de travail, pas comme des stéréotypes

Les risques concrets à observer sont :

- manière de signaler un désaccord ou un retard ;
- autonomie attendue ;
- relation à la hiérarchie ;
- usage d'une terminologie commune ;
- tolérance à l'ambiguïté ;
- qualité des écrits asynchrones ;
- capacité à demander de l'aide tôt.

Ces comportements varient au sein de chaque pays et dépendent aussi fortement du management, du contrat, de l'ancienneté de l'équipe et de la sécurité psychologique.

---

## 7. Verbatims publics illustratifs

> **Précaution d'usage** — Les citations ci-dessous illustrent des mécanismes ; elles ne constituent pas une mesure de prévalence. Les commentaires de forum reflètent une expérience individuelle et peuvent contenir des biais. Ils ne doivent pas être interprétés comme un jugement sur une nationalité ou l'ensemble des équipes offshore.

### Visibilité et contexte

> “Lack of full visibility across IT infrastructure remains the largest pain point.”[^2]

Lecture : la douleur déclarée ne porte pas seulement sur le temps de correction, mais sur l'incapacité à obtenir rapidement une représentation fiable du système touché.

### Réversibilité

> « Trop souvent la réversibilité/transférabilité est prévue dans les contrats, mais est concrètement peu évoquée opérationnellement. »[^5]

Lecture : le risque est connu depuis longtemps, mais sa traduction en capacité testable reste un sujet de gouvernance.

### Latence de feedback offshore

> “Many lost days because of unanswered blocker questions during their working day.”[^11]

Lecture : une question courte peut devenir une journée perdue lorsqu'il n'existe ni recouvrement horaire, ni autonomie locale, ni mécanisme d'escalade.

### Transparence de l'exécution

> “Time zones, saying yes to one thing but doing something different, very high attrition rates.”[^11]

Lecture : trois douleurs sont ici mêlées — temporalité, alignement sur l'attendu et stabilité de l'équipe. Ce commentaire reste strictement anecdotique.

### Confiance dans l'IA opérationnelle

> “AI is at best ‘a co-worker you can’t trust’.”[^1]

Lecture : ce commentaire d'experte intégré au rapport Catchpoint souligne l'intérêt d'une IA vérifiable, sourcée et supervisée plutôt que d'une autonomie opaque.

### Chaîne de sous-traitance

> « Toute la chaîne de sous-traitance [...] devrait être considérée. »[^9]

Lecture : la visibilité opérationnelle et réglementaire doit dépasser le fournisseur contractuel direct.

---

## 8. Hypothèses de problèmes à valider sur le terrain

Les hypothèses ci-dessous sont formulées pour préparer des entretiens, et non comme des conclusions déjà démontrées dans une entreprise donnée.

### Hypothèse H1 — Le coût de qualification dépasse souvent le coût du correctif

À mesurer : temps entre création et premier propriétaire pertinent, nombre de réassignations, temps passé à réunir les preuves, part des tickets résolus par un changement très court après une longue investigation.

### Hypothèse H2 — Les KPI contractuels masquent les problèmes récurrents

À mesurer : SLA respectés versus réouvertures, récurrence à 30/90 jours, satisfaction utilisateur, contournements, incidents liés à une même dette.

### Hypothèse H3 — La documentation existe mais n'est ni fiable ni actionnable

À mesurer : âge des documents, contradictions avec le code ou la configuration, temps nécessaire pour trouver un runbook, pourcentage de procédures réellement testées.

### Hypothèse H4 — Le client paie un « coût retenu » non visible dans le contrat

À mesurer : temps interne consacré à spécifier, relancer, contrôler, corriger, escalader, préparer les comités et compenser les lacunes de connaissance.

### Hypothèse H5 — Le changement d'équipe ou de fournisseur crée un pic durable de risque

À mesurer : incidents, temps de résolution, taux de réouverture et erreurs de changement avant, pendant et après une transition.

### Hypothèse H6 — L'offshore échoue surtout sur les travaux ambigus et fortement couplés

À comparer : performance des tickets standardisés versus problèmes nouveaux, évolutions métier complexes, incidents P1 et changements transverses.

### Hypothèse H7 — La dette la plus coûteuse n'est pas celle qui paraît la plus ancienne

À mesurer : incidents, effort de changement, dépendance humaine, coût infra, vulnérabilités et temps d'onboarding associés à chaque zone.

### Hypothèse H8 — Le feedback utilisateur est sous-exploité pour détecter et prioriser le RUN

À mesurer : délai entre premier signal utilisateur et détection technique, taux de feedbacks reliés à un ticket ou une cause, part des correctifs suivis d'une communication de fermeture de boucle.

---

## 9. Opportunités pour une offre « RUN IA »

## 9.1 Une couche de preuve unifiée

Connecter sans remplacer les systèmes existants : ITSM, monitoring, logs, traces, dépôt de code, CI/CD, documentation, support client, analytics et communication.

Fonctions :

- normaliser les identités de service, composant, version et propriétaire ;
- conserver les liens vers les sources ;
- dater chaque information ;
- détecter les contradictions ;
- calculer un niveau de confiance ;
- appliquer les politiques d'accès.

## 9.2 Une « RUN Inbox » intelligente

- ingestion multicanal ;
- classification bug/incident/demande/incompréhension/dette ;
- déduplication ;
- regroupement par cause ou parcours ;
- estimation du périmètre affecté ;
- demande automatique des preuves manquantes ;
- routage vers le propriétaire probable.

## 9.3 Le dossier d'incident ou de bug

À partir d'un signal, produire :

- résumé factuel ;
- chronologie ;
- impact utilisateur et métier ;
- changement récent corrélé ;
- composants et dépendances ;
- incidents similaires ;
- hypothèses avec preuves pour/contre ;
- prochaines actions ;
- communication interne et externe proposée.

## 9.4 La documentation vivante et sourcée

- cartographie fonctionnelle et technique ;
- runbooks générés puis validés à partir des résolutions réelles ;
- historique des décisions ;
- détection de documents obsolètes ;
- indicateur de fraîcheur ;
- niveau de confiance ;
- propriétaire et date de validation ;
- preuve du dernier exercice de la procédure.

## 9.5 L'assistant de passation offshore / follow-the-sun

- état de situation structuré ;
- questions ouvertes ;
- décisions et raisons ;
- actions tentées et résultats ;
- risques et seuils d'escalade ;
- vérification que l'équipe entrante a accusé réception et compris ;
- traduction contrôlée de la terminologie, sans perdre les identifiants techniques.

## 9.6 Le « knowledge transfer cockpit »

- inventaire des connaissances à transférer ;
- tâches guidées par complexité ;
- mesure de l'autonomie ;
- zones encore dépendantes d'un expert ;
- questions non résolues ;
- score de réversibilité fondé sur des exercices, pas seulement sur des documents.

## 9.7 La dette technique reliée au coût opérationnel

- relier dette, incidents, tickets, changements et temps passé ;
- détecter les composants à forte fréquence de panne et de modification ;
- estimer les intérêts de la dette ;
- simuler l'effet d'une remédiation ;
- produire un dossier d'arbitrage avec incertitude explicite.

## 9.8 La boucle feedback → produit → RUN → utilisateur

- regrouper les verbatims ;
- associer segments et parcours ;
- rapprocher feedback et signaux techniques ;
- suivre la résolution ;
- proposer la réponse utilisateur ;
- vérifier après déploiement que le comportement s'est amélioré.

## 9.9 Le pilotage fournisseur par résultat

- compléter les SLA avec récurrence, résolution définitive, qualité documentaire et autonomie ;
- rendre visible le coût client retenu ;
- comparer les périmètres sur des définitions communes ;
- identifier les renvois de tickets et les temps d'attente inter-équipes ;
- mesurer la stabilité réelle du staffing et de la connaissance.

## 9.10 La gouvernance de l'autonomie

Niveaux recommandés :

1. **Observer** : synthétiser et signaler.
2. **Recommander** : proposer avec preuves.
3. **Préparer** : rédiger ticket, test, documentation, réponse ou pull request.
4. **Exécuter après approbation** : action validée par un humain.
5. **Agir dans un périmètre réversible** : automatisation surveillée avec garde-fous et rollback.

Le MVP devrait privilégier les niveaux 1 à 3. Les actions de production autonomes sont moins différenciantes à court terme que la qualité du contexte, et nettement plus risquées.

---

## 10. Périmètre MVP suggéré

### Proposition : « RUN Context & Knowledge Control »

Un premier produit pourrait se concentrer sur trois résultats :

1. **Réduire le temps de qualification et de reconstruction du contexte.**
2. **Empêcher la perte de connaissance après incident, transition ou changement d'équipe.**
3. **Relier les récurrences à la dette technique et à l'impact utilisateur.**

### Flux MVP

1. Connexion à l'ITSM, au code, au monitoring, à la documentation et au support utilisateur.
2. Ingestion d'un ticket ou d'une alerte.
3. Recherche de doublons et d'incidents analogues.
4. Construction automatique d'un dossier de contexte.
5. Identification des preuves manquantes et du propriétaire probable.
6. Préparation des actions : ticket enrichi, scénario de reproduction, requête de diagnostic, brouillon de communication.
7. Après résolution, mise à jour proposée du runbook et du graphe de connaissance.
8. Détection de la récurrence et création éventuelle d'un cas de dette.

### Pourquoi ce wedge paraît crédible

- valeur observable sans donner à l'IA un accès d'écriture sensible ;
- pertinent en interne comme en TMA ;
- particulièrement utile en multi-fournisseurs et distribué ;
- crée le socle de données nécessaire à une autonomie future ;
- améliore simultanément incidents, documentation, transition et dette.

---

## 11. Métriques à collecter pour confirmer le problème

### Flux et qualification

- délai création → propriétaire pertinent ;
- nombre moyen de réassignations ;
- pourcentage de tickets dupliqués ;
- part de tickets nécessitant une demande d'information supplémentaire ;
- temps humain d'enrichissement ;
- taux de tickets sans composant ou service identifié.

### Incident

- MTTA, temps de qualification, temps de diagnostic, temps de restauration ;
- incidents récurrents ;
- changements impliqués ;
- nombre de personnes mobilisées ;
- temps d'attente entre équipes ou fuseaux ;
- fréquence des escalades.

### Connaissance

- couverture documentaire des services critiques ;
- âge et fraîcheur ;
- contradictions détectées ;
- taux de runbooks testés ;
- temps d'onboarding ;
- dépendance à des experts nommés ;
- autonomie après transfert.

### TMA et fournisseurs

- temps client retenu par mois ;
- coût complet par ticket définitivement résolu ;
- réouverture ;
- renvoi inter-fournisseurs ;
- rotation de l'équipe ;
- stabilité des profils clés ;
- résultats des exercices de réversibilité.

### Offshore

- heures de recouvrement ;
- questions bloquantes restant sans réponse jusqu'au cycle suivant ;
- nombre de handovers par incident ;
- perte d'information détectée ;
- différence de performance entre travail standardisé et travail ambigu ;
- délai de revue/validation.

### Dette et amélioration continue

- heures de RUN associées à chaque composant ;
- incidents par dette identifiée ;
- part de capacité consacrée au préventif ;
- actions post-mortem achevées ;
- réduction observée après remédiation.

---

## 12. Guide d'entretien terrain

### Pour un responsable RUN / production

1. À quel moment perdez-vous le plus de temps pendant un incident : détection, qualification, mobilisation, diagnostic, décision ou communication ?
2. Quelles informations devez-vous encore chercher manuellement ?
3. Combien de fois un incident est-il réassigné avant d'atteindre la bonne équipe ?
4. Quelles classes d'incidents reviennent régulièrement ?
5. Quelles actions post-incident restent le plus souvent ouvertes ?
6. Quel travail répétitif voudriez-vous éliminer sans prendre de risque de production ?

### Pour un responsable applicatif ou produit

1. Savez-vous relier les retours utilisateurs aux incidents et aux versions ?
2. Quels composants sont difficiles à faire évoluer, et pourquoi ?
3. Comment arbitrez-vous fiabilité, dette et roadmap ?
4. La documentation vous permet-elle de reprendre le produit sans l'équipe de build ?
5. Quel est le délai entre un feedback récurrent et une décision produit ?

### Pour un responsable de TMA / fournisseur

1. Quels KPI pilotent réellement la relation ?
2. Quels comportements ces KPI encouragent-ils involontairement ?
3. Où se trouvent les principales zones de responsabilité ambiguë ?
4. Quelle part du travail du client est nécessaire pour que la prestation fonctionne ?
5. Comment la stabilité et l'expérience de l'équipe sont-elles mesurées ?
6. Quand la réversibilité a-t-elle été testée pour la dernière fois ?

### Pour une équipe nearshore/offshore

1. Combien d'heures de recouvrement sont réellement disponibles ?
2. Que se passe-t-il lorsqu'une question bloque le travail hors de cette fenêtre ?
3. Quelles décisions l'équipe peut-elle prendre sans validation distante ?
4. Le handover contient-il les actions tentées et les hypothèses rejetées ?
5. Quels sujets exigent encore systématiquement un expert côté client ?
6. Quels signaux rendent difficile l'annonce d'un risque ou d'un retard ?

### Pour le support utilisateur

1. Quels champs sont rarement remplis correctement par les utilisateurs ?
2. Combien de retours différents correspondent au même problème ?
3. Quels tickets sont transférés plusieurs fois ?
4. Recevez-vous une information fiable pour répondre après résolution ?
5. Quels segments ou parcours produisent le plus d'effort ?

### Pour les développeurs et SRE

1. Quel pourcentage du temps passe dans le toil ?
2. Quelles données manquent le plus souvent pour reproduire ?
3. Quels documents ne sont pas fiables ?
4. Quels correctifs d'urgence ont créé de la dette ?
5. Quelles recommandations d'IA accepteriez-vous, et sous quelles preuves ?

---

## 13. Données à demander pour une étude client de quatre semaines

- 6 à 12 mois de tickets et incidents, avec historique des assignations ;
- problèmes, post-mortems et actions associées ;
- changements, déploiements, commits et rollbacks ;
- alertes et événements d'observabilité ;
- catalogue de services et ownership ;
- documentation, runbooks et date de dernière validation ;
- verbatims support et catégories de feedback ;
- SLA, SLO et tableaux de bord fournisseur ;
- organigramme opérationnel, RACI et chaînes d'escalade ;
- rotations de staffing et ancienneté sur le périmètre ;
- temps internes de pilotage et de contrôle ;
- inventaire des accès et sous-traitants ultérieurs ;
- backlog de dette technique et historique des arbitrages.

### Livrables possibles

- cartographie des flux de travail et des pertes de contexte ;
- top des classes de récurrence ;
- mesure du coût de qualification ;
- estimation du coût client retenu ;
- score de fraîcheur documentaire ;
- cartographie des dépendances humaines ;
- analyse des handovers et temps d'attente ;
- backlog de cas d'usage RUN IA ;
- choix d'un pilote à faible risque et valeur mesurable.

---

## 14. Principes de conception à retenir

1. **Sourcer chaque affirmation de l'IA.** Une conclusion sans preuve doit être présentée comme hypothèse.
2. **Conserver l'incertitude.** Le système doit montrer contradictions et données manquantes.
3. **Mesurer l'impact utilisateur.** La santé technique ne suffit pas.
4. **Optimiser la résolution durable, pas la clôture.**
5. **Mettre à jour la connaissance comme sous-produit du travail.**
6. **Concevoir pour le multi-fournisseurs.** La donnée de contexte ne doit pas appartenir à une seule équipe.
7. **Tester la réversibilité.** Un document non exercé ne prouve pas la capacité de reprise.
8. **Traiter l'offshore comme une architecture de collaboration.** Pas seulement comme une localisation de ressources.
9. **Commencer en lecture et préparation.** L'autonomie de production vient après la confiance et l'auditabilité.
10. **Évaluer le RUN IA lui-même.** Faux positifs, recommandations rejetées, temps réellement gagné, incidents aggravés ou évités.

---

## 15. Ce que les sources ne permettent pas de conclure

- Elles ne démontrent pas qu'une TMA est en moyenne meilleure ou moins bonne qu'un RUN interne.
- Elles ne démontrent pas qu'un pays ou une région produit intrinsèquement une qualité supérieure ou inférieure.
- Elles ne donnent pas un ROI universel de l'offshore, du nearshore ou de l'IA.
- Elles ne permettent pas d'estimer la taille du marché « RUN IA » sans recherche complémentaire.
- Elles ne permettent pas de connaître la fréquence exacte de chaque douleur dans les entreprises françaises.
- Elles décrivent des tendances et mécanismes à transformer en hypothèses, puis à valider par entretiens et données opérationnelles.

---

## 16. Sources et appréciation critique

[^1]: Catchpoint, **The SRE Report 2025**, 7e édition. Données utiles sur le toil, la part du travail d'exploitation, la pression release/fiabilité, l'observabilité, le volume d'incidents et le soutien post-incident. Rapport éditeur fondé sur une enquête annuelle ; pertinent pour les pratiques de fiabilité, mais pas représentatif de toutes les organisations IT. [PDF](https://resources.catchpoint.com/hubfs/Website%20Assets%20-%20Briefs,%20EBooks,%20etc/The%20SRE%20Report%202025%20Catchpoint.pdf)

[^2]: Atlassian, **State of Incident Management Report 2024**. Enquête de plus de 500 développeurs, professionnels IT et décideurs IT aux États-Unis, tous managers ou plus, dans des organisations de 101 salariés ou plus pratiquant DevOps. Très utile pour les douleurs d'incident ; biais possible d'une enquête commanditée par un éditeur ITSM. [PDF](https://dam-cdn.atl.orangelogic.com/AssetLink/qe5386w6c841vkxka3108i43k7hisg3g/fl_keep_metadata/CSD-12265_Whitepaper_State_of_Incident_Managment_2024.pdf)

[^3]: Deloitte, **Global Outsourcing Survey 2024**. Plus de 500 dirigeants dans le monde. Source utile sur le rééquilibrage outsourcing/insourcing, les GIC, la maturité du VMO et l'IA dans les services externalisés. Périmètre plus large que la seule TMA et source issue d'un cabinet de conseil. [Page de synthèse](https://www.deloitte.com/global/en/issues/work/global-outsourcing-survey.html)

[^4]: I. Nurdiani, R. Jabangwe, D. Šmite, D. Damian, **Risk Identification and Risk Mitigation Instruments for Global Software Development: Systematic Review and Survey Results**. Revue de 86 études empiriques et enquête industrielle ; source plus ancienne mais utile pour les mécanismes durables de communication, coordination et contrôle dans le développement distribué. [PDF](https://www.diva-portal.org/smash/get/diva2:834236/FULLTEXT01.pdf)

[^5]: CIGREF / Syntec informatique, **Charte Infogérance et TMA** (2004) et **Mémento de pilotage pour des contrats d'infogérance et de TMA** (2006). Sources historiques françaises, non utilisables comme mesure actuelle de prévalence, mais pertinentes pour les invariants contractuels : périmètre, responsabilités, ressources, suivi, multi-prestataires, réversibilité et évolution technique. [Charte](https://www.cigref.fr/charte-cigref-syntec-informatique-infogerance-et-tma) — [Mémento](https://www.cigref.fr/mementos-de-pilotage-cigref-syntec-informatique)

[^6]: PagerDuty, **2024 State of Digital Operations Study**, enquête déclarée auprès de 350 dirigeants métier et techniques. Source utile comme signal directionnel sur la croissance des incidents impliquant les clients ; étude fournisseur à interpréter avec prudence. [Communiqué en français](https://www.pagerduty.com/fr/newsroom/2024-state-of-digital-operations-study/)

[^7]: Deloitte, **Global Business Services Survey 2025**. Étude menée du T3 au T4 2024, avec réponses de leaders dans plus de 30 pays et données accumulées auprès de plus de 2 000 répondants sur huit ans. Le champ GBS dépasse l'IT, mais éclaire les sujets de compétences, turnover, coûts et expansion des centres globaux. [Synthèse](https://www.deloitte.com/ie/en/services/consulting/research/global-business-services-survey.html)

[^8]: O. Krancher, J. Dibbern, **Knowledge Transfer in Software Maintenance Outsourcing: The Key Roles of Software Knowledge and Guided Learning Tasks** (2020). Étude multi-cas de cinq transferts dans une banque suisse. Très pertinente pour la transition de maintenance ; généralisation limitée par le contexte et la taille de l'échantillon. [Résumé académique](https://link.springer.com/chapter/10.1007/978-3-030-45819-5_7)

[^9]: CNIL, **Sécurité : gérer la sous-traitance**, mise à jour du 14 mars 2024. Référence normative et pratique sur les garanties du sous-traitant, les clauses, les incidents, les transferts et la chaîne de sous-traitance. [Page CNIL](https://www.cnil.fr/fr/securite-gerer-la-sous-traitance)

[^10]: M. Looi, M. Szepan, **Outsourcing in Global Software Development: Effects of Temporal Location and Methodologies**. Article référencé comme publié en 2021 et déposé sur arXiv en 2026 ; enquête de 80 clients et six entretiens. Résultats directionnels en faveur du nearshore pour les activités intensives en communication ; taille et contexte à prendre en compte. [Résumé arXiv](https://arxiv.org/abs/2602.08084)

[^11]: Hacker News, **Ask HN: What challenges are you facing offshoring development to India?** (2023). Commentaires publics individuels, non représentatifs et susceptibles de biais ; utilisés uniquement comme verbatims illustratifs de la latence, de l'alignement et du turnover. [Discussion](https://news.ycombinator.com/item?id=36119709)

### Sources complémentaires consultées

- Google Cloud DORA, **State of AI-assisted Software Development 2025** : l'IA est présentée comme un amplificateur des forces et faiblesses organisationnelles existantes, ce qui renforce l'idée qu'une automatisation du RUN doit s'appuyer sur des processus, données et contrôles solides. [Page DORA](https://dora.dev/research/2025/dora-report/)
- Numeum / KPMG, **Grand Angle ESN & ICT 2024** : contexte français sur les tensions de recrutement, la demande de profils expérimentés et l'adaptation des modèles de delivery, dont nearshore et offshore. [PDF](https://numeum.fr/wp-content/uploads/2024/10/Etude-ESN-2024.pdf)
- CNIL, **Guide de la sécurité des données personnelles 2024** : sous-traitance, maintenance, traçabilité, continuité et gestion des incidents. [PDF](https://www.cnil.fr/sites/default/files/2024-03/cnil_guide_securite_personnelle_2024.pdf)

---

## 17. Conclusion

La recherche converge vers une idée simple : les organisations ne souffrent pas uniquement d'un manque d'automatisation, mais d'un manque de **continuité opérationnelle de la connaissance**.

Le RUN interne concentre souvent la connaissance mais la laisse tribale et sous tension. La TMA peut industrialiser le service, mais ajoute une frontière client/prestataire et des incitations contractuelles. Le nearshore et l'offshore donnent accès à de la capacité et à une couverture élargie, mais rendent plus coûteux tout travail ambigu, fortement couplé ou mal documenté. Le multi-fournisseurs ajoute enfin un problème de responsabilité de bout en bout.

Dans ce contexte, une proposition « RUN IA » différenciante ne devrait pas commencer par promettre qu'un agent corrigera automatiquement la production. Elle devrait d'abord rendre le système **compréhensible, traçable et transmissible** : réunir les preuves, reconstruire le contexte, maintenir la documentation, sécuriser les handovers, identifier les récurrences et objectiver la dette.

> **Positionnement possible :** « RUN IA réduit le coût de compréhension et de coordination du RUN, puis transforme chaque incident, ticket et retour utilisateur en connaissance durable et en amélioration mesurable. »
