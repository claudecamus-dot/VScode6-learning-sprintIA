"""Contrat entre les generateurs de decks et le kit agentic (constat d'audit
risque_technique, 2026-09-23).

Les generateurs importent pptx_deck (skill pptx-deck) et framed_image /
nature_images / stock_images (skill pptx-framed-image) par sys.path, sans les
recopier. Une regeneration du kit depuis le hub pouvait donc renommer ou retirer
une fonction et casser un generateur sans toucher a son code. Ce test extrait
les noms reellement utilises par les generateurs et exige qu'ils existent dans
le kit installe : la dependance devient declaree ET verifiee en CI (sans
dependre du gabarit OCTO, contrairement a test_generation_decks).
"""

import importlib.util
import os
import re

import pytest

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GENERATEURS = [
    os.path.join(RACINE, "docs", "run-ia", "generer_deck.py"),
    os.path.join(RACINE, "docs", "run-ia", "atelier-agentic-run", "generer_deck.py"),
]
SKILLS = os.path.join(RACINE, ".claude", "skills")


def _charger(skill, module):
    chemin = os.path.join(SKILLS, skill, "scripts", module + ".py")
    assert os.path.isfile(chemin), f"skill du kit absente : {chemin}"
    dossier = os.path.dirname(chemin)
    import sys
    if dossier not in sys.path:
        sys.path.insert(0, dossier)
    spec = importlib.util.spec_from_file_location(module, chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _source():
    return "\n".join(open(g, encoding="utf-8").read() for g in GENERATEURS)


def test_chaque_fonction_pptx_deck_utilisee_existe_dans_le_kit():
    utilises = sorted(set(re.findall(r"\bD\.([A-Za-z_]\w*)", _source())))
    assert utilises, "motif D.<nom> introuvable : le test ne verifierait plus rien"
    D = _charger("pptx-deck", "pptx_deck")
    manquants = [n for n in utilises if not hasattr(D, n)]
    assert not manquants, f"pptx_deck du kit n'expose plus : {manquants}"


@pytest.mark.parametrize(("module", "motif"), [
    ("framed_image", r"from framed_image import ([\w, ]+)"),
    ("nature_images", r"\bnature_images\.([A-Za-z_]\w*)"),
    ("stock_images", r"\bstock_images\.([A-Za-z_]\w*)"),
])
def test_chaque_fonction_framed_image_utilisee_existe_dans_le_kit(module, motif):
    noms = set()
    for m in re.findall(motif, _source()):
        noms.update(x.strip() for x in m.split(",") if x.strip())
    assert noms, f"aucun usage de {module} trouve : motif perime ?"
    mod = _charger("pptx-framed-image", module)
    manquants = sorted(n for n in noms if not hasattr(mod, n))
    assert not manquants, f"{module} du kit n'expose plus : {manquants}"
