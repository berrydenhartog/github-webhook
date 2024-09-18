from collections.abc import Sequence
from typing import Any

from fastapi.exceptions import ValidationException


class MyappValidationException(ValidationException):
    def __init__(self, errors: Sequence[Any]) -> None:
        self._errors = errors
        super().__init__(errors)


class MyappValueClientError(ValueError):
    def __init__(self, client: str) -> None:  # pragma: no cover
        self.client = f"Unknown client: {client}"
        super().__init__(client)
