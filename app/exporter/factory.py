import logging
from typing import Literal

from ..exceptions import MyappValueExporterError
from .baseexporter import BaseExporter
from .dummy import DummyExporter
from .mattermost import MattermostExporter

logger = logging.getLogger(__name__)

Exporters = Literal["mattermost", "dummy"]


def exporter_factory(exporter_ids: Exporters | list[Exporters]) -> list[BaseExporter]:
    logger.debug(f"Creating exporter of type {exporter_ids}")

    if not isinstance(exporter_ids, list):
        exporter_ids = [exporter_ids]

    exporters: list[BaseExporter] = []

    for exporter_id in exporter_ids:
        if exporter_id == "mattermost":
            exporters.append(MattermostExporter())
        elif exporter_id == "dummy":
            exporters.append(DummyExporter())
        else:  # pragma: no cover
            raise MyappValueExporterError(str(exporter_ids))

    return exporters
