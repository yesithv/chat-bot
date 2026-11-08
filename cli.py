from chatbot.conversation import Conversation
from chatbot.implementations.blenderbot_engine import BlenderBotEngine


def main() -> None:
    conversation = Conversation(BlenderBotEngine())
    print('Chatbot ready! (type exit to quit)\n')

    while True:
        try:
            user_input = input('> ').strip()
        except (EOFError, KeyboardInterrupt):
            break

        if user_input.lower() == 'exit':
            break
        if not user_input:
            continue

        print(f'Bot: {conversation.reply(user_input)}')


if __name__ == '__main__':
    main()
