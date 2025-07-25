import webbrowser
import urllib.parse
from pytube import YouTube
import yt_dlp
import os

def youtube(comando: dict):
    action = comando.get("action")
    parametros = comando.get("parametros", {})


    query = parametros.get("termo_pesquisa") or comando.get("query", "")

    if action == "buscar_video" or action == "abrir_video":
        if query:
            url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
            webbrowser.open(url)

    elif action == "abrir_home":
        webbrowser.open("https://www.youtube.com")

def baixar_video(link, caminho_destino="videos_baixados"):
    try:
        if not os.path.exists(caminho_destino):
            os.makedirs(caminho_destino)

        ydl_opts = {
            'format': 'mp4',
            'outtmpl': os.path.join(caminho_destino, '%(title)s.%(ext)s'),
            'quiet': False,
            'no_warnings': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Baixando: {link}")
            info = ydl.extract_info(link, download=True)
            titulo = info.get("title", "vídeo")
            print("Download concluído!")
            return f"Download do vídeo '{titulo}' concluído com sucesso."

    except Exception as e:
        print("Erro ao baixar vídeo:", e)
        return f"Erro ao baixar o vídeo: {str(e)}"