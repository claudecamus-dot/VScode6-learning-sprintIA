"""Audit finding (robustness): get_board_custom_fields must keep the field `type`."""
from tests.test_trello_robustesse import FakeSession, _client

BOARD_FIELDS = [
    {"id": "cf1", "idModel": "b1", "modelType": "board", "name": "Done",
     "type": "checkbox", "pos": 1},
    {"id": "cf2", "idModel": "b1", "modelType": "board", "name": "Priority",
     "type": "list", "pos": 2,
     "options": [{"id": "o1", "idCustomField": "cf2", "value": {"text": "High"}, "pos": 1}]},
]


def test_get_board_custom_fields_conserve_le_type():
    session = FakeSession({"/boards/b1/customFields": BOARD_FIELDS})
    defs = _client(session).get_board_custom_fields("b1")
    assert defs["cf1"]["type"] == "checkbox"
    assert defs["cf2"]["type"] == "list"


def test_flux_reel_checkbox_resolu_par_le_type():
    # value dict carrying an extra key first: only the declared type picks "checked".
    cards = [{"id": "c1", "name": "Card", "customFieldItems": [
        {"id": "i1", "idCustomField": "cf1", "idModel": "c1",
         "value": {"extra": "zzz", "checked": "true"}}]}]
    session = FakeSession({"/boards/b1/customFields": BOARD_FIELDS, "/boards/b1/cards": cards})
    out = _client(session).get_board_cards("b1", with_comments=False)
    assert out[0].custom_fields["Done"] == "true"
