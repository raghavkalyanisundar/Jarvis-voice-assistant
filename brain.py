import ollama

conversation = []

def ask_jarvis(user_input):

    conversation.append(
        {
            'role': 'user',
            'content': user_input
        }
    )
    try:
        response = ollama.chat(
        model='llama3',
        messages=conversation
    )
        # extracts the message from the Ai safely to give the response
        reply = response.get('message',{}).get('content',"")

        if not reply or reply.strip() =="":
            reply = "I'm here, but didn't generate a response."

    except Exception as e:
        reply="I had trouble generating a response."

    conversation.append(
        {
            'role': 'assistant',
            'content': reply
        }
    )

    return reply