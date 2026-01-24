from nicegui import Client, ui
from typing import Callable, Literal
from webbrowser import open_new
def navigate(link:str,new_tab:bool=False):ui.navigate.to(link,new_tab)
def openLink(link:str):open_new(link)
def Label(text="", model=None, model_configs=None):
    lbl = ui.label(text)
    if model:
        model_configs = model_configs or {}
        lbl.bind_text(model, target_name='value', **model_configs)
    return lbl
def Drawer(**kwargs):return ui.left_drawer(**kwargs)
def Header(): return ui.header(fixed=True, elevated=False)
def Html(html: str): return ui.html(html, sanitize=lambda x:x)
def Col(): return ui.column()
def Row(): return ui.row()
def RawCol(): return ui.element().classes("flex flex-col")
def RawRow(): return ui.element().classes("flex flex-row")
def Center(): return ui.element( ).classes("flex justify-center items-center" )
def Footer(config: dict|None = None): return ui.footer(**(config or {}))
def Card(align: Literal['start', 'end', 'center', 'baseline', 'stretch']|None = None ):
    return ui.card(align_items=align).classes("bg-card-l dark:bg-card-d")

def Link(
        text: str = "",
        link: str = "",
        underline:  bool = True,
        new_tab: bool = False,
    ):
    return ui.link(text, link, new_tab).classes("hover:underline"*underline )

def Choice(choices:list|dict, value, **kwargs):
    return ui.toggle(choices, value=value, **kwargs)

def Input(
        model = None,
        default_props: bool|None = True,
        bindings: dict|None = None,
        type: Literal['text', 'color', 'number', 'file'] = 'text',
        **kwargs
    ):
    bindings = bindings or {}
    inp = None
    if type == "text": inp = ui.input(**kwargs)
    elif type == "color": inp = ui.color_input(**kwargs)
    elif type == 'number': inp = ui.number(**kwargs)
    else: inp = ui.input().props(f'type="{type}"')
    if inp:
        inp.classes("bg-inp rounded-sm")
        inp.props('input-class="text-text-secondary"')
        inp.props("dense outlined"*bool(default_props) + ' ')
        if model: inp.bind_value(model, 'value', **bindings)
    return inp

def Select(
        model = None,
        options: list|dict|None = None,
        default_props: bool|None = True,
        bindings: dict|None = None,
        **kwargs
    ):
    bindings = bindings or {}
    slc = ui.select(options=options or [], **kwargs)
    slc.props("dense outlined"*bool(default_props) + ' ')
    if model: slc.bind_value(model, 'value', **bindings)
    slc.classes("bg-inp rounded-sm").props('input-class="text-text-secondary"')
    return slc

def Button(
        text: str = "", 
        on_click = lambda: (),
        link="",
        new_tab=False,
        config: dict|None = None,color='primary'
    ):
    if not config: config = {}
    btn = ui.button(text=text, on_click=on_click, color=color, **config).props("unelevated").classes("bg-btn-l dark:bg-btn-d")
    if link:
        btn.props(f'href="{link}"')
    if new_tab:
        btn.props(f'target="_blank"')
    return btn

def TextArea(
        content: str = "",
        model=None,
        autogrow: bool = False,
        max_h: str|None = None,
        min_h: str|None = None,
        overflow: str|None = None,
        flexible: bool = False,
        config: dict|None = None,
        inp_cls: str = "",
        inp_prp: str = "",
        inp_sty: str = "",
    ):
    if not config: config = {}
    ta = ui.input(value=content, **config)
    inner_classes = ""
    if model: ta.bind_value(model)
    if flexible: inner_classes += " flex-grow flex-shrink resize-none"
    if min_h: inner_classes += f" min-h-[{min_h}]"
    if max_h: inner_classes += f" max-h-[{max_h}]"
    if overflow: inner_classes += f" overflow-{overflow}"
    if autogrow: ta.props('autogrow')
    ta.classes(inner_classes)
    ta.props('dense outlined')
    ta.classes("bg-inp rounded-sm").props(f'input-class="{inp_cls}" input-props="{inp_prp}" input-style="{inp_sty}"')
    return ta

def CheckBox(
        text:str = "",
        value:bool = False,
        on_change:Callable = lambda x:()
    ):
    return ui.checkbox(text, value=value, on_change=on_change)

def AddSpace():
    return ui.space()

def Icon(
        name: str = "" , 
        size: str|None = None,
        color: str|None = None,
    ):
    return ui.icon(name, size=size, color=color)

def Notify(
        message:str = '', 
        position:Literal['top-left', 'top-right', 'bottom-left', 
                        'bottom-right', 'top', 'bottom', 'left', 
                        'right', 'center'
                        ]='top-right',
        close_button='✖', 
        **kwargs
    ): ui.notify(message, position=position, close_button=close_button, **kwargs)

def Dialog():
    return ui.dialog().props('backdrop-filter="hue-rotate(10deg)"')

class logger(ui.html):    
    def __init__(self, content: str = '', *, sanitize: Callable[[str], str] | Literal[False] = lambda x:x, tag: str = 'div') -> None:
        super().__init__(content, sanitize=sanitize, tag=tag)
    def print(self, line: str, classes="", props="", style=""):
        self.content = f'{self.content}<p class="{classes}" {props} style="{style}">{line}</p>'
        self.update()

def Logger():
    return logger()

def confirm(statement="", on_yes=None, on_no=None):
    d = Dialog().props("persistent")
    def yes():
        if on_yes: on_yes()
        d.delete()  # close the dialog after yes

    def no():
        if on_no: on_no()
        else: d.delete()  # close if no function is not provided

    with d:
        with Card():
            Label(statement).classes("text-md font-semibold")
            with Row():
                Button("Yes", config=dict(icon='check'), color="positive", on_click=yes)
                Button("No", config=dict(icon='close'), color="negative", on_click=no)
    d.open()  # make sure the dialog actually opens
    return d

def navBar(icon = "", links:dict|None = None, bkp="sm"):
    with ui.element().classes("w-fit h-fit") as nav:
        with ui.element().classes(f"items-center justify-between gap-2 hidden {bkp}:!flex", remove='hidden') as desktop:
            for name,opts in (links or {}).items():
                if isinstance(opts, (dict)):
                    condition = opts.pop("cond", True)
                    if condition:
                        Button(name, **opts)
                else:
                    Button(name, link=opts)
        with Button(config=dict(icon="menu")).classes(f"flex {bkp}:hidden") as mobile:
            with ui.menu().props("auto-close"):
                with RawCol().classes("w-fit gap-1 p-1 bg-secondary"):
                    for name,opts in (links or {}).items():
                        if isinstance(opts, (dict)):
                            condition = opts.pop("cond", True)
                            if condition:
                                Button(name, **opts).classes("w-full")
                        else:
                            Button(name, link=opts).classes("w-full")
    return nav, desktop, mobile