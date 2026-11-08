import os
import secrets

from flask import Flask, jsonify, render_template, request, session
from flask_cors import CORS

from chatbot.conversation import Conversation
from chatbot.engine import ChatEngine

MAX_PROMPT_LENGTH = 500


def create_app(engine: ChatEngine) -> Flask:
    app = Flask(__name__)
    # Signs the session cookie that stores each user's conversation history
    app.secret_key = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
    CORS(app)

    @app.get('/')
    def home():
        return render_template('index.html')

    @app.post('/chatbot')
    def chat():
        data = request.get_json(silent=True) or {}
        prompt = data.get('prompt')

        if not isinstance(prompt, str) or not prompt.strip():
            return jsonify(error='Invalid message! Please type something.'), 400
        if len(prompt) > MAX_PROMPT_LENGTH:
            return jsonify(error=f'Message too long! Maximum {MAX_PROMPT_LENGTH} characters.'), 400

        conversation = Conversation(engine, session.get('history'))
        response = conversation.reply(prompt.strip())
        session['history'] = conversation.history

        return jsonify(response=response)

    return app


if __name__ == '__main__':
    from chatbot.implementations.blenderbot_engine import BlenderBotEngine

    create_app(BlenderBotEngine()).run()