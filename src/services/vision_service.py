import cv2
import tempfile
import os
import subprocess

def capturar_foto():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        return None
    tmp_path = os.path.join(tempfile.gettempdir(), "thor_vision.jpg")
    cv2.imwrite(tmp_path, frame)
    return tmp_path

def descrever_cena():
    path = capturar_foto()
    if not path:
        return "[X] Não foi possível capturar imagem."

    prompt = "Descreva detalhadamente o que você vê nesta imagem."
    try:
        result = subprocess.run(
            ["ollama", "run", "llava", prompt, "--image", path],
            capture_output=True, text=True
        )
        return result.stdout.strip() or "[!] Não consegui gerar descrição."
    except Exception as e:
        return f"[X] Erro ao usar LLaVA: {e}"

def reconhecer_texto():
    path = capturar_foto()
    if not path:
        return "[X] Não foi possível capturar imagem."

    try:
        result = subprocess.run(
            ["tesseract", path, "stdout", "-l", "por"],
            capture_output=True, text=True
        )
        texto = result.stdout.strip()
        return texto if texto else "[!] Nenhum texto reconhecido."
    except Exception as e:
        return f"[X] Erro ao usar Tesseract: {e}"

