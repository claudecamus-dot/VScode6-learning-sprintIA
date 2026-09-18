# Deck AGENTIC PRODUCT RUN — offre de service OCTO

Livrable : `AGENTIC-PRODUCT-RUN-offre-octo.pptx` (17 slides : 1 couverture,
1 sommaire, 4 intercalaires de chapitre, 11 contenus).

Le nom de l'offre est **AGENTIC PRODUCT RUN** (ex-« RUN IA », puis « TMIA ») :
en capitales sur la couverture, en casse normale dans le corps du texte.
Cible : soutenance avec un commercial, pour arbitrer la pertinence de l'offre
et sa vendabilité. Angle retenu : **offre de service** (pas plateforme),
**client générique grand compte** (DSI/CTO avec un patrimoine en RUN).

## Régénérer

```bash
cd docs/run-ia
python generer_deck.py                 # -> AGENTIC-PRODUCT-RUN-offre-octo.pptx, 4 contrôles géométriques
```

Vérification au rendu réel (obligatoire, python-pptx est un parseur tolérant) :

```powershell
..\..\.claude\skills\pptx-verify\scripts\render-pptx.ps1 `
  -Pptx .\AGENTIC-PRODUCT-RUN-offre-octo.pptx -OutDir .\render
```

## Fichiers

| Fichier | Rôle |
| --- | --- |
| `contenu_deck.py` | contenu éditorial seul — c'est là qu'on retouche le discours |
| `generer_deck.py` | mise en page, calibration typographique, garde-fous |
| `pptx_deck.py` | copie de la bibliothèque du hub (`.claude/skills/pptx-deck`) |
| `render/` | PNG du rendu PowerPoint réel, preuve de la dernière vérification |

## Structure — 4 chapitres

Un sommaire ouvre le deck ; ses quatre cartes sont générées depuis le MÊME
tuple `CHAPITRES` que les intercalaires, donc les deux ne peuvent pas diverger.

| # | Chapitre | Slides |
| --- | --- | --- |
| 1 | Contexte et enjeux clients | pourquoi c'est possible maintenant · le RUN où la valeur se perd (5 constats) |
| 2 | Enjeux et opportunités OCTO | la preuve · l'apport produit · le terrain agentique |
| 3 | L'offre | la promesse · où l'offre se branche (TMA/MCO) · le parcours en 3 temps · le RUN Readiness Check |
| 4 | Next steps | comment ça se vend · ce que le client achète |

**Trame arbitrée le 2026-09-18**, après une table ronde `atelier-deck`. Elle
remplace les 4 chapitres précédents (Le constat / L'offre / Ce qui la rend
défendable / Conclusion).

Le principe est une **structure en miroir** : le temps 1 est le côté client
(son contexte ET ses douleurs, réunis — ce sont les mêmes faits vus sous deux
angles), le temps 2 est le nôtre. L'ancien chapitre « ce qui la rend
défendable » ne disparaît donc pas : il devient le temps OCTO, et c'est là que
`slide_preuve` trouve son toit — la table ronde avait identifié cette slide
comme la seule qui réponde à l'objection n°1 d'un DSI face à une offre IA
(« et si votre IA raconte n'importe quoi ? »).

Le nombre de chapitres reste à **4**, et c'est une contrainte dure, pas un
hasard : `SCENES` (`generer_deck.py`) mappe exactement 4 numéros de chapitre
vers leur requête photo, et `SCENES[num]` n'est pas gardé — un 5ᵉ chapitre fait
planter le générateur par `KeyError` tant qu'une scène neuve n'y est pas
ajoutée. Le repli procédural hors ligne ne connaît par ailleurs que 6 scènes au
total.

Le chapitre « ce qui la rend défendable » était déjà passé de 5 à 3 slides le
2026-09-17 : `slide_trajectoire` a fusionné dans `slide_modules` (les incréments
1/2/3 redisaient la progression des modules M1/M2/M3, niveau d'autonomie
compris), et « comment ça se vend » a rejoint la conclusion, dont elle est le
pendant côté OCTO.

### Points soulevés en salle et NON traités par ce changement

La table ronde du 2026-09-18 a relevé quatre écarts qui survivent à la nouvelle
trame — ils restent ouverts, aucun n'a été arbitré :

1. **`slide_agentique` revendique une exclusivité non étayée** — son titre dit
   « Le terrain où nous sommes seuls ». Aucune source du corpus ne soutient une
   affirmation d'exclusivité concurrentielle.
2. **La ligne « aucun chiffrage » est déjà franchie par les durées** :
   `slide_modules` affiche « 2 à 4 semaines », « 3 à 6 mois », « 12 à 24 mois ».
3. **Chiffres non citables** de `recherche_douleurs_RUN_TMA_offshore.md` : les
   verbatims Hacker News (que le document qualifie lui-même d'anecdotiques) et
   le « 83 % / 25 % » sur l'IA dans l'outsourcing (périmètre trop large). Les
   quatre chiffres solides se citent avec leur limite accolée.
4. **Trous commerciaux** qu'aucune trame ne comble : pas de référence client,
   aucun livrable montré, rien pour répondre à « ça me coûte quoi ».

`slide_decisions` (« Ce que je vous demande de trancher ») a été retirée du plan
le 2026-09-17 sur demande. La fonction et son contenu restent définis : la
rebrancher dans `plan` suffit à la faire revenir.

Les intercalaires utilisent le **layout natif « 50 - Chapitre [1] »**, repris de
**VSCode3** (`docs/cadrage-ppt/generate_deck.py::slide_chapitre`) qui tient
l'implémentation de référence de la flotte sur ce template — le nôtre est le
même fichier, md5 identique. La variante de **VSCode4**
(`scripts/generate_deck_ohc.py::slide_chapitre`) est à lire quand le layout
cible n'est pas le 50 : elle repositionne un layout 51 pour imiter la géométrie
mesurée de VSCode3.

Deux pièges que ces deux projets avaient déjà payés, et qu'on avait reproduits
avant d'aller les lire :

- **Le cadre photo teardrop doit être rempli.** Laissé vide, le texte gabarit
  « ici mettre une Photo » s'imprime en rouge sur la slide. Il se remplit via
  `pptx-framed-image` (photo Openverse CC0, repli procédural hors ligne), et le
  repli s'écrit sous un nom **distinct** de la vraie photo — sinon
  `os.path.exists` passe à True pour de bon et aucun build ne retente le réseau.
- **Le numéro de chapitre a besoin de marges à zéro.** La puce héritée pose
  `marL = 0.5 in` dans un encart de 0.55 in : le chiffre part à la ligne, hors
  cadre. Il faut 17 pt, marges nulles, `D.sans_puce`, ancrage MIDDLE, centré.

Et la leçon de VSCode3 sur les requêtes photo, vérifiée ici aussi : *une requête
mot-clé n'a aucun jugement*. « turquoise water » a rendu une carte postale de
Santorin pour le chapitre 3 — remplacé par « steel bridge structure » après
lecture du rendu. Chaque photo se valide à l'œil.

## Source

`RUN_IA_brainstorm.md` (2026-09-17), 14 sections. Le deck en retient : le
constat (§2), le passage BUILD→RUN et le Readiness Check (§4), les niveaux
d'autonomie (§7), les trois incréments (§10) et la différenciation (§11).
Sont volontairement écartés du deck : l'architecture en six couches (§6), le
RUN Case (§5) et le naming des sous-domaines (§13) — ils appartiennent à un
récit *produit*, pas à une offre de service.

## Ce que le deck n'affirme pas

**Aucun prix, aucun chiffrage, aucune modalité contractuelle** (arbitrage du
2026-09-17) : la soutenance porte sur la pertinence de l'offre, pas sur son
tarif. Les durées restent des ordres de grandeur. Aucune référence client
n'est citée — le deck la pose comme un manque à combler.

## Leçons figées dans le générateur

1. **Calibration typographique mesurée, pas héritée.** La valeur par défaut de
   `estimer_lignes` (10.7 car./pouce) est calibrée sur une police plus large
   qu'Outfit, où un rendu réel donne ~14.8. La garder gonflait chaque carte de
   ~40 % et produisait des panneaux aux trois quarts vides. `CPI_LAYOUT = 14.0`.
2. **Aucune hauteur négative.** Un `min(souhaité, reste)` non borné a produit
   une forme de hauteur `-0.14` que python-pptx a acceptée et que PowerPoint a
   refusé d'ouvrir (HRESULT 0x80070570). `reste()` lève désormais.
3. **`add_card_header` consomme 0.545 in**, pas 0.32 : budget faux = dernière
   puce hors de sa carte, sur quatre slides à la fois. Constante `H_HEADER`.
4. **Pas de liste uniforme**, et commun aux colonnes sœurs : un pas calculé
   item par item casse le rythme dès qu'une estimation se trompe d'une ligne.
5. **Espace insécable devant `? : ; !` et `%`** (`typo_fr`) : typographie
   française correcte, et plus de « ? » orphelin sur sa propre ligne.
6. **Varier les formes, pas seulement les contenus.** Au 2026-09-17, 8 slides
   sur 18 étaient des cartes en colonnes. Trois ont changé de forme en puisant
   dans `deck-design-library` : le parcours en 3 temps en fiches-étapes à chip
   chevauchant + rail (catalogue-restitution #10), l'apport produit en boucle
   de cercles reliés par chevrons avec rail de retour
   (catalogue-transformation-commerciale #4), les produits agentiques en
   blueprint de 3 bandes de pastilles (catalogue-restitution #8).
7. **Le bandeau de clôture est redessiné ici, pas pris au helper.**
   `D.add_quote_banner` pose sa boîte de texte à +0,20 in alors que son
   guillemet décoratif de 24 pt occupe jusqu'à ~0,54 in : la première ligne
   d'une phrase longue passe SOUS le guillemet, sur toutes les slides à la
   fois. `bandeau()` le redessine avec un retrait symétrique de 0,62 in. Le
   helper du hub n'est pas modifié depuis ici (règle : corriger au hub) — le
   défaut est tracé dans `.claude/supervision/diagnostic.json`, cible
   `hub:pptx-deck/add_quote_banner`. Ni `verifier_geometrie` ni
   `verifier_debordements_texte` ne peuvent l'attraper : c'est une collision
   entre deux formes, cas que `pptx-deck` documente comme non couvert.
8. **Deux pièges des helpers, trouvés au rendu.** `add_chip(outline=True)`
   prend `color` pour la bordure ET le texte : lui passer du blanc donne des
   pastilles vides. `melanger_blanc(c, frac)` prend la part de BLANC ajoutée :
   `0.14` laisse la couleur quasi pure, il faut `0.86` pour une teinte de fond.
9. **Un chevron n'a pas la largeur de son cadre.** L'encoche OOXML vaut
   `adj × plus petit côté` : à la valeur par défaut (0.5) elle mange 0,25 in de
   CHAQUE côté d'un chevron haut de 0,50 in — sur 1,18 in de large il ne reste
   que 0,68 in utiles. Un libellé posé dans une boîte flottante centrée sur le
   cadre extérieur chevauchait donc les biseaux. Le texte vit maintenant DANS la
   forme (un seul objet dans PowerPoint), avec `adj = 0.20`, des marges égales à
   l'encoche et une taille commune calculée sur la largeur utile réelle.
