import json
import os
import threading
import time
from datetime import datetime, timedelta
from dateparser import parse as parse_date
from ..interfaces.output.output_interface import say

NOTES_FILE = "notes.json"

def speak(text):
    if text and isinstance(text, str):
        say(text)

def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_notes(notes):
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=4)

def add_note(text, remind_at=None):
    notes = load_notes()
    note = {
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "texto": text
    }
    if remind_at:
        note["lembrar_em"] = remind_at.strftime("%Y-%m-%d %H:%M:%S")
        schedule_reminder(text, remind_at)
    notes.append(note)
    save_notes(notes)
    speak("Nota salva com sucesso.")

def list_notes():
    notes = load_notes()
    if not notes:
        speak("Você não tem nenhuma nota.")
        return
    speak("Aqui estão suas notas:")
    for note in notes:
        msg = f"{note['data']}: {note['texto']}"
        if "lembrar_em" in note:
            msg += f" (Lembrete em {note['lembrar_em']})"
        speak(msg)

def schedule_reminder(text, remind_at):
    delay = (remind_at - datetime.now()).total_seconds()
    if delay > 0:
        threading.Timer(delay, lambda: speak(f"Lembrete: {text}")).start()

def parse_and_add(text):
    """
    Detecta se há tempo no texto e cria nota com lembrete.
    Exemplo: "me lembra de desligar o forno daqui 20 minutos"
    """
    reminder_time = None
    parsed = parse_date(text, settings={"PREFER_DATES_FROM": "future"})
    if parsed and parsed > datetime.now():
        reminder_time = parsed
    add_note(text, reminder_time)
