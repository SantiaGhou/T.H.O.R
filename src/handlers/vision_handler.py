from src.services import vision_service
from src.core.utils import speak

def handle(action, params, history, user_input):
    if action == "descrever_cena":
        speak(vision_service.descrever_cena())
    elif action == "ler_texto":
        speak(vision_service.ler_texto())
    elif action == "detectar_pessoas":
        speak(vision_service.detectar_pessoas())
    else:
        speak("[X] Ação de visão não reconhecida.")
