from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import json

with open(r"C:\Users\KUMARAGURU\Desktop\Presidency-project\FAqs intent.json", encoding="utf-8") as f:
    faq_data = json.load(f)["conversations"]

training_data = []
for faq in faq_data:
    question = faq["topic"]
    answer = faq["response"]
    training_data.append(question)
    training_data.append(answer)

chatbot = ChatBot(
    "FAQBot",
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch"
        }
    ],
    read_only=True,
)

trainer = ListTrainer(chatbot)
trainer.train(training_data)

print("FAQBot: Hi! Ask me anything or type 'exit' to quit.")
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("FAQBot: Goodbye!")
        break
    response = chatbot.get_response(user_input)
    print("FAQBot:", response)
