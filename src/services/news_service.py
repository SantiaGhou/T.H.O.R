from ..interfaces.output.output_interface import say
from dotenv import load_dotenv
import requests
import os

load_dotenv()
GNEWS_KEY = os.getenv("GNEWS_KEY")

def speak(text):
    if text and isinstance(text, str):
        say(text)

def get_news(language="pt", max_results=5):
    url = f"https://gnews.io/api/v4/top-headlines?lang={language}&max={max_results}&apikey={GNEWS_KEY}"
    r = requests.get(url)
    data = r.json()
    if "articles" in data:
        return [a["title"] for a in data["articles"]]
    return []



def read_news(language="pt"):
    news = get_news(language)
    if not news:
        speak("Não encontrei notícias agora.")
        return
    speak("Aqui estão as últimas notícias:")
    for n in news:
        speak(n)
