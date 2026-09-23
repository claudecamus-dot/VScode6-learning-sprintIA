---
updated: 2026-09-23
generated-by: .claude/supervision/scan_transcripts.py (superviseur d'agents, étage 1)
---

# Supervision des agents — tableau de bord d'usage

> ⚠️ **Page générée automatiquement** (hook SessionStart → `.claude/supervision/scan_transcripts.py`).
> **Ne pas éditer à la main** — toute modification serait écrasée au prochain scan.

Dernier scan : 2026-09-23T20:59:17+02:00 · **3 sessions** (transcripts) · **8** invocations de skills · **3** lancements de sous-agents.

## Skills — usage réel

| Skill | Famille | Invocations | Première | Dernière |
| --- | --- | --- | --- | --- |
| `agent-orchestrator` | projet | 3 | 2026-09-15 | 2026-09-18 |
| `bmad-review` | BMAD | 3 | 2026-09-18 | 2026-09-18 |
| `bmad-party-mode` | BMAD | 1 | 2026-09-18 | 2026-09-18 |
| `deck-design-library` | projet | 1 | 2026-09-18 | 2026-09-18 |

## Sous-agents

| Sous-agent | Lancements | Premier | Dernier |
| --- | --- | --- | --- |
| `bmad-revue` | 3 | 2026-09-18 | 2026-09-18 |

## Jamais utilisés

**projet** — 5/13 jamais invoqués :

`agent-securite`, `agent-supervisor`, `restitution-deck-design`, `revue-increment`, `veille-agentic`

**BMAD** — 27/29 jamais invoqués :

<details><summary>Voir la liste</summary>

`bmad-advanced-elicitation`, `bmad-agent-analyst`, `bmad-agent-architect`, `bmad-agent-dev`, `bmad-agent-pm`, `bmad-agent-ux-designer`, `bmad-architecture`, `bmad-brainstorming`, `bmad-build`, `bmad-build-auto`, `bmad-code-review`, `bmad-correct-course`, `bmad-create-epics-and-stories`, `bmad-customize`, `bmad-deep-recon`, `bmad-forge-idea`, `bmad-help`, `bmad-prd`, `bmad-prfaq`, `bmad-product-brief`, `bmad-project-context`, `bmad-qa-generate-e2e-tests`, `bmad-retrospective`, `bmad-spec`, `bmad-sprint-planning`, `bmad-ux`, `bmad-walkthrough`

</details>

**global** — 2/3 jamais invoqués :

`skill-creator`, `synced`

## Skills hub-only

_S'invoquent DEPUIS le hub de supervision, en ciblant ce projet — jamais depuis ce dépôt (leur `SKILL.md` le déclare). Leur `n=0` ici est le fonctionnement nominal, pas un défaut d'usage : aucun usage local ne le corrigera, il n'y a donc rien à en conclure ni rien à désinstaller._

`audit-technique`

## Skills bibliothèque / référence

_Consommés en lisant/exécutant leurs `scripts/`, ou via un sous-agent qui les suit (ex. `ppt-designer`, qui n'a pas l'outil Skill) — le compteur d'invocations ne peut structurellement pas les voir. `n=0` n'y vaut donc PAS « mort » : ne pas désinstaller sur ce seul signal (constat superviseur #2)._

`pdf-quality`, `pptx-deck`, `pptx-framed-image`, `pptx-verify`, `roadmap-keeper`, `slide-text-polish`

## TODO agents (constats automatiques)

1. **Élaguer les skills BMAD** : 27/29 jamais invoqués — confirmer l'utilité des non-utilisés.
2. **`revue-increment` jamais invoquée** malgré le rappel SessionStart à chaque session — revoir son déclencheur (l'ancrer au flux de commit ?) ou la simplifier.
3. **Skills projet sans usage** : `agent-securite`, `agent-supervisor`, `restitution-deck-design`, `veille-agentic` — vérifier pertinence et déclencheurs.

## Arbitrages enregistrés

_Constats clos par décision humaine (`.claude/supervision/arbitrages.json`) — l'usage réel reste mesuré ci-dessus._

- **`hub:pptx-deck/verifier_geometrie`** (2026-09-18) : ACCEPTE + APPLIQUE (commit 3667ca5 hub, garde propagee a VSCode2 app/services/ commit fe77645, propagation au kit de skill des 7 autres depots en cours) : verifier_geometrie() teste desormais w<=0 or h<=0 en plus des bords. 5 tests adversariaux (tests/test_pptx_deck_geometrie.py au hub), rouge confirme avant correctif. Arbitrage ecrit cote hub (arbitrages.json), duplique ici car ce depot lit son PROPRE arbitrages.json pour masquer ses findings locaux.
- **`hub:pptx-deck/add_card_header`** (2026-09-18) : ACCEPTE + APPLIQUE (commit 69b01d0 hub, source + export) : constante H_CARD_HEADER=0.545 nommee, calcul inchange. Test adversarial verifiant le comportement reel, pas seulement la valeur.
- **`hub:pptx-deck/add_chip`** (2026-09-18) : ACCEPTE + APPLIQUE (commit c3f4eb8 hub, source + export) : text_color=None comme sentinelle, un appelant qui le passe explicitement l'obtient enfin en mode outline. Retro-compatibilite verifiee sur l'appelant reel de CE depot (docs/run-ia/generer_deck.py:905, appelle sans text_color).
- **`hub:pptx-deck/add_quote_banner`** (2026-09-18) : ACCEPTE + APPLIQUE (commit fb098f3 hub, source + export) : nouveau parametre retrait=0.62 (au lieu du 0.20 fige), suivant la proposition du finding. shapes_overlap(bbox1, bbox2) ecrite en meme temps : comble l'angle mort commun a ce finding et a composant-chevron (aucun filtre existant ne voit une collision entre deux formes). 6 tests, retro-compatibilite verifiee flotte-wide.
- **`hub:deck-design-library/composant-chevron`** (2026-09-18) : ACCEPTE + APPLIQUE PARTIELLEMENT (commit fb098f3 hub) : la formule adj x min(largeur, hauteur) et le pattern de retrait symetrique (meme logique que add_quote_banner) sont documentes dans catalogue-transformation-commerciale.md, avec shapes_overlap() cite comme outil de verification. Le defaut lui-meme est cote APPELANT (VScode6/docs/run-ia/*/generer_deck.py, plusieurs usages reels de chevron) -- documentation plutot que code, le hub ne peut pas corriger un placement de texte qu'il ne pose pas lui-meme.
- **`hub:pptx-deck/add_quote_banner`** (2026-09-21) : REFUSE (deja fait, constat) : le parametre retrait=0.62 est deja implemente et utilise dans add_text_runs (l + retrait, w - 2*retrait) avec docstring datee du 2026-09-18 documentant le finding.
- **`hub:pptx-deck/verifier_geometrie`** (2026-09-21) : REFUSE (deja fait, constat) : le test 'if w <= 0 or h <= 0' est present lignes 874-882, avant le test de bornes, avec message explicite.
- **`hub:pptx-deck/add_chip`** (2026-09-21) : REFUSE (deja fait, constat) : text_color=None par defaut (sentinelle), et 'txt = text_color or color' en mode outline (ligne 579), 'txt = text_color or "#ffffff"' en mode plein (ligne 582), avec docstring datee du 2026-09-18 expliquant pourquoi None (pas '#ffffff') etait necessaire.
- **`hub:pptx-deck/verifier_geometrie`** (2026-09-21) : REFUSE (deja fait, constat) : le test 'if w <= 0 or h <= 0' est present lignes 874-882 de verifier_geometrie, avant le test de bornes, avec message explicite ; l'arbitrage precedent portait un titre reformule par erreur et n'a pas ferme ce constat.
- **`hub:pptx-deck/add_chip`** (2026-09-21) : REFUSE (deja fait, constat) : text_color=None par defaut (sentinelle), et 'txt = text_color or color' en mode outline (ligne 579), 'txt = text_color or #ffffff' en mode plein (ligne 582), avec docstring datee du 2026-09-18 expliquant pourquoi None (pas #ffffff) etait necessaire ; l'arbitrage precedent portait un titre sans les backticks et n'a pas ferme ce constat.
- **`hub:deck-design-library/template-octo.md`** (2026-09-22) : ACCEPTE + APPLIQUE (cote hub) : deck-design-library/references/template-octo.md complete avec le layout 50-Chapitre (5), un paragraphe 5bis documentant les 2 pieges (numero 17pt/marges zero/sans-puce/MIDDLE, cadre teardrop a remplir) et le renvoi nominatif aux 2 implementations de reference (VSCode3 generate_deck.py::slide_chapitre, VSCode4 generate_deck_ohc.py::slide_chapitre).
- **`hub:pptx-deck/estimer_lignes`** (2026-09-22) : ACCEPTE + APPLIQUE (cote hub, defauts non changes comme recommande) : deck-design-library/references/template-octo.md porte desormais un 4bis 'Calibration typographique mesuree' (Outfit ~14.8 car/pouce a 10.5pt, cpi_ref/cpi_pessimiste=14.0 sur ce gabarit precis). pptx-deck/SKILL.md renvoie explicitement a cette section et rappelle que ces calibrations sont des defauts a re-mesurer, pas des constantes universelles.

## Diagnostic qualitatif (étage 2 — `agent-supervisor`)

_Diagnostic à jour — rien à signaler, tous les constats précédents ont été arbitrés._

_7 constat(s) de ce diagnostic écarté(s) par un arbitrage — pour en rouvrir un, demander au superviseur un `re_challenge` avec des données nouvelles :_

- ~~Les slides de chapitre de reference de la flotte sont chez VSCode3 et VSCode4, et la bibliotheque de design ne le dit pas~~ (`hub:deck-design-library/template-octo.md`)
- ~~add_quote_banner fait passer la premiere ligne du texte SOUS son guillemet decoratif~~ (`hub:pptx-deck/add_quote_banner`)
- ~~Aucun des quatre filets ne detecte une forme de hauteur ou largeur NEGATIVE, que PowerPoint refuse d'ouvrir~~ (`hub:pptx-deck/verifier_geometrie`)
- ~~La calibration par defaut d'estimer_lignes est ~30 % trop pessimiste pour Outfit, la police du template OCTO de la flotte~~ (`hub:pptx-deck/estimer_lignes`)
- ~~add_card_header consomme 0.545in sans que sa hauteur soit documentee, ce qui fait deborder la derniere puce des cartes a en-tete~~ (`hub:pptx-deck/add_card_header`)
- ~~add_chip(outline=True) ignore silencieusement text_color et rend des pastilles vides si `color` est clair~~ (`hub:pptx-deck/add_chip`)
- ~~L'encoche d'un chevron vaut adj x le PLUS PETIT COTE : le catalogue ne le dit pas, et un libelle centre sur le cadre chevauche les biseaux~~ (`hub:deck-design-library/composant-chevron`)

## Seuil de qualification — la mesure

Depuis le 2026-09-15 : **48** demande(s) vue(s) hors commande slash (+ 7 slash), **0** run(s) orchestré(s) journalisé(s) sur la même fenêtre — soit **0 %** des demandes orchestrées.
_Ce chiffre ne dit pas ce qui AURAIT dû être orchestré : le hook compte, il ne juge pas. Il donne le dénominateur qui manquait pour arbitrer le seuil sur données plutôt que sur habitude._

---

_Étage O-C (croisement modèle × tâche × reprises, exploitation de `runs.jsonl`) : voir `.claude/orchestration/routing-hints.json`, régénéré à chaque session._
