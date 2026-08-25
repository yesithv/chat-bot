from bot import generate_response

print('Chatbot ready! (type exit to quit)\n')

conversation_history = []

while True:
    conversation_history = conversation_history[-6:]
    history_string = "\n".join(conversation_history)

    input_text = input('> ')
    if input_text.lower() == 'exit':
        break

    prompt = history_string + f"\n User: {input_text} \n Bot:"
    response = generate_response(prompt)

    conversation_history.append(f'User: {input_text}')
    conversation_history.append(f' Bot: {response}')

    print(f"Bot: {response}")
