import logging

from .baseexporter import BaseExporter

logger = logging.getLogger(__name__)


class DummyExporter(BaseExporter):
    async def handle_event(self, event: str, data: str) -> None:
        logger.info(f"Dummy exporter received - {event}: {data}")
