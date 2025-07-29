import os
import difflib
import psutil
import dotenv
import platform
import socket
import subprocess
import glob
import pythoncom
from win32com.shell import shell

GITHUB_PATH = dotenv.get_key('.env', 'GITHUB_PATH')

def list_projects():
    try:
        return [name for name in os.listdir(GITHUB_PATH) if os.path.isdir(os.path.join(GITHUB_PATH, name))]
    except Exception:
        return []

def find_project(user_input):
    projects = list_projects()
    if not projects:
        return None, "No projects found in GitHub folder."
    user_input = user_input.lower()
    matches = difflib.get_close_matches(user_input, projects, n=1, cutoff=0.4)
    if matches:
        project_name = matches[0]
        path = os.path.join(GITHUB_PATH, project_name)
        return path, f"Project '{project_name}' found."
    return None, f"No matching project found for '{user_input}'."

def open_project(params):
    name = params.get("query") or params.get("project")
    if not name:
        return "No project name provided."
    path, message = find_project(name)
    if path:
        os.system(f'code "{path}"')
    return message

def get_system_status():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    return f"CPU: {cpu}% RAM: {ram}% Disco: {disk}%"

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
    resposta = ""
    for p in top_procs:
        resposta += f"{p['name']} (PID {p['pid']}): {p['memory_percent']:.1f}%\n"
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
    output = ""
    for chave, valor in info.items():
        output += f"{chave}: {valor}\n"
    return output

def resolve_lnk(lnk_path):
    pythoncom.CoInitialize()
    shell_link = pythoncom.CoCreateInstance(shell.CLSID_ShellLink, None, pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IShellLink)
    persist_file = shell_link.QueryInterface(pythoncom.IID_IPersistFile)
    persist_file.Load(lnk_path)
    target, _ = shell_link.GetPath(shell.SLGP_UNCPRIORITY)
    return target

def encontrar_executavel_atalho(query):
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    start_menu = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs")
    query = query.lower()
    for pasta in (desktop, start_menu):
        pattern = os.path.join(pasta, "**", "*.lnk")
        for caminho in glob.glob(pattern, recursive=True):
            if query in os.path.basename(caminho).lower():
                target = resolve_lnk(caminho)
                if target and os.path.exists(target):
                    return target
    return None

def encontrar_executavel(query):
    caminho = encontrar_executavel_atalho(query)
    if caminho:
        return caminho
    extensoes = (".exe", ".bat", ".lnk")
    possiveis_pastas = [
        r"C:\Program Files",
        r"C:\Desktop",
        r"C:\Program Files (x86)",
        r"C:\Games",
        r"C:\SteamLibrary",
        os.path.join(os.path.expanduser("~"), "AppData", "Local"),
        os.path.join(os.path.expanduser("~"), "AppData", "Roaming"),
        os.path.join(os.path.expanduser("~"), "Desktop"),
    ]
    query = query.lower()
    candidatos = []
    for pasta in possiveis_pastas:
        if not os.path.exists(pasta):
            continue
        for raiz, dirs, arquivos in os.walk(pasta):
            for arquivo in arquivos:
                nome_arquivo = arquivo.lower()
                if nome_arquivo.endswith(extensoes) and query in nome_arquivo:
                    candidatos.append(os.path.join(raiz, arquivo))
    if candidatos:
        candidatos.sort(key=lambda x: len(x))
        return candidatos[0]
    return None

def open_program(params):
    nome = params.get("query", "")
    caminho = encontrar_executavel(nome)
    if caminho:
        subprocess.Popen(caminho)
        return f"{nome} aberto"
    return f"Não encontrei nenhum programa relacionado a: {nome}"

def get_data():
    try:
        from datetime import datetime
        agora = datetime.now()
        return agora.strftime("%d/%m/%Y %H:%M:%S")
    except Exception as e:
        return f"Erro ao obter data: {e}"
