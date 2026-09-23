"""Constat d'audit du hub VScode5 (dimension risque_technique, #7) : le
gabarit OCTO etait un chemin absolu Windows hors depot, en dur dans les deux
generateurs et le test. Desormais configurable via TEMPLATE_OCTO_PATH, avec
repli sur l'ancien chemin (pour ne pas casser l'usage actuel sur ce poste).
"""
import importlib.util
import os

import pytest

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GENERATEURS = [
    os.path.join(RACINE, "docs", "run-ia", "generer_deck.py"),
    os.path.join(RACINE, "docs", "run-ia", "atelier-agentic-run", "generer_deck.py"),
]


def _charger(chemin, nom):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("chemin", GENERATEURS, ids=["offre", "atelier"])
def test_template_octo_path_est_prioritaire_sur_le_repli_code_en_dur(chemin, monkeypatch):
    monkeypatch.setenv("TEMPLATE_OCTO_PATH", r"D:\ailleurs\template-octo.pptx")
    module = _charger(chemin, "g_template_env_" + os.path.basename(os.path.dirname(chemin)))
    assert module.TEMPLATE == r"D:\ailleurs\template-octo.pptx"


@pytest.mark.parametrize("chemin", GENERATEURS, ids=["offre", "atelier"])
def test_sans_variable_d_environnement_le_repli_historique_est_conserve(chemin, monkeypatch):
    monkeypatch.delenv("TEMPLATE_OCTO_PATH", raising=False)
    module = _charger(chemin, "g_template_repli_" + os.path.basename(os.path.dirname(chemin)))
    assert module.TEMPLATE == (
        r"C:\Users\claude.camus\Documents\VSCode2\app\assets\template-octo.pptx"
    )
