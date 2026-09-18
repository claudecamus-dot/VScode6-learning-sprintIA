---
title: "RUN IA — Brainstorming et cadrage"
date: "2026-09-17"
lang: fr
---

# RUN IA — Brainstorming et cadrage

## Cadrage proposé

> **RUN IA est la couche d’intelligence opérationnelle qui maintient un produit compréhensible, fiable et évolutif, quelle que soit la manière dont il a été construit.**

Ce n’est donc pas seulement de l’AIOps ou un chatbot connecté à Jira. Le sujet couvre simultanément :

1. **L’IA au service du RUN** : bugs, incidents, retours utilisateurs, documentation, dette technique.
2. **Le RUN des produits IA ou agentiques** : qualité des agents, dérives, coûts, traces, évaluations, autonomie.
3. **Le passage du BUILD au RUN** : transformer un produit livré — parfois vite, parfois sans documentation — en un système exploitable et maintenable.

---

## 1. Une proposition de valeur simple

Le RUN IA transforme des signaux dispersés en actions traçables :

> **Signal → compréhension → décision → action → validation → apprentissage**

Les signaux peuvent provenir de :

- tickets de support ;
- logs et alertes ;
- retours utilisateurs ;
- analytics produit ;
- dépôts de code ;
- pipelines CI/CD ;
- documentation existante ;
- conversations de projet ;
- traces d’agents IA ;
- incidents et post-mortems ;
- dépendances, vulnérabilités et obsolescences.

Les actions générées peuvent être :

- créer ou enrichir un ticket ;
- dédupliquer des bugs ;
- reproduire une anomalie ;
- proposer une cause racine ;
- générer des tests ;
- préparer une pull request ;
- mettre à jour un runbook ;
- produire une rétro-documentation ;
- identifier une dette technique ;
- recommander une priorité ;
- alerter un responsable ;
- répondre à un utilisateur ;
- bloquer ou surveiller un déploiement risqué.

---

# 2. Les grands domaines fonctionnels

## A. Bug et incident intelligence

L’idée est de ne plus traiter chaque bug comme un objet isolé, mais comme un dossier enrichi par toutes les preuves disponibles.

| Étape | Apport du RUN IA |
|---|---|
| Détection | Repérer une anomalie dans les logs, les retours utilisateurs ou les métriques |
| Déduplication | Regrouper les tickets décrivant probablement le même problème |
| Qualification | Identifier le périmètre, la sévérité, les utilisateurs concernés et la version touchée |
| Reproduction | Générer un scénario de reproduction et collecter les éléments manquants |
| Investigation | Corréler logs, commits, déploiements, dépendances et changements récents |
| Remédiation | Proposer un correctif, un rollback, une configuration ou un contournement |
| Validation | Générer ou exécuter des tests de non-régression |
| Capitalisation | Mettre à jour le runbook, la documentation et la base de connaissances |

### Exemples de cas d’usage

- « Ces 17 tickets correspondent-ils au même bug ? »
- « Quel changement récent est le plus probablement responsable ? »
- « Peux-tu reproduire l’erreur sur un environnement isolé ? »
- « Ce correctif est-il suffisamment couvert par des tests ? »
- « Cet incident s’est-il déjà produit sous une autre forme ? »
- « Quelles documentations doivent être mises à jour après ce correctif ? »

---

## B. User Feedback Intelligence

Les retours utilisateurs arrivent généralement sous des formes difficiles à rapprocher : verbatims, tickets, enquêtes, avis, échanges commerciaux, sessions enregistrées ou données d’usage.

Le RUN IA pourrait :

- regrouper les retours par problème réel ou besoin utilisateur ;
- distinguer bug, incompréhension, demande de fonctionnalité et problème d’adoption ;
- identifier les segments d’utilisateurs concernés ;
- mesurer la fréquence et l’impact ;
- rapprocher les verbatims des données d’usage ;
- repérer les signaux faibles avant qu’ils deviennent des incidents majeurs ;
- proposer une priorité produit ;
- générer une réponse contextualisée ;
- fermer la boucle avec les utilisateurs une fois le problème résolu.

### Une sortie intéressante

Au lieu de remonter seulement « 38 retours négatifs », le système pourrait produire :

> « Les utilisateurs administrateurs de comptes de plus de 50 personnes rencontrent une incompréhension récurrente lors de l’attribution des rôles. Le problème est apparu après la version X, provoque un abandon dans 22 % des sessions concernées et génère environ 15 % des tickets support de cette population. »

