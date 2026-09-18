# -*- coding: utf-8 -*-
"""Contenu éditorial du deck « Agentic Product Run — atelier ».

Source : Agentic Product Run.pdf (2026-09-18), 8 slides numérotées dans le
PDF source. Slides 1, 2 et 3 sont REPRISES TEL QUEL (texte non modifié, mise
en forme seule retravaillée). Les slides 4 à 8 étaient sommaires ou vides
dans le PDF (parfois un seul titre) : leur contenu est PROPOSÉ ici — arbitré
avec l'utilisateur le 2026-09-18 sur trois points (fusion du reporting dans
la slide 7, fusion opportunités/pitch/next steps en une slide 8, ajout d'une
slide 4 de preuve sourcée) — à valider au rendu, pas encore committé comme
définitif.
"""

COUVERTURE = {
    "titre": "AGENTIC PRODUCT RUN",
    "sous_titre": "Atelier de cadrage — du Build au Run augmenté",
    "mention": "OCTO Technology",
    "date": "Septembre 2026",
}

# Pas de sommaire ni d'intercalaires (retires le 2026-09-18) : le deck suit
# EXACTEMENT les 8 slides de la note de cadrage, couverture mise a part.

# --- S1 : contexte (VERBATIM PDF) ---
# TEXTE ET FORME REPRIS INTEGRALEMENT de la relecture JL du 2026-09-18
# (« OK forme et fond ») : les deux phrases d'introduction passent en PUCES,
# il n'y a plus de sous-titre, et le bandeau s'ouvre par un chevron.
CONTEXTE = {
    "titre": "Contexte",
    "claim": None,
    "intro": [
        "L'IA bouscule le découpage entre Build et Run, en particulier avec la "
        "création d'Agentic Software Factories.",
        "Le Run n'est pas encore pleinement entré dans les réflexions chez OCTO, "
        "naturellement concentrées sur le Build.",
    ],
    "verbatims": [
        # Negation retablie (2026-09-18) : « on n'a pas », pas « on a pas ».
        ("Reine", "Agentic PM", "On n'a pas d'expérience sur le Run !"),
        # coquille corrigee a la relecture : « reflechit » -> « reflechi »
        ("Clarisse", "Agentic Dev", "On n'a pas réfléchi au Run"),
        ("Maxime", "Agentic BizDev",
         "Le Run avec l'IA est une question qui revient souvent avec les clients"),
    ],
    "banner": "Les appels d'offres MCO Agentique arrivent.",
}

# --- S2 : enjeux pour OCTO — TEXTE ET FORME REPRIS de la relecture JL :
# retour a la LISTE A PUCES (les cartes 2x2 proposees sont abandonnees ici),
# reformulations sur les items 1 et 2, bandeau « Découvrez… ».
ENJEUX_OCTO = {
    "titre": "Enjeux pour OCTO",
    "claim": "Quatre raisons de s'y positionner maintenant.",
    "items": [
        "Opportunité de développer du Biz sur un segment absent pour OCTO",
        "Opportunité d'entrer chez des clients pour (et éventuellement ensuite "
        "vendre du Build)",
        "Conserver une position durablement chez un client",
        "Protéger notre savoir-faire en sortie de projet produit par une ASF "
        "(tout est dans le repo)",
    ],
    "banner": "Découvrez Notre offre Agentic Product Run",
}

# --- S3 : offre Agentic Product Run — douleurs (VERBATIM PDF) ---
OFFRE_DOULEURS = {
    "titre": "Offre Agentic Product Run",
    "claim": "Les douleurs du Run telles que vous nous les avez exprimées.",
    "items": [
        "Valeur du forfait TMA difficile à démontrer",
        "Prestataire exécutant, jamais force de proposition",
        "Rotation des équipes et perte de connaissance",
        # Raccourci a la relecture du 2026-09-18 : la parenthese
        # « (insuffisance des indicateurs de SLA) » est retiree.
        "Indicateurs conformes mais service dégradé",
        "Accumulation de dette technique et baisse de qualité",
        "Manque de visibilité sur l'état réel des applications",
        "Réversibilité théorique et dépendance de fait",
    ],
}

