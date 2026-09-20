"""Client HTTP lecture seule pour l'API Trello.

Portée : cartes d'un board donné, avec leurs labels ("tags"), leurs custom
fields résolus (nom + valeur, y compris les champs de type liste déroulante)
et leurs commentaires. Authentification par clé API + token, jamais en dur —
`TrelloClient.from_env()` les lit dans TRELLO_API_KEY / TRELLO_TOKEN (voir
docs/trello-api-setup.md pour les obtenir).
"""
from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from typing import Optional

import requests

API_BASE = "https://api.trello.com/1"

#: Trello limite à 100 requêtes / 10 s par token. Un 429 est retenté, borné.
MAX_TENTATIVES = 4
BACKOFF_INITIAL = 1.0
STATUTS_RETENTES = (429, 500, 502, 503, 504)
#: Plafond implicite de l'API sur /boards/{id}/cards.
TAILLE_PAGE = 1000


class TrelloAuthError(RuntimeError):
    """Clé API ou token Trello manquant."""


class TrelloSchemaError(RuntimeError):
    """Une réponse de l'API n'a pas la forme attendue.

    Remplace le `KeyError` brut : porte le champ manquant ET l'identifiant de
    la carte ou de l'action en cause, seule information qui permet de savoir
    où la lecture s'est arrêtée.
    """


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

    def _secrets(self) -> tuple:
        return (self._auth["key"], self._auth["token"])

    def _get(self, path: str, **params):
        attente = BACKOFF_INITIAL
        derniere = None
        for tentative in range(MAX_TENTATIVES):
            response = self._session.get(
                f"{API_BASE}{path}", params={**self._auth, **params}, timeout=30
            )
            try:
                response.raise_for_status()
            except requests.HTTPError as exc:
                derniere = _redacted_http_error(exc, self._secrets())
                if response.status_code not in STATUTS_RETENTES:
                    raise derniere from None
                if tentative == MAX_TENTATIVES - 1:
                    raise derniere from None
                time.sleep(_delai_retry(response, attente))
                attente *= 2
                continue
            return response.json()
        raise derniere  # pragma: no cover - inatteignable, la boucle sort avant

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
        """Commentaires d'UNE carte — un appel réseau.

        `get_board_cards` ne passe plus par ici : elle demande les commentaires
        dans la requête de board (`actions=commentCard`), ce qui supprime le
        N+1. Méthode conservée pour la lecture d'une carte isolée.
        """
        actions = self._get(f"/cards/{card_id}/actions", filter="commentCard")
        return _construire_commentaires(actions, card_id)

    def get_board_cards(self, board_id: str, with_comments: bool = True) -> list:
        """Cartes d'un board, avec labels, custom fields résolus et commentaires.

        Deux requêtes par page (définitions des custom fields une seule fois,
        puis une requête de cartes paginée) au lieu de 2 + N : les commentaires
        sont demandés en même temps que les cartes.
        """
        custom_field_defs = self.get_board_custom_fields(board_id)
        cards = []
        for raw in self._iter_raw_cards(board_id, with_comments):
            card_id = _champ(raw, "id", "carte", "<sans id>")
            labels = [label["name"] for label in raw.get("labels", []) if label.get("name")]
            custom_fields = {}
            for item in raw.get("customFieldItems", []):
                field_id = _champ(item, "idCustomField", "custom field de la carte", card_id)
                field_def = custom_field_defs.get(field_id, {})
                field_name = field_def.get("name", field_id)
                custom_fields[field_name] = _resolve_custom_field_value(item, field_def)
            comments = (
                _construire_commentaires(raw.get("actions", []), card_id)
                if with_comments
                else []
            )
            cards.append(
                Card(
                    id=card_id,
                    name=_champ(raw, "name", "carte", card_id),
                    labels=labels,
                    custom_fields=custom_fields,
                    comments=comments,
                )
            )
        return cards

    def _iter_raw_cards(self, board_id: str, with_comments: bool):
        """Parcourt TOUTES les pages de cartes du board.

        Sans pagination, l'appelant ne voit jamais rien au-delà du plafond
        implicite de l'API (constat d'audit 12). Trello pagine par `before`,
        sur l'identifiant de la dernière carte reçue.
        """
        params = {
            "fields": "name,labels",
            "customFieldItems": "true",
            "limit": str(TAILLE_PAGE),
        }
        if with_comments:
            params["actions"] = "commentCard"
        before = None
        while True:
            page_params = dict(params)
            if before:
                page_params["before"] = before
            page = self._get(f"/boards/{board_id}/cards", **page_params)
            if not page:
                return
            for raw in page:
                yield raw
            if len(page) < TAILLE_PAGE:
                return
            before = page[-1].get("id")
            if not before:
                return


