from nicegui import ui, app
import side_bar
from chat_area import CreateChatArea
from ai import initialize_model_stream, loadModel
from utils import Loading
from backend import get_messages, create_chat
from UI import Dialog, Icon, Label, Card, RawCol, Row, Col, Button
import dialogs

@ui.page('/')
async def page():
    AI_BLUE = {
        "primary": "#2563EB",     
        "secondary": "#F8FAFC",   
        "background": "#FFFFFF",  
        "surface": "#EEF2FF",     
        "text": "#0F172A",        
        "muted_text": "#64748B",  
        "accent": "#22D3EE",      
        "border": "#CBD5E1",      
        "btn-secondary": "#60A5FA",
        "chat-bg": "#F8FAFF",
        "ai-msg": "#EEF2FF",
        "ai-msg-text": "#0F172A",
        "user-msg": "#2563EB",
        "user-msg-text": "#FFFFFF",
        "ai-border": "#CBD5E1",
        "user-border": "#1D4ED8",
        "ai-msg-active": "#E0F7FF",
    }
    ui.colors(**AI_BLUE)
    await ui.context.client.connected()
    error_occured = {"error": False}
    def onError(e):
        chat_area.clear()
        with chat_area:
            with RawCol().classes("w-full h-fit bg-surface rounded-md text-left leading-loose text-negative p-3 gap-1"):
                Label("Cannot Load the Model").classes("w-full h-fit text-xl font-bold")
                Label(str(e)).classes("w-full h-fit capitalize text-lg")
        error_occured.update({"error":True})
    async def LoadModel():
        loading = Loading("Loading Models...")
        try:
            _ = await loadModel() #type:ignore
            loading.delete() #type:ignore
            return _, True
        except Exception as e:
            loading.delete() # type:ignore
            onError(e)
            return (None, None, None), False
    
    def empty():
        if list(error_occured.values())[0]: return
        chat_area.clear()
        with chat_area:
            with Row().classes("justify-center items-center h-[95vh]"):
                with Col().classes("items-center justify-center gap-4 max-w-xl h-fit"):
                    with Card().classes("w-full bg-primary text-white shadow-lg rounded-xl flex flex-col items-center gap-4"):
                        Label("No conversation yet").classes("text-2xl font-bold text-center")
                        Label("Your AI assistant is ready and waiting.").classes("text-base opacity-90 text-center")
                        with Row():
                            Button("New Chat", on_click=creator, color='accent')
                            Button("Read Docs", on_click=dialogs.docs, color='accent')

    def openChat(id, models, lister, drawer):
        chat_area.clear()
        msgs = get_messages(id)
        if len(msgs) > 10: msgs = msgs[-10:]
        assistant = initialize_model_stream(**models, msgs=msgs)
        with chat_area: CreateChatArea(id, assistant, lister, drawer)

    def createChat(models, lister, drawer):
        chat_area.clear()
        created_chat = create_chat()
        assistant = initialize_model_stream(**models, msgs=[])
        with chat_area: CreateChatArea(created_chat['id'], assistant, lister, drawer)
    
    chat_area = ui.element().classes("w-full h-full flex items-center justify-center")
    _, _, creator = await side_bar.Create_Side_Bar(createChat, openChat, LoadModel, empty)
    empty()

app.on_disconnect(lambda: [app.shutdown(), exit()])
import os
PORT = os.getenv("PORT", 8080)
ui.run(reload=False, port=62343)