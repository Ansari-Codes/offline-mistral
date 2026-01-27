import json
from datetime import datetime
import uuid
from pathlib import Path
import os

def exists():
    app_dir = Path.home() / ".qod"
    app_dir.mkdir(parents=True, exist_ok=True)
    config_file = app_dir / "config.json"
    chat_file = app_dir / "chats.json"
    if not config_file.exists():
        config_file.write_text(json.dumps({"top_p": 0.8, "temperature": 0.9, "max_new_tokens": 2048, "custom_instructions": ""}, indent=2))
        try:
            os.chmod(config_file, 0o644)
        except Exception:
            pass
    if not chat_file.exists():
        chat_file.write_text(json.dumps({}, indent=2))
        try:
            os.chmod(chat_file, 0o644)
        except Exception:
            pass
    return config_file, chat_file

def read_chats() -> dict:
    _,cf = exists()
    try:
        with open(cf, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        with open(cf, 'w', encoding='utf-8') as f:
            json.dump({}, f)
        return {}

def read_config() -> dict:
    cgf, _ = exists()
    try:
        with open(cgf, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        with open(cgf, 'w', encoding='utf-8') as f:
            json.dump({"max_new_tokens": 1000, "temperature": 0.7, "top_p":0.9, "custom_instructions": ""}, f)
        return {"max_new_tokens": 1000, "temperature": 0.7, "top_p":0.9, "custom_instructions":""}

def write_config(config: dict) -> None:
    cgf, _ = exists()
    with open(cgf, 'w', encoding='utf-8') as f:
        json.dump(config, f)

def create_chat(title: str = '') -> dict:
    _,cf = exists()
    chats = read_chats()
    now = datetime.now().isoformat()
    chat_id = str(uuid.uuid4())
    chats[chat_id] = {
        'title': title or f"Chat-{chat_id[:8]}",
        'created_at': now,
        'last_update': now,
        'chat': []
    }
    with open(cf, 'w', encoding='utf-8') as f:
        json.dump(chats, f, indent=2, ensure_ascii=False)
    return {'id': chat_id, 'chat': chats[chat_id]}

def write_message(chat_id, user_msg=None, assistant_msg=None):
    _,cf = exists()
    chats = read_chats()
    if chat_id not in chats:
        raise ValueError(f"Chat ID {chat_id} does not exist")
    now = datetime.now().isoformat()
    if user_msg: chats[chat_id]['chat'].append({'USER': user_msg})
    if assistant_msg: chats[chat_id]['chat'].append({'ASSISTANT': assistant_msg})
    chats[chat_id]['last_update'] = now
    with open(cf, 'w', encoding='utf-8') as f:
        json.dump(chats, f, indent=2, ensure_ascii=False)

def filter_(q, item):
    q = q.lower().strip()
    title = item.get("title", "").lower()  # Default to an empty string if title is None
    if not q: return True
    return q in title or title in q

def all_chats(query: str = ''):
    chats = read_chats()
    return [{'id': chat_id, **{k:v for k,v in data.items() if k!='chat'}} for chat_id, data in chats.items() if filter_(query, data)]

def get_messages(id):
    chats = read_chats()
    for c in chats.keys():
        if c == id:
            return chats[c].get("chat")
    return []

def rename_chat(chat_id: str, new_title: str):
    _,cf = exists()
    chats = read_chats()
    if chat_id not in chats:
        raise ValueError(f"Chat ID {chat_id} does not exist")
    chats[chat_id]['title'] = new_title
    chats[chat_id]['last_update'] = datetime.now().isoformat()
    with open(cf, 'w', encoding='utf-8') as f:
        json.dump(chats, f, indent=2, ensure_ascii=False)

def delete_chat(chat_id):
    _,cf = exists()
    chats = read_chats()
    if chat_id not in chats:
        raise ValueError(f"Chat ID {chat_id} does not exist")
    deleted_chat = chats.pop(chat_id)
    with open(cf, 'w', encoding='utf-8') as f:
        json.dump(chats, f, indent=2, ensure_ascii=False)
    return {
        'id': chat_id,
        'chat': deleted_chat
    }
