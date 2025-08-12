import json
from src.core.utils import speak, save_history, load_history, extract_json
from src.core.router import route_command
from src.services import ai_service

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
{{{{ 
  "controller": "youtube",
  "action": "baixar_video",
  "params": {{"link": "<link_do_video>"}}
}}}}
- Se pedir para buscar vídeos:
{{{{ 
  "controller": "youtube",
  "action": "buscar_video",
  "params": {{"query": "<termo_busca>"}}
}}}}
- Se pedir para abrir o YouTube ou abrir canal (ex: "abre o YouTube", "abre o canal do fulano"):
{{{{ 
  "controller": "youtube",
  "action": "abrir_home",
  "params": {{"query": "<nome_canal>"}}
}}}}
(O campo query pode ser vazio se não for canal específico)

### Projetos Locais:
{{{{ 
  "controller": "os",
  "action": "abrir_projeto",
  "params": {{"query": "<nome_do_projeto>"}}
}}}}

### Programas Instalados:
{{{{ 
  "controller": "os",
  "action": "abrir_programa",
  "params": {{"query": "<nome_do_programa>"}}
}}}}

### Status do Sistema:
{{{{ 
  "controller": "os",
  "action": "status_sistema",
  "params": {{}}
}}}}
{{{{ 
  "controller": "os",
  "action": "get_data",
  "params": {{}}
}}}}
{{{{ 
  "controller": "os",
  "action": "desligar",
  "params": {{}}
}}}}
{{{{ 
  "controller": "os",
  "action": "reiniciar",
  "params": {{}}
}}}}

### Diagnóstico e Desempenho:
{{{{ 
  "controller": "openai",
  "action": "responder",
  "params": {{"query": "<texto_original_da_pergunta>"}}
}}}}

### Spotify:
{{{{ 
  "controller": "spotify",
  "action": "tocar",
  "params": {{"query": "<nome_musica_ou_artista>"}}
}}}}

{{{{ 
  "controller": "spotify",
  "action": "parar_musica",
  "params": {{}}
}}}}

### Visão por Webcam:
{{{{ 
  "controller": "vision",
  "action": "descrever_cena",
  "params": {{}}
}}}}

{{{{ 
  "controller": "vision",
  "action": "ler_texto",
  "params": {{}}
}}}}

{{{{ 
  "controller": "vision",
  "action": "detectar_pessoas",
  "params": {{}}
}}}}


### Notas:
{{{{ 
  "controller": "notes",
  "action": "adicionar",
  "params": {{"texto": "<conteúdo_da_nota_ou_lembrete>"}}
}}}}
{{{{ 
  "controller": "notes",
  "action": "listar",
  "params": {{}}
}}}}

### WhatsApp:
- Só envie mensagem se o usuário indicar claramente o nome do contato e o que deve ser enviado. Se não tiver certeza do nome do contato ou da mensagem, não preencha nenhum campo e deixe params vazio.
- Se o usuário pedir para enviar uma mensagem, mas não fornecer o contato ou a mensagem, solicite esses dados.
- Se o usuário fornecer um contato, mas não a mensagem, pergunte o que enviar.
{{{{ 
  "controller": "whatsapp",
  "action": "enviar_mensagem",
  "params": {{"contato": "<nome_contato>", "mensagem": "<mensagem_final>"}}
}}}}

### Programação:
{{{{ 
  "controller": "code_ai",
  "action": "gerar_codigo",
  "params": {{"query": "<texto_da_pergunta>"}}
}}}}

### Notícias:
{{{{ 
  "controller": "news",
  "action": "ler",
  "params": {{"categoria": "<categoria_ou_vazio_para_geral>"}}
}}}}

### Qualquer coisa que não se encaixe nos módulos acima:
{{{{ 
  "controller": "openai",
  "action": "responder",
  "params": {{"query": "<mensagem_original>"}}
}}}}


COMANDO DO USUÁRIO: "{user_input}"
Responda SOMENTE com o JSON.
"""

    try:
        response_text = ai_service.question_to_chatgpt([{"role": "user", "content": prompt}])
        data = json.loads(extract_json(response_text))

        controller = data.get("controller")
        action = data.get("action")
        params = data.get("params", {})

        conversation_history.append({"role": "user", "content": user_input})
        route_command(controller, action, params, conversation_history, user_input)

    except Exception as e:
        speak(f"[X] Erro no processamento: {e}")
        try:
            fallback = ai_service.question_to_chatgpt([{"role": "user", "content": user_input}])
            conversation_history.append({"role": "assistant", "content": fallback})
            speak(fallback)
        except Exception as e2:
            speak(f"[X] Erro no fallback: {e2}")
    finally:
        save_history(conversation_history)
