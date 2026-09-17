"""Tests unitaires du client Trello — pas d'appel réseau réel (aucun credential
disponible pour l'instant, voir docs/trello-api-setup.md)."""
from unittest.mock import MagicMock

import pytest

from trello_client.client import TrelloAuthError, TrelloClient


def _mock_session(responses_by_path):
    session = MagicMock()

    def fake_get(url, params=None, timeout=None):
        for path, payload in responses_by_path.items():
            if url.endswith(path):
                response = MagicMock()
                response.json.return_value = payload
                response.raise_for_status.return_value = None
                return response
        raise AssertionError(f"URL non mockée : {url}")

    session.get.side_effect = fake_get
    return session


def test_missing_credentials_raise():
    with pytest.raises(TrelloAuthError):
        TrelloClient(api_key="", token="")


def test_get_board_cards_resolves_labels_custom_fields_and_comments():
    board_id = "board123"
    session = _mock_session(
        {
            f"/boards/{board_id}/customFields": [
                {
                    "id": "cf1",
                    "name": "Priorité",
                    "options": [{"id": "opt1", "value": {"text": "Haute"}}],
                }
            ],
            f"/boards/{board_id}/cards": [
                {
                    "id": "card1",
                    "name": "Corriger le bug X",
                    "labels": [{"name": "bug"}, {"name": "urgent"}],
                    "customFieldItems": [{"idCustomField": "cf1", "idValue": "opt1"}],
                }
            ],
            "/cards/card1/actions": [
                {
                    "id": "action1",
                    "date": "2026-09-15T10:00:00.000Z",
                    "data": {"text": "En cours"},
                    "memberCreator": {"fullName": "Claude Camus"},
                }
            ],
        }
    )
    client = TrelloClient(api_key="k", token="t", session=session)

    cards = client.get_board_cards(board_id)

    assert len(cards) == 1
    card = cards[0]
    assert card.name == "Corriger le bug X"
    assert card.labels == ["bug", "urgent"]
    assert card.custom_fields == {"Priorité": "Haute"}
    assert len(card.comments) == 1
    assert card.comments[0].text == "En cours"
    assert card.comments[0].author == "Claude Camus"


def test_get_board_cards_without_comments_skips_actions_call():
    board_id = "board123"
    session = _mock_session(
        {
            f"/boards/{board_id}/customFields": [],
            f"/boards/{board_id}/cards": [{"id": "card1", "name": "Carte", "labels": []}],
        }
    )
    client = TrelloClient(api_key="k", token="t", session=session)

    cards = client.get_board_cards(board_id, with_comments=False)

    assert cards[0].comments == []
    session.get.assert_called()
    called_paths = [c.args[0] for c in session.get.call_args_list]
    assert not any("/actions" in p for p in called_paths)
