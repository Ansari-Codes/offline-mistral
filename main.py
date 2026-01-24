from nicegui import ui, app
import side_bar
from chat_area import CreateChatArea
from ai import initialize_model_stream, loadModel
from utils import Loading
from backend import get_messages, create_chat

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
    async def LoadModel():
        loading = Loading("Loading Models...")
        _ = await loadModel() #type:ignore
        loading.delete() #type:ignore
        return _

    def emtpy():
        chat_area.clear()
        with chat_area:
            empty_state = ui.html("""
                <style>
                .empty-wrap {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    gap: 16px;
                    padding: 40px;
                    border-radius: 20px;
                    text-align: center;
                    background: linear-gradient(
                        135deg,
                        #7dd3fc,
                        #2563eb
                    );
                    color: white;
                    animation: float 4s ease-in-out infinite;
                    box-shadow: 0 20px 40px rgba(37,99,235,0.35);
                    max-width: 420px;
                }

                @keyframes float {
                    0%,100% { transform: translateY(0); }
                    50% { transform: translateY(-10px); }
                }

                .empty-title {
                    font-size: 1.6rem;
                    font-weight: bold;
                }

                .empty-sub {
                    font-size: 0.95rem;
                    opacity: 0.9;
                }

                .empty-hint {
                    font-size: 0.85rem;
                    opacity: 0.8;
                }
                </style>

                <div class="empty-wrap">
                    <div class="empty-title">No conversation yet 💬</div>
                    <div class="empty-sub">
                        Your AI assistant is ready and waiting.
                    </div>
                    <div class="empty-hint">
                        Type a message below to get started ✨
                    </div>
                </div>
                """, 
            sanitize=lambda x:x)
    
    def openChat(id, models, lister):
        chat_area.clear()
        msgs = get_messages(id)
        if len(msgs) > 10:
            msgs = msgs[-10:]
        assistant = initialize_model_stream(**models, msgs=msgs)
        with chat_area: CreateChatArea(id, assistant, lister)

    def createChat(models, lister):
        chat_area.clear()
        created_chat = create_chat()
        assistant = initialize_model_stream(**models, msgs=[])
        with chat_area: CreateChatArea(created_chat['id'], assistant, lister)

    await side_bar.Create_Side_Bar(createChat, openChat, LoadModel, emtpy)
    chat_area = ui.element().classes("w-full h-full flex items-center justify-center")
    emtpy()
# app.on_disconnect(lambda: [app.shutdown(), exit()])
ui.run(reload=True, native=True)