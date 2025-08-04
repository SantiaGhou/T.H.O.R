from TTS.api import TTS
import sounddevice as sd

import logging
logging.getLogger("TTS").setLevel(logging.ERROR)

tts_model = TTS(model_name="tts_models/pt/cv/vits", progress_bar=False, gpu=False)


def fale(texto):
    try:
        audio = tts_model.tts(text=texto)
        sd.play(audio, samplerate=tts_model.synthesizer.output_sample_rate)
        sd.wait()
    except Exception as e:
        print(f"[X] Falha ao falar com Coqui: {e}")
