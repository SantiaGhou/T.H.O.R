from src.handlers import youtube_handler, os_handler, spotify_handler, notes_handler, news_handler, whatsapp_handler, vision_handler, openai_handler, code_ai_handler

handlers = {
    "youtube": youtube_handler.handle,
    "os": os_handler.handle,
    "spotify": spotify_handler.handle,
    "notes": notes_handler.handle,
    "news": news_handler.handle,
    "whatsapp": whatsapp_handler.handle,
    "vision": vision_handler.handle,
    "openai": openai_handler.handle,
    "code_ai": code_ai_handler.handle
}

def route_command(controller, action, params, history, user_input):
    if controller in handlers:
        handlers[controller](action, params, history, user_input)
    else:
        openai_handler.handle("responder", {"query": user_input}, history, user_input)
