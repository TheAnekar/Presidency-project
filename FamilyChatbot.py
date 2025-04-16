import json
import re
import difflib
from spellchecker import SpellChecker

spell = SpellChecker()

with open("FAqs intent.json", encoding="utf-8") as f:
    qa_data = json.load(f)

qa_dict = {item["question"]: item["answer"] for item in qa_data}
questions = list(qa_dict.keys())

keyword_phrases = set()
for q in questions:
    
    words = q.lower().split()
    for i in range(len(words) - 1):
        phrase = ' '.join(words[i:i+2])
        keyword_phrases.add(phrase)

phrase_freq = {}
for phrase in keyword_phrases:
    for q in questions:
        if phrase in q.lower():
            phrase_freq[phrase] = phrase_freq.get(phrase, 0) + 1

top_phrases = sorted(phrase_freq.items(), key=lambda x: x[1], reverse=True)[:10]
top_keywords_list = [f"{i+1}. {phrase[0].capitalize()}" for i, phrase in enumerate(top_phrases)]

def correct_spelling(text):
    words = text.split()
    corrected_words = [spell.correction(word) if word.lower() not in spell else word for word in words]
    return ' '.join(corrected_words)

def find_best_match(user_input, qa_dict):
    user_input = correct_spelling(user_input)
    user_input_lower = user_input.lower()
    user_words = set(re.findall(r'\b\w{3,}\b', user_input_lower))

    best_score = 0
    best_answer = None

    for question, answer in qa_dict.items():
        question_lower = question.lower()
        question_words = set(re.findall(r'\b\w{3,}\b', question_lower))

        common_words = user_words.intersection(question_words)
        word_overlap_score = len(common_words) / max(len(question_words), 1)

        fuzzy_score = difflib.SequenceMatcher(None, user_input_lower, question_lower).ratio()

        combined_score = (0.5 * word_overlap_score) + (0.5 * fuzzy_score)

        if combined_score > best_score:
            best_score = combined_score
            best_answer = answer

    return best_answer if best_score >= 0.5 else None

print("FAQBot: Hi! Ask me anything or type 'exit' to quit. Type '/help' to see common keywords.")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("FAQBot: Goodbye!")
        break
    elif user_input.lower() == "/help":
        print("\nHere are some keyword sets and sample responses:")

        answer_map = {}
        for item in qa_data:
            question = item["question"]
            answer = item["answer"]
        
            key = ' '.join(answer.lower().split())[:100] 
            if key not in answer_map:
                answer_map[key] = {"answer": answer, "questions": []}
            answer_map[key]["questions"].append(question)

        for idx, (key, data) in enumerate(answer_map.items(), start=1):
            keywords = []
            for q in data["questions"]:
            
                words = q.lower().split()
                phrases = [' '.join(words[i:i+2]) for i in range(len(words) - 1)]
                keywords.extend(phrases)
            unique_keywords = sorted(set(keywords))[:3] 
            preview = ' '.join(data["answer"].split()[:10]) + "..."
            print(f"{idx}. Keywords: {', '.join(unique_keywords)} → {preview}")

        print()
        continue


    best_answer = find_best_match(user_input, qa_dict)
    if best_answer:
        print("FAQBot:", best_answer)
    else:
        print("FAQBot: I'm not sure how to help with that. Could you try asking in a different way?")