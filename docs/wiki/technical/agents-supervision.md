---
updated: 2026-09-15
generated-by: .claude/supervision/scan_transcripts.py (superviseur d'agents, étage 1)
---

# Supervision des agents — tableau de bord d'usage

> ⚠️ **Page générée automatiquement** (hook SessionStart → `.claude/supervision/scan_transcripts.py`).
> **Ne pas éditer à la main** — toute modification serait écrasée au prochain scan.

Dernier scan : ? · **0 sessions** (transcripts) · **0** invocations de skills · **0** lancements de sous-agents.

## Skills — usage réel

| Skill | Famille | Invocations | Première | Dernière |
| --- | --- | --- | --- | --- |
| _(aucun)_ | | | |

## Sous-agents

| Sous-agent | Lancements | Premier | Dernier |
| --- | --- | --- | --- |
| _(aucun)_ | | |

## Jamais utilisés

**projet** — 6/13 jamais invoqués :

`agent-securite`, `agent-supervisor`, `deck-design-library`, `restitution-deck-design`, `revue-increment`, `veille-agentic`

**global** — 1/2 jamais invoqués :

`skill-creator`

## Skills hub-only

_S'invoquent DEPUIS le hub de supervision, en ciblant ce projet — jamais depuis ce dépôt (leur `SKILL.md` le déclare). Leur `n=0` ici est le fonctionnement nominal, pas un défaut d'usage : aucun usage local ne le corrigera, il n'y a donc rien à en conclure ni rien à désinstaller._

`audit-technique`

## Skills bibliothèque / référence

_Consommés en lisant/exécutant leurs `scripts/`, ou via un sous-agent qui les suit (ex. `ppt-designer`, qui n'a pas l'outil Skill) — le compteur d'invocations ne peut structurellement pas les voir. `n=0` n'y vaut donc PAS « mort » : ne pas désinstaller sur ce seul signal (constat superviseur #2)._

`agent-orchestrator`, `pdf-quality`, `pptx-deck`, `pptx-framed-image`, `pptx-verify`, `roadmap-keeper`, `slide-text-polish`

## TODO agents (constats automatiques)

1. **`revue-increment` jamais invoquée** malgré le rappel SessionStart à chaque session — revoir son déclencheur (l'ancrer au flux de commit ?) ou la simplifier.
2. **Skills projet sans usage** : `agent-securite`, `agent-supervisor`, `deck-design-library`, `restitution-deck-design`, `veille-agentic` — vérifier pertinence et déclencheurs.

## Diagnostic qualitatif (étage 2 — `agent-supervisor`)

_Jamais lancé — invoquer la skill `agent-supervisor` (intégrée à `revue-increment`) pour un diagnostic qualitatif (KO répétés, efficacité, interactions entre agents)._

## Seuil de qualification — la mesure

Depuis le 2026-09-15 : **1** demande(s) vue(s) hors commande slash (+ 0 slash), **0** run(s) orchestré(s) journalisé(s) sur la même fenêtre — soit **0 %** des demandes orchestrées.
_Ce chiffre ne dit pas ce qui AURAIT dû être orchestré : le hook compte, il ne juge pas. Il donne le dénominateur qui manquait pour arbitrer le seuil sur données plutôt que sur habitude._

---

_Étage O-C (croisement modèle × tâche × reprises, exploitation de `runs.jsonl`) : voir `.claude/orchestration/routing-hints.json`, régénéré à chaque session._
