from src.services import openai_service
from src.services import youtube_service
from ..interfaces.input.input_interface import text_input
import json

def extract_json(text: str) -> str:
    start = text.find('{')
    end = text.rfind('}') + 1
    if start == -1 or end == -1:
        raise ValueError("JSON não encontrado na resposta")
    return text[start:end]

def process_command(user_input: str):
    prompt = f"""
Você é o cérebro do T.H.O.R. Dado o comando do usuário, retorne um JSON com:
- controller: nome do serviço (ex: youtube, os, openai)
- action: ação que deve ser executada (ex: buscar_video, abrir_home, abrir_projeto, baixar_video)
- parâmetros relevantes com nomes simples como 'query', 'link' ou 'termo'

Para YouTube:
- Use "action": "baixar_video" apenas se:
  - o usuário fornecer um link do YouTube (ex: https://www.youtube.com/...)
  - ou der um comando direto como "baixe esse vídeo do YouTube", "faça download do vídeo X do YouTube"
- Sempre inclua o campo "link" se o usuário quiser baixar um vídeo.

Para projetos locais:
- Se o usuário pedir para abrir um projeto local da pasta GitHub (ex: "abra o projeto do Fitout"), retorne:
{{
  "controller": "os",
  "action": "abrir_projeto",
  "params": {{
    "query": "nome_do_projeto"
  }}
}}

Responda apenas com o JSON. Não adicione explicações ou texto fora do JSON.

Comando do usuário: "{user_input}"
"""

    response = openai_service.question_to_chatgpt(prompt)

    try:
        json_str = extract_json(response)
        data = json.loads(json_str)
        controller = data.get("controller")
        action = data.get("action")
        params = data.get("params", {})

        if controller == "youtube":
            if action == "baixar_video":
                link = (
                    params.get("link")
                    or params.get("query")
                    or params.get("termo")
                )

                if not link:
                    print("[?] Sem problemas. Cole aqui o link do vídeo que você quer baixar:")
                    link = input(">>> ")

                if link:
                    from src.services.youtube_service import baixar_video
                    result = baixar_video(link)
                    print(result)
                else:
                    print("[X] Nenhum link informado. Operação cancelada.")
            else:
                print("[INFO] Chamando youtube_service...")
                youtube_service.youtube(data)

        elif controller == "os":
            if action == "abrir_projeto":
                from src.services.os_service import open_project
                result = open_project(params)
                print(result)

        elif controller == "openai":
            openai_response = openai_service.question_to_chatgpt(user_input)
            print(openai_response)

        else:
            fallback_response = openai_service.question_to_chatgpt(user_input)
            print(fallback_response)

    except Exception as e:
        print("[X] Erro no brain:", e)
        print("Resposta bruta:", response)
        fallback_response = openai_service.question_to_chatgpt(user_input)
        print(fallback_response)
