def chatbot_response(transcript: str) -> str:
    rules = {
        "hello": "Hi there! How can I help you?",
        "problem": "Can you describe your problem in more detail?",
        "account": "I can help you with your account issues.",
        "password": "Would you like to reset your password?",
        "goodbye": "Goodbye! Have a nice day!"
    }

    response = []
    transcript_lower = transcript.lower()

    for keyword, reply in rules.items():
        if keyword in transcript_lower:
            response.append(reply)

    if not response:
        return "I'm sorry, I didn't understand that. Could you say it differently?"

    return " ".join(response)