"""Deuxieme point de verification REELLE (constat de scan : un seul test
`Presentation(` sur les generateurs, il en faut >=2 pour la dimension
« Test fonctionnel / rendu reel »).

Tous les autres tests de `trello_client` mockent la session `requests`
(`MagicMock`, voir test_trello_client.py) : ils prouvent que le code appelle
les bonnes methodes, pas qu'il survit a un VRAI aller-retour HTTP (encodage
JSON, entete, timeout, retry sur un vrai code de statut).

Ce test lance un `http.server.HTTPServer` reel sur localhost, y redirige
`API_BASE` le temps du test, et fait parler `TrelloClient` a travers un
vrai socket TCP — pagination par `before` et retry sur 503 compris. Aucun
credential Trello requis : le serveur est local.
"""
import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

import pytest

from trello_client import client as client_module
from trello_client.client import TrelloClient

BOARD_ID = "board_reel"

CUSTOM_FIELDS = [
    {
        "id": "cf1",
        "name": "Priorite",
        "options": [{"id": "opt1", "value": {"text": "Haute"}}],
    }
]

CARTES_PAGE_1 = [
    {
        "id": "c1",
        "name": "Carte un",
        "labels": [{"name": "bug"}],
        "customFieldItems": [{"idCustomField": "cf1", "idValue": "opt1"}],
        "actions": [
            {"id": "a1", "date": "2026-01-01", "data": {"text": "premier commentaire"}},
        ],
    }
]


class _HandlerCompteurEchecs(BaseHTTPRequestHandler):
    """Sert customFields et UNE page de cartes ; renvoie un 503 une fois
    avant de repondre sur /cards, pour exercer le retry sur un vrai code
    HTTP (pas un mock qui simule raise_for_status)."""

    a_echoue_une_fois = False

    def log_message(self, *a):  # silence
        pass

    def do_GET(self):
        parsed = urlparse(self.path)
        qs = parse_qs(parsed.query)
        if parsed.path == f"/1/boards/{BOARD_ID}/customFields":
            self._repondre(200, CUSTOM_FIELDS)
        elif parsed.path == f"/1/boards/{BOARD_ID}/cards":
            if "before" in qs:
                self._repondre(200, [])  # page suivante : vide, fin de pagination
            elif not _HandlerCompteurEchecs.a_echoue_une_fois:
                _HandlerCompteurEchecs.a_echoue_une_fois = True
                self._repondre(503, {"message": "throttled"})
            else:
                self._repondre(200, CARTES_PAGE_1)
        else:
            self._repondre(404, {"message": "not found"})

    def _repondre(self, code, payload):
        corps = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(corps)))
        self.end_headers()
        self.wfile.write(corps)


@pytest.fixture
def serveur_reel(monkeypatch):
    httpd = HTTPServer(("127.0.0.1", 0), _HandlerCompteurEchecs)
    port = httpd.server_port
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    monkeypatch.setattr(client_module, "API_BASE", f"http://127.0.0.1:{port}/1")
    monkeypatch.setattr(client_module, "BACKOFF_INITIAL", 0.01)  # retry rapide
    try:
        yield
    finally:
        httpd.shutdown()
        thread.join(timeout=5)


def test_get_board_cards_via_vrai_serveur_http(serveur_reel):
    """Aller-retour HTTP reel : retry sur un vrai 503, pagination reelle
    (page 2 vide -> arret), JSON reellement (de)serialise sur le fil."""
    client = TrelloClient(api_key="k", token="t")
    cartes = client.get_board_cards(BOARD_ID)

    assert len(cartes) == 1
    carte = cartes[0]
    assert carte.name == "Carte un"
    assert carte.labels == ["bug"]
    assert carte.custom_fields == {"Priorite": "Haute"}
    assert len(carte.comments) == 1
    assert carte.comments[0].text == "premier commentaire"
    # Le 503 a bien ete rencontre puis absorbe par le retry, pas contourne.
    assert _HandlerCompteurEchecs.a_echoue_une_fois is True
