from abc import ABC, abstractmethod


class BaseClient(ABC):
    @abstractmethod
    async def handle_event(self, event: str, data: str) -> None:
        """This is an abstract method to write a message to a chat service."""
