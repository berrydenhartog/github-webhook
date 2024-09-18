import secrets
from logging import _nameToLevel  # type: ignore[reportPrivateUsage]
from typing import Any

from pydantic import model_validator
from pydantic.networks import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

from .clients import Clients
from .exceptions import MyappValidationException


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file="prod.env", yaml_file="config.yaml")

    SECRET_KEY: str = secrets.token_urlsafe(32)
    LOGGING_LEVEL: str = "INFO"
    DEBUG: bool = False
    CLIENT_ID: Clients = "dummy"
    CLIENT_URL: HttpUrl | None = None
    GITHUB_WEBHOOK_SECRET: str | None = None

    @model_validator(mode="after")
    def _enforce_allowed_logging_levels(self: "Settings") -> "Settings":
        if self.LOGGING_LEVEL not in _nameToLevel:
            raise MyappValidationException(errors=["Invalid logging level"])

        return self


def get_settings(**kwargs: Any) -> Settings:  # noqa: ANN401
    return Settings(**kwargs)
