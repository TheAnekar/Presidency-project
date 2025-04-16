# chatbot_core.py
import json
import re
import difflib
from spellchecker import SpellChecker
import os

# Initialize spell checker
spell = SpellChecker()

# Load Q&A Data
def load_data(file_path="FAqs intent.json"):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Cannot find '{file_path}'. Please ensure the file exists.")
    
    with open(file_path, encoding="utf-8") as f:
        qa_data = json.load(f)

    qa_dict = {item["question"]: item["answer"] for item in qa_data}
    return qa_dict

qa_dict = load_data()

# Spell correction
def correct_spelling(text):
    words = text.split()
    corrected_words = [
        spell.correction(word) if word.lower() not in spell else word
        for word in words
    ]
    return ' '.join(corrected_words)

# Best-match response engine
def find_best_match(user_input):
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

    return best_answer if best_score >= 0.5 else "I'm not sure how to help with that. Please rephrase your question."