REDACTED = "***REDACTED***"


def redact_secrets(text: str, secrets) -> str:
    """Remplace toute occurrence d'un secret par un masque.

    Les secrets courts ou vides sont ignorés : masquer "" remplacerait tout.
    """
    for secret in secrets:
        if secret and len(secret) >= 8:
            text = text.replace(secret, REDACTED)
    return text


def _redacted_http_error(exc: "requests.HTTPError", secrets) -> "requests.HTTPError":
    """Reconstruit une HTTPError dont ni le message ni l'URL ne portent de secret.

    `requests` place la clé et le token dans la query string, donc dans
    `response.url`, que `raise_for_status()` recopie dans le message de
    l'exception — donc dans les logs, les traces et les remontées d'erreur.
    """
    response = getattr(exc, "response", None)
    if response is not None and getattr(response, "url", None):
        response.url = redact_secrets(str(response.url), secrets)
    request = getattr(exc, "request", None)
    if request is not None and getattr(request, "url", None):
        request.url = redact_secrets(str(request.url), secrets)
    message = redact_secrets("".join(str(a) for a in exc.args) or str(exc), secrets)
    return requests.HTTPError(message, response=response, request=request)


def _champ(source: dict, cle: str, quoi: str, contexte: str):
    """Lit une clé obligatoire, ou lève une erreur qui dit où on en était."""
    if cle not in source:
        raise TrelloSchemaError(
            "champ '%s' absent de la reponse Trello (%s : %s)" % (cle, quoi, contexte)
        )
    return source[cle]


def _delai_retry(response, defaut: float) -> float:
    """Honore l'en-tête Retry-After quand Trello le fournit."""
    entetes = getattr(response, "headers", None) or {}
    try:
        return max(float(entetes.get("Retry-After", defaut)), 0.0)
    except (TypeError, ValueError):
        return defaut


def _construire_commentaires(actions, card_id: str) -> list:
    return [
        Comment(
            id=_champ(a, "id", "action de la carte", card_id),
            text=_champ(
                _champ(a, "data", "action de la carte", card_id),
                "text",
                "commentaire de la carte",
                card_id,
            ),
            author=a.get("memberCreator", {}).get("fullName", ""),
            date=a.get("date", ""),
        )
        for a in actions
    ]


#: Clé porteuse de la valeur dans `item["value"]`, par type de custom field.
CLE_PAR_TYPE = {
    "text": "text",
    "number": "number",
    "date": "date",
    "checkbox": "checked",
}


def _resolve_custom_field_value(item: dict, field_def: dict) -> str:
    """Valeur d'un custom field, résolue par le TYPE déclaré du champ.

    L'ancienne version rendait `next(iter(value.values()))` : la première clé
    du dict quelle qu'elle soit, sans garantie d'ordre sémantique sur un champ
    à plusieurs clés. Elle confondait aussi « valeur fausse » et « vide » —
    un dict `{"checked": "false"}` est VRAI en Python.
    """
    value = item.get("value")
    if isinstance(value, dict) and value:
        cle = CLE_PAR_TYPE.get(field_def.get("type"))
        if cle is not None:
            brute = value.get(cle)
            return "" if brute is None else str(brute)
        return str(next(iter(value.values()), ""))
    id_value = item.get("idValue")
    if id_value:
        return field_def.get("options", {}).get(id_value, id_value)
    return ""
