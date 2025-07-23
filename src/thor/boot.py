import time
import sys
from colorama import init, Fore, Style
import pyfiglet

init()

def type_writer(text, color=Fore.WHITE, delay=0.03):
    for char in text:
        sys.stdout.write(color + char + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def iniciar_thor():
    ascii_art = pyfiglet.figlet_format("T. H . O . R .")
    print(ascii_art)
    print(Fore.LIGHTGREEN_EX + "Bem-vindo ao T.H.O.R., o sistema de inteligência artificial avançada." + Style.RESET_ALL)
    print()

    boot_sequence = [
        "[INICIANDO SISTEMA T.H.O.R...]",
        "Verificando integridade de arquivos...",
        "Inicializando módulos de controle...",
        "Conectando com núcleo de IA...",
        "Sincronizando sensores...",
        "Status: Estável ✅",
        "Autenticação biométrica confirmada.",
        "Acesso autorizado.",
        "",
        ">>> SISTEMA T.H.O.R. ONLINE <<<"
    ]

    colors = [
        Fore.CYAN,
        Fore.YELLOW,
        Fore.BLUE,
        Fore.MAGENTA,
        Fore.GREEN,
        Fore.LIGHTGREEN_EX,
        Fore.LIGHTCYAN_EX,
        Fore.LIGHTWHITE_EX,
        "",
        Fore.LIGHTRED_EX
    ]

    for line, color in zip(boot_sequence, colors):
        type_writer(line, color=color)
        time.sleep(0.4)

    for _ in range(3):
        sys.stdout.write("\r" + Fore.LIGHTGREEN_EX + ">>> SISTEMA T.H.O.R. ONLINE <<<" + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(0.4)
        sys.stdout.write("\r" + " " * 40)
        sys.stdout.flush()
        time.sleep(0.3)

    print("\r" + Fore.GREEN + ">>> SISTEMA T.H.O.R. ONLINE <<<" + Style.RESET_ALL)

if __name__ == "__main__":
    iniciar_thor()
