import os
from dotenv import load_dotenv
from src.core.boot import iniciar_thor
from getpass import getpass
from src.interfaces.input.input_interface import text_input, start_listening
from src.core.brain import process_command

load_dotenv()

def confirm_password():
    senha_correta = ""
    tentativa = getpass("Digite a senha de acesso: ")
    if tentativa == senha_correta:
        print("✅ Acesso autorizado.")
        return True
    else:
        print("Acesso negado. Saindo do programa...")
        return False

def thor_text_loop():
    print("Digite 'sair' para encerrar o assistente.\n")
    while True:
        texto = text_input()
        process_command(texto)

def thor():
    iniciar_thor()
    start_listening(process_command)
    print("🎤 Diga 'thor' e depois o comando. Texto também ativo.\n")
    thor_text_loop()

if __name__ == "__main__":
    if confirm_password():
        thor()
