
  
# T.H.O.R. - Technological Helper for Operations and Response

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/github/license/SantiaGhou/T.H.O.R)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/SantiaGhou/T.H.O.R)](https://github.com/SantiaGhou/T.H.O.R/stargazers)

> T.H.O.R. é um assistente de IA pessoal, local-first e modular, inspirado no J.A.R.V.I.S. Desenvolvido para rodar em sua própria máquina, ele utiliza múltiplos modelos de linguagem (LLMs) para diferentes tarefas, garantindo especialização e privacidade.

## Índice

- [Recursos](#recursos)
- [Arquitetura do Projeto](#arquitetura-do-projeto)
- [Requisitos](#requisitos)
- [Instalação e Configuração](#instalação-e-configuração)
- [Como Usar](#como-usar)
- [Contribuição](#contribuição)
- [Licença](#licença)
- [Autor](#autor)

## Recursos

- **Suporte a abrir o youtube e baixar videos:** utilizando o Pytube e o Webbrowser
- **Suporte a envio de mensagens no Whatsapp** utilizando o whatsapp webjs
- **IA Local-First:** Opera primariamente com modelos de linguagem rodando localmente via **Ollama**, garantindo privacidade e funcionamento offline.
- **Sistema de IA Dupla:** Utiliza um sistema de roteamento inteligente para direcionar as tarefas:
    - **IA de Conversação Geral (Gemma):** Para diálogos, classificação de comandos e tarefas gerais.
    - **IA Especialista em Código (CodeGemma):** Para gerar, analisar e responder perguntas sobre programação.
- **Memória Persistente:** Lembra-se de conversas anteriores entre sessões, salvando o histórico em um arquivo local.
- **Controle de Mídia:** Integração com o Spotify para tocar e pausar músicas.
- **Operações de Sistema:** Capaz de executar comandos no sistema operacional, como abrir pastas de projetos e verificar o status de uso de CPU, RAM e disco.
- **Arquitetura Modular:** Construído com uma clara separação entre o "cérebro" (lógica de decisão) e os "serviços" (executores de ação), facilitando a expansão.

## Arquitetura do Projeto

O T.H.O.R. funciona com um fluxo de comando centralizado no `brain.py`, que atua como um roteador.

```bash
            +----------------------+
            |  Entrada do Usuário  |
            +----------------------+
                     |
                     V
+------------------------------------------+
|           brain.py (O Cérebro)           |
+------------------------------------------+
|                                          |
|  1. Classificação da Intenção            |
|     (Usa a IA Geral para entender a      |
|      pergunta e gerar um JSON)           |
|                                          |
|      e.g., {'controller': 'code_ai'}     |
|                                          |
+------------------------------------------+
                     |
                     | 2. Roteamento da Missão
                     |
+--------------------+---------------------+---------------------+
|                    |                     |                     |
V                    V                     V                     V
+--------------+   +---------------+   +-------------+   +--------------+
| IA de Código |   | IA de Conversa|   |   Serviço   |   |   Serviço    | ...
| (CodeGemma)  |   | (Gemma)       |   |  (Spotify)  |   |     (OS)     |
+--------------+   +---------------+   +-------------+   +--------------+
```
## Requisitos

### Software
- **Python 3.11+**
- **Ollama:** Essencial para rodar os modelos de IA localmente.
- Dependências Python listadas no `requirements.txt`:
  - `openai` (usado como cliente para a API compatível do Ollama)
  - `spotipy` (para controle do Spotify)
  - `python-dotenv` (para gerenciar as chaves de API)
  - `psutil` (para monitoramento do sistema)

### Hardware
- Uma **GPU dedicada com no mínimo 8GB de VRAM** é altamente recomendada para uma experiência fluida.
- Alternativamente, **32GB de RAM** ou mais se for rodar os modelos apenas na CPU.

## Instalação e Configuração

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/SantiaGhou/T.H.O.R.git](https://github.com/SantiaGhou/T.H.O.R.git)
    cd T.H.O.R
    ```

2.  **Instale o Ollama:**
    -   Faça o download e instale o Ollama a partir do [site oficial](https://ollama.com/).

3.  **Baixe os Modelos de IA:**
    -   Abra o terminal e puxe os modelos que o T.H.O.R. utiliza:
    ```bash
    # IA de conversação geral
    ollama run gemma

    # IA especialista em código
    ollama run codegemma
    ```

4.  **Instale as dependências Python:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Configure o Ambiente:**
    -   Crie um arquivo chamado `.env` na raiz do projeto.
    -   Você precisará de credenciais da API do Spotify. Siga o [guia do Spotipy](https://spotipy.readthedocs.io/en/latest/#credentials) para obtê-las.
    -   Adicione suas credenciais ao arquivo `.env`:
    ```env
    # Arquivo .env
    SPOTIFY_CLIENT_ID="SEU_CLIENT_ID_AQUI"
    SPOTIFY_CLIENT_SECRET="SEU_CLIENT_SECRET_AQUI"
    SPOTIFY_REDIRECT_URI="http://localhost:8888/callback"
    ```

## Como Usar

1.  Certifique-se de que o **Ollama está rodando** em segundo plano.

2.  Execute o arquivo principal:
    ```bash
    python main.py
    ```

3.  Na primeira execução, um arquivo `conversation_history.json` será criado para armazenar a memória do assistente.

4. Antes de iniciar o projeto inicie o servidor do whatsapp web na pasta ``` /wppServer ```

5. Use o comando ``` npm i  & node server.js ```

6. Escaneie o qrcode gerado e conecte ao seu whatsapp

## Contribuição

Contribuições são sempre bem-vindas! Por favor, leia o `CONTRIBUTING.md` primeiro.

1.  Faça um Fork do projeto
2.  Crie sua Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4.  Push para a Branch (`git push origin feature/AmazingFeature`)
5.  Abra um Pull Request

##  Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

##  Autor

<img src="https://github.com/SantiaGhou.png?size=100" width="100px" style="border-radius: 50%;">

**Filipe Santiago**

-   GitHub: [@SantiaGhou](https://github.com/SantiaGhou)
-   LinkedIn: [Filipe Santiago](https://linkedin.com/in/filipe-santiago)

---

<div align="center">
  Feito com ❤️ por SantiaGhou
</div>