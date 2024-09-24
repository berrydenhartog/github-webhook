from abc import ABC, abstractmethod


class BaseExporter(ABC):
    @abstractmethod
    async def handle_event(self, event: str, data: str) -> None:
        """This is an abstract method to write a message to a chat service."""
