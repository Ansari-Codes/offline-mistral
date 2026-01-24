import torch, time, asyncio
from transformers import AutoTokenizer, AutoModelForCausalLM, StoppingCriteria, StoppingCriteriaList
from backend import read_config
model_id = "./models"
processing = lambda label: f"""<div style="
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    height: 40px;
    font-family: sans-serif;
    font-weight: bold;
    font-size: 16px;
    color: white;
    padding: 0 15px;
    border-radius: 8px;
    background-color: #2563EB;
    cursor: default;
">
    <svg width="18" height="18" viewBox="0 0 50 50">
        <circle cx="25" cy="25" r="20"
            fill="none"
            stroke="white"
            stroke-width="4"
            stroke-linecap="round"
            stroke-dasharray="90 150">
            <animateTransform
                attributeName="transform"
                type="rotate"
                from="0 25 25"
                to="360 25 25"
                dur="0.7s"
                repeatCount="indefinite" />
        </circle>
    </svg>
    <span>{label}</span>
</div>
"""

def _load_model_sync():
    start = time.time()
    tokenizer = AutoTokenizer.from_pretrained(
        model_id,
    )
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map="auto",
        max_memory={"cpu": "16GB"},  # adjust based on your RAM
        torch_dtype=torch.float32,
    )
    return tokenizer, model, time.time() - start

async def loadModel():
    return await asyncio.to_thread(_load_model_sync)
# def initialize_model(tokenizer, model, msgs=None):

#     messages = [
#         {
#             "role": "system",
#             "content": (
#                 "You are Offline-Assistant, created by Muhammad Abubakar Siddique Ansari. "
#                 "You are created to assist users when there is no internet available. "
#                 "You are helpful and concise."
#             )
#         }
#     ]

#     if msgs:
#         for m in msgs:
#             role, msg = list(m.items())[0]
#             messages.append({
#                 "role": role.lower(),
#                 "content": msg
#             })

#     def _generate(user_input, max_new_tokens, temperature, top_p):
#         """Blocking model generation (runs in worker thread)"""
#         messages.append({"role": "user", "content": user_input})

#         inputs = tokenizer.apply_chat_template(
#             messages,
#             add_generation_prompt=True,
#             tokenize=True,
#             return_dict=True,
#             return_tensors="pt",
#         ).to(model.device)

#         start = time.time()
#         with torch.no_grad():
#             output = model.generate(
#                 **inputs,
#                 max_new_tokens=max_new_tokens,
#                 temperature=temperature,
#                 top_p=top_p,
#             )
#         elapsed = time.time() - start

#         reply = tokenizer.decode(
#             output[0][inputs["input_ids"].shape[-1]:],
#             skip_special_tokens=True
#         )

#         messages.append({"role": "assistant", "content": reply})
#         return reply, elapsed

#     async def chat(user_input, max_new_tokens=512, temperature=0.7, top_p=0.9):
#         reply, elapsed = await asyncio.to_thread(
#             _generate,
#             user_input,
#             max_new_tokens,
#             temperature,
#             top_p
#         )
#         return reply, elapsed

#     return chat

def initialize_model_stream(tokenizer, model, msgs=None):
    messages = [
        {
            "role": "system",
            "content": (
                "You are Offline-Assistant, created by Muhammad Abubakar Siddique Ansari. "
                "You assist users when offline. Be concise and helpful."
            )
        }
    ]

    # Preload previous messages
    if msgs:
        for i,m in enumerate(msgs):
            role, msg = list(m.items())[0]
            messages.append({"role": role.lower(), "content": msg})
    class StreamCallback(StoppingCriteria):
        """Stream token-by-token and stop if stop_flag is set"""
        def __init__(self, tokenizer, token_callback, stop_flag):
            self.tokenizer = tokenizer
            self.token_callback = token_callback
            self.stop_flag = stop_flag

        def __call__(self, input_ids, *args, **kwargs):
            if self.stop_flag["stop"]:
                return True  # immediately stop generation
            # decode last token
            last_token_id = input_ids[0, -1]
            text = self.tokenizer.decode(last_token_id, skip_special_tokens=True)
            if self.token_callback:
                self.token_callback(text)
            return False  # continue generating

    def _generate_stream(user_input, max_new_tokens=5000, temperature=0.7, top_p=0.9,
                         token_callback=None, stop_flag=None, box=None):
        """
        Blocking token-by-token generation (run in worker thread)
        """
        if stop_flag is None:
            stop_flag = {"stop": False}
        MAX_TURNS = 5
        messages.append({"role": "user", "content": user_input})
        msgss = messages.copy()
        SYSTEM = {
            "role": "system",
            "content": (
                "You are Offline-Assistant, created by Muhammad Abubakar Siddique Ansari. "
                "You assist users when offline. Be concise and helpful."
            )
        }
        HISTORY = msgss[1:]
        HISTORY = HISTORY[-(MAX_TURNS * 2):]
        msgss = [SYSTEM] + HISTORY

        # Apply chat template
        box.set_content(processing("Understanding Inputs..."))
        inputs = tokenizer.apply_chat_template(
            msgss,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt"
        )#.to(model.device)
        box.set_content(processing("Defining Criteria..."))

        stopping_criteria = StoppingCriteriaList([StreamCallback(tokenizer, token_callback, stop_flag)])
        box.set_content(processing("Generating Response..."))
        with torch.no_grad():
            output = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_p=top_p,
                stopping_criteria=stopping_criteria
            )

        # Decode full output
        reply = tokenizer.decode(output[0][inputs["input_ids"].shape[-1]:], skip_special_tokens=True)
        messages.append({"role": "assistant", "content": reply})
        return reply

    async def chat_stream(user_input, token_callback=None, stop_flag=None, box=None):

        if stop_flag is None:
            stop_flag = {"stop": False}
        config = read_config()
        reply = await asyncio.to_thread(
            _generate_stream,
            user_input,
            max_new_tokens=config.get("max_new_tokens", 5000),
            temperature=config.get("temperature", 0.7),
            top_p=config.get("top_p", 0.9),
            token_callback=token_callback,
            stop_flag=stop_flag,
            box=box
        )
        return reply

    return chat_stream
