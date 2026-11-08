import unittest

from chatbot.conversation import Conversation
from chatbot.engine import ChatEngine


class EchoEngine(ChatEngine):
    def __init__(self):
        self.prompts = []

    def generate(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return f"reply {len(self.prompts)}"


class TestConversation(unittest.TestCase):
    def test_first_prompt_has_no_history(self):
        conversation = Conversation(EchoEngine())
        self.assertEqual(conversation.build_prompt("Hi"), "User: Hi\nBot:")

    def test_reply_returns_engine_output_and_updates_history(self):
        conversation = Conversation(EchoEngine())
        self.assertEqual(conversation.reply("Hi"), "reply 1")
        self.assertEqual(conversation.history, ["User: Hi", "Bot: reply 1"])

    def test_prompt_includes_previous_turns(self):
        engine = EchoEngine()
        conversation = Conversation(engine)
        conversation.reply("Hi")
        conversation.reply("How are you?")
        self.assertEqual(engine.prompts[-1], "User: Hi\nBot: reply 1\nUser: How are you?\nBot:")

    def test_history_is_limited(self):
        conversation = Conversation(EchoEngine(), max_history_lines=4)
        for i in range(5):
            conversation.reply(f"msg {i}")
        self.assertEqual(conversation.history, ["User: msg 3", "Bot: reply 4", "User: msg 4", "Bot: reply 5"])

    def test_initial_history_is_trimmed(self):
        conversation = Conversation(EchoEngine(), history=[str(i) for i in range(10)], max_history_lines=6)
        self.assertEqual(conversation.history, ["4", "5", "6", "7", "8", "9"])


if __name__ == "__main__":
    unittest.main()
