from openai import OpenAI
from typing import List, Dict

client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama',
)

def get_code_suggestion(history: List[Dict[str, str]]) -> str:
    try:
        system_prompt = {"role": "system", "content": "Você é um assistente especialista em programação. Forneça respostas claras, código bem formatado em blocos de markdown e explique o que o código faz."}
        messages_to_send = [system_prompt] + history

        response = client.chat.completions.create(
            model="codegemma", 
            messages=messages_to_send
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[X] Deu B.O. pra conectar no CodeGemma (Ollama): {e}"
