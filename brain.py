import ollama

conversation = []

def ask_jarvis(user_input):

    conversation.append(
        {
            'role': 'user',
            'content': user_input
        }
    )

    response = ollama.chat(
        model='llama3',
        messages=conversation
    )

    reply = response['message']['content']

    conversation.append(
        {
            'role': 'assistant',
            'content': reply
        }
    )

    return reply