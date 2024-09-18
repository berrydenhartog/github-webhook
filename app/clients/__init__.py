from typing import Literal

from .baseclient import BaseClient
from .factory import client_factory

__all__ = ["client_factory", "Clients", "BaseClient"]

Clients = Literal["mattermost", "dummy"]
