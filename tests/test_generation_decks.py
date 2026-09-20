"""Les deux generateurs de deck produisent reellement un .pptx sans defaut.

Constat d'audit : la quasi-totalite du Python du depot n'avait aucun test. Les
deux `docs/run-ia/**/generer_deck.py` pesent 1953 des 2820 lignes de code
applicatif (`wc -l`, 2026-09-20) et n'etaient exerces par rien : seule
`trello_client` l'etait. Les tests existants ne verifient que la NON-DUPLICATION
de `pptx_deck.py`, pas que les generateurs tournent.

Ce test les lance de bout en bout, dans un repertoire temporaire, et s'appuie sur
la verification que les generateurs portent DEJA (verifier_geometrie /
verifier_debordements_texte / verifier_chrome_gabarit / verifier_plancher) : un
defaut geometrique fait sortir le script en code non nul. Le contrat teste est
donc « le deck se construit ET passe ses propres controles », pas seulement
« le module s'importe ».

Le template OCTO est reference par un chemin absolu hors depot (VSCode2) : sur un
poste qui ne l'a pas, le test est saute plutot que rouge — c'est une dependance
d'environnement, pas une regression du code.
"""
import os
import subprocess
import sys

import pytest

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = r"C:\Users\claude.camus\Documents\VSCode2\app\assets\template-octo.pptx"
GENERATEURS = {
    "offre": os.path.join(RACINE, "docs", "run-ia", "generer_deck.py"),
    "atelier": os.path.join(
        RACINE, "docs", "run-ia", "atelier-agentic-run", "generer_deck.py"),
}


@pytest.mark.parametrize("nom", sorted(GENERATEURS))
def test_le_generateur_produit_un_pptx_sans_defaut(nom, tmp_path):
    if not os.path.exists(TEMPLATE):
        pytest.skip("template OCTO absent de ce poste : %s" % TEMPLATE)
    generateur = GENERATEURS[nom]
    sortie = tmp_path / ("%s.pptx" % nom)

    proc = subprocess.run(
        [sys.executable, generateur, str(sortie)],
        capture_output=True, text=True, cwd=os.path.dirname(generateur))

    assert proc.returncode == 0, \
        "%s sort en %d :\n%s\n%s" % (nom, proc.returncode, proc.stdout, proc.stderr)
    assert sortie.exists(), "aucun fichier produit : %s" % proc.stdout

    from pptx import Presentation
    prs = Presentation(str(sortie))
    # Un .pptx valide mais vide passerait le code de retour : on exige des slides.
    assert len(prs.slides._sldIdLst) >= 10, \
        "%s : %d slides seulement" % (nom, len(prs.slides._sldIdLst))
