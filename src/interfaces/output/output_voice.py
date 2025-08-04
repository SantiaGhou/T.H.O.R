from torch.serialization import add_safe_globals
from TTS.tts.models.xtts import XttsArgs
from TTS.tts.configs.xtts_config import XttsConfig, XttsAudioConfig
from TTS.config.shared_configs import BaseDatasetConfig
from TTS.api import TTS
import sounddevice as sd
import logging

add_safe_globals([
    XttsArgs,
    XttsConfig,
    XttsAudioConfig,
    BaseDatasetConfig
])

logging.getLogger("TTS").setLevel(logging.ERROR)

tts_model = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False, gpu=False)

def fale(texto):
    try:
        audio = tts_model.tts(
            text=texto,
            speaker=tts_model.speakers[0],
            language="pt"
        )
        sd.play(audio, samplerate=tts_model.synthesizer.output_sample_rate)
        sd.wait()
    except Exception as e:
        print(f"[X] Falha ao falar com Coqui: {e}")
