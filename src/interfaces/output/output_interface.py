import os
import tempfile
from playsound import playsound
from openai import OpenAI

def say(text):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("[X] OPENAI_API_KEY não definida no ambiente.")
        return
    model = os.getenv("THOR_TTS_MODEL", "gpt-4o-mini-tts")
    voice = os.getenv("THOR_TTS_VOICE", "echo")
    client = OpenAI(api_key=api_key)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        path = tmp.name
    with client.audio.speech.with_streaming_response.create(
        model=model,
        voice=voice,
        input=text
    ) as resp:
        resp.stream_to_file(path)
    playsound(path)
    try:
        os.remove(path)
    except:
        pass
