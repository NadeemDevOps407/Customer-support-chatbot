from flask import Flask, render_template, request, jsonify
import services.open_ai_services as openai
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/voice", methods=["POST"])
def voice():
    
    if "audio" not in request.files:
        return jsonify({"error":"no audio provided"}),400
    response = request.files["audio"]
    return jsonify({"reply":response})



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
