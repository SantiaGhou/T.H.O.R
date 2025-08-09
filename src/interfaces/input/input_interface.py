import os
from src.interfaces.input.voice_input_openai import start_voice_thread

def text_input():
    entrada = input("Você: ")
    if entrada.lower() in ['sair', 'exit', 'quit']:
        print("Encerrando...")
        exit()
    return entrada

def start_listening(callback):
    if os.getenv("THOR_VOICE") == "api":
        start_voice_thread(callback)
