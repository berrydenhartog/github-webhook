from collections.abc import Sequence
from typing import Any

from fastapi.exceptions import ValidationException


class MyappValidationException(ValidationException):
    def __init__(self, errors: Sequence[Any]) -> None:
        self._errors = errors
        super().__init__(errors)


class MyappValueExporterError(ValueError):
    def __init__(self, exporter: str) -> None:  # pragma: no cover
        super().__init__(f"Unknown exporter: {exporter}")


class MyappValueEnricherError(ValueError):
    def __init__(self, enricher: str) -> None:  # pragma: no cover
        super().__init__(f"Unknown enricher: {enricher}")
