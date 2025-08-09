import os, io, re, wave, queue, threading, numpy as np, sounddevice as sd, webrtcvad
from openai import OpenAI

RATE = 16000
BLOCK = 1024
CHANNELS = 1
DEV = os.getenv("THOR_INPUT_DEVICE")
if DEV is not None:
    DEV = int(DEV)
NAME = os.getenv("THOR_INPUT_DEVICE_NAME")
AUDIO_Q = queue.Queue()
VAD = webrtcvad.Vad(2)
HOT = re.compile(r"\b(thor|tor|for|t[oó]|th[oó]r)\b", re.I)

def _resolve_device():
    if NAME:
        for i, d in enumerate(sd.query_devices()):
            if NAME.lower() in d["name"].lower():
                return i
    return DEV

def _callback(indata, frames, time_info, status):
    AUDIO_Q.put(indata.copy())

def _is_speech(frame):
    pcm = (frame * 32767).astype(np.int16).tobytes()
    return VAD.is_speech(pcm, RATE)

def _wav_bytes_from_float32(mono):
    pcm = (np.clip(mono, -1, 1) * 32767).astype(np.int16).tobytes()
    buf = io.BytesIO()
    wf = wave.open(buf, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(RATE)
    wf.writeframes(pcm)
    wf.close()
    buf.seek(0)
    return buf

def _transcribe_wav_bytes(bio):
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    bio.name = "audio.wav"
    model = os.getenv("THOR_TRANSCRIBE_MODEL", "gpt-4o-mini-transcribe")
    r = client.audio.transcriptions.create(model=model, file=bio, language="pt")
    return (r.text or "").strip().lower()

def start_voice(on_text):
    try:
        import winsound
        def beep(): winsound.Beep(1200, 120)
    except:
        def beep(): pass

    device = _resolve_device()
    with sd.InputStream(channels=CHANNELS, samplerate=RATE, blocksize=BLOCK,
                        callback=_callback, dtype="float32", device=device):
        state = "wake"
        buf = np.zeros((0, 1), dtype=np.float32)
        silence = 0
        speaking = False
        while True:
            data = AUDIO_Q.get()
            buf = np.concatenate([buf, data], axis=0)
            if state == "wake":
                if buf.shape[0] >= int(1.0 * RATE):
                    chunk = buf[-int(1.0 * RATE):, 0]
                    txt = _transcribe_wav_bytes(_wav_bytes_from_float32(chunk))
                    if HOT.search(txt):
                        beep()
                        state = "cmd"
                        buf = np.zeros((0, 1), dtype=np.float32)
                        silence = 0
                        speaking = False
                    else:
                        buf = np.zeros((0, 1), dtype=np.float32)
            else:
                frame = buf[-BLOCK:, 0] if buf.shape[0] >= BLOCK else buf[:, 0]
                if frame.size == BLOCK:
                    if _is_speech(frame):
                        speaking = True
                        silence = 0
                    else:
                        if speaking:
                            silence += 1
                    if speaking and silence >= int(0.9 / (BLOCK / RATE)):
                        audio = buf[:, 0]
                        txt = _transcribe_wav_bytes(_wav_bytes_from_float32(audio))
                        if txt:
                            on_text(txt)
                        state = "wake"
                        buf = np.zeros((0, 1), dtype=np.float32)
                        silence = 0
                        speaking = False

def start_voice_thread(on_text):
    t = threading.Thread(target=start_voice, args=(on_text,), daemon=True)
    t.start()
    return t
