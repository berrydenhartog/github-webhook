import logging

import httpx
from pydantic import BaseModel, field_validator, model_validator
from pydantic.networks import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

from ..contants import GITHUB_EVENTS
from .baseclient import BaseClient

logger = logging.getLogger(__name__)


class MattermostclientSettings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore", env_file="mattermost.env", yaml_file="mattermost.yaml", env_prefix="MATTERMOST_"
    )

    DEFAULT_CHANNEL: str | None = None
    EVENT_CHANNEL_MAPPING: dict[str, str] = {}

    @model_validator(mode="after")
    def _enforce_allowed_logging_levels(self: "MattermostclientSettings") -> "MattermostclientSettings":
        for event in self.EVENT_CHANNEL_MAPPING:
            if event not in GITHUB_EVENTS:
                raise Exception(f"Invalid event type {event} in MATTERMOST_EVENT_CHANNEL_MAPPING")  # noqa: TRY002
        return self


class MattermostWebhookModel(BaseModel):
    text: str  # markdown formatted text
    username: str | None = None
    icon_url: HttpUrl | None = None
    channel: str | None = None
    icon_emoji: str | None = None
    # attachments:   not included for now
    type: str | None = None
    props: dict[str, str] | None = None
    priority: str | None = None

    @field_validator("type")
    @classmethod
    def check_type(cls, v: str) -> str:  # noqa: ANN102
        if not v.startswith("custom_"):  # pragma: no cover
            raise ValueError()
        return v  # pragma: no cover

    @field_validator("priority")
    @classmethod
    def check_priority(cls, v: str) -> str:  # noqa: ANN102
        if v not in ("urgent", "important", "standard"):  # pragma: no cover
            raise ValueError()
        return v  # pragma: no cover


class MattermostClient(BaseClient):
    def __init__(self, url: str, retries: int = 5, timeout: int = 1) -> None:
        self.url = url
        self.transport = httpx.AsyncHTTPTransport(retries=retries)
        self.client = httpx.AsyncClient(transport=self.transport, timeout=timeout)
        self.settings = MattermostclientSettings()

    async def handle_event(self, event: str, data: str) -> None:
        channel = None
        if self.settings.DEFAULT_CHANNEL:
            channel = self.settings.DEFAULT_CHANNEL

        if event in self.settings.EVENT_CHANNEL_MAPPING:
            channel = self.settings.EVENT_CHANNEL_MAPPING[event]

        mater_most_model = MattermostWebhookModel(text=data, channel=channel)

        logger.debug(f"Sending message to Mattermost: {mater_most_model.model_dump()}")

        response = await self.client.post(self.url, json=mater_most_model.model_dump())

        logger.debug(f"Response from Mattermost: {response.status_code}")

        if response.status_code >= 400:
            logger.warning(f"Failed to send message to Mattermost: {data}")
