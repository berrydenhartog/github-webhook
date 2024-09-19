import logging
from typing import Literal

from ..exceptions import MyappValueClientError
from .baseclient import BaseClient
from .dummy import DummyClient
from .mattermost import MattermostClient

logger = logging.getLogger(__name__)

Clients = Literal["mattermost", "dummy"]


def client_factory(client_ids: Clients | list[Clients]) -> list[BaseClient]:
    logger.debug(f"Creating client of type {client_ids}")

    if not isinstance(client_ids, list):
        client_ids = [client_ids]

    clients: list[BaseClient] = []

    for client_id in client_ids:
        if client_id == "mattermost":
            clients.append(MattermostClient())
        elif client_id == "dummy":
            clients.append(DummyClient())
        else:  # pragma: no cover
            raise MyappValueClientError(str(client_ids))

    return clients
