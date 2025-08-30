# from openai import OpenAI
# from config import Config

# client = OpenAI(api_key=Config.OPENAI_API_KEY)


# def get_voice_text(input_voice):
#     try:
#         input = open(input_voice, "rb")
#         response = client.audio.transcriptions.create(
#             model="whisper-1",
#             file=input
#         )
#         return response.text
#     except Exception as e:
#         return f"Error: {str(e)}"
    
# def text_to_audio(text):
#     output_voice = "ouput.mp3"
#     try:
#         response = client.audio.speech.create(
#             model="text-to-speech",
#             input=text
#         )
#         with open(output_voice,"wb") as f:
#             f.write(response.audio)

#         return output_voice
#     except Exception as e:
#         return f"Error: {str(e)}"

# def ask_openai_voice(input_voice)->str:
#     try:
#         text = get_voice_text(input_voice)
#         response = ask_openai(text)
#         response_audio = text_to_audio(response)
#         return response_audio 
        
#     except Exception as e:
#         return f"Error: {str(e)}"

# def ask_openai(prompt: str) -> str:
#     try:
#         response = client.chat.completions.create(
#             model="gpt-4o-mini",  
#             messages=[{"role": "user", "content": prompt}],
#              max_completion_tokens = 10

#         )
#         return response.choices[0].message.content
#     except Exception as e:
#         return f"Error: {str(e)}"

from openai import OpenAI
from config import Config
import io

client = OpenAI(api_key=Config.OPENAI_API_KEY)

# Global chat history
chat_history = [
    {"role": "system", "content": "MY name is nadem . your name is pokemon .. You are a helpful assistant."}
]

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


def ask_openai(history):
    response = client.chat.completions.create(
        model="gpt-4o-mini",   # or gpt-4.1-mini
        messages=history
    )
    return response.choices[0].message.content



def ask_openai_voice(input_voice) -> str:
    try:
        text = get_voice_text(input_voice)

        # add user input to chat history
        chat_history.append({"role": "user", "content": text})

        # get assistant response with full history
        response_text = ask_openai(chat_history)

        # add assistant response to chat history
        chat_history.append({"role": "assistant", "content": response_text})

        # convert response to audio
        response_audio = text_to_audio(response_text)
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