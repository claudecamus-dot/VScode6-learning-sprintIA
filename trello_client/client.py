"""Client HTTP lecture seule pour l'API Trello.

Portée : cartes d'un board donné, avec leurs labels ("tags"), leurs custom
fields résolus (nom + valeur, y compris les champs de type liste déroulante)
et leurs commentaires. Authentification par clé API + token, jamais en dur —
`TrelloClient.from_env()` les lit dans TRELLO_API_KEY / TRELLO_TOKEN (voir
docs/trello-api-setup.md pour les obtenir).
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Optional

import requests

API_BASE = "https://api.trello.com/1"


class TrelloAuthError(RuntimeError):
    """Clé API ou token Trello manquant."""


@dataclass
class Comment:
    id: str
    text: str
    author: str
    date: str


@dataclass
class Card:
    id: str
    name: str
    labels: list = field(default_factory=list)
    custom_fields: dict = field(default_factory=dict)
    comments: list = field(default_factory=list)


class TrelloClient:
    """Client lecture seule pour un board Trello."""

    def __init__(self, api_key: str, token: str, session: Optional[requests.Session] = None):
        if not api_key or not token:
            raise TrelloAuthError("TRELLO_API_KEY et TRELLO_TOKEN sont requis")
        self._auth = {"key": api_key, "token": token}
        self._session = session or requests.Session()

    @classmethod
    def from_env(cls) -> "TrelloClient":
        return cls(
            api_key=os.environ.get("TRELLO_API_KEY", ""),
            token=os.environ.get("TRELLO_TOKEN", ""),
        )

    def _get(self, path: str, **params):
        response = self._session.get(
            f"{API_BASE}{path}", params={**self._auth, **params}, timeout=30
        )
        response.raise_for_status()
        return response.json()

    def get_board_custom_fields(self, board_id: str) -> dict:
        """Définitions des custom fields d'un board : id -> {name, options}."""
        fields = self._get(f"/boards/{board_id}/customFields")
        result = {}
        for f in fields:
            options = {
                opt["id"]: opt["value"]["text"]
                for opt in f.get("options", [])
                if "value" in opt
            }
            result[f["id"]] = {"name": f["name"], "options": options}
        return result

    def get_card_comments(self, card_id: str) -> list:
        actions = self._get(f"/cards/{card_id}/actions", filter="commentCard")
        return [
            Comment(
                id=a["id"],
                text=a["data"]["text"],
                author=a.get("memberCreator", {}).get("fullName", ""),
                date=a["date"],
            )
            for a in actions
        ]

    def get_board_cards(self, board_id: str, with_comments: bool = True) -> list:
        """Cartes d'un board, avec labels, custom fields résolus et commentaires."""
        custom_field_defs = self.get_board_custom_fields(board_id)
        raw_cards = self._get(
            f"/boards/{board_id}/cards",
            fields="name,labels",
            customFieldItems="true",
        )

        cards = []
        for raw in raw_cards:
            labels = [label["name"] for label in raw.get("labels", []) if label.get("name")]
            custom_fields = {}
            for item in raw.get("customFieldItems", []):
                field_def = custom_field_defs.get(item["idCustomField"], {})
                field_name = field_def.get("name", item["idCustomField"])
                custom_fields[field_name] = _resolve_custom_field_value(item, field_def)
            comments = self.get_card_comments(raw["id"]) if with_comments else []
            cards.append(
                Card(
                    id=raw["id"],
                    name=raw["name"],
                    labels=labels,
                    custom_fields=custom_fields,
                    comments=comments,
                )
            )
        return cards


def _resolve_custom_field_value(item: dict, field_def: dict) -> str:
    value = item.get("value")
    if value:
        return next(iter(value.values()), "")
    id_value = item.get("idValue")
    if id_value:
        return field_def.get("options", {}).get(id_value, id_value)
    return ""
