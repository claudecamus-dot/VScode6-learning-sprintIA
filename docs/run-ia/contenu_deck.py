# -*- coding: utf-8 -*-
"""Contenu éditorial du deck AGENTIC PRODUCT RUN — séparé de la mise en page.

Source : RUN_IA_brainstorm.md (2026-09-17), condensé pour une soutenance
commerciale. Le deck ne porte AUCUN prix ni chiffrage (arbitrage utilisateur
du 2026-09-17) : la soutenance porte sur la pertinence de l'offre, pas sur son
tarif.
"""

COUVERTURE = {
    "titre": "AGENTIC PRODUCT RUN",
    "sous_titre": "La TMA augmentée par l'IA",
    "mention": "OCTO Technology",
    "date": "Septembre 2026",
}

# --- Intercalaires : 3 chapitres structurants ---
CHAPITRES = [
    (
        "1", "Contexte et enjeux clients",
        "Où le RUN perd la valeur aujourd'hui, et pourquoi c'est réparable maintenant",
    ),
    (
        "2", "Enjeux et opportunités OCTO",
        "Ce que nous savons faire que personne ne fait à notre place",
    ),
    ("3", "L'offre", "Ce que nous vendons, où ça se branche, et ce que le client y gagne"),
    ("4", "Next steps", "À qui la vendre, et ce qu'il reste à trancher pour commencer"),
]

SOMMAIRE = {
    "titre": "Ce que nous allons couvrir",
    "claim": (
        "Quatre temps : là où le client perd de la valeur, ce qu'OCTO sait y apporter, "
        "l'offre, et ce qu'on enclenche."
    ),
}

# --- S2 : le problème ---
CONSTATS = {
    "titre": "Où vous perdez de la valeur aujourd'hui",
    "claim": "Vous payez deux fois : une fois pour construire, une fois pour ne plus comprendre.",
    "cartes": [
        ("1", "Le produit tourne, plus personne ne l'explique",
         "L'équipe de build est partie et les décisions d'architecture ne sont "
         "écrites nulle part."),
        ("2", "Chaque bug est traité comme un objet isolé",
         "Dix-sept tickets pour un seul défaut. Le même incident revient six "
         "mois plus tard."),
        ("3", "La dette se discute, elle ne se mesure pas",
         "Elle est arbitrée à l'opinion la plus forte, jamais au coût réel des "
         "incidents."),
        ("4", "Les retours utilisateurs n'atteignent pas le code",
         "Verbatims, tickets, analytics et dépôts vivent dans quatre outils "
         "que personne ne rapproche."),
        ("5", "Le design system dérive sans que personne le voie",
         "Composants dupliqués hors bibliothèque, écarts de charte non "
         "détectés, adoption réelle jamais mesurée."),
    ],
    "banner": "Le RUN n'est pas un centre de coût à comprimer : c'est le seul endroit "
              "où l'on sait vraiment ce que le produit vaut.",
}

# --- S3 : pourquoi maintenant ---
RUPTURES = {
    "titre": "Pourquoi c'est réparable maintenant",
    "claim": (
        "Deux ruptures se croisent : l'IA sait enfin lire un patrimoine, et le build "
        "agentique en produit plus vite qu'on ne le maîtrise."
    ),
    # Titre = (texte, mention_italique|None) : la mention est posee en run
    # italique DANS la phrase (emphase en ligne), pas en phrase separee.
    "colonnes": [
        ("RUPTURE 1", ("L'IA sait lire un patrimoine entier", None),
         ["Code, logs, tickets, traces et documents : une seule matière analysable.",
          "Une cartographie qui demandait six semaines se produit en quelques jours.",
          "Chaque conclusion cite ses preuves : commits, appels d'API, tests."],
         False),
        ("RUPTURE 2", ("Le build agentique livre plus vite qu'il ne documente",
                      "hypothèse ?"),
         ["Des produits fonctionnent sans que personne sache pourquoi.",
          "Nouveaux objets à exploiter : agents, prompts, modèles, outils.",
          "Le non-déterminisme rend inopérants les réflexes de RUN classiques."],
         True),
    ],
    "banner": "Vous allez accumuler ces produits en 2026. Personne ne vous vend "
              "encore la mise sous contrôle qui va avec.",
}

