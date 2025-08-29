from flask import Flask, render_template, request, jsonify
from services.open_ai_services import ask_openai

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    response = ask_openai(user_message)
    return jsonify({"reply": response})

if __name__ == "__main__":
    app.run(debug=True)
