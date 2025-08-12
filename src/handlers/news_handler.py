from src.services import news_service
from src.core.utils import speak

def handle(action, params, history, user_input):
    if action == "ler":
        categoria = params.get("categoria", "general")
        news_service.read_news(categoria)
    else:
        speak("[X] Ação de notícias não reconhecida.")
