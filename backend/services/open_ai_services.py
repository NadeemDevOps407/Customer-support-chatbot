from openai import OpenAI
from config import Config

client = OpenAI(api_key=Config.OPENAI_API_KEY)


def get_voice_text(input_voice):
    try:
        input = open(input_voice, "rb")
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=input
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"
    
def text_to_audio(text):
    output_voice = "ouput.mp3"
    try:
        response = client.audio.speech.create(
            model="text-to-speech",
            input=text
        )
        with open(output_voice,"wb") as f:
            f.write(response.audio)

        return output_voice
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
             max_completion_tokens = 1

        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"