"""Garde-fou anti-duplication de `pptx_deck.py` (constat d'audit 1).

La SOURCE est la copie du kit agentic `.claude/skills/pptx-deck/scripts/` ;
les scripts de deck doivent l'importer, pas en heberger une copie.
"""
import hashlib
import os
import subprocess
import sys

import pytest

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(RACINE, ".claude", "skills", "pptx-deck", "scripts", "pptx_deck.py")
GENERATEURS = [
    os.path.join(RACINE, "docs", "run-ia", "generer_deck.py"),
    os.path.join(RACINE, "docs", "run-ia", "atelier-agentic-run", "generer_deck.py"),
]


def test_aucune_copie_de_pptx_deck_hors_de_la_skill():
    copies = []
    for dossier, _, fichiers in os.walk(RACINE):
        if ".git" in dossier or "_bmad" in dossier:
            continue
        if "pptx_deck.py" in fichiers:
            chemin = os.path.join(dossier, "pptx_deck.py")
            if os.path.abspath(chemin) != os.path.abspath(SOURCE):
                copies.append(chemin)
    assert copies == [], "copies de pptx_deck.py hors de la skill source : %s" % copies


@pytest.mark.parametrize("generateur", GENERATEURS, ids=["offre", "atelier"])
def test_le_generateur_importe_pptx_deck_depuis_la_skill(generateur):
    code = (
        "import importlib.util,sys,os;"
        "spec=importlib.util.spec_from_file_location('g',r'%s');"
        "m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);"
        "print(os.path.abspath(m.D.__file__))" % generateur
    )
    proc = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    resolu = proc.stdout.strip().splitlines()[-1]
    assert os.path.abspath(resolu) == os.path.abspath(SOURCE), resolu
    assert hashlib.md5(open(resolu, "rb").read()).hexdigest() == \
        hashlib.md5(open(SOURCE, "rb").read()).hexdigest()
