# Deck ATELIER AGENTIC PRODUCT RUN — cadrage interne

Livrable : `AGENTIC-PRODUCT-RUN-atelier.pptx` (10 slides : 1 couverture + les
8 slides de la note de cadrage source, dans son ordre, **plus une slide 8
« Ce que cela change chez nos clients »** ajoutée le 2026-09-18).

Cette slide ajoutée n'invente aucune promesse : chaque ligne « aujourd'hui »
reprend une douleur exprimée en slide 3, chaque ligne « avec Agentic Product
Run » nomme une activité réelle du parcours (slide 7) ou une garantie de la
proposition de valeur (slide 6). Les formulations, elles, sont proposées.

**Ni sommaire, ni intercalaires de chapitre** (arbitrage du 2026-09-18) : le
deck suit exactement le découpage du PDF, sans slide ajoutée.

Deck **SÉPARÉ** de `docs/run-ia/AGENTIC-PRODUCT-RUN-offre-octo.pptx` (l'offre
de soutenance) : source, contenu et arbitrages différents, ne pas fusionner
les deux sans arbitrage explicite.

## Source

`Agentic Product Run (1).pdf` (v2, 2026-09-18), 8 slides numérotées. La v1
du même jour a servi au premier jet ; la v2 enrichit la slide 6 (renommée
« En pratique ») et donne enfin un contenu à la slide 7 « Reporting ».

**Slides 1, 2 et 3 reprises TEL QUEL** (texte non modifié, mise en forme
retravaillée). Les slides 4 à 8 étaient sommaires dans le PDF — leur mise en
récit a été **proposée** puis arbitrée avec l'utilisateur :

- slide 8 « Next steps » regroupe la matière libre du PDF (« Opportunités
  pour OCTO », « PITCH de l'Offre ») en une clôture à trois volets ;
- le bloc « next steps » de cette slide est une **proposition**, pas un
  contenu source : le PDF ne donne aucun texte sous ce titre.

### Décisions successives, et pourquoi

| Date | Décision | Motif |
| --- | --- | --- |
| 2026-09-18 | Reporting FUSIONNÉ dans « En pratique » | la slide 7 du PDF v1 était vide |
| 2026-09-18 | Reporting REDÉTACHÉ en slide 7 | le PDF v2 lui donne deux niveaux distincts (temps réel / mensuel, deux publics) |
| 2026-09-18 | Sommaire retiré | le deck doit suivre exactement les 8 slides de la note |
| 2026-09-18 | Slide de preuve (Whitelane) retirée du plan | idem — contenu conservé dans `contenu_deck.py`, hors plan |

## Régénérer

```bash
cd docs/run-ia/atelier-agentic-run
python generer_deck.py                # -> AGENTIC-PRODUCT-RUN-atelier.pptx
```

Vérification au rendu réel (obligatoire, python-pptx est un parseur
tolérant) :

```powershell
..\..\..\.claude\skills\pptx-verify\scripts\render-pptx.ps1 `
  -Pptx .\AGENTIC-PRODUCT-RUN-atelier.pptx -OutDir .\render
```

## Fichiers

| Fichier | Rôle |
| --- | --- |
| `contenu_deck.py` | contenu éditorial — c'est là qu'on retouche le discours |
| `generer_deck.py` | mise en page, boilerplate copié de `../generer_deck.py` |
| `pptx_deck.py` | copie de la bibliothèque du hub |
| `render/` | PNG du rendu PowerPoint réel, preuve de la vérification |

## Visuel de la slide 7 (Reporting)

Photo **CC0 via Openverse**, posée par le helper `photo()` :

- fichier : `Real-time_bus_tracking_control_room_in_Lebanon.jpg`
- auteur : UrusHyby — <https://commons.wikimedia.org/w/index.php?curid=175250226>

Le cache local vit dans `_img/`, nommé d'après la **requête** (et non d'après
le repli procédural) : une vraie photo rangée sous `mountains_3.jpg` trompait
la lecture du dossier.

## Piège SSL — diagnostiqué le 2026-09-18, à remonter au hub

La récupération de photo échouait en `CERTIFICATE_VERIFY_FAILED: certificate
has expired`, ce qui laissait croire à une panne d'Openverse. **Ce n'était pas
le cas** :

| Hôte | Verdict |
| --- | --- |
| `api.openverse.org` (recherche) | certificat valide, recherche OK |
| `upload.wikimedia.org` (téléchargement) | certificat valide jusqu'au 9 nov. 2026 |
| magasin de certificats **par défaut de Python** sur ce poste | **porte une autorité racine expirée** |

Le même hôte se vérifie sans erreur avec le bundle `certifi`. Le correctif est
donc local à ce générateur — `os.environ.setdefault("SSL_CERT_FILE",
certifi.where())` dans `photo()` — et **le script du kit partagé
(`.claude/skills/pptx-framed-image`) n'est pas modifié : il n'est pas fautif.**

À remonter au hub : tout projet de la flotte qui télécharge une image depuis ce
poste rencontrera le même faux diagnostic.

## Piège reproduit ici (leçon déjà payée sur le deck offre)

Le contrôle `D.verifier_debordements_texte` du hub a un défaut par défaut
(`cpi_pessimiste=10.7`) calibré sur une police plus large qu'Outfit — il
faut l'appeler avec `cpi_pessimiste=CPI_LAYOUT` (14.0), sinon il produit des
faux positifs en cascade sur toutes les slides à texte dense. Déjà
documenté dans `../generer_deck.py`, reproduit ici pour la même raison.

## Ce qui reste à trancher

- Le contenu proposé pour les slides 4, 5, 6, 7 et 8 (tout sauf 1-3) n'est
  pas figé — c'est une proposition à valider ou amender.
- Aucune donnée chiffrée n'est inventée : la slide 4 cite ses sources, la
  slide 7 (reporting) ne simule aucun tableau de bord.
