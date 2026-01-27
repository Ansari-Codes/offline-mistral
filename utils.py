from datetime import datetime
from env import ui
import socket

def time_ago(ts):
    now = datetime.now()
    dt = datetime.fromisoformat(ts)
    diff = now - dt

    seconds = diff.total_seconds()

    if seconds < 60:
        return "Just now"
    elif seconds < 3600:
        return f"{int(seconds//60)} min ago"
    elif seconds < 86400:
        return f"{int(seconds//3600)} hr ago"
    else:
        return dt.strftime("%d %b %Y")

def Loading(text=None, spinner={"type":"box", "size": "lg", "color":"primary"}, rs="r"):
    text = text or "Loading..."
    with ui.row().classes("w-full h-full justify-center items-center") as r:
        ui.spinner(**spinner)
        h = ui.html(text, sanitize=lambda x:x)
    if rs == 'r': return r
    elif rs == 'rh': return r,h
    return r,h

def get_free_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 0))
    port = sock.getsockname()[1]
    sock.close()
    return port
