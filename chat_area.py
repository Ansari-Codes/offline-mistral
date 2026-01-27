from env import ui, app
from UI import TextArea, Input, Button, RawRow, RawCol, Row, Col, Card, Label, Html, Notify, AddSpace
from backend import read_chats, write_message, rename_chat

def message(msg, ai=False):
    """Render a single message bubble with copy button."""
    with Row().classes("w-full") as c:
        with Col().classes(
            f"{'ml' if not ai else 'mr'}-auto max-w-[70%]"
        ):
            with Card().classes(
                f"""
                relative group
                bg-{'user' if not ai else 'ai'}-msg
                text-{'user' if not ai else 'ai'}-msg-text
                rounded-lg border-2
                border-[var(--q-{'user' if not ai else 'ai'}-border)]
                p-2
                """
            ) as card:

                Button(
                    config={'icon': 'content_copy'},
                    on_click=lambda m=msg: [ui.clipboard.write(m), Notify("Content Copied!", type='positive')]
                ).classes(
                    """
                    absolute top-1 right-1
                    opacity-0 group-hover:opacity-100
                    transition-opacity duration-200
                    text-xs
                    """
                )
                if ai:
                    m = ui.markdown(
                        msg
                        .replace("\\[", "$$").replace("\\]", "$$")
                        .replace("\\(", "$").replace("\\)", "$")
                        # .replace("\n\n", "<br>")
                        # .replace("\n", "<br>"),
                        ,
                        extras=["fenced-code-blocks", "tables", "mermaid", "latex"]
                    ).classes("p-0 m-0 q-markdown")
                else:
                    m = Html(
                        msg,
                    ).classes("p-0 m-0")
    return c, card, m

def TitleChat(chat_id: str, lister, drawer=None):
    chats = read_chats()
    title = chats.get(chat_id, {}).get("title", "New Chat")
    editing = {"mode": False}  
    def activate_edit():
        editing["mode"] = True
        update_ui()
    def confirm_edit():
        nonlocal title
        new_title = title_input.value.strip()
        if new_title:
            rename_chat(chat_id, new_title)
        title = new_title
        lister()
        editing["mode"] = False
        update_ui()
    def update_ui():
        contianer.clear()
        with contianer:
            if editing["mode"]:
                with RawRow().classes("max-w-[1000px] w-full bg-secondary p-2 rounded-full gap-1 border-2 border-[var(--q-primary)]"):
                    nonlocal title_input
                    title_input = Input(value=title).classes("bg-secondary flex flex-1 rounded-full").props("rounded")
                    Button(config={"icon": "check"}, on_click=confirm_edit).classes(
                        "bg-positive text-white p-1 text-xs"
                    ).props('dense rounded')
            else:
                with RawRow().classes("max-w-[1000px] group w-full bg-secondary p-2 px-3 rounded-full gap-2 items-center border-2 border-[var(--q-primary)]"):
                    Label(title).classes("w-fit flex flex-1 text-lg font-medium")
                    Button(config={"icon": "edit"}, on_click=activate_edit).classes(
                        "bg-primary text-white p-1"
                    ).props('dense rounded').classes(
                        """
                        opacity-0 group-hover:opacity-100
                        transition-opacity duration-200
                        text-xs
                        """
                    )
    with ui.page_sticky('top-left', x_offset=20, y_offset=20, expand=True):
        with RawRow().classes("w-full gap-2"):
            Button(config={"icon":"menu"}, color="primary", on_click=drawer.toggle).props("dense").classes("p-2 w-fit h-fit")
            contianer = RawRow().classes("flex flex-1")
            title_input = None
        update_ui()

def ChatArea(chat_id: str):
    chats = read_chats()
    chat = chats.get(chat_id, {})
    with ui.scroll_area().classes(
        "w-full h-[93vh] bg-chat-bg"
    ) as scroller:
        with RawCol().classes("w-full h-fit bg-transparent pt-[70px] pb-[70px] gap-3") as container:
            messages = chat.get('chat', [])
            nol = None
            if not messages:
                nol = Html("""
                        <div style="
                            display:flex;
                            flex-direction:column;
                            align-items:center;
                            justify-content:center;
                            gap:10px;
                            padding:40px 20px;
                            text-align:center;
                        ">
                            <div style="
                                font-size:64px;
                                animation: float 2.5s ease-in-out infinite;
                            ">
                                💬
                            </div>

                            <div style="
                                font-size:22px;
                                font-weight:700;
                                color: var(--q-primary)
                            ">
                                No messages yet
                            </div>

                            <div style="
                                font-size:15px;
                                color:var(--q-accent);
                                max-width:320px;
                            ">
                                Start the conversation
                                Ask anything, I’m ready to help you think, build, and explore.
                            </div>
                        </div>

                        <style>
                        @keyframes float {
                            0%   { transform: translateY(0px); }
                            50%  { transform: translateY(-8px); }
                            100% { transform: translateY(0px); }
                        }
                        </style>
                        """)
            for m in messages:
                role, msg = list(m.items())[0]
                message(msg, ai=role == 'ASSISTANT')
            scroller.scroll_to(percent=100, axis='vertical')
    return container, scroller, nol

