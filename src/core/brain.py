import json
import os
from src.services import youtube_service, ai_service, spotify_service, os_service
from ..interfaces.input.input_interface import text_input

HISTORY_FILE = "conversation_history.json"

def save_history(history):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return []

def extract_json(text: str) -> str:
    start = text.find('{')
    end = text.rfind('}') + 1
    if start == -1 or end == -1:
        raise ValueError("JSON não encontrado na resposta")
    return text[start:end]

conversation_history = load_history()

def process_command(user_input: str):
    global conversation_history

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

Se o usuário pedir para procurar ou mostrar vídeos de alguém ou sobre algum tema (ex: "procura vídeo do Felca", "quero ver algo do Ei Nerd", "vídeo sobre eletricidade"), use:
{{
  "controller": "youtube",
  "action": "buscar_video",
  "params": {{
    "query": "tema ou nome procurado"
  }}
}}

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
- Se o usuário quiser consultar o status atual do sistema, use:
{{
  "controller": "os",
  "action": "status_sistema",
  "params": {{}}
}}

Se ele pedir dicas de como melhorar desempenho, resolver problemas de lentidão, etc, retorne:
{{
  "controller": "openai",
  "action": "responder",
  "params": {{
    "query": "texto original da pergunta"
  }}
}}

Para Spotify:
- Se o usuário pedir para tocar uma música, playlist ou álbum:
{{
  "controller": "spotify",
  "action": "tocar",
  "params": {{
    "query": "nome da música ou artista"
  }}
}}

Se não conseguir classificar claramente o comando, envie:
{{
  "controller": "openai",
  "action": "responder",
  "params": {{
    "query": "texto original da pergunta"
  }}
}}
- Se o usuário pedir para PARAR a música (ex: "pare a música", "para de tocar", "stop"), retorne:
{{
  "controller": "spotify",
  "action": "parar_musica",
  "params": {{}}
}}
Comando do usuário: "{user_input}"
Responda apenas com o JSON. Não adicione explicações ou texto fora do JSON.
"""

    try:
        response_text = ai_service.question_to_chatgpt([{"role": "user", "content": prompt}])
        json_str = extract_json(response_text)
        data = json.loads(json_str)

        controller = data.get("controller")
        action = data.get("action")
        params = data.get("params", {})

        conversation_history.append({"role": "user", "content": user_input})

        if controller == "youtube":
            if action == "baixar_video":
                link = (
                    params.get("link")
                    or params.get("query")
                    or params.get("termo")
                )
                if not link:
                    print("[?] Cole aqui o link do vídeo que você quer baixar:")
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

            conversation_history.append({"role": "assistant", "content": "Comando YouTube executado."})

        elif controller == "os":
            if action == "abrir_projeto":
                from src.services.os_service import open_project
                result = open_project(params)
                print(result)

            elif action == "status_sistema":
                from src.services.os_service import get_system_status
                result = get_system_status()
                print(result)

            conversation_history.append({"role": "assistant", "content": "Comando OS executado."})

        elif controller == "spotify":
            if action == "tocar":
                query = params.get("query") or params.get("uri")
                if query:
                    uri = query if query.startswith("spotify:") else spotify_service.buscar_uri_por_nome(query)
                    if uri:
                        result = spotify_service.tocar(uri)
                        print(result)
                    else:
                        print(f"[X] Não foi possível encontrar a música: {query}")
                else:
                    print("[X] Nenhum nome ou URI foi informado.")

            elif action == "parar_musica":
                result = spotify_service.parar_musica()
                print(result)

            conversation_history.append({"role": "assistant", "content": "Comando Spotify executado."})

        elif controller == "openai":
            query = params.get("query", user_input)
            openai_response = ai_service.question_to_chatgpt(conversation_history + [{"role": "user", "content": query}])
            conversation_history.append({"role": "assistant", "content": openai_response})
            print(openai_response)

        else:
            fallback_response = ai_service.question_to_chatgpt(conversation_history + [{"role": "user", "content": user_input}])
            conversation_history.append({"role": "assistant", "content": fallback_response})
            print(fallback_response)

    except Exception as e:
        print(f"[X] Erro no processamento do comando: {e}")
        fallback_response = ai_service.question_to_chatgpt(conversation_history + [{"role": "user", "content": user_input}])
        conversation_history.append({"role": "assistant", "content": fallback_response})
        print(fallback_response)

    finally:
        save_history(conversation_history)