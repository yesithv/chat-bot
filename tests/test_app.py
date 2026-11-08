import unittest

from app import MAX_PROMPT_LENGTH, create_app
from chatbot.engine import ChatEngine


class FakeEngine(ChatEngine):
    def __init__(self):
        self.prompts = []

    def generate(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return "Hello there!"


class TestApp(unittest.TestCase):
    def setUp(self):
        self.engine = FakeEngine()
        self.client = create_app(self.engine).test_client()

    def test_home_renders_chat_ui(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"AI Chat Assistant", response.data)

    def test_chatbot_returns_reply(self):
        response = self.client.post("/chatbot", json={"prompt": "Hi"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"response": "Hello there!"})

    def test_history_is_kept_per_session(self):
        self.client.post("/chatbot", json={"prompt": "Hi"})
        self.client.post("/chatbot", json={"prompt": "Again"})
        self.assertIn("User: Hi\nBot: Hello there!", self.engine.prompts[-1])

        other_client = self.client.application.test_client()
        other_client.post("/chatbot", json={"prompt": "New user"})
        self.assertEqual(self.engine.prompts[-1], "User: New user\nBot:")

    def test_rejects_invalid_prompts(self):
        for body in ({}, {"prompt": ""}, {"prompt": "   "}, {"prompt": 123}, {"prompt": "x" * (MAX_PROMPT_LENGTH + 1)}):
            with self.subTest(body=body):
                response = self.client.post("/chatbot", json=body)
                self.assertEqual(response.status_code, 400)
                self.assertIn("error", response.get_json())
        self.assertEqual(self.engine.prompts, [])

    def test_rejects_non_json_body(self):
        response = self.client.post("/chatbot", data="hello")
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
