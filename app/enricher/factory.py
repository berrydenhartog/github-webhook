import logging
from typing import Literal

from ..exceptions import MyappValueEnricherError
from .baseenricher import BaseEnricher
from .github import GithubEnricher

logger = logging.getLogger(__name__)

Enrichers = Literal["github"]


def enricher_factory(enricher_ids: Enrichers | list[Enrichers]) -> list[BaseEnricher]:
    logger.debug(f"Creating enricher of type {enricher_ids}")

    if not isinstance(enricher_ids, list):
        enricher_ids = [enricher_ids]

    enrichers: list[BaseEnricher] = []

    for enricher_id in enricher_ids:
        if enricher_id == "github":
            enrichers.append(GithubEnricher())

        else:  # pragma: no cover
            raise MyappValueEnricherError(str(enricher_id))

    return enrichers
