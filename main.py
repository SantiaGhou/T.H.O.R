from src.thor.boot import iniciar_thor
from getpass import getpass  

def confirm_password():
    senha_correta = "122456"
    tentativa = getpass("Digite a senha de acesso: ")  # Não mostra a senha no terminal
    if tentativa == senha_correta:
        print("✅ Acesso autorizado.")
        return True
    else:
        print("❌ Acesso negado. Saindo do programa...")
        return False

def thor():
    iniciar_thor()

if __name__ == "__main__":
    if confirm_password():
        thor()