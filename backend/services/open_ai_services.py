from openai import OpenAI
from config import Config

client = OpenAI(api_key=Config.OPENAI_API_KEY)

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