from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import json

# Load simplified question-answer pairs
with open("FAqs intent.json", encoding="utf-8") as f:
    qa_data = json.load(f)

# Prepare training pairs
training_data = []
for item in qa_data:
    question = item["question"]
    answer = item["answer"]
    training_data.append([question, answer])

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

trainer = ListTrainer(chatbot)
for pair in training_data:
    trainer.train(pair)

# Start chat
print("FAQBot: Hi! Ask me anything or type 'exit' to quit.")
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("FAQBot: Goodbye!")
        break
    response = chatbot.get_response(user_input)
    if float(response.confidence) < 0.3:
        print("FAQBot: I'm not sure how to help with that. Could you try asking in a different way?")
    else:
        print("FAQBot:", response)
