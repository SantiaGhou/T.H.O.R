import os
import difflib
import psutil


GITHUB_PATH = r"C:\Users\Filipe Santiago\Documents\GitHub"

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