---

## C. Documentation vivante et rétro-documentation

Ici, le RUN IA ne doit pas seulement « écrire de la documentation ». Il doit reconstruire une représentation fiable du produit à partir des preuves disponibles.

### Documents potentiellement générés ou maintenus

- cartographie fonctionnelle ;
- architecture applicative ;
- cartographie des flux de données ;
- catalogue des API ;
- modèle de données ;
- responsabilités et ownership ;
- dépendances entre composants ;
- ADR — Architecture Decision Records ;
- procédures de déploiement ;
- procédures de rollback ;
- runbooks d’incident ;
- guides d’onboarding développeur ;
- matrice des environnements ;
- documentation de configuration ;
- historique des décisions ;
- inventaire des composants IA, prompts, outils et modèles.

### Principe essentiel : la documentation avec niveau de confiance

Chaque élément généré devrait indiquer :

- ses sources ;
- sa date de dernière vérification ;
- son niveau de confiance ;
- les contradictions détectées ;
- le responsable humain de sa validation ;
- les composants concernés.

Par exemple :

> « Le service Billing semble être responsable du calcul des remises — confiance 82 %. Cette conclusion repose sur six appels API, trois tests et deux références dans le code. Une documentation Confluence plus ancienne attribue toutefois cette responsabilité au service Pricing. »

Cela évite de produire une documentation élégante mais fausse.

---

## D. Tech Debt Intelligence

La dette technique est souvent gérée comme une liste subjective de sujets. Le RUN IA peut la rendre observable et reliée à ses conséquences.

### Sources possibles

- complexité du code ;
- duplication ;
- absence de tests ;
- dépendances obsolètes ;
- vulnérabilités ;
- composants sans propriétaire ;
- documentation manquante ;
- incidents récurrents ;
- temps de résolution ;
- lenteur des pipelines ;
- fréquence des rollbacks ;
- zones de code souvent modifiées ;
- incohérences architecturales ;
- coûts d’infrastructure ;
- fragilité des intégrations ;
- dépendance à une personne ou une équipe.

### Une meilleure unité de mesure

Plutôt que de mesurer uniquement la « quantité de dette », on peut estimer les **intérêts de la dette** :

- combien d’incidents elle provoque ;
- combien de temps elle ajoute à chaque évolution ;
- combien de bugs lui sont associés ;
- combien elle coûte en infrastructure ;
- combien elle ralentit l’onboarding ;
- quel risque elle fait porter à l’entreprise.

Le système pourrait ainsi produire une recommandation comme :

> « La refonte du module d’authentification paraît coûteuse, mais ce module est impliqué dans 31 % des incidents critiques, ralentit six équipes et ne possède pas de suite de tests fiable. Son coût d’inaction est probablement supérieur à celui de sa remise à niveau. »

---

# 3. Deux contextes à différencier

## Produit construit de manière standard

Les problématiques dominantes sont généralement :

- code historique difficile à comprendre ;
- documentation incomplète ;
- décisions anciennes non tracées ;
- dépendances implicites ;
- manque de tests ;
- ownership incertain ;
- architecture ayant évolué par accumulation ;
- dette technique peu objectivée.

Le RUN IA agit ici comme un **archéologue et un copilote de maintenance** :

1. cartographier ;
2. expliquer ;
3. documenter ;
4. sécuriser les changements ;
5. réduire progressivement la dette.

---

## Produit construit avec une approche agentique

Le RUN doit couvrir le code classique, mais aussi de nouveaux objets opérationnels :

- agents ;
- prompts et instructions ;
- modèles utilisés ;
- outils accessibles par les agents ;
- mémoires ;
- bases de connaissances ;
- stratégies d’orchestration ;
- permissions ;
- traces de raisonnement et d’action ;
- jeux d’évaluation ;
- niveaux d’autonomie ;
- mécanismes de validation humaine.

### Risques particuliers

- comportement non déterministe ;
- dérive de performance après changement de modèle ;
- régression provoquée par une modification de prompt ;
- erreurs d’utilisation d’outil ;
- boucles ou actions inutiles ;
- dépassements de coûts ;
- latence excessive ;
- mémoires incorrectes ou obsolètes ;
- propagation d’une information erronée ;
- difficulté à reproduire une exécution ;
- code généré rapidement mais peu maintenable ;
- absence de documentation des décisions prises pendant le build.

### Le RUN IA doit alors ajouter une couche d’AgentOps

Elle pourrait surveiller :

