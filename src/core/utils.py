import json
import os
import re
from ..interfaces.output.output_interface import say

HISTORY_FILE = "conversation_history.json"

def speak(text):
    print(text)
    try:
        if text and isinstance(text, str):
            say(text)
    except:
        pass

def save_history(history):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def extract_json(text):
    start = text.find('{')
    end = text.rfind('}') + 1
    if start == -1 or end == -1:
        raise ValueError("JSON não encontrado")
    return text[start:end]

def mensagem_exata(contexto):
    match = re.search(r'"([^\"]+)"|\'([^\']+)\'', contexto)
    if match:
        return match.group(1) or match.group(2)
    padroes = [
        r"exatamente assim: (.+)",
        r"envia isso: (.+)",
        r"mensagem literal: (.+)",
        r"manda (.+) exatamente"
    ]
    for padrao in padroes:
        m2 = re.search(padrao, contexto, re.IGNORECASE)
        if m2:
            return m2.group(1).strip()
    return None
