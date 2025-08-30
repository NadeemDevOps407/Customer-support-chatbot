from flask import Flask, render_template, request, jsonify
from services.open_ai_services import ask_openai

app = Flask(__name__)

chat_history = [{"role": "system", "content": "You are a helpful assistant."}]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        # Add user message to history
        chat_history.append({"role": "user", "content": user_message})

        # Get OpenAI reply using history
        response_text = ask_openai(chat_history)

        # Add assistant reply to history
        chat_history.append({"role": "assistant", "content": response_text})

        return jsonify({"reply": response_text})

    except Exception as e:
        print("❌ ERROR:", e)   # log error in Flask console
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
