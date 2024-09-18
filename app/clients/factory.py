import logging

from ..exceptions import MyappValueClientError
from .baseclient import BaseClient
from .dummy import DummyClient
from .mattermost import MattermostClient

logger = logging.getLogger(__name__)


def client_factory(client_type: str, url: str) -> BaseClient:
    logger.debug(f"Creating client of type {client_type}")

    if client_type == "mattermost":
        return MattermostClient(url=url)
    elif client_type == "dummy":
        return DummyClient()
    else:  # pragma: no cover
        raise MyappValueClientError(client_type)