# --- S4 : la promesse ---
PROMESSE = {
    "titre": "La promesse : des signaux dispersés, des actions traçables",
    "claim": (
        "Une seule chaîne, du signal émis par le système à l'adoption mesurée "
        "chez l'utilisateur."
    ),
    "chaine": ["Signal", "Compréhension", "Décision", "Action", "Validation",
               "Apprentissage", "Adoption"],
    "entrees": ("CE QUI ENTRE", [
        "Tickets de support et incidents",
        "Logs, alertes, traces d'agents",
        "Retours utilisateurs et analytics",
        "Dépôts, pipelines et dépendances",
        "Documentation existante",
    ]),
    "sorties": ("CE QUI EN SORT", [
        "Un dossier de bug enrichi, dédoublonné",
        "Une cause racine proposée et prouvée",
        "Des tests de non-régression générés",
        "Un runbook et une documentation à jour",
        "Une priorité argumentée, pas subie",
    ]),
    "banner": "Chaque action reste attribuée à un humain qui décide. L'IA instruit le "
              "dossier, elle ne prend pas la main.",
}

# --- S5 : positionnement par rapport a la TMA et au MCO ---
SOCLE = {
    "titre": "Où Agentic Product Run se branche : sur la TMA et le MCO",
    "claim": (
        "Nous ne remplaçons pas le contrat existant — nous rendons enfin tenables "
        "les engagements qu'il porte déjà."
    ),
    "colonnes": ("CE QUE LA TMA ET LE MCO ENGAGENT DÉJÀ",
                 "CE QU'AGENTIC PRODUCT RUN CHANGE"),
    "lignes": [
        ("Correctif",
         "Rétablir le service dans le délai prévu",
         "La cause racine est prouvée, pas devinée"),
        ("Évolutif",
         "Absorber les évolutions au fil de l'eau",
         "L'impact est connu avant de s'engager"),
        ("Disponibilité",
         "Tenir les niveaux de service et l'astreinte",
         "Les récurrents sont traités à la source"),
        ("Documentation",
         "Maintenir la documentation d'exploitation",
         "Elle se met à jour par la résolution, datée"),
        ("Sécurité",
         "Appliquer les correctifs de sécurité",
         "Vulnérabilités alertées avant l'incident"),
        ("Réversibilité",
         "Rendre le patrimoine reprenable à la sortie",
         "La cartographie est produite en continu"),
    ],
    "banner": "Le meilleur point d'entrée commercial n'est pas un nouveau budget : "
              "c'est le prochain renouvellement de TMA.",
}

# --- S9 : l'apport produit (product growth) ---
PRODUIT = {
    "titre": "Nous ne réparons pas que l'exploitation : nous alimentons le produit",
    "claim": (
        "Un incident bien instruit est une donnée produit ; aujourd'hui elle se perd "
        "entre le support et la roadmap."
    ),
    "boucle": [
        ("Écouter", "Verbatims, tickets et usage regroupés par problème réel"),
        ("Arbitrer", "Fréquence et impact mesurés, dette priorisée par son coût"),
        ("Refermer", "L'utilisateur recontacté, l'effet sur l'usage mesuré"),
    ],
    "retour": "Ce qui a marché devient une règle réutilisable",
    "banner": "C'est ce qui transforme un contrat de maintenance en levier de croissance "
              "produit — et ce qui rend l'offre défendable face à un directeur produit.",
}

