import json
import os
import re
from src.services import youtube_service, ai_service, spotify_service, os_service, code_ai_service
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

def mensagem_exata(contexto):
    match = re.search(r'"([^\"]+)"|\'([^\']+)\'', contexto)
    if match:
        return match.group(1) or match.group(2)
    padroes = [
        r"exatamente assim: (.+)",
        r"envia isso: (.+)",
        r"mensagem literal: (.+)",
        r"manda (.+) exatamente"
    ]
    for padrao in padroes:
        m2 = re.search(padrao, contexto, re.IGNORECASE)
        if m2:
            return m2.group(1).strip()
    return None

conversation_history = load_history()

def process_command(user_input: str):
    global conversation_history

    prompt = f"""
Você é o cérebro do T.H.O.R., um sistema de interpretação de comandos do usuário. Seu objetivo é analisar a intenção do usuário e retornar um JSON bem-formado no formato:

{{
  "controller": "<nome_do_serviço>",
  "action": "<ação_a_ser_executada>",
  "params": {{
    "chave": "valor"
  }}
}}

Regras:
1. Responda exclusivamente com o JSON válido. Não coloque nada fora do JSON.
2. Sempre inclua: "controller", "action" e "params". Se não houver parâmetros, use "params": {{}}
3. Todos os valores são string, exceto quando claramente número.
4. Normalize textos dos parâmetros.

MÓDULOS SUPORTADOS:

### YouTube:
- Se o usuário pedir para baixar vídeo e fornecer um link:
{{
  "controller": "youtube",
  "action": "baixar_video",
  "params": {{"link": "<link_do_video>"}}
}}
- Se pedir para buscar vídeos:
{{
  "controller": "youtube",
  "action": "buscar_video",
  "params": {{"query": "<termo_busca>"}}
}}
- Se pedir para abrir o YouTube ou abrir canal (ex: "abre o YouTube", "abre o canal do fulano"):
{{
  "controller": "youtube",
  "action": "abrir_home",
  "params": {{"query": "<nome_canal>"}}
}}
(O campo query pode ser vazio se não for canal específico)

### Projetos Locais:
{{
  "controller": "os",
  "action": "abrir_projeto",
  "params": {{"query": "<nome_do_projeto>"}}
}}

### Programas Instalados:
{{
  "controller": "os",
  "action": "abrir_programa",
  "params": {{"query": "<nome_do_programa>"}}
}}

### Status do Sistema:
{{
  "controller": "os",
  "action": "status_sistema",
  "params": {{}}
}}
{{
  "controller": "os",
  "action": "get_data",
  "params": {{}}
}}

### Diagnóstico e Desempenho:
{{
  "controller": "openai",
  "action": "responder",
  "params": {{"query": "<texto_original_da_pergunta>"}}
}}

### Spotify:
{{
  "controller": "spotify",
  "action": "tocar",
  "params": {{"query": "<nome_musica_ou_artista>"}}
}}
{{
  "controller": "spotify",
  "action": "parar_musica",
  "params": {{}}
}}

### WhatsApp:
- Só envie mensagem se o usuário indicar claramente o nome do contato e o que deve ser enviado. Se não tiver certeza do nome do contato ou da mensagem, **não preencha nenhum campo e deixe params vazio**.
- Se o usuário pedir para enviar uma mensagem, mas não fornecer o contato ou a mensagem, solicite esses dados.
- Se o usuário fornecer um contato, mas não a mensagem, pergunte o que enviar.
{{
  "controller": "whatsapp",
  "action": "enviar_mensagem",
  "params": {{"contato": "<nome_contato>", "mensagem": "<mensagem_final>"}}
}}

### Programação:
{{
  "controller": "code_ai",
  "action": "gerar_codigo",
  "params": {{"query": "<texto_da_pergunta>"}}
}}

### Qualquer coisa que não se encaixe nos módulos acima:
{{
  "controller": "openai",
  "action": "responder",
  "params": {{"query": "<mensagem_original>"}}
}}

COMANDO DO USUÁRIO: "{user_input}"
Responda SOMENTE com o JSON.
"""

    try:
        response_text = ai_service.question_to_chatgpt([{"role": "user", "content": prompt}])
        json_str = extract_json(response_text)
        data = json.loads(json_str)

        controller = data.get("controller")
        action = data.get("action")
        params = data.get("params", {})

        conversation_history.append({"role": "user", "content": user_input})

        if controller == "code_ai":
            response = code_ai_service.get_code_suggestion(conversation_history)
            print(response)
            conversation_history.append({"role": "assistant", "content": response})

        elif controller == "youtube":
            if action == "baixar_video":
                link = params.get("link")
                if not link or not ("youtube.com" in link or "youtu.be" in link):
                    print("[?] Cole aqui o link do vídeo do YouTube que você quer baixar:")
                    link = input(">>> ")
                if link and ("youtube.com" in link or "youtu.be" in link):
                    from src.services.youtube_service import baixar_video
                    result = baixar_video(link)
                    print(result)
                else:
                    print("[X] Nenhum link válido informado. Operação cancelada.")
            elif action == "buscar_video":
                youtube_service.youtube(data)
            elif action == "abrir_home":
                canal = params.get("query", "").strip()
                import webbrowser
                if canal:
                    # tenta abrir canal no formato correto (pode adaptar pra @ se preferir)
                    canal_url = canal.replace("canal", "").replace(" ", "")
                    url = f"https://www.youtube.com/@{canal_url}"
                else:
                    url = "https://www.youtube.com/"
                webbrowser.open(url)
                print(f"Abrindo YouTube{' no canal ' + canal if canal else ''}...")
            else:
                print("[X] Ação do YouTube não reconhecida.")

            conversation_history.append({"role": "assistant", "content": "Comando YouTube executado."})

        elif controller == "os":
            if action == "abrir_projeto":
                from src.services.os_service import open_project
                print(open_project(params))
            elif action == "status_sistema":
                from src.services.os_service import get_system_status
                print(get_system_status())
            elif action == "abrir_programa":
                from src.services.os_service import open_program
                print(open_program(params))
            elif action == "get_data":
                from src.services.os_service import get_data
                result = get_data()
                print(result)
                conversation_history.append({"role": "assistant", "content": result})
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

        elif controller == "openai" and action == "responder":
            query = params.get("query", user_input)
            openai_response = ai_service.question_to_chatgpt([{"role": "user", "content": query}])
            conversation_history.append({"role": "assistant", "content": openai_response})
            print(openai_response)

        elif controller == "whatsapp":
            from src.services.whatsapp_service import enviar_mensagem, gerar_mensagem_ia
            contato = params.get("contato") or params.get("query") or params.get("destinatario")
            mensagem = params.get("mensagem") or params.get("contexto") or params.get("msg") or params.get("texto")

            if not contato:
                contato = input("Pra quem você quer enviar? ").strip()

            if not mensagem:
                contexto = input(f"O que você quer enviar para {contato}? ").strip()
            else:
                contexto = mensagem

            mensagem = gerar_mensagem_ia(contato, contexto)

            tentativa = enviar_mensagem(contato, mensagem)
            if tentativa and "[X]" not in tentativa:
                print(tentativa)
                conversation_history.append({"role": "assistant", "content": tentativa})
                return






        else:
           
            openai_response = ai_service.question_to_chatgpt([{"role": "user", "content": user_input}])
            conversation_history.append({"role": "assistant", "content": openai_response})
            print(openai_response)

    except Exception as e:
        print(f"[X] Erro no processamento do comando: {e}")
        fallback_response = ai_service.question_to_chatgpt([{"role": "user", "content": user_input}])
        conversation_history.append({"role": "assistant", "content": fallback_response})
        print(fallback_response)

    finally:
        save_history(conversation_history)
