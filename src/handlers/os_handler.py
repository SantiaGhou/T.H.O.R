from src.services import os_service
from src.core.utils import speak

def handle(action, params, history, user_input):
    if action == "abrir_projeto":
        speak(os_service.open_project(params))
    elif action == "status_sistema":
        speak(os_service.get_system_status())
    elif action == "abrir_programa":
        speak(os_service.open_program(params))
    elif action == "get_data":
        result = os_service.get_data()
        speak(result)
        history.append({"role": "assistant", "content": result})
    elif action == "desligar":
        speak(os_service.desligar_computador())
    elif action == "reiniciar":
        speak(os_service.reiniciar_computador())
    history.append({"role": "assistant", "content": "Comando OS executado."})
