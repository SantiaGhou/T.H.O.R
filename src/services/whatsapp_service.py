import requests
from src.services.ai_service import question_to_chatgpt

def gerar_mensagem_ia(contato, contexto):
    prompt = f"""
Gere uma mensagem de WhatsApp educada para enviar para {contato}.
Contexto/intenção: {contexto}
Assine no final: 'Mensagem enviada por T.H.O.R.'
Fale como se fosse o assistente do usuário, não o próprio usuário.
Não use emojis, apenas texto.
Responda apenas com a mensagem a ser enviada, sem explicações.
"""
    return question_to_chatgpt([{"role": "user", "content": prompt}]).strip()

def enviar_mensagem(contato, mensagem=None):
    url = "http://localhost:3001/enviar"
    data = {"contato": contato, "mensagem": mensagem}
    print(f"[DEBUG] Enviando mensagem para: '{contato}'")

    try:
        r = requests.post(url, json=data)
        print(f"[DEBUG] Status: {r.status_code} | Resposta: {r.text}")

        if r.ok:
            print(f"Mensagem enviada para {contato}!")
            return f"Mensagem enviada para {contato}!"

        try:
            resposta_json = r.json()
        except:
            resposta_json = None

        if resposta_json and "sugestoes" in resposta_json:
            sugestoes = resposta_json["sugestoes"]
            for sugestao in sugestoes:
                resposta = input(f'Contato sugerido: {sugestao}. É esse? [s/n]: ').strip().lower()
                if resposta == 's':
                    if not mensagem:
                        contexto = input(f'O que você quer enviar para {sugestao}? ').strip()
                        mensagem = gerar_mensagem_ia(sugestao, contexto)
                    return enviar_mensagem(sugestao, mensagem)
            print("[X] Nenhum contato confirmado. Mensagem NÃO enviada.")
            return "[X] Nenhum contato confirmado. Mensagem NÃO enviada."

        if "Contato não encontrado" in r.text:
            print(f"[X] Contato '{contato}' não encontrado.")
            return "[X] Contato não encontrado."

        print(f"[X] Erro ao enviar mensagem: {r.text}")
        return f"[X] Erro ao enviar mensagem: {r.text}"

    except Exception as e:
        print(f"[X] Erro ao conectar com o servidor WhatsApp: {e}")
        return f"[X] Erro ao conectar com o servidor WhatsApp: {e}"