from flask import Flask, request, render_template
from flask_cors import CORS
from bot import generate_response

app = Flask(__name__)
CORS(app)

conversation_history = []

@app.route('/chatbot', methods = ['POST'])
def handle_prompt():
    # Read prompt from HTTP request body
    data = request.get_json()
    input_text = data['prompt']

    # Keep only the recent conversation
    conversation_history[:] = conversation_history[-6:]

    # Create conversation history string
    history = "\n".join(conversation_history)
    prompt = history + f"\nUser: {input_text}\nBot:"

    response = generate_response(prompt)

    # Add interaction to conversation history
    conversation_history.append(f"User: {input_text}")
    conversation_history.append(f"Bot : {response}")

    return response

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()