import requests

def enviar_mensagem(contato, mensagem):
    url = "http://localhost:3001/enviar"
    data = {"contato": contato, "mensagem": mensagem}
    print(f"[DEBUG] Enviando mensagem para: '{contato}' | Mensagem: '{mensagem}'")
    try:
        r = requests.post(url, json=data)
        print(f"[DEBUG] Status code: {r.status_code}, Resposta: {r.text}")

        if r.ok:
            print(f"Mensagem enviada para {contato}!")
            return f"Mensagem enviada para {contato}!"

        try:
            resposta_json = r.json()
        except Exception:
            resposta_json = None

        if resposta_json and "sugestoes" in resposta_json:
            sugestoes = resposta_json["sugestoes"]
            for sugestao in sugestoes:
                resposta = input(f'Contato sugerido: {sugestao}. É esse? [s/n]: ').strip().lower()
                if resposta == 's':
                    if not mensagem:
                        mensagem = input(f'Qual mensagem devo enviar para {sugestao}? ').strip()
                    return enviar_mensagem(sugestao, mensagem)
            print("[X] Nenhum contato confirmado. Mensagem NÃO enviada.")
            return "[X] Nenhum contato confirmado. Mensagem NÃO enviada."

        elif "Contato não encontrado" in r.text:
            print(f"[!] Contato '{contato}' não encontrado no WhatsApp.")
            return "[X] Contato não encontrado no WhatsApp."

        else:
            print(f"[X] Erro ao enviar mensagem: {r.text}")
            return f"[X] Erro ao enviar mensagem: {r.text}"

    except Exception as e:
        print(f"[X] Erro ao conectar com o servidor WhatsApp: {e}")
        return f"[X] Erro ao conectar com o servidor WhatsApp: {e}"