# --- S6 : l'offre ---
MODULES = {
    "titre": "Le parcours en trois temps",
    "claim": (
        "Une porte d'entrée courte et bornée, puis deux prolongements que le client "
        "déclenche s'il a vu la valeur."
    ),
    # Chaque temps porte son niveau d'autonomie : la slide « trajectoire »
    # separee racontait la meme progression une seconde fois (fusion 2026-09-17).
    "etapes": [
        ("1", "RUN Readiness Check", "2 à 4 semaines",
         ["Diagnostic de mise sous contrôle",
          "Cartographie sur le code réel",
          "Score de maturité RUN sur 10 domaines"],
         "Un état des lieux opposable",
         "Autonomie 0-1 — l'IA observe et recommande, rien ne s'exécute",
         False),
        ("2", "Mise sous contrôle", "3 à 6 mois",
         ["Documentation vivante et datée",
          "Runbooks et procédures de rollback",
          "Observabilité des parcours critiques"],
         "Un produit reprenable sans son équipe de build",
         "Autonomie 2-3 — tout est préparé, un humain valide avant d'appliquer",
         False),
        ("3", "RUN augmenté", "12 à 24 mois",
         ["Triage, investigation, reproduction",
          "Maintenance préventive et alerting sécurité",
          "AgentOps pour les produits agentiques"],
         "Un RUN qui apprend de chaque incident",
         "Autonomie 4 — périmètre restreint et réversible, rollback obligatoire",
         True),
    ],
}

# --- S6 : la porte d'entrée ---
READINESS = {
    "titre": "La porte d'entrée : le RUN Readiness Check",
    "claim": (
        "Dix questions auxquelles presque aucun de nos clients ne sait répondre "
        "sur son propre produit."
    ),
    "domaines": [
        ("Architecture", "Composants et flux critiques identifiés ?"),
        ("Ownership", "Chaque composant a-t-il un propriétaire ?"),
        ("Observabilité", "Parcours critiques sous monitoring ?"),
        ("Tests", "Couverture de tests sur le critique ?"),
        ("Documentation", "Exploitation et rollback documentés ?"),
        ("Sécurité", "Secrets et dépendances maîtrisés ?"),
        ("Dette", "Risques techniques connus et chiffrés ?"),
        ("IA et agents", "Modèles, prompts et outils inventoriés ?"),
        ("Continuité", "Reprise possible sans l'équipe de build ?"),
        ("Gouvernance", "Niveaux d'autonomie explicites ?"),
    ],
    "livrables": ("CE QUE LE CLIENT REPART AVEC", [
        "Un score de maturité RUN par domaine",
        "La cartographie du produit, sourcée",
        "La liste explicite des zones inconnues",
        "Un backlog de sécurisation priorisé",
        "Les risques bloquants avant production",
    ]),
    "accroche": "Un diagnostic court et borné, qui ouvre la conversation sur tout le reste.",
}

# --- S7 : le différenciateur ---
PREUVE = {
    "titre": "Ce qui nous distingue : la preuve, pas la fluidité",
    "claim": (
        "Une documentation élégante et fausse coûte plus cher que pas de "
        "documentation du tout."
    ),
    "avant": ("SANS CETTE EXIGENCE", [
        ("Une réponse plausible", "que personne ne peut vérifier"),
        ("Une documentation lisse", "dont on ignore la date et la source"),
        ("Une contradiction", "silencieusement arbitrée par le modèle"),
        ("Une recommandation", "sans responsable ni niveau de confiance"),
    ]),
    "apres": ("AVEC L'EXIGENCE DE PREUVE", [
        ("Chaque conclusion cite ses sources", "commits, appels d'API, tests"),
        ("Tout élément porte sa date", "de dernière vérification"),
        ("Les contradictions sont remontées", "jamais tranchées sans un humain"),
        ("Chaque recommandation nomme", "sa confiance et son valideur"),
    ]),
    "banner": "Le service Billing semble responsable du calcul des remises — confiance 82 %, "
              "sur six appels d'API et trois tests ; une page Confluence plus ancienne dit le "
              "contraire.",
}

