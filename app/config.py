from logging import _nameToLevel  # type: ignore[reportPrivateUsage]
from typing import Any

import jq
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from .clients import Clients
from .constants import FilterType, PermissionType
from .exceptions import MyappValidationException


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file="prod.env", yaml_file="config.yaml")

    LOGGING_LEVEL: str = "INFO"
    DEBUG: bool = False
    CLIENT_IDS: list[Clients] | Clients = ["dummy"]
    WEBHOOK_SECRET: str | None = None
    EVENT_FORMATS: dict[str, str] = {}
    EVENT_HEADER: str = "x-github-event"
    EVENT_FILTERS: dict[PermissionType, list[dict[FilterType, int | str | bool | float]]] = {}
    EVENT_TYPE_FILTERS: dict[PermissionType, list[str]] = {}

    @model_validator(mode="after")
    def _enforce_allowed_logging_levels(self: "Settings") -> "Settings":
        if self.LOGGING_LEVEL not in _nameToLevel:
            raise MyappValidationException(errors=["Invalid logging level"])

        return self

    @model_validator(mode="after")
    def _enforce_compilable_jq_filters(self: "Settings") -> "Settings":
        allow_filter = self.EVENT_FILTERS.get("ALLOW", [])
        deny_filter = self.EVENT_FILTERS.get("DENY", [])

        for filter in allow_filter:
            jq_filter = filter.get("FILTER")
            try:
                jq.compile(jq_filter)  # type: ignore
            except Exception as err:
                raise MyappValidationException(errors=[f"Invalid jq filter {jq_filter}"]) from err

        for filter in deny_filter:
            jq_filter = filter.get("FILTER")
            try:
                jq.compile(jq_filter)  # type: ignore
            except Exception as err:
                raise MyappValidationException(errors=[f"Invalid jq filter: {jq_filter}"]) from err

        return self


def get_settings(**kwargs: Any) -> Settings:  # noqa: ANN401
    return Settings(**kwargs)
