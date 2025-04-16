import json
with open("FAqs intent.json", "r") as f:
    faq_data = json.load(f)
intent_responses = {
    item["intent"]: item["response"] for item in faq_data["conversations"]
}
keywords_to_intents = {
    "alimony": "ask_alimony_info",
    "spousal support": "ask_alimony_info",
    "paternity": "ask_paternity_info",
    "collaborative": "ask_collaborative_divorce",
    "parenting": "ask_parenting_agreements",
    "restraining": "ask_restraining_orders",
    "house": "ask_who_gets_house",
    "child support": "ask_child_support_nonpayment",
    "adoption": "ask_relative_adoption",
    "modify alimony": "ask_change_alimony_amount",
    "move kids": "ask_ex_move_kids_out_of_state",
    "relocation": "ask_ex_move_kids_out_of_state",
    "DOCUMENTS TO BE CARRIED": "DOCUMENTS TO BE CARRIED"
}
def get_intent(user_input):
    user_input = user_input.lower()
    for keyword, intent in keywords_to_intents.items():
        if keyword in user_input:
            return intent
    return None
print(" Family Law Assistant Chatbot\n(Type 'exit' to quit)\n")

while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit']:
        break
    
    intent = get_intent(user_input)
    
    if intent and intent in intent_responses:
        print("Bot:", intent_responses[intent])
    else:
        print("Bot: I'm sorry, I don't have information on that topic. Can you try rephrasing?")
