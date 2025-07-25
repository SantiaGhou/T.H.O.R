import webbrowser
import urllib.parse

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