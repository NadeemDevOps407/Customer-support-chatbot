from openai import OpenAI
from config import Config
import io

client = OpenAI(api_key=Config.OPENAI_API_KEY)


def get_voice_text(input_voice):
    try:
        with open(input_voice, "rb") as audio_file:
            response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
            )
            
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"
    
def text_to_audio(text):
    
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice = "alloy",
            input=text
        )
        audio_bytes = io.BytesIO()
        for chunk in response.iter_bytes():
            audio_bytes.write(chunk)
        audio_bytes.seek(0)
        
        return audio_bytes
    except Exception as e:
        return f"Error: {str(e)}"

def ask_openai_voice(input_voice)->str:
    try:
        text = get_voice_text(input_voice)
        response = ask_openai(text)
        response_audio = text_to_audio(response)
        return response_audio 
        
    except Exception as e:
        return f"Error: {str(e)}"

def ask_openai(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  
            messages=[{"role": "user", "content": prompt}],
             max_completion_tokens = 1000

        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"