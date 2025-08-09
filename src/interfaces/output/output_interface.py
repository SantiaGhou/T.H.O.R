import os, tempfile
from playsound import playsound
from openai import OpenAI
client=OpenAI()
def say(text):
    model=os.getenv("THOR_TTS_MODEL","gpt-4o-mini-tts")
    voice=os.getenv("THOR_TTS_VOICE","echo")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        path=tmp.name
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
