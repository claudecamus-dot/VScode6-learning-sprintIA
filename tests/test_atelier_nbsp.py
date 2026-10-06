"""The atelier deck generator uses a real no-break space (U+00A0) before high punctuation.

Regression: the atelier used to pass `sep=" "` (a plain U+0020) to the shared
module, so its typo_fr was a no-op and « ? » could be orphaned on its own line.
"""
import importlib.util
import os

import pytest

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ATELIER = os.path.join(RACINE, "docs", "run-ia", "atelier-agentic-run", "generer_deck.py")


@pytest.fixture(scope="module")
def atelier():
    spec = importlib.util.spec_from_file_location("g_atelier_nbsp", ATELIER)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


@pytest.mark.parametrize("p", list("?!:;"))
def test_atelier_typo_fr_insere_une_espace_insecable(atelier, p):
    assert atelier.typo_fr("Pourquoi %s" % p) == "Pourquoi\u00a0%s" % p
    assert "\u00a0" in atelier.typo_fr("a %s b" % p)


def test_atelier_typo_fr_pose_aussi_avant_pourcent(atelier):
    assert atelier.typo_fr("80 %") == "80\u00a0%"
