from src.services import ai_service
from src.core.utils import speak

def handle(action, params, history, user_input):
    if action == "responder":
        query = params.get("query", user_input)
        response = ai_service.question_to_chatgpt([{"role": "user", "content": query}])
        history.append({"role": "assistant", "content": response})
        speak(response)
