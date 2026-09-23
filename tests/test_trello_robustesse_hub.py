"""Constats d'audit du hub VScode5 (.claude/audits/VScode6-learning-sprintIA.json,
dimension robustesse) 1, 2 et 3 :

  1. get_board_custom_fields indexait f["id"]/f["name"] et opt["value"]["text"]
     en direct : KeyError brut au lieu de TrelloSchemaError.
  2. Les commentaires etaient demandes via actions=commentCard SANS nActions :
     Trello plafonne a 50 par defaut, en silence au-dela.
  3. response.json() n'etait pas garde : une reponse 200 non-JSON levait
     ValueError au lieu de TrelloSchemaError.

Chaque test a ete verifie rouge en revertant temporairement la garde
correspondante (voir rapport de la seance du 2026-09-23).
"""
import requests
import pytest

from trello_client.client import TrelloClient, TrelloSchemaError


class FakeSession:
    def __init__(self, routes):
        self.routes = routes
        self.appels = []

    def get(self, url, params=None, timeout=None):
        self.appels.append((url, params or {}))
        for motif, payload in self.routes.items():
            if url.endswith(motif):
                return _reponse(url, 200, payload)
        raise AssertionError("URL non routee : %s" % url)


def _reponse(url, code, payload, texte=None, json_leve=None):
    r = requests.Response()
    r.status_code = code
    r.url = url
    if json_leve is not None:
        def _json():
            raise json_leve
        r.json = _json
        r._content = (texte or "").encode("utf-8")
    else:
        r.json = lambda: payload
    return r


def _client(session):
    return TrelloClient(api_key="cle-factice-1234", token="token-factice-1234", session=session)


# --- 1 : id de custom field absent -> TrelloSchemaError, pas KeyError -----

def test_custom_field_sans_id_leve_une_erreur_typee_pas_un_keyerror():
    session = FakeSession({"/boards/b1/customFields": [{"name": "Sans id"}]})
    with pytest.raises(TrelloSchemaError) as excinfo:
        _client(session).get_board_custom_fields("b1")
    assert "b1" in str(excinfo.value)


def test_custom_field_sans_name_retombe_sur_l_id_sans_lever():
    # Le libelle, lui, a un repli sur : Trello peut faire evoluer une option
    # sans invalider le champ entier.
    session = FakeSession({"/boards/b1/customFields": [{"id": "f1", "options": []}]})
    resultat = _client(session).get_board_custom_fields("b1")
    assert resultat["f1"]["name"] == "f1"


# --- 2 : nActions demande explicitement, sinon plafond silencieux a 50 ----

def test_get_board_cards_demande_nactions_pour_ne_pas_tronquer_l_historique():
    session = FakeSession({"/customFields": [], "/cards": []})
    _client(session).get_board_cards("b1")
    urls_cards = [p for u, p in session.appels if u.endswith("/cards")]
    assert urls_cards, "aucune requete /cards observee"
    assert urls_cards[0].get("nActions") == "1000", \
        "nActions absent : Trello plafonnerait a 50 commentaires par carte en silence"


# --- 3 : reponse 200 non-JSON -> TrelloSchemaError, pas ValueError brute --

def test_reponse_200_non_json_leve_une_erreur_typee_pas_une_valueerror():
    session = FakeSession({})

    def get(url, params=None, timeout=None):
        session.appels.append((url, params or {}))
        return _reponse(url, 200, None, texte="<html>pas du json</html>",
                         json_leve=ValueError("Expecting value"))

    session.get = get
    with pytest.raises(TrelloSchemaError) as excinfo:
        _client(session).get_board_custom_fields("b1")
    assert "boards/b1/customFields" in str(excinfo.value)
