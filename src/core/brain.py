from services import ai_service
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
- controller: nome do serviço (ex: youtube, os, openai, spotify)
- action: ação que deve ser executada (ex: buscar_video, abrir_home, abrir_projeto, baixar_video, status_sistema, responder, tocar)
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

Para verificar o status da máquina (CPU, RAM, Disco):
- Se o usuário quiser **consultar** o status atual do sistema, com frases como:
  - "como está meu PC"
  - "status da máquina"
  - "quais os status da minha máquina"
  - "uso da CPU"
  - "memória RAM"
  - "como está o desempenho do sistema"
- Retorne:
{{
  "controller": "os",
  "action": "status_sistema",
  "params": {{}}
}}

⚠️ Se o usuário estiver perguntando **por que está alto**, **como resolver**, **como melhorar o desempenho**, ou pedindo **sugestões para reduzir uso de RAM ou CPU**, **não** retorne "status_sistema". Nesse caso, responda com:
{{
  "controller": "openai",
  "action": "responder",
  "params": {{
    "query": "texto original da pergunta"
  }}
}}

Para Spotify:
- Se o usuário pedir para tocar uma música, playlist ou álbum, retorne:
{{
  "controller": "spotify",
  "action": "tocar",
  "params": {{
    "query": "nome da música ou artista"
  }}
}}

Se não conseguir classificar claramente o comando, envie como fallback:
{{
  "controller": "openai",
  "action": "responder",
  "params": {{
    "query": "texto original da pergunta"
  }}
}}
Para YouTube:
- Use "action": "baixar_video" apenas se:
  ...
- Se o usuário pedir para procurar ou mostrar vídeos de alguém ou sobre algum tema (ex: "procura vídeo do Felca", "quero ver algo do Ei Nerd", "vídeo sobre eletricidade"), use:
{{
  "controller": "youtube",
  "action": "buscar_video",
  "params": {{
    "query": "tema ou nome procurado"
  }}
}}


Responda apenas com o JSON. Não adicione explicações ou texto fora do JSON.

Comando do usuário: "{user_input}"
"""

    response = ai_service.question_to_chatgpt(prompt)

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

            elif action == "status_sistema" or action == "get_system_status":
                from src.services.os_service import get_system_status
                result = get_system_status()
                print(result)

        elif controller == "spotify":
            if action == "tocar":
                from src.services.spotify_service import tocar, buscar_uri_por_nome
                query = params.get("query") or params.get("uri")
                if query:
                    uri = query if query.startswith("spotify:") else buscar_uri_por_nome(query)
                    if uri:
                        result = tocar(uri)
                        print(result)
                    else:
                        print(f"[X] Não foi possível encontrar a música: {query}")
                else:
                    print("[X] Nenhum nome ou URI foi informado.")

        elif controller == "openai":
            openai_response = ai_service.question_to_chatgpt(user_input)
            print(openai_response)

        else:
            fallback_response = ai_service.question_to_chatgpt(user_input)
            print(fallback_response)

    except Exception as e:
        print("[X] Erro no brain:", e)
        print("Resposta bruta:", response)
        fallback_response = ai_service.question_to_chatgpt(user_input)
        print(fallback_response)