- le taux de réussite par type de tâche ;
- le nombre d’interventions humaines ;
- le taux d’abandon ou de boucle ;
- les erreurs d’outils ;
- le coût par résultat obtenu ;
- la latence par étape ;
- les violations de politique ;
- les écarts entre comportement attendu et observé ;
- les régressions après changement de prompt, modèle ou outil ;
- la qualité des réponses selon les segments d’utilisateurs.

---

# 4. Le passage BUILD → RUN

Un axe différenciant pourrait être de créer un **protocole de mise sous contrôle opérationnel** d’un produit.

Lorsqu’un produit arrive en RUN, la plateforme effectue un diagnostic initial.

## Le « RUN Readiness Check »

Il pourrait vérifier :

| Domaine | Questions |
|---|---|
| Architecture | Les composants et flux critiques sont-ils identifiés ? |
| Ownership | Chaque composant a-t-il un propriétaire ? |
| Observabilité | Les parcours critiques sont-ils monitorés ? |
| Tests | Existe-t-il une couverture minimale sur les fonctions critiques ? |
| Documentation | Les procédures d’exploitation et de rollback existent-elles ? |
| Sécurité | Les secrets, permissions et dépendances sont-ils maîtrisés ? |
| Dette | Les principaux risques techniques sont-ils connus ? |
| IA/Agents | Les modèles, prompts, outils et évaluations sont-ils inventoriés ? |
| Continuité | Peut-on reprendre le produit sans l’équipe qui l’a construit ? |
| Gouvernance | Les niveaux d’autonomie et de validation sont-ils explicites ? |

### Livrables générés

- score de maturité RUN ;
- cartographie du produit ;
- liste des zones inconnues ;
- backlog de sécurisation ;
- documentation minimale ;
- plan de monitoring ;
- runbooks prioritaires ;
- baseline de dette technique ;
- baseline d’évaluation des agents ;
- matrice d’ownership ;
- risques bloquants avant mise en production.

C’est particulièrement utile après un build agentique rapide, où le produit peut fonctionner sans être réellement maîtrisé.

---

# 5. Une unité commune : le « RUN Case »

Pour unifier les différents cas d’usage, chaque signal pourrait devenir un **RUN Case**.

Un RUN Case peut représenter :

- un bug ;
- un incident ;
- un retour utilisateur ;
- une anomalie d’agent ;
- un manque documentaire ;
- une dette technique ;
- un risque de déploiement ;
- une opportunité d’amélioration.

## Contenu d’un RUN Case

- type de problème ;
- résumé ;
- preuves et sources ;
- périmètre affecté ;
- utilisateurs concernés ;
- sévérité ;
- impact métier ;
- niveau de confiance ;
- cause supposée ;
- propriétaire recommandé ;
- actions proposées ;
- niveau d’autonomie autorisé ;
- tests ou validations nécessaires ;
- artefacts à mettre à jour ;
- résultat final ;
- enseignement capitalisé.

Ce modèle évite d’avoir d’un côté les tickets support, de l’autre les bugs techniques, ailleurs la dette, et encore ailleurs les retours produit.

---

# 6. Architecture conceptuelle

Le produit pourrait être structuré en six couches.

## 1. Signal Hub

Connexion aux sources :

- GitHub ou GitLab ;
- Jira, Linear ou équivalent ;
- Sentry, Datadog, Grafana ;
- Zendesk, Intercom ;
- Slack ou Teams ;
- Notion, Confluence ;
- CI/CD ;
- analytics produit ;
- bases de données ;
- traces LLM et agents.

## 2. Evidence Layer

Une couche qui conserve les preuves :

- logs ;
- traces ;
- événements ;
- commits ;
- tickets ;
- conversations ;
- versions ;
- tests ;
- documents ;
- dépendances.

L’objectif est que l’IA puisse justifier ses conclusions.

## 3. Product Knowledge Graph

Une représentation des relations entre :

- fonctionnalité ;
- utilisateur ;
- service ;
- dépôt ;
- fichier ;
- API ;
- base de données ;
- équipe ;
- incident ;
- agent ;
- prompt ;
- modèle ;
- déploiement ;
- documentation.

## 4. Agents spécialisés

Quelques agents possibles :

- **Triage Agent** : qualification et déduplication ;
- **Reproduction Agent** : création d’un scénario reproductible ;
- **Investigation Agent** : recherche de cause racine ;
- **Feedback Agent** : analyse des retours utilisateurs ;
- **Documentation Agent** : création et maintenance documentaire ;
- **Debt Agent** : détection et priorisation de la dette ;
- **Release Guardian** : analyse des risques avant et après déploiement ;
- **Agent Supervisor** : surveillance des produits agentiques.