def UserChatBox(chat_id: str, assistant=None, container:ui.element|None=None, scroller:ui.scroll_area|None = None, nol=None):
    stop_flag = {"stop": False}  # shared flag for stopping streaming

    def append_message(role, text):
        msg, card, md = message(text, role == 'ASSISTANT')
        msg.move(container)
        container.update()
        scroller.scroll_to(percent=100, axis='vertical')
        if nol and (not nol.is_deleted): nol.delete()
        return md, card

    async def send():
        nonlocal stop_flag
        try:
            msg = textarea.value.strip()
            if not msg: 
                return
            
            write_message(chat_id, user_msg=msg)
            textarea.value = ''
            textarea.update()

            append_message('USER', msg)
            stp_btn.set_visibility(True)
            snd_btn.set_visibility(False)

            last_container, last_card = append_message('ASSISTANT', '')
            last_text = ''
            last_card.classes("bg-ai-msg-active")

            def token_Callback(token):
                nonlocal last_text
                if stop_flag["stop"]:
                    return
                last_text += str(token)
                last_container.set_content(last_text
                    .replace("\\[", "$$").replace("\\]", "$$")
                    .replace("\\(", "$").replace("\\)", "$"))

            if assistant:
                stop_flag["stop"] = False
                try:
                    await assistant(msg, token_Callback, stop_flag=stop_flag, box=last_container)
                    last_card.classes("bg-ai-msg")
                except Exception as e:
                    last_text += f"\n##### An Error Occured While Generation: \n**{str(e)}**"
                    last_container.set_content(last_text
                    .replace("\\[", "$$").replace("\\]", "$$")
                    .replace("\\(", "$").replace("\\)", "$"))
                    last_card.classes("bg-negative text-white")
                write_message(chat_id, assistant_msg=last_text)
                scroller.scroll_to(percent=100, axis='vertical') # pyright: ignore[reportOptionalMemberAccess]
                last_container.set_content(last_text
                    .replace("\\[", "$$").replace("\\]", "$$")
                    .replace("\\(", "$").replace("\\)", "$"))
        finally:
            stp_btn.set_visibility(False)
            snd_btn.set_visibility(True)

    def stop_stream():
        stop_flag["stop"] = True
        Notify("AI Response Stopped", type="warning")
        stp_btn.set_visibility(False)
        snd_btn.set_visibility(True)

    # --- UI Layout ---
    with ui.page_sticky('bottom', y_offset=30, expand=True):
        with RawCol().classes("max-w-[900px] w-full h-full justify-center items-center content-center"):
            with RawRow().classes(
                """
                relative max-w-[900px] w-full bg-surface p-2 rounded-xl
                shadow-lg transition-all duration-300
                focus-within:shadow-[0_0_30px_rgba(34,211,238,0.35)]
                """
            ):
                with RawCol().classes(
                    "w-full max-h-[30vh] overflow-y-auto pr-14"
                ):
                    textarea = TextArea(
                        autogrow=True,
                        flexible=True
                    ).classes(
                        """
                        bg-secondary rounded-lg
                        focus:outline-none
                        focus:ring-0
                        """
                    )
                with RawCol().classes(
                    "h-[43px] absolute bottom-2 right-2 py-0.5 pb-0.5 pr-0.5"
                ):
                    # Stop button
                    stp_btn = Button(
                        config=dict(icon='stop'),
                        on_click=stop_stream,
                        color='negative'
                    ).classes(
                        """
                        text-white h-full w-full
                        shadow-md hover:shadow-lg
                        transition-all duration-200
                        """
                    )

                    # Send button
                    snd_btn = Button(
                        config=dict(icon='send'),
                        on_click=send,
                        color='user-msg'
                    ).classes(
                        """
                        text-white h-full w-full
                        shadow-md hover:shadow-lg
                        transition-all duration-200
                        """
                    )
                    stp_btn.set_visibility(False)
            Label("You have to verify AI responses — they can assist, but may not always be fully accurate.").classes("mt-2 text-xs font-light text-muted_text")


def CreateChatArea(chat_id: str, assistant=None, lister=None, drawer=None):
    """Create the entire chat area, including title, messages, and input box."""
    container, scroller, nol = ChatArea(chat_id)
    TitleChat(chat_id, lister, drawer)
    UserChatBox(chat_id, assistant, container, scroller, nol)
