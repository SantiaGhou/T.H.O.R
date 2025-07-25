def text_input():
    entrada = input("Você: ")
    if entrada.lower() in ['sair', 'exit', 'quit']:
        print("Encerrando...")
        exit()
    return entrada