## 5. Policy and Autonomy Engine

Cette couche décide ce que l’IA peut faire :

- en lecture seule ;
- sous forme de recommandation ;
- après approbation ;
- automatiquement dans un périmètre restreint ;
- avec rollback obligatoire ;
- jamais sans intervention humaine.

## 6. Control Tower

Une interface commune pour voir :

- la santé du produit ;
- les RUN Cases ouverts ;
- les incidents émergents ;
- les irritants utilisateurs ;
- la dette prioritaire ;
- la fraîcheur documentaire ;
- la performance des agents ;
- les actions proposées ou exécutées ;
- les validations humaines en attente.

---

# 7. Niveaux d’autonomie

Une graduation explicite est essentielle.

| Niveau | Comportement |
|---|---|
| 0 — Observation | L’IA lit, synthétise et signale |
| 1 — Recommandation | Elle propose une action argumentée |
| 2 — Préparation | Elle prépare ticket, test, réponse, documentation ou PR |
| 3 — Approbation | Elle exécute après validation humaine |
| 4 — Autonomie encadrée | Elle agit seule dans un périmètre réversible et surveillé |

Exemples :

- générer un résumé d’incident : niveau 0 ou 1 ;
- rédiger un ticket complet : niveau 2 ;
- ouvrir une pull request : niveau 2 ;
- fusionner une correction : niveau 3 ;
- redémarrer automatiquement un service connu : niveau 4, avec politique et rollback ;
- modifier les droits d’accès d’un agent : probablement niveau 3, même à maturité.

---

# 8. Les indicateurs à suivre

## Efficacité opérationnelle

- temps de qualification ;
- temps de reproduction ;
- temps moyen de résolution ;
- taux de réouverture ;
- nombre d’incidents récurrents ;
- nombre de tickets dupliqués ;
- taux de correctifs accompagnés de tests ;
- taux d’échec des changements.

## Qualité de la connaissance

- couverture documentaire ;
- fraîcheur de la documentation ;
- pourcentage de composants avec un propriétaire ;
- nombre de zones critiques non documentées ;
- taux de recommandations fondées sur des preuves suffisantes.

## Expérience utilisateur

- délai entre retour utilisateur et décision ;
- nombre de retours reliés à une action produit ;
- irritants récurrents ;
- taux de fermeture de boucle avec l’utilisateur ;
- évolution de l’usage après correction.

## Dette technique

- intérêts estimés de la dette ;
- incidents associés à la dette ;
- temps de développement perdu ;
- composants sans tests ;
- dépendances critiques obsolètes ;
- concentration du risque sur certaines zones.

## Produits agentiques

- taux de succès par tâche ;
- taux d’intervention humaine ;
- coût par tâche réussie ;
- latence ;
- erreurs d’outils ;
- régressions après changement ;
- violations de règles ;
- taux de rollback ;
- taux de décisions humaines contredisant l’agent.

## Qualité du RUN IA lui-même

- taux d’acceptation des recommandations ;
- taux de faux positifs ;
- taux d’actions annulées ;
- qualité perçue des explications ;
- proportion d’actions réellement utiles ;
- incidents causés ou aggravés par l’automatisation.

---

# 9. Un périmètre initial réaliste

Le risque serait de commencer directement par « l’agent autonome qui corrige tout ». Un premier produit pourrait plutôt combiner quatre briques.

## Brique 1 — RUN Inbox

Une boîte d’entrée unifiée regroupant :

- bugs ;
- incidents ;
- feedbacks ;
- alertes ;
- anomalies d’agents ;
- trous documentaires.

Chaque élément est résumé, classé, dédupliqué et enrichi.

## Brique 2 — Living Product Map

Une cartographie automatiquement construite à partir du code, de l’infrastructure, des tickets et de la documentation.

Elle répond à :

- qui possède quoi ?
- quel composant sert quelle fonctionnalité ?
- quelles dépendances sont critiques ?
- quels utilisateurs seraient affectés par un changement ?

## Brique 3 — Documentation Gap Detector

Le système identifie :

- les composants sans documentation ;
- les documents obsolètes ;
- les contradictions ;
- les runbooks manquants ;
- les décisions d’architecture non formalisées.

## Brique 4 — Debt and Risk Radar

Une vue priorisée des zones qui :

