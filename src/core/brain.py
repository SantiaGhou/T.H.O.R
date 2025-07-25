from src.services import openai_service
from src.services import youtube_service
from ..interfaces.input.input_interface import text_input
import json

def extrair_json(texto: str) -> str:
    start = texto.find('{')
    end = texto.rfind('}') + 1
    if start == -1 or end == -1:
        raise ValueError("JSON não encontrado na resposta")
    return texto[start:end]

def process_command(texto_usuario: str):
    prompt = f"""
Você é o cérebro do T.H.O.R. Dado o comando do usuário, retorne:
- controller: nome do serviço (ex: youtube)
- action: ação que deve ser executada (ex: buscar_video, abrir_home)
- parâmetros relevantes com nomes simples como 'query', 'busca' ou 'termo_pesquisa'

Comando do usuário: "{texto_usuario}"

Responda apenas com o JSON. Não adicione explicações ou texto fora do JSON.
"""

    resposta = openai_service.question_to_chatgpt(prompt)

    try:
        json_str = extrair_json(resposta)
        dados = json.loads(json_str)
        controller = dados.get("controller")

        if controller == "youtube":
            print("[INFO] Chamando youtube_service...")
            youtube_service.youtube(dados)

        elif controller == "openai":
            resposta_openai = openai_service.question_to_chatgpt(texto_usuario)
            print(resposta_openai)
        else:
            resposta_openai = openai_service.question_to_chatgpt(texto_usuario)
            print(resposta_openai)

    except Exception as e:
        print("[X] Erro no brain:", e)
        print("Resposta bruta:", resposta)
        resposta_openai = openai_service.question_to_chatgpt(texto_usuario)
        print(resposta_openai)