# --- HORS PLAN depuis le 2026-09-18 : slide de preuve sourcée (étude
# Whitelane), retirée sur demande pour que le deck suive exactement les
# 8 slides du PDF. Le contenu reste défini : la rebrancher dans `plan`
# (generer_deck.py) suffit à la faire revenir.
PREUVE_RECHERCHE = {
    "titre": "Ce que confirme la recherche",
    "claim": "Six points documentés par une étude indépendante recoupent "
             "exactement les douleurs exprimées en slide 3.",
    "items": [
        ("Rapport qualité/prix",
         "32 % des clients français jugent que les prestataires n'apportent pas "
         "assez de valeur pour leur prix ; 26 % prévoient de réduire leurs "
         "dépenses externes sous deux ans."),
        ("Un prestataire qui exécute sans challenger",
         "30 % en France ; au Benelux, 37 % ne challengent pas assez et 26 % "
         "n'agissent pas en partenaire."),
        ("Ressources inexpérimentées, connaissance qui s'évapore",
         "27 % en France ; une étude sur 139 professionnels de l'infogérance "
         "relie le turnover à la dégradation de la qualité de service."),
        ("L'effet pastèque : SLA verts, utilisateurs rouges",
         "Tickets clôturés dans les délais, mais une équipe mesurée au volume "
         "de tickets traite les faciles, pas les critiques."),
        ("Dette et obsolescence sous le forfait",
         "Le Cigref cite Gartner : 14 à 15 % du budget IT devrait être "
         "sanctuarisé pour la dette — la maintenance préventive est la plus "
         "difficile à défendre dans un forfait."),
        ("Un périmètre flou",
         "Confusion entre « roadmap évolutive » et « patchs correctifs » : la "
         "TMA mal cadrée génère dépendance, dette et perte de maîtrise du SI."),
    ],
    "banner": "Sources : étude Whitelane France 2025 et Benelux 2026 ; Cigref "
              "citant Gartner sur le budget de dette.",
}

# --- S5 (contenu sommaire dans le PDF, mise en forme proposée) ---
OCTO_ACTEUR = {
    "titre": "OCTO, acteur de la révolution de l'IA générative",
    "claim": "Trois atouts qui légitiment l'offre.",
    "cartes": [
        ("Expérience ASF",
         "Une expérience éprouvée en matière d'Agentic Software Factory."),
        ("Greenfield et Brownfield",
         "Aussi à l'aise sur un produit neuf que sur un patrimoine existant."),
        ("Approche produit",
         "Une expertise reconnue de l'approche produit, pas seulement projet."),
    ],
}

# --- S6 (contenu sommaire dans le PDF, schéma proposé) ---
PROPOSITION_VALEUR = {
    "titre": "Notre proposition de valeur",
    "claim": "Ce que l'offre garantit, au-delà du contrat de maintenance classique.",
    "entete": "CE QUE LE CLIENT OBTIENT",
    "items": [
        "Une MCO garantie",
        "Des coûts maîtrisés",
        "Une captation des signaux (bugs, logs, attaques cyber…) au plus tôt",
        "Une qualité aux meilleurs standards du marché",
        "Une base documentaire toujours à jour",
        # 6e garantie, reformulee a la relecture du 2026-09-18. La parenthese
        # ouvrante n'etait pas refermee dans la source : refermee ici.
        "Une expérience produit maintenue (saisir les opportunités et rester "
        "dans l'amélioration continue)",
    ],
    # Schema (etait note "Schéma" sans contenu dans le PDF) : la chaine
    # deja portee par la matiere RUN IA du projet (syntheses_RUN_IA.md,
    # RUN_IA_brainstorm.md), pas une invention pour cette slide.
    "chaine": ["Signal", "Compréhension", "Décision", "Action", "Validation",
               "Apprentissage"],
    "banner": "C'est la boucle qui transforme un contrat de maintenance en "
              "levier de valeur produit.",
}