- génèrent le plus d’incidents ;
- ralentissent le plus les évolutions ;
- sont les moins testées ;
- sont les moins comprises ;
- présentent le plus grand risque opérationnel.

---

# 10. Trois incréments possibles

## Incrément 1 — Observer et comprendre

- connecter les sources ;
- centraliser les signaux ;
- qualifier et dédupliquer ;
- produire la cartographie ;
- identifier les manques ;
- fournir des recommandations.

Aucune action automatique sensible.

## Incrément 2 — Préparer et assister

- préparer les tickets ;
- produire les scénarios de reproduction ;
- générer des tests ;
- créer les brouillons de PR ;
- rédiger les réponses utilisateurs ;
- mettre à jour la documentation sous validation.

## Incrément 3 — Agir sous contrôle

- actions automatiques réversibles ;
- remédiations connues ;
- génération et exécution de tests ;
- mises à jour documentaires automatiques ;
- surveillance post-déploiement ;
- escalade lorsque la confiance est insuffisante.

---

# 11. Différenciation possible

Le produit sera plus distinctif s’il ne se limite pas à juxtaposer plusieurs copilotes.

Les éléments différenciants pourraient être :

### 1. Une compréhension transversale du produit

Relier le feedback utilisateur à la fonctionnalité, au code, au déploiement, à l’équipe et à la documentation.

### 2. Une approche fondée sur les preuves

Chaque recommandation est explicable et sourcée.

### 3. La documentation comme conséquence du RUN

Une résolution de bug entraîne automatiquement la mise à jour des connaissances associées.

### 4. La mesure des intérêts de la dette

La dette est priorisée selon son impact réel et non selon l’opinion la plus forte.

### 5. Un modèle commun aux produits standards et agentiques

Le système comprend aussi bien un microservice classique qu’un agent utilisant plusieurs modèles et outils.

### 6. La continuité BUILD → RUN

Le produit crée automatiquement les conditions d’exploitation au moment de la livraison.

---

# 12. Quelques formulations de positionnement

### Version plateforme

> **La plateforme de pilotage intelligent du RUN produit et technologique.**

### Version orientée résultat

> **Transformer chaque bug, retour utilisateur et incident en une amélioration durable du produit.**

### Version BUILD → RUN

> **Rendre tout produit exploitable, compréhensible et maintenable dès sa sortie du build.**

### Version agentique

> **Le système de contrôle et d’apprentissage continu des produits logiciels et des agents IA.**

### Version « système nerveux »

> **Le système nerveux du produit : il observe, comprend, agit et apprend.**

---

# 13. Idées de naming pour les sous-domaines

Sous la bannière **RUN IA**, on pourrait imaginer :

- **RUN Control** : tour de contrôle ;
- **RUN Cases** : unité de traitement ;
- **RUN Knowledge** : cartographie et documentation ;
- **RUN Feedback** : voix des utilisateurs ;
- **RUN Fix** : bugs et remédiation ;
- **RUN Debt** : dette technique ;
- **RUN Guardian** : surveillance des releases ;
- **RUN AgentOps** : exploitation des systèmes agentiques ;
- **RUN Readiness** : diagnostic de passage BUILD → RUN.

---

# 14. Les questions structurantes pour un atelier

Un atelier de cadrage peut partir d’un cas concret et répondre à huit questions :

1. **Quel signal déclenche le processus ?**
2. **Quelles sources permettent de comprendre le problème ?**
3. **Quelle décision humaine doit aujourd’hui être prise ?**
4. **Quelle partie peut être assistée ou automatisée ?**
5. **Quelles preuves sont nécessaires ?**
6. **Quel est le risque d’une mauvaise décision ?**
7. **Quels artefacts doivent être mis à jour après l’action ?**
8. **Comment le système apprend-il du résultat ?**

Il est utile d’appliquer ce canvas successivement à :

- un bug critique ;
- un retour utilisateur récurrent ;
- un composant non documenté ;
- une dette technique ancienne ;
- une anomalie d’agent ;
- un produit venant d’être livré par une équipe de build.

---

# Recommandation de point de départ

> **Une tour de contrôle BUILD-to-RUN qui crée automatiquement la cartographie du produit, centralise les signaux, qualifie les problèmes et maintient la documentation vivante.**

C’est un socle suffisamment concret pour délivrer rapidement de la valeur, tout en permettant ensuite d’ajouter la reproduction de bugs, la génération de correctifs, la gestion active de la dette et l’autonomie encadrée.
