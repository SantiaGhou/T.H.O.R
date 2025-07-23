from src.core.boot import iniciar_thor
from getpass import getpass  
from src.services.openai_service import question_to_chatgpt

def confirm_password():
    senha_correta = "122456"
    tentativa = getpass("Digite a senha de acesso: ")  
    if tentativa == senha_correta:
        print("✅ Acesso autorizado.")
        return True
    else:
        print("❌ Acesso negado. Saindo do programa...")
        return False

#--------------------------------------------------------------------------------------------------------------------------------#

def thor():
    iniciar_thor()
    print("Digite 'sair' para encerrar o assistente.\n")

    while True:
        pergunta = input(">>")
        if pergunta.lower() in ['sair', 'exit', 'quit']:
            print("Encerrando...")
            break

        resposta = question_to_chatgpt(pergunta)
        print(f"\nThor: {resposta}\n")

if __name__ == "__main__":
    thor()