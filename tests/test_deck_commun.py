"""Le code commun aux deux generateurs vit dans `docs/run-ia/deck_commun.py`.

Constat d'audit (duplication structurelle) : modele de hauteur, typographie,
grille et bandeau etaient recopies dans `generer_deck.py` et dans
`atelier-agentic-run/generer_deck.py`. Ce test verrouille (1) le comportement
du module partage, (2) que les deux generateurs L'UTILISENT au lieu d'en
reheberger une copie.
"""
import importlib.util
import os
import re
import sys

import pytest

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUN_IA = os.path.join(RACINE, "docs", "run-ia")
GENERATEURS = {
    "offre": os.path.join(RUN_IA, "generer_deck.py"),
    "atelier": os.path.join(RUN_IA, "atelier-agentic-run", "generer_deck.py"),
}
PARTAGES = ["typo_fr", "lh", "nlignes", "hbox", "hbox_max", "reste",
            "hauteur_bandeau", "_init_couleurs"]


@pytest.fixture(scope="module")
def K():
    sys.path.insert(0, os.path.join(RACINE, ".claude", "skills", "pptx-deck", "scripts"))
    sys.path.insert(0, RUN_IA)
    try:
        import deck_commun
        import pptx_deck
    finally:
        sys.path.pop(0)
        sys.path.pop(0)
    return deck_commun, pptx_deck


def test_typo_fr_pose_l_espace_insecable_par_defaut(K):
    k, D = K
    c = k.Commun(D)
    assert c.typo_fr("Pourquoi ? Oui : 50 %") == "Pourquoi\u00a0? Oui\u00a0: 50\u00a0%"
    assert c.typo_fr(None) is None


def test_sep_configurable_par_instance_sans_fuite_entre_instances(K):
    k, D = K
    atelier = k.Commun(D, sep=" ")
    offre = k.Commun(D)
    assert atelier.typo_fr("a ?") == "a ?"
    assert offre.typo_fr("a ?") == "a\u00a0?"


def test_reste_leve_quand_la_bande_est_saturee(K):
    k, _ = K
    with pytest.raises(ValueError, match="saturee"):
        k.reste(k.B_CONT - 0.1, 1.0)
    assert k.reste(1.0, 0.5) == 0.5


def test_hauteur_bandeau_croit_avec_le_texte(K):
    k, D = K
    c = k.Commun(D)
    assert c.hauteur_bandeau("mot " * 60) > c.hauteur_bandeau("mot")


@pytest.mark.parametrize("nom", sorted(GENERATEURS))
def test_les_generateurs_reutilisent_le_module_commun(nom):
    src = open(GENERATEURS[nom], encoding="utf8").read()
    assert "import deck_commun as K" in src
    for f in PARTAGES:
        if f == "_init_couleurs":
            continue
        assert not re.search(r"^def %s\(" % f, src, re.M), \
            "%s redefinit %s au lieu de l'importer de deck_commun" % (nom, f)
    # les constantes de grille ne sont plus re-affectees localement
    for c in ("L", "R", "CW", "B_CONT", "T_CONT", "CPI_LAYOUT", "COEF_LIGNE"):
        assert not re.search(r"^%s = " % c, src, re.M), "%s re-affecte %s" % (nom, c)


@pytest.mark.parametrize("nom", sorted(GENERATEURS))
def test_les_generateurs_chargent_et_exposent_les_memes_noms(nom):
    spec = importlib.util.spec_from_file_location("g_commun_" + nom, GENERATEURS[nom])
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    for f in PARTAGES + ["bandeau"]:
        assert callable(getattr(m, f)), f
    assert m.CW == pytest.approx(m.R - m.L)
