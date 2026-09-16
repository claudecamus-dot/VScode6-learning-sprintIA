r"""Test scopé du correctif : `.claude/warn_verif_before_commit.json` local doit
faire que le garde-fou surveille `trello_client/` et `tests/` (le code réel de
ce projet), pas seulement le repli générique `app/` (qui n'existe pas ici).

Provenance du correctif : campagne flotte 2026-09-16, salle atelier-dev — écart
retenu « le garde-fou ne matche jamais le code réel de ce dépôt ».

Style imité de `VSCode3/tests/test_warn_verif_before_commit.py` (canon) :
chargement du hook par chemin de fichier (il vit hors package), stdin simulé
en JSON, `subprocess.run` monkeypatché pour ne jamais toucher le vrai git, et
`_config_path()` monkeypatché vers un `tmp_path` — jamais le fichier réel du
projet.
"""
import importlib.util
import io
import json
import sys
from pathlib import Path

import pytest

_HOOK_PATH = Path(__file__).resolve().parent / "warn_verif_before_commit.py"


def _load_hook():
    spec = importlib.util.spec_from_file_location("warn_verif_before_commit", _HOOK_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


hook = _load_hook()


def _fake_run_factory(staged_files):
    """Double de `subprocess.run` : répond à `git diff --cached --name-only`
    avec les fichiers stagés fournis, et à tout le reste (dont `git grep` pour
    la garde périmètre, désactivée ici) par une sortie vide sans erreur."""

    class _Result:
        def __init__(self, stdout, returncode=0):
            self.stdout = stdout
            self.returncode = returncode

    def _fake_run(args, **kwargs):
        if args[:4] == ["git", "diff", "--cached", "--name-only"]:
            return _Result("\n".join(staged_files) + "\n")
        return _Result("", returncode=1)

    return _fake_run


def _run_hook(monkeypatch, tmp_path, cfg, staged_files, capsys):
    """Charge la config JSON dans `tmp_path`, simule le commit stagé, exécute
    `hook.main()` avec stdin JSON, retourne la sortie stdout (chaîne vide si
    aucun avertissement)."""
    cfg_path = tmp_path / "warn_verif_before_commit.json"
    cfg_path.write_text(json.dumps(cfg), encoding="utf-8")
    monkeypatch.setattr(hook, "_config_path", lambda: str(cfg_path))
    # Recharge les constantes module-level dérivées de _load_config() au moment
    # du chargement, comme le fait réellement le hook (process neuf par commit).
    watched, verif_bash, verif_skill = hook._load_config()
    monkeypatch.setattr(hook, "_WATCHED_PREFIXES", watched)
    monkeypatch.setattr(hook, "_VERIF_BASH", verif_bash)
    monkeypatch.setattr(hook, "_VERIF_SKILL", verif_skill)
    # Désactive les signaux opt-in (dod/dispositif/perimetre/lot) : ce test ne
    # vise que le repli watched_prefixes du correctif.
    monkeypatch.setattr(hook, "_DOD_ENABLED", False)
    monkeypatch.setattr(hook, "_DISPOSITIF_TESTS", ())
    monkeypatch.setattr(hook, "_PERIMETRE_ENABLED", False)
    monkeypatch.setattr(hook, "_PLAFOND_LOT", 0)

    monkeypatch.setattr(hook.subprocess, "run", _fake_run_factory(staged_files))
    # Pas de session/transcript : aucun signal "verif" détecté -> le garde-fou
    # doit parler si le périmètre surveillé est touché.
    payload = {
        "tool_input": {"command": 'git commit -m "wip"'},
        "cwd": str(tmp_path),
        "transcript_path": str(tmp_path / "absent-transcript.jsonl"),
    }
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))
    hook.main()
    return capsys.readouterr().out


_CFG_PROJET = {
    "watched_prefixes": ["trello_client/", "tests/"],
    "verif_bash": ["pytest", "-m pytest"],
    "verif_skill": ["revue-increment"],
}


def test_commit_touchant_trello_client_declenche_le_rappel(monkeypatch, tmp_path, capsys):
    out = _run_hook(monkeypatch, tmp_path, _CFG_PROJET,
                     ["trello_client/board.py"], capsys)
    assert out.strip() != ""
    message = json.loads(out)["systemMessage"]
    assert "incr" in message  # "incrément" (accent) — comparé via le JSON décodé
    assert "trello_client/" in message


def test_commit_touchant_tests_declenche_le_rappel(monkeypatch, tmp_path, capsys):
    out = _run_hook(monkeypatch, tmp_path, _CFG_PROJET,
                     ["tests/test_trello_client.py"], capsys)
    assert out.strip() != ""
    message = json.loads(out)["systemMessage"]
    assert "tests/" in message


def test_commit_touchant_uniquement_readme_reste_silencieux(monkeypatch, tmp_path, capsys):
    out = _run_hook(monkeypatch, tmp_path, _CFG_PROJET, ["README.md"], capsys)
    assert out.strip() == ""


def test_sans_config_locale_le_repli_generique_app_ne_matche_pas_trello_client(
        monkeypatch, tmp_path, capsys):
    """Preuve du défaut corrigé : sans `.claude/warn_verif_before_commit.json`,
    le repli générique (`app/`) ne surveille pas `trello_client/`, donc un
    commit qui le touche reste silencieux — c'est l'écart que ce correctif
    ferme via la configuration locale ci-dessus."""
    out = _run_hook(monkeypatch, tmp_path, {}, ["trello_client/board.py"], capsys)
    assert out.strip() == ""


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
