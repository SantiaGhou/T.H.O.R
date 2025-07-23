from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()  
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def question_to_chatgpt(question: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente inteligente chamado Thor, que responde perguntas de forma intuitiva e controla o sistema que está rodando."},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erro ao consultar a OpenAI: {e}"
