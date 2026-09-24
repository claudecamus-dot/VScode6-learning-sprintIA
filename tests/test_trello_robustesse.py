"""Constats d'audit 8 (KeyError brut), 9 (429 / reseau), 10 (custom fields),
11 (N+1 requetes) et 12 (pagination)."""
import pytest
import requests

from trello_client.client import (
    TrelloClient,
    TrelloSchemaError,
    _resolve_custom_field_value,
)


class FakeSession:
    """Session comptant ses appels, sans aucune socket."""

    def __init__(self, routes):
        self.routes = routes
        self.appels = []

    def get(self, url, params=None, timeout=None):
        self.appels.append(url)
        for motif, payload in self.routes.items():
            if url.endswith(motif):
                if isinstance(payload, list) and payload and isinstance(payload[0], int):
                    code = payload.pop(0)
                else:
                    code = 200
                return _reponse(url, code, payload)
        raise AssertionError("URL non routee : %s" % url)


def _reponse(url, code, payload):
    r = requests.Response()
    r.status_code = code
    r.url = url
    r._payload = payload
    r.json = lambda: payload
    return r


def _client(session):
    return TrelloClient(api_key="cle-factice-1234", token="token-factice-1234", session=session)


# --- 8 : plus de KeyError brut --------------------------------------------

def test_commentaire_sans_data_text_leve_une_erreur_typee_portant_l_id():
    session = FakeSession({"/cards/card1/actions": [{"id": "a1", "date": "2026-01-01", "data": {}}]})
    with pytest.raises(TrelloSchemaError) as excinfo:
        _client(session).get_card_comments("card1")
    assert "card1" in str(excinfo.value)
    assert "text" in str(excinfo.value)


def test_carte_sans_name_leve_une_erreur_typee_pas_un_keyerror():
    session = FakeSession({
        "/boards/b1/customFields": [],
        "/boards/b1/cards": [{"id": "card1"}],
    })
    with pytest.raises(TrelloSchemaError) as excinfo:
        _client(session).get_board_cards("b1", with_comments=False)
    assert "card1" in str(excinfo.value)


# --- 9 : rate limit 429 et erreurs reseau ---------------------------------

def test_429_est_retente_avec_backoff_puis_reussit(monkeypatch):
    import trello_client.client as mod
    pauses = []
    monkeypatch.setattr(mod.time, "sleep", pauses.append)
    session = FakeSession({"/boards/b1/customFields": [429, 429, 200]})
    session.routes["/boards/b1/customFields"] = [429, 429, 200]
    # payload renvoye a chaque fois : liste vide de definitions
    def get(url, params=None, timeout=None):
        session.appels.append(url)
        codes = [429, 429, 200]
        code = codes[min(len(session.appels) - 1, 2)]
        return _reponse(url, code, [])
    session.get = get
    assert _client(session).get_board_custom_fields("b1") == {}
    assert len(session.appels) == 3
    assert pauses, "aucun backoff observe"


def test_429_persistant_finit_par_lever_sans_boucler_indefiniment(monkeypatch):
    import trello_client.client as mod
    monkeypatch.setattr(mod.time, "sleep", lambda _s: None)
    session = FakeSession({"/boards/b1/customFields": []})
    session.get = lambda url, params=None, timeout=None: (
        session.appels.append(url), _reponse(url, 429, []))[1]
    with pytest.raises(requests.HTTPError):
        _client(session).get_board_custom_fields("b1")
    assert len(session.appels) <= 5


# --- 10 : resolution des custom fields par TYPE ----------------------------

@pytest.mark.parametrize("field_type,value,attendu", [
    ("checkbox", {"checked": "false"}, "false"),
    ("checkbox", {"checked": "true"}, "true"),
    ("number", {"number": "0"}, "0"),
    ("text", {"text": "bonjour"}, "bonjour"),
    ("date", {"date": "2026-09-20T10:00:00.000Z"}, "2026-09-20T10:00:00.000Z"),
])
def test_resolution_par_type_declare(field_type, value, attendu):
    assert _resolve_custom_field_value({"value": value}, {"type": field_type}) == attendu


def test_checkbox_false_n_est_pas_confondu_avec_vide():
    # le dict {"checked": "false"} est VRAI en Python : l'ancien `if value:`
    # passait, mais un dict {"number": "0"} tombait dans la meme branche sans
    # distinction. Ici on verifie la semantique booleenne exposee.
    assert _resolve_custom_field_value({"value": {"checked": "false"}},
                                       {"type": "checkbox"}) == "false"
    assert _resolve_custom_field_value({"value": {}}, {"type": "checkbox"}) == ""


# --- 11 : plus de N+1 -------------------------------------------------------

def _routes_board(nb_cartes):
    cartes = [
        {
            "id": "card%d" % i,
            "name": "Carte %d" % i,
            "labels": [],
            "actions": [{"id": "a%d" % i, "date": "2026-01-01",
                         "data": {"text": "commentaire %d" % i},
                         "memberCreator": {"fullName": "X"}}],
        }
        for i in range(nb_cartes)
    ]
    return {"/customFields": [], "/cards": cartes}


def test_les_commentaires_sont_recuperes_sans_une_requete_par_carte():
    session = FakeSession(_routes_board(10))
    cartes = _client(session).get_board_cards("b1")
    assert len(cartes) == 10
    assert cartes[0].comments[0].text == "commentaire 0"
    # 1 requete customFields + 1 requete cards (+ eventuelle page suivante)
    assert len(session.appels) <= 3, session.appels
    assert not any("/actions" in u for u in session.appels), session.appels


# --- 12 : pagination --------------------------------------------------------

def test_le_client_pagine_au_dela_du_plafond_de_l_api():
    page1 = [{"id": "c%d" % i, "name": "n%d" % i, "labels": [], "actions": []}
             for i in range(1000)]
    page2 = [{"id": "z1", "name": "derniere", "labels": [], "actions": []}]
    pages = [page1, page2, []]
    session = FakeSession({})

    def get(url, params=None, timeout=None):
        session.appels.append(url)
        if "/customFields" in url:
            return _reponse(url, 200, [])
        return _reponse(url, 200, pages.pop(0) if pages else [])

    session.get = get
    cartes = _client(session).get_board_cards("b1", with_comments=False)
    assert len(cartes) == 1001
    assert cartes[-1].name == "derniere"


def test_la_resolution_suit_le_type_declare_et_non_l_ordre_des_cles():
    """Tue le mutant qui rendrait la PREMIERE valeur du dict.

    Avec une seule cle, `next(iter(value.values()))` donne la meme reponse que
    la resolution par type : le test ne prouverait rien. Il faut un dict a
    plusieurs cles dont la premiere n'est PAS la valeur semantique.
    """
    item = {"value": {"text": "libelle-parasite", "checked": "true"}}
    assert _resolve_custom_field_value(item, {"type": "checkbox"}) == "true"

    item = {"value": {"text": "12 jours", "number": "12"}}
    assert _resolve_custom_field_value(item, {"type": "number"}) == "12"


def test_un_champ_number_a_zero_n_est_pas_rendu_vide():
    assert _resolve_custom_field_value({"value": {"number": "0"}}, {"type": "number"}) == "0"
