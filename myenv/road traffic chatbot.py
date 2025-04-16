import json
import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s?]', '', text)
    return text

def create_intent_map(data):
    intent_map = {}
    for item in data:
        intent = item['intent']
        for question in item['questions']:
            cleaned_question = clean_text(question)
            intent_map[cleaned_question] = intent
    return intent_map

def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def get_response(user_input, data, intent_map):
    cleaned_input = clean_text(user_input)
    
   
    matched_intent = intent_map.get(cleaned_input)
    
    if matched_intent:
        for item in data:
            if item['intent'] == matched_intent:
                return item['answer']
    else:
    
        for item in data:
            for question in item['questions']:
                cleaned_question = clean_text(question)
                if any(keyword in cleaned_input.split() for keyword in cleaned_question.split()):
                    return item['answer']
        
        return "I'm not sure how to answer that. Please try another question."

def main():
    file_path = '/home/ashraf/Documents/Presidency-project/myenv/intent.json'
    data = load_data(file_path)
    intent_map = create_intent_map(data)
    
    print("Chatbot is ready. Type 'quit' to exit.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
        
        response = get_response(user_input, data, intent_map)
        print("Bot:", response)

if __name__ == "__main__":
    main()
