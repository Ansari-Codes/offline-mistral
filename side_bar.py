from UI import Drawer, Button, Col, RawCol, Row, Card, Input, openLink, AddSpace, Label, confirm
from backend import all_chats, delete_chat
import env
import dialogs

async def Create_Side_Bar(chat_creator=None, chat_opener=None, loader=None, empty=None):
    drawer = Drawer().classes("bg-surface")
    (tokenizer, model, tm), model_loaded = await loader() # type:ignore
    if not model_loaded:
        return None, None, None
    def open_chat(chat):
        if chat_opener: chat_opener(chat['id'], dict(model=model, tokenizer=tokenizer), ListChats)
    def create_chat():
        if chat_creator: chat_creator(dict(model=model, tokenizer=tokenizer), ListChats)
        ListChats()
    def del_chat(c):
        confirm(f"Are you sure to delete the chat `{c['title']}` forever? This is not reversible!",
            on_yes=lambda: [delete_chat(c['id']), ListChats(), empty() if empty else None])
    def ListChats(e=None):
        query = search.value.lower().strip()  # type:ignore
        chats.clear()
        with chats:
            for chat in all_chats(query):
                g20 = len(chat.get('title','')) > 20
                title = chat.get('title', '')
                short_title = title[:g20*20 + (not g20)*len(title)] + '...'*g20
                with Row().classes("w-full items-center justify-between relative group"):
                    Button(
                        text=short_title,
                        on_click=lambda c=chat: open_chat(c)
                    ).props('icon="message" color="btn-secondary" align="left"').classes("w-full flex-1 text-left")
                    Button(
                        config=dict(icon='delete_forever'),
                        on_click=lambda c=chat: del_chat(c)
                    ).props('dense rounded color="negative"').classes(
                        """absolute right-1 text-xs opacity-0 group-hover:opacity-100
                        transition-opacity duration-200"""
                    )
    
    with drawer:
        with RawCol().classes("w-full h-full flex flex-col"):
            with Card().classes("w-full h-fit mb-1 bg-primary"):
                Label(env.LOGO + ' ' + env.NAME).classes("text-2xl font-bold w-full text-white")
            Button(
                'New Chat',
                on_click=create_chat,
                config={'icon':'add'}
            ).classes("w-full mb-2")

            search = Input(
                placeholder='Search chats...'
            ).classes("w-full mb-1")

            chats = RawCol().classes(
                "gap-1 w-full flex-1 overflow-y-auto mt-1 mb-2 p-0.5 border-1 border-[var(--q-border)] rounded-sm bg-secondary"
            )
            search.on_value_change(ListChats)
            ListChats()
            Button(
                'Settings',
                on_click=lambda: dialogs.createSettings().open(),
                config={'icon': 'settings'}
            ).classes("w-full mb-2")
            Button(
                'About',
                on_click=lambda:(),
                config={'icon':'info'}
            ).classes("w-full mb-2")
    return drawer, ListChats, create_chat
