import spotipy
from spotipy.oauth2 import SpotifyOAuth
import dotenv

CLIENT_ID = dotenv.get_key('.env', 'SPOTIFY_CLIENT_ID')
CLIENT_SECRET = dotenv.get_key('.env', 'SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = dotenv.get_key('.env', 'SPOTIFY_REDIRECT_URI')

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-read-playback-state user-modify-playback-state"
))

def buscar_uri_por_nome(nome):
    result = sp.search(q=nome, type="track", limit=1)
    tracks = result.get("tracks", {}).get("items", [])
    if not tracks:
        return None
    return tracks[0]["uri"]

def tocar(uri):
    devices = sp.devices()
    if not devices['devices']:
        return "[X] Nenhum dispositivo ativo encontrado com Spotify."

    device_id = devices['devices'][0]['id']
    sp.start_playback(device_id=device_id, uris=[uri])
    return "[✔] Música tocando!"

def tocar_por_nome(nome):
    uri = buscar_uri_por_nome(nome)
    if not uri:
        return f"[X] Música '{nome}' não encontrada no Spotify."
    return tocar(uri)

def parar_musica():
   
    try:
        playback = sp.current_playback()
        if not playback:
            return "[i] Nenhuma música tocando no momento."
   
        if playback and playback['is_playing']:
            sp.pause_playback()
            return "[✔] Música pausada!"
        else:
            return "[i] Nenhuma música tocando no momento."
    except Exception as e:
        return f"[X] Erro ao tentar parar a música: {e}"