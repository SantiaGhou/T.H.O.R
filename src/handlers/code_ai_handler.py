from src.services import code_ai_service
from src.core.utils import speak

def handle(action, params, history, user_input):
    if action == "gerar_codigo":
        response = code_ai_service.get_code_suggestion(history)
        speak(response)
        history.append({"role": "assistant", "content": response})
