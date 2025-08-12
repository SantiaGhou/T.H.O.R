from src.services.whatsapp_service import enviar_mensagem, gerar_mensagem_ia
from src.core.utils import speak

def handle(action, params, history, user_input):
    if action == "enviar_mensagem":
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
            speak(tentativa)
            history.append({"role": "assistant", "content": tentativa})
