import logging

from .baseclient import BaseClient

logger = logging.getLogger(__name__)


class DummyClient(BaseClient):
    async def handle_event(self, event: str, data: str) -> None:
        logger.debug(f"Dummy client received data: {data}")
