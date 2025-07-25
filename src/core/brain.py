from src.services import openai_service
from src.services import youtube_service
from ..interfaces.input.input_interface import text_input
import json

def extrair_json(texto: str) -> str:
    start = texto.find('{')
    end = texto.rfind('}') + 1
    if start == -1 or end == -1:
        raise ValueError("JSON não encontrado na resposta")
    return texto[start:end]

def process_command(texto_usuario: str):
    prompt = f"""
Você é o cérebro do T.H.O.R. Dado o comando do usuário, retorne um JSON com:
- controller: nome do serviço (ex: youtube)
- action: ação que deve ser executada (ex: buscar_video, abrir_home, baixar_video)
- parâmetros relevantes com nomes simples como 'query', 'link' ou 'termo_pesquisa'
- sempre inclua o campo "link" se o usuário deseja baixar um vídeo, mesmo que ele não tenha enviado diretamente o link

Apenas utilize "action": "baixar_video" se o comando do usuário:
- contiver um link do YouTube (ex: "https://www.youtube.com/...")
- ou for uma ordem direta como "baixe esse vídeo do YouTube", "faça download do vídeo X do YouTube"

Não bloqueie downloads se o comando for claro e direto.

Comando do usuário: "{texto_usuario}"

Responda apenas com o JSON. Não adicione explicações ou texto fora do JSON.
"""

    resposta = openai_service.question_to_chatgpt(prompt)
 

    try:
        json_str = extrair_json(resposta)
        dados = json.loads(json_str)
        controller = dados.get("controller")
        action = dados.get("action")
        parametros = dados.get("parametros", {})

        if controller == "youtube":
            if action == "baixar_video":
                link = (
                    parametros.get("link")
                    or parametros.get("query")
                    or parametros.get("termo_pesquisa")
                )
                
                
                if not link:
                    print("[?] Claro sem problemas. Por favor, cole o link do vídeo do YouTube que vc quer:")
                    link = input(">>> ")

                if link:
                    from src.services.youtube_service import baixar_video
                    resultado = baixar_video(link)
                    print(resultado)
                else:
                    print("[X] Nenhum link fornecido. Cancelando operação.")

            else:
                print("[INFO] Chamando youtube_service...")
                youtube_service.youtube(dados)

        elif controller == "openai":
            resposta_openai = openai_service.question_to_chatgpt(texto_usuario)
            print(resposta_openai)
        else:
            resposta_openai = openai_service.question_to_chatgpt(texto_usuario)
            print(resposta_openai)

    except Exception as e:
        print("[X] Erro no brain:", e)
        print("Resposta bruta:", resposta)
        resposta_openai = openai_service.question_to_chatgpt(texto_usuario)
        print(resposta_openai)