# --- S6 : « En pratique » (mise a jour 2026-09-18 sur le PDF v2 — le titre
# et le contenu de cette slide seule sont mis a jour sur cet arbitrage ;
# fusion du reporting dans "Piloter en continu" maintenue de la version
# precedente, meme si le PDF v2 donne desormais un vrai contenu a sa slide 7
# "Reporting" (a arbitrer separement si on veut la redetacher).
COMMENT = {
    "titre": "En pratique",
    "claim": "Trois phases, du diagnostic au pilotage continu.",
    "etapes": [
        ("1", "Diagnostiquer",
         ["Run Readiness Check",
          "Niveau de criticité",
          "Rétrodocumentation de l'application",
          "Audit sécurité",
          "Audit qualité"],
         False),
        ("2", "Mettre sous contrôle",
         ["Mise en place du monitoring (observabilité)",
          "Définition des indicateurs SLA et XLA",
          # Acronyme developpe a la demande du 2026-09-18.
          "Mise en place de l'ASRF (Agentic Software Run Factory)"],
         False),
        ("3", "Piloter en continu",
         ["Reporting en temps réel et alerting",
          "Reporting exécutif mensuel",
          # Formulation RACCOURCIE volontairement : le pas de liste est
          # uniforme (choix du design system), donc un item de 3 lignes
          # etire l'interligne de TOUTE la colonne. 2 lignes max ici.
          "Tickets : analyse auto → validation humaine → mise en œuvre",
          "Planning partagé avec le client"],
         True),
    ],
}

# --- S7 : Reporting (slide autonome — le PDF v2 lui donne un contenu propre,
# elle n'est PLUS fusionnée dans « En pratique », arbitrage du 2026-09-18) ---
REPORTING = {
    "titre": "Reporting",
    "claim": "Un même socle de mesure, restitué à deux rythmes.",
    # La phrase forte passe en bandeau de cloture (composant 7) plutot que de
    # rester en sous-titre : c'est elle qu'on veut voir rester.
    "banner": "Deux rythmes, deux publics : l'un pour réagir, l'autre pour décider.",
    # XLA ajoute le 2026-09-18 : ce qui ALIMENTE le reporting, en regard des
    # deux rythmes qui le restituent. Occupe la colonne droite, a la place du
    # panneau photo — le contenu prime sur la decoration.
    "xla_label": "XLA — TROIS FAMILLES CROISÉES",
    "xla": [
        ("Le ressenti", "déclaré par les utilisateurs, recueilli par sondage"),
        ("Les processus", "délais, respect des SLA, KPI"),
        ("Les outils", "performance des postes, des applications, du réseau"),
    ],
    "niveaux": [
        ("TEMPS RÉEL", "Pour le management opérationnel",
         "Alerting inclus : l'écart se voit quand il se produit, pas au bilan.",
         False),
        ("MENSUEL", "Pour le pilotage",
         "Vue exécutive : la tendance, la dette et les engagements de service.",
         True),
    ],
}

# --- S8 (PROPOSÉE, fusion opportunités OCTO / pitch / next steps) ---
# Le PITCH sort du rang des trois cartes egales (2026-09-18) : il devient un
# panneau hero pleine largeur, les deux autres volets passent en soutien.
CLOTURE = {
    "titre": "Opportunités, pitch et next steps",
    "claim": "Le pitch d'abord — c'est la phrase qui doit rester en tête.",
    "pitch_label": "LE PITCH",
    "pitch": [
        ("Un Run augmenté", "pas seulement maintenu"),
        ("Une boucle", "entre maturité du Run et croissance produit"),
        ("Le Run maîtrisé", "devient une opportunité de growth"),
    ],
    # Blocs REMPLACES a la relecture du 2026-09-18 : « Positionnement sur un
    # segment de marché » cede la place a deux actions, et un bloc
    # « Contacter d'autres OCTOs » remplace l'ancien volet « Pitch de l'offre »
    # (le pitch lui-meme reste, en panneau hero au-dessus).
    "blocs": [
        ("OPPORTUNITÉS POUR OCTO", [
            "Valider la valeur pour OCTO",
            "Finaliser la présentation",
        ]),
        ("CONTACTER D'AUTRES OCTOs", [
            "Équipe AI OPS en cours de formation chez C&P",
            "Reynald RIVI est intéressé",
            "Identifier d'autres interlocuteurs",
        ]),
        ("NEXT STEPS — proposition", [
            "Un Run Readiness Check sur un premier périmètre client",
            "Identifier un compte pilote pour la démonstration",
            "Un jalon de livrable montrable sous quelques semaines",
        ]),
    ],
}
