"""Baseline de lint — plafond, sur le modèle de VsCode4/tests/test_lint_baseline.py.

Finding P3 du 2026-09-24 : `ruff check .` remontait 88 erreurs (66 E501, 13
E741, 7 I001, 2 F401 — `py -m ruff check . --statistics`). Correctif appliqué :
`ruff check . --select I001,F401 --fix` (9 erreurs corrigées, purement
mécanique — tri d'imports et imports inutilisés, aucune correction de masse
sur E501/E741 qui demanderait de la relecture). Nouveau total mesuré :
79 erreurs (66 E501, 13 E741).

Correctif du même jour, en deux temps : les 66 E501/13 E741 portées par
`.claude` (`scan_transcripts.py`, `log_run.py` et d'autres) sont des COPIES
SYNCHRONISÉES du canon du hub de supervision VScode5 (bannière « GÉNÉRÉ — NE
PAS ÉDITER LOCALEMENT ») — corrigées localement une première fois par erreur,
puis REVERTÉES et sorties du périmètre lint via `extend-exclude = [".claude"]`
dans `ruff.toml` : leur qualité se corrige au hub, une correction locale
serait écrasée à la prochaine propagation. Les erreurs restantes (docs/,
tests/) ont été coupées à la main (jamais de reformatage global). Total
mesuré après correctif : **0 erreur**. Ce test fige ce chiffre en plafond,
comme sur VsCode4 : toute hausse barre, toute baisse doit être inscrite ici.
"""
import json
import os
import subprocess
import sys

import pytest

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Mesuré le 2026-09-24 par `_mesurer` ci-dessous, après correction manuelle des
# E501/E741 de docs/ et tests/, et sortie de `.claude` du périmètre lint
# (copies canon du hub — cf. docstring du module).
_BASELINE = {}


def _zone(chemin_relatif):
    tete = chemin_relatif.split("/")[0]
    return tete


def _mesurer():
    """Le compte de points ruff par (zone, règle). Rend `None` si ruff est
    absent — un poste sans outillage de dev ne doit pas voir un ÉCHEC là où il
    n'y a qu'une mesure impossible."""
    try:
        r = subprocess.run(
            [sys.executable, "-m", "ruff", "check", ".",
             "--output-format=json", "--quiet"],
            cwd=RACINE, capture_output=True, text=True, timeout=180)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if r.returncode not in (0, 1):
        return None
    try:
        points = json.loads(r.stdout)
    except json.JSONDecodeError:
        return None
    compte = {}
    for p in points:
        rel = os.path.relpath(p["filename"], RACINE).replace("\\", "/")
        cle = (_zone(rel), p["code"])
        compte[cle] = compte.get(cle, 0) + 1
    return compte


@pytest.fixture(scope="module")
def mesure():
    compte = _mesurer()
    if compte is None:
        pytest.skip("ruff indisponible ou illisible sur ce poste")
    return compte


def _libelle(cle):
    zone, code = cle
    return f"{zone}/{code}"


class TestBaselineRuff:
    def test_aucune_regression_de_lint(self, mesure):
        """Une AUGMENTATION est une régression : elle barre."""
        hausses = {_libelle(c): (_BASELINE.get(c, 0), n)
                   for c, n in mesure.items() if n > _BASELINE.get(c, 0)}
        assert not hausses, (
            "régression de lint — points en hausse (baseline -> mesuré) : "
            f"{hausses}. Corriger le code ; ne relever la baseline de "
            "tests/test_lint_baseline.py que si le point est délibérément "
            "toléré, et dire pourquoi.")

    def test_aucune_dette_payee_non_inscrite(self, mesure):
        """Une BAISSE barre aussi — sinon la baseline dérive sans que
        personne le voie."""
        baisses = {_libelle(c): (n, mesure.get(c, 0))
                   for c, n in _BASELINE.items() if mesure.get(c, 0) < n}
        assert not baisses, (
            "dette de lint payée mais non inscrite (baseline -> mesuré) : "
            f"{baisses}. Abaisser la baseline de tests/test_lint_baseline.py "
            "au chiffre mesuré — une baseline qu'on ne descend jamais cesse "
            "d'être une référence.")

    def test_aucune_regle_neuve(self, mesure):
        """Une règle absente de la baseline est une famille de défaut
        NEUVE, pas une variation de compte : elle mérite d'être nommée."""
        neuves = sorted(_libelle(c) for c in mesure if c not in _BASELINE)
        assert not neuves, (
            f"règles ruff neuves, absentes de la baseline : {neuves}")

    def test_la_baseline_est_a_zero(self, mesure):
        """Contre-garde : la baseline est désormais vide par construction (0
        erreur soldée) — ce test la fait échouer si `mesure` retrouve un point
        que `test_aucune_regle_neuve` n'aurait pas détecté."""
        assert _BASELINE == {}
        assert mesure == {}
