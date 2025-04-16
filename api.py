from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot_core import find_best_match

app = Flask(__name__)
CORS(app)  # Allow requests from frontend

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "")
    response = find_best_match(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
