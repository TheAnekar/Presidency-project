import json
import re
import difflib
from spellchecker import SpellChecker

spell = SpellChecker()

with open("FAqs intent.json", encoding="utf-8") as f:
    qa_data = json.load(f)

qa_dict = {item["question"]: item["answer"] for item in qa_data}
questions = list(qa_dict.keys())

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

print("FAQBot: Hi! Ask me anything or type 'exit' to quit.")
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("FAQBot: Goodbye!")
        break
    best_answer = find_best_match(user_input, qa_dict)
    if best_answer:
        print("FAQBot:", best_answer)
    else:
        print("FAQBot: I'm not sure how to help with that. Could you try asking in a different way?")
