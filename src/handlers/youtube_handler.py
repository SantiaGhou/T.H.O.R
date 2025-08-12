from src.services import youtube_service
from src.core.utils import speak

def handle(action, params, history, user_input):
    if action == "baixar_video":
        link = params.get("link")
        if not link or not ("youtube.com" in link or "youtu.be" in link):
            speak("[?] Cole o link do vídeo:")
            link = input(">>> ")
        if link:
            from src.services.youtube_service import baixar_video
            speak(baixar_video(link))
        else:
            speak("[X] Nenhum link válido.")
    elif action == "buscar_video":
        youtube_service.youtube({"params": params})
        speak("Busca concluída.")
    elif action == "abrir_home":
        import webbrowser
        canal = params.get("query", "").strip()
        url = f"https://www.youtube.com/@{canal.replace(' ', '')}" if canal else "https://www.youtube.com/"
        webbrowser.open(url)
        speak(f"Abrindo YouTube{' no canal ' + canal if canal else ''}...")
