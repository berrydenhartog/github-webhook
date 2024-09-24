from abc import ABC, abstractmethod
from typing import Any


class BaseEnricher(ABC):
    @abstractmethod
    async def handle_event(self, event: str, data: dict[str, Any]) -> dict[str, Any]:
        """This is an abstract method to handle to enriching of events."""
        return data
