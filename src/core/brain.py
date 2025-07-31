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

    prompt = fPROMPT_THOR = """
Você é o cérebro do T.H.O.R., um sistema avançado de interpretação de comandos do usuário. Sua função é analisar a intenção do usuário e retornar apenas UM objeto JSON válido e bem-formado, seguindo rigorosamente o formato abaixo:

{
  "controller": "<nome_do_serviço>",
  "action": "<ação_a_ser_executada>",
  "params": {
    "chave": "valor"
  }
}

REGRAS GERAIS:
1. A resposta deve ser exclusivamente um JSON válido. Não adicione comentários, explicações, saudações ou qualquer texto fora do JSON.
2. Sempre inclua os campos: "controller", "action" e "params". Se não houver parâmetros, use "params": {}.
3. Todos os valores devem ser strings, exceto quando claramente for um número.
4. Normalize os valores: remova espaços, quebras de linha e caracteres desnecessários.

MÓDULOS E FORMATAÇÃO:

YouTube:
- Se receber um link do YouTube ou o comando para baixar vídeo:
{
  "controller": "youtube",
  "action": "baixar_video",
  "params": {
    "link": "<link_do_video>"
  }
}
- Se receber comando de busca de vídeos:
{
  "controller": "youtube",
  "action": "buscar_video",
  "params": {
    "query": "<termo_de_busca>"
  }
}

Projetos Locais (GitHub):
- Se o comando for abrir um projeto:
{
  "controller": "os",
  "action": "abrir_projeto",
  "params": {
    "query": "<nome_do_projeto>"
  }
}

Programas Instalados:
- Se o comando for abrir um programa:
{
  "controller": "os",
  "action": "abrir_programa",
  "params": {
    "query": "<nome_do_programa>"
  }
}

Status do Sistema:
- Para checar CPU, RAM ou Disco:
{
  "controller": "os",
  "action": "status_sistema",
  "params": {}
}
- Para data e hora:
{
  "controller": "os",
  "action": "get_data",
  "params": {}
}

Diagnóstico e Desempenho:
- Para dicas de performance, lentidão ou solução de problemas:
{
  "controller": "openai",
  "action": "responder",
  "params": {
    "query": "<texto_original_da_pergunta>"
  }
}

Spotify:
- Para tocar música, playlist ou álbum:
{
  "controller": "spotify",
  "action": "tocar",
  "params": {
    "query": "<nome_da_musica_ou_artista>"
  }
}
- Para parar música:
{
  "controller": "spotify",
  "action": "parar_musica",
  "params": {}
}

WhatsApp:
- Para enviar mensagem, siga estas regras:
  - Se for mensagem exata (entre aspas ou explicitamente "exatamente assim"), envie literalmente.
  - Caso contrário, monte a mensagem finalizando com "Mensagem enviada por T.H.O.R.".
Exemplo:
{
  "controller": "whatsapp",
  "action": "enviar_mensagem",
  "params": {
    "contato": "<nome_do_contato>",
    "mensagem": "<mensagem_final>"
  }
}

Programação:
- Para dúvidas, bugs, scripts ou algoritmos:
{
  "controller": "code_ai",
  "action": "gerar_codigo",
  "params": {
    "query": "<texto_da_pergunta>"
  }
}

Comando do usuário: "{user_input}"
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
                conversation_history.append({"role":"assistant","content":result})
            conversation_history.append({"role":"assistant","content":"Comando OS executado."})


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

        elif controller == "whatsapp":
            from src.services.whatsapp_service import enviar_mensagem
            contato = params.get("contato") or params.get("query") or params.get("destinatario")
            contexto = params.get("contexto") or params.get("mensagem") or params.get("msg") or params.get("texto")
            if not contato:
                contato = input("Pra quem você quer enviar? ").strip()
            if not contexto:
                contexto = input(f"O que você quer enviar para {contato}? ").strip()
            if contato and contexto:
                texto_exato = mensagem_exata(contexto)
                if texto_exato:
                    mensagem_final = texto_exato
                else:
                    prompt_ia = f"""
Gere uma mensagem de WhatsApp como eu pedir, para enviar para {contato}.
Contexto/intenção: {contexto}
Assine no final: 'Mensagem enviada por T.H.O.R.'
Fale como se fosse o assistente do usuário, não o próprio usuário.
Não use emojis, apenas texto.
Responda apenas com a mensagem a ser enviada, sem explicações.
"""
                    mensagem_final = ai_service.question_to_chatgpt(
                        conversation_history + [{"role": "user", "content": prompt_ia}]
                    ).strip()
                result = enviar_mensagem(contato, mensagem_final)
                print(result)
                conversation_history.append({"role": "assistant", "content": result})
            else:
                print("[X] Faltou o contato ou contexto para enviar mensagem no WhatsApp.")

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
