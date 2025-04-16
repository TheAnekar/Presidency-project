from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import json

# Load the improved JSON file
with open("/home/ashraf/Documents/Presidency-project/FAqs intent.json", encoding="utf-8") as f:
    intents_data = json.load(f)["intents"]

# Prepare training data
training_data = []
for intent in intents_data:
    tag = intent["tag"]
    patterns = intent.get("patterns", [])
    responses = intent.get("responses", [])

    for pattern in patterns:
        for response in responses:
            training_data.append(pattern)
            training_data.append(response)

# Initialize chatbot
chatbot = ChatBot(
    "FAQBot",
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch"
        }
    ],
    read_only=True
)

# Train chatbot
trainer = ListTrainer(chatbot)
trainer.train(training_data)

# Chat loop
print("FAQBot: Hi! Ask me anything or type 'exit' to quit.")
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("FAQBot: Goodbye!")
        break
    response = chatbot.get_response(user_input)
    print("FAQBot:", response)
