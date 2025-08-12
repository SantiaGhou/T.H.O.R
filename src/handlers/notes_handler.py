from src.services import notes_service
from src.core.utils import speak

def handle(action, params, history, user_input):
    if action == "adicionar":
        notes_service.parse_and_add(params.get("texto", ""))
    elif action == "listar":
        notes_service.list_notes()
    else:
        speak("[X] Ação de notas não reconhecida.")