# --- S8 : agentique ---
AGENTIQUE = {
    "titre": "Le terrain où nous sommes seuls : les produits agentiques",
    "claim": (
        "Ce que nos clients construisent en 2026 avec des agents, ils devront "
        "l'exploiter en 2027."
    ),
    # Pastilles courtes plutot que puces : la bande se lit d'un coup d'oeil et
    # le format tranche avec les cartes en colonnes du reste du deck.
    "bandes": [
        ("CE QU'IL FAUT EXPLOITER", False,
         ["Agents", "Prompts", "Modèles", "Outils", "Mémoires", "Traces",
          "Jeux d'évaluation", "Permissions"]),
        ("CE QUI DÉRAILLE", False,
         ["Dérive de modèle", "Régression de prompt", "Boucles",
          "Erreurs d'outil", "Dépassements de coût", "Exécutions non reproductibles"]),
        ("CE QUE NOUS INSTRUMENTONS", True,
         ["Réussite par tâche", "Intervention humaine", "Coût par résultat",
          "Latence par étape", "Régressions après changement",
          "Autonomie explicite"]),
    ],
    "banner": "Un seul modèle pour le microservice classique et pour l'agent : c'est ce qui "
              "nous évite de vendre deux offres qui ne se parlent pas.",
}

# --- S9 : trajectoire ---
# --- S10 : vendabilité ---
VENTE = {
    "titre": "Comment cette offre se vend",
    "claim": (
        "Une offre ne tient que si l'on sait à qui l'adresser, sur quel événement, "
        "et avec qui la délivrer."
    ),
    "blocs": [
        ("À QUI", [
            "DSI et CTO au patrimoine applicatif chargé",
            "Directions produit héritant d'un build externalisé",
            "Responsables d'exploitation face à des produits IA",
        ]),
        ("SUR QUEL DÉCLENCHEUR", [
            "Fin de build ou transfert à une autre équipe",
            "Incident majeur dont personne ne retrouve la cause",
            "Premier produit agentique qui passe en production",
        ]),
        ("AVEC QUELLE ÉQUIPE", [
            "Un tech lead qui connaît le patrimoine",
            "Un architecte pour la cartographie et les risques",
            "Un expert IA pour les agents et leur évaluation",
        ]),
        ("CE QU'IL NOUS MANQUE POUR VENDRE", [
            "Une référence client, même anonymisée",
            "Un point d'accroche dans nos contrats TMA en cours",
            "Un exemple de livrable à montrer en rendez-vous",
        ]),
    ],
}

# --- S11 : la demande ---
DECISIONS = {
    "titre": "Ce que je vous demande de trancher aujourd'hui",
    "claim": (
        "Trois décisions suffisent à savoir si Agentic Product Run devient une offre "
        "ou reste une note."
    ),
    "cartes": [
        ("1", "L'offre est-elle vendable en l'état ?",
         "Le RUN Readiness Check tient-il comme porte d'entrée face à un acheteur, "
         "ou faut-il l'adosser à une offre existante ?", False),
        ("2", "Sur quel compte la tester en premier ?",
         "Nous avons besoin d'un client pilote pour transformer le module 1 en "
         "référence montrable.", True),
        ("3", "Offre autonome ou extension de TMA ?",
         "La vend-on seule, ou comme l'option qui fait gagner nos "
         "renouvellements de TMA et de MCO ?", False),
    ],
    "banner": "Prochain jalon proposé : un compte pilote identifié et un livrable de "
              "démonstration prêt d'ici deux semaines.",
}

# --- S16 : conclusion ---
CONCLUSION = {
    "titre": "Ce que le client achète, en trois arguments",
    "claim": (
        "Si vous ne deviez retenir que trois phrases pour ouvrir la conversation, "
        "ce sont celles-ci."
    ),
    "arguments": [
        ("1", "Il reprend la main sur un produit qu'il ne comprend plus",
         "Cartographie sur le code réel, zones inconnues nommées.",
         "« Je peux reprendre ce produit sans l'équipe qui l'a construit. »"),
        ("2", "Il arrête de payer deux fois le même incident",
         "Causes racines prouvées, dette priorisée par son coût.",
         "« Ce qui casse chez moi cesse de revenir. »"),
        ("3", "Son contrat de maintenance produit de la valeur",
         "Les retours utilisateurs alimentent la roadmap.",
         "« Ma TMA ne défend plus l'existant : elle fait avancer le produit. »"),
    ],
    "banner": "Et le premier pas ne demande aucun arbitrage budgétaire lourd : "
              "un diagnostic court sur un seul produit suffit à le prouver.",
}
