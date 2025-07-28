import os
import difflib
import psutil
import dotenv
import platform
import socket

GITHUB_PATH = dotenv.get_key('.env', 'GITHUB_PATH')

def list_projects():
    try:
        return [name for name in os.listdir(GITHUB_PATH)
                if os.path.isdir(os.path.join(GITHUB_PATH, name))]
    except Exception as e:
        return []

def find_project(user_input):
    projects = list_projects()

    if not projects:
        return None, "[X] No projects found in GitHub folder."

    user_input = user_input.lower()
    matches = difflib.get_close_matches(user_input, projects, n=1, cutoff=0.4)
    
    if matches:
        project_name = matches[0]
        path = os.path.join(GITHUB_PATH, project_name)
        return path, f"[✔] Project '{project_name}' found."
    
    return None, f"[X] No matching project found for '{user_input}'."

def open_project(params: dict):
    name = params.get("query") or params.get("project")
    if not name:
        return "[X] No project name provided."

    path, message = find_project(name)
    
    if path:
        os.system(f'code "{path}"')
    return message

def get_system_status():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    return f"""
[📊 STATUS DO SISTEMA]
CPU: {cpu}%
RAM: {ram}%
Disco: {disk}%
"""

def listar_processos_pesados(top=5):
    processos = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
        try:
            info = proc.info
            if info['memory_percent'] > 0.1:  
                processos.append(info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    processos.sort(key=lambda x: x['memory_percent'], reverse=True)
    top_procs = processos[:top]

    resposta = "[💾 Processos que mais usam RAM agora]\n"
    for p in top_procs:
        resposta += f"- {p['name']} (PID {p['pid']}): {p['memory_percent']:.1f}%\n"

    return resposta

def get_system_info():
    info = {
        "Sistema Operacional": platform.system(),
        "Versão do SO": platform.version(),
        "Distribuição": platform.platform(),
        "Nome da Máquina": socket.gethostname(),
        "Arquitetura": platform.machine(),
        "Processador": platform.processor(),
        "CPU Física": psutil.cpu_count(logical=False),
        "CPU Lógica": psutil.cpu_count(logical=True),
        "RAM Total": f"{round(psutil.virtual_memory().total / (1024**3), 2)} GB"
    }

    output = "[🧠 CONFIGURAÇÕES DO SISTEMA]\n"
    for chave, valor in info.items():
        output += f"{chave}: {valor}\n"

    return output
