---
updated: 2026-09-18
generated-by: .claude/supervision/scan_transcripts.py (superviseur d'agents, étage 1)
---

# Supervision des agents — tableau de bord d'usage

> ⚠️ **Page générée automatiquement** (hook SessionStart → `.claude/supervision/scan_transcripts.py`).
> **Ne pas éditer à la main** — toute modification serait écrasée au prochain scan.

Dernier scan : 2026-09-18T16:06:29+02:00 · **3 sessions** (transcripts) · **8** invocations de skills · **3** lancements de sous-agents.

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

## Diagnostic qualitatif (étage 2 — `agent-supervisor`)

_Diagnostic à jour._

1. **Aucun des quatre filets ne detecte une forme de hauteur ou largeur NEGATIVE, que PowerPoint refuse d'ouvrir** — Ajouter au module un controle de validite des dimensions, en amont des quatre autres : toute forme dont width <= 0 ou height <= 0 est un fichier invalide, pas un defaut de mise en page. · **Proposition** : Dans verifier_geometrie, avant le test de bornes : `if shp.width <= 0 or shp.height <= 0: problemes.append(f"slide {num}: '{shp.name}' dimension non positive (w={w:.2f} h={h:.2f}) — PowerPoint refusera d'ouvrir le fichier")`. Zero faux positif possible (une dimension nulle ou negative n'a aucun usage legitime) et cela transforme une bisection manuelle en un message immediat.
2. **Les slides de chapitre de reference de la flotte sont chez VSCode3 et VSCode4, et la bibliotheque de design ne le dit pas** — Inscrire VSCode3 (docs/cadrage-ppt/generate_deck.py::slide_chapitre) comme implementation de reference des intercalaires de chapitre sur ce template, et VSCode4 (scripts/generate_deck_ohc.py::slide_chapitre) comme la variante a lire quand le layout cible n'est pas le 50. · **Proposition** : Ajouter au canon du hub, dans deck-design-library/references/template-octo.md : (1) au §5, une ligne « Intercalaire de chapitre | 2 | 50 - Chapitre [1] | idx0 titre (+ sous-titre en 2e paragraphe) - idx1 numero ; cadre photo teardrop OBLIGATOIRE a remplir » ; (2) un §5bis « Deux pieges du layout Chapitre » portant le numero a 17pt/marges zero/sans-puce/ancrage MIDDLE et le remplissage du cadre teardrop via pptx-framed-image, avec renvoi nominatif aux deux implementations de reference. Puis resynchroniser l'export vers les projets.
3. **add_quote_banner fait passer la premiere ligne du texte SOUS son guillemet decoratif** — Decaler la boite de texte au-dela du guillemet, avec un retrait symetrique pour que le bloc centre reste centre : x = l + retrait, largeur = w - 2*retrait, retrait >= 0.60in a 24pt. · **Proposition** : Dans add_quote_banner, remplacer `add_text_runs(slide, l + 0.20, t, w - 0.40, h, ...)` par un retrait parametrable `retrait=0.62` (proportionnel a la taille du guillemet si celle-ci devient un argument) : `add_text_runs(slide, l + retrait, t, w - 2 * retrait, h, ...)`. Ajouter au test du module un cas a phrase longue qui remplit la premiere ligne, et verifier que le debut du texte commence apres le guillemet.
4. **La calibration par defaut d'estimer_lignes est ~30 % trop pessimiste pour Outfit, la police du template OCTO de la flotte** — Ne pas changer les defauts (ils servent d'autres gabarits), mais documenter dans la fiche du template la calibration MESUREE pour Outfit, et rappeler dans la skill que ces deux valeurs se re-mesurent sur un rendu reel avant d'etre utilisees sur un nouveau gabarit. · **Proposition** : Ajouter a deck-design-library/references/template-octo.md un paragraphe « Calibration typographique mesuree » : Outfit ~14.8 car./pouce a 10.5pt, hauteur de ligne ~0.19in a interligne 1.1 ; passer cpi_ref=14.0 a estimer_lignes et cpi_pessimiste=14.0 a verifier_debordements_texte sur ce gabarit. Et dans SKILL.md de pptx-deck, une ligne : « ces calibrations sont des DEFAUTS, pas des constantes universelles — les re-mesurer sur un rendu reel du gabarit cible ».
5. **add_card_header consomme 0.545in sans que sa hauteur soit documentee, ce qui fait deborder la derniere puce des cartes a en-tete** — Exposer la hauteur consommee comme une constante du module, pour que l'appelant dimensionne sa carte sans la deviner. · **Proposition** : Dans pptx_deck.py : `H_CARD_HEADER = 0.545  # 0.36 (libelle) + 0.045 (filet) + 0.14 (respiration)`, utilisee par add_card_header et citee dans sa docstring et dans SKILL.md.

## Seuil de qualification — la mesure

Depuis le 2026-09-15 : **47** demande(s) vue(s) hors commande slash (+ 7 slash), **0** run(s) orchestré(s) journalisé(s) sur la même fenêtre — soit **0 %** des demandes orchestrées.
_Ce chiffre ne dit pas ce qui AURAIT dû être orchestré : le hook compte, il ne juge pas. Il donne le dénominateur qui manquait pour arbitrer le seuil sur données plutôt que sur habitude._

---

_Étage O-C (croisement modèle × tâche × reprises, exploitation de `runs.jsonl`) : voir `.claude/orchestration/routing-hints.json`, régénéré à chaque session._
