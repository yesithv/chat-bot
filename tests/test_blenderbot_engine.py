import os
import unittest


@unittest.skipUnless(os.environ.get("RUN_MODEL_TESTS") == "1", "set RUN_MODEL_TESTS=1 to load the real model")
class TestBlenderBotEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from chatbot.implementations.blenderbot_engine import BlenderBotEngine

        cls.engine = BlenderBotEngine()

    def test_generates_non_empty_reply(self):
        reply = self.engine.generate("User: Hello, how are you?\nBot:")
        self.assertIsInstance(reply, str)
        self.assertTrue(reply)

    def test_handles_prompt_longer_than_model_limit(self):
        reply = self.engine.generate("User: " + "tell me a story " * 200 + "\nBot:")
        self.assertIsInstance(reply, str)


if __name__ == "__main__":
    unittest.main()
