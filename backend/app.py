from flask import Flask, render_template, request, jsonify,send_file
import services.open_ai_services as openai
import tempfile

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/voice", methods=["POST"])
def voice():
    print("Voice endpoint called")
    
    if "audio" not in request.files:
        print("No audio file found in request")
        return jsonify({"error": "no audio provided"}), 400
    
    audio_file = request.files["audio"]
    print(f"Audio file received: {audio_file.filename}, size: {audio_file.content_length}")
    
    temp_path = None  # Initialize variable
    
    try:
        import tempfile
        import os
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            audio_file.save(temp_file.name)
            temp_path = temp_file.name
            print(f"Saved temporary file: {temp_path}")
            
            # Check file size
            file_size = os.path.getsize(temp_path)
            print(f"Temporary file size: {file_size} bytes")
            
            if file_size == 0:
                print("ERROR: Uploaded file is empty!")
                return jsonify({"error": "uploaded audio file is empty"}), 400
        
        # Pass the file path to your function
        response_audio = openai.ask_openai_voice(temp_path)
        
        # IMPORTANT: Make sure all file handles are closed before deletion
        # This is where the error was occurring
        
        # Now delete the temporary file
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)
            print("Temporary file deleted successfully")
        
        if response_audio is None:
            print("ERROR: ask_openai_voice returned None")
            return jsonify({"error": "failed to generate audio response"}), 500
            
        response_audio.seek(0)
        
        print("Sending audio response back to client")
        return send_file(
            response_audio,
            mimetype="audio/mpeg",
            as_attachment=False,
            download_name="response.wav"
        )
    
    except Exception as e:
        print(f"ERROR in voice route: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Clean up temporary file if it exists
        if temp_path and os.path.exists(temp_path):
            try:
                os.unlink(temp_path)
                print("Temporary file deleted successfully")
            except PermissionError:
                print("Temp file still in use, scheduling later cleanup")
        
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    response = openai.ask_openai(user_message)
    return jsonify({"reply": response})

if __name__ == "__main__":
    app.run(debug=True)
