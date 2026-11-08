from chatbot.engine import ChatEngine

MAX_HISTORY_LINES = 6  # 3 user/bot exchanges


class Conversation:
    """Keeps a short rolling history and builds the prompt sent to the engine."""

    def __init__(self, engine: ChatEngine, history: list[str] | None = None,
                 max_history_lines: int = MAX_HISTORY_LINES):
        self._engine = engine
        self._max_history_lines = max_history_lines
        self.history = list(history or [])[-max_history_lines:]

    def build_prompt(self, user_input: str) -> str:
        return "\n".join([*self.history, f"User: {user_input}", "Bot:"])

    def reply(self, user_input: str) -> str:
        response = self._engine.generate(self.build_prompt(user_input))
        self.history = [*self.history, f"User: {user_input}", f"Bot: {response}"][-self._max_history_lines:]
        return response
