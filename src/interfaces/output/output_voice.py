from gtts import gTTS
import tempfile
from playsound import playsound
import os

def fale(texto):
    try:
        tts = gTTS(text=texto, lang='pt-br')
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            caminho_audio = f.name
        tts.save(caminho_audio)
        playsound(caminho_audio)
        os.remove(caminho_audio)
    except Exception as e:
        print(f"[X] Falha ao falar: {e}")
