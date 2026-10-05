"""Audit finding (risque_technique): a missing OCTO template must fail with a
clear message naming TEMPLATE_OCTO_PATH, not a raw python-pptx error."""
import importlib.util
import os

import pytest

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GENERATEURS = [
    os.path.join(RACINE, "docs", "run-ia", "generer_deck.py"),
    os.path.join(RACINE, "docs", "run-ia", "atelier-agentic-run", "generer_deck.py"),
]


@pytest.mark.parametrize("chemin", GENERATEURS, ids=["offre", "atelier"])
def test_gabarit_absent_leve_une_erreur_explicite(chemin, tmp_path, monkeypatch):
    monkeypatch.setenv("TEMPLATE_OCTO_PATH", str(tmp_path / "absent.pptx"))
    spec = importlib.util.spec_from_file_location("g_absent_" + str(abs(hash(chemin))), chemin)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with pytest.raises(FileNotFoundError, match="TEMPLATE_OCTO_PATH"):
        module.construire(str(tmp_path / "out.pptx"))
