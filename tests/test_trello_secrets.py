"""La cle API et le token ne doivent JAMAIS apparaitre dans un message d'erreur.

requests met les query params dans response.url ; raise_for_status() recopie cette
URL dans le message de l'HTTPError, donc dans les logs et les traces.
"""
import pytest
import requests

from trello_client.client import TrelloClient

FAKE_KEY = "FAKEKEY0000000000000000000000000"
FAKE_TOKEN = "FAKETOKEN1111111111111111111111111111111111111111111111111111111"


def _session_returning(status_code):
    session = requests.Session()

    def fake_get(url, params=None, timeout=None):
        response = requests.Response()
        response.status_code = status_code
        response.url = url + "?" + "&".join(f"{k}={v}" for k, v in (params or {}).items())
        response._content = b"{}"
        return response

    session.get = fake_get
    return session


def test_http_error_message_never_contains_key_or_token():
    client = TrelloClient(api_key=FAKE_KEY, token=FAKE_TOKEN, session=_session_returning(401))
    with pytest.raises(requests.HTTPError) as excinfo:
        client.get_board_custom_fields("board123")
    message = str(excinfo.value)
    assert FAKE_KEY not in message, message
    assert FAKE_TOKEN not in message, message
    assert "401" in message


def test_http_error_message_never_contains_secret_via_args_or_response_url():
    client = TrelloClient(api_key=FAKE_KEY, token=FAKE_TOKEN, session=_session_returning(429))
    with pytest.raises(requests.HTTPError) as excinfo:
        client.get_board_custom_fields("board123")
    blob = repr(excinfo.value.args) + str(
        getattr(excinfo.value, "response", None) and excinfo.value.response.url
    )
    assert FAKE_KEY not in blob, blob
    assert FAKE_TOKEN not in blob, blob
