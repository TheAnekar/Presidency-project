import json

# Load intents with UTF-8 encoding
with open('FAqs intent.json', 'r', encoding='utf-8') as file:
    intents = json.load(file)

def find_response(user_input):
    user_input = user_input.lower()

    for intent in intents:
        topic = intent["topic"].lower()
        if topic in user_input:
            return intent["response"]

    return "Sorry, I couldn't find an answer for that. Please try asking differently."

# Run the chatbot
print("👩‍⚖️ Family Law Bot (type 'exit' to quit)")
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    response = find_response(user_input)
    print("Bot:", response)
