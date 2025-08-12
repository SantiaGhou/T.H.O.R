from src.services import spotify_service
from src.core.utils import speak

def handle(action, params, history, user_input):
    if action == "tocar":
        query = params.get("query") or params.get("uri")
        if query:
            uri = query if query.startswith("spotify:") else spotify_service.buscar_uri_por_nome(query)
            if uri:
                result = spotify_service.tocar(uri)
                speak(result)
            else:
                speak(f"[X] Não foi possível encontrar a música: {query}")
        else:
            speak("[X] Nenhum nome ou URI informado.")
    elif action == "parar_musica":
        result = spotify_service.parar_musica()
        speak(result)
    history.append({"role": "assistant", "content": "Comando Spotify executado."})
