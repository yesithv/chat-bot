from abc import ABC, abstractmethod


class ChatEngine(ABC):
    """Common interface for any model that can produce a chatbot reply."""

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Return the bot reply for a prompt that already includes the conversation context."""
