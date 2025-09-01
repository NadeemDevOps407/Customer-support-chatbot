from flask import Flask, render_template, request, jsonify,send_file
import services.open_ai_services as openai
import tempfile

app = Flask(__name__)

chat_history = [{"role": "system", "content": "You are a helpful assistant."}]

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/voice", methods=["POST"])
def voice():
    
    
    if "audio" not in request.files:
        return jsonify({"error": "no audio provided"}), 400
    
    audio_file = request.files["audio"]
    
    temp_path = None  # Initialize variable
    
    try:
        import tempfile
        import os
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            audio_file.save(temp_file.name)
            temp_path = temp_file.name
            
            # Check file size
            file_size = os.path.getsize(temp_path)
            
            if file_size == 0:
                return jsonify({"error": "uploaded audio file is empty"}), 400
        
        # Pass the file path to your function
        response_audio = openai.ask_openai_voice(temp_path)
        
        # IMPORTANT: Make sure all file handles are closed before deletion
        # This is where the error was occurring
        
        # Now delete the temporary file
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)
        
        if response_audio is None:
            return jsonify({"error": "failed to generate audio response"}), 500
            
        response_audio.seek(0)
        
        return send_file(
            response_audio,
            mimetype="audio/mpeg",
            as_attachment=False,
            download_name="response.wav"
        )
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        
        # Clean up temporary file if it exists
        if temp_path and os.path.exists(temp_path):
            try:
                os.unlink(temp_path)
            except PermissionError:
                pass  # Ignore if file is already deleted or locked
        
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        response = openai.ask_openai_chat(user_message)
        return jsonify({"reply": response})
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
