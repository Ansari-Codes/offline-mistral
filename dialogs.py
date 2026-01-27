from UI import Dialog, confirm, Label, Button, Input, Select, TextArea, Card, Row, Col, Slider, Icon, AddSpace, Html, openLink
from backend import write_config, read_config
from env import ui
doc_string = """
# 🤖 Qwen On Desktop (QOD)

This software was created with one question in mind: **"Can we create an offline chatbot utility?"**

Companies like OpenAI, Google, or DeepSeek run **massive, multi-billion parameter models** on high-end hardware. Running such models on a regular PC is challenging as the result is shown in fig:

<img src="https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExcmkyeDN2empjcjhocGZtdDNidmI1c3l6aW5uZ2h0cGdwY3lpNWJidiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/XrNry0aqYWEhi/giphy.gif" alt="An Image Showing Bomb Blast></img> 😥😯

So, I used:

1. **Qwen2.5-0.5B**: <a href="https://huggingface.co/Qwen/Qwen2.5-0.5B" target="_blank">Hugging Face</a>

   * Small enough to run on **16GB RAM** and general CPU machines.
   * Tested and working -- trust me!

2. **NiceGUI**: <a href="https://nicegui.io" target="_blank">Website</a>

   * Provides a **modern, lightweight UI** for the model.

## Developer

Since there’s no one to introduce me, I’ll do it myself. I am **Muhammad Abubakar Siddique Ansari**, passionate about **Data Science and AI**. I love creating utilities and solving problems.

I am currently (2026) a **1st Year ICS student at KIPS College**. You can learn more about me at my portfolio: <a href="https://ansari-codes.github.io/portfolio" target="_blank">Portfolio</a>.

## Use Case

QOD is suitable for **general-purpose assistance**, especially when you don’t have access to online chatbots. You can use it for:

* General Discussion
* General Knowledge
* Math Problems
* Content Writing
* Simple Coding Problems

**Important:** QOD **does not have updated information**. It can answer factual and creative questions but may not provide current real-world data. For example:

Works:

> Hey, what is the solution for (x^2 + 2 - 4x = 0)?

Doesn’t work reliably:

> Hey, what is the temperature in Siberia?

It might answer “It is 40°C in Siberia” 😅 -- always **verify critical information**.

## Settings

You can tweak parameters to get outputs **exactly the way you like**. The adjustable parameters are:

* **`temperature`**: Controls the **creativity / randomness** of responses.

  * Low (0.1 – 0.3) → focused, deterministic answers
  * High (0.7 – 1.0) → creative, exploratory answers

* **`top_p`**: Controls the **range of words** the AI considers.

  * Low (0.8) → safe, coherent responses
  * High (0.95 – 1.0) → more varied and surprising responses

* **`max_new_tokens`**: Maximum length of AI’s response.

  * Short (50–100) → quick answers
  * Long (200–500) → detailed explanations or creative writing

### Recommended Settings for Different Cases

| Use Case                          | Temperature | Top p      | Max New Tokens | Notes                           |
| --------------------------------- | ----------- | ---------- | -------------- | ------------------------------- |
| Quick & Precise Answers           | 0.1 – 0.3   | 0.8        | 50 – 100       | Factual answers or coding help  |
| Casual Chat / Fun                 | 0.6 – 0.8   | 0.9        | 100 – 200      | Adds personality and variety    |
| Creative Writing / Brainstorming  | 0.8 – 1.0   | 0.95 – 1.0 | 200 – 500      | Explore ideas freely            |
| Detailed Explanations / Summaries | 0.3 – 0.5   | 0.9        | 200 – 300      | Balanced creativity and clarity |

**Tip:** Adjust **temperature**, **top\_p**, and **max\_new\_tokens** together to get the exact style and length you want.


## Help

If you encounter problems or find a bug, please **open an issue on the repo**: <a href="https://github.com/Ansari-Codes/offline-assistant/issues" target="_blank">GitHub Issues</a>.
"""
def createSettings():
    settings_dialog = Dialog()
    settings_dialog.props('persistent')
    config = read_config()
    edited = config.copy()
    with settings_dialog, Card().classes("w-full h-fit max-w-[90vw] max-h-[90vh] sm:max-w-[50vw] sm:max-h-[50vh]"):
        with Row().classes("w-full"):
            Icon("settings", "lg", "primary")
            Label("Settings").classes("text-2xl font-bold text-primary")
            AddSpace()
            Button("Help", config={"icon":"help"}, on_click=docs).tooltip("Help")
        with Col().classes("w-full mt-4 gap-2"):
            with Row().classes("w-full"):
                Label("Temperature").classes("w-fit font-bold text-lg")
                Slider(0.1, 2, 0.1, onchange=lambda e: edited.update({"temperature": float(e.value)})).props('label-always').classes("flex flex-1").set_value(config.get("temperature"))
            with Row().classes("w-full"):
                Label("Top P").classes("w-fit font-bold text-lg")
                Slider(0.1, 1, 0.1, onchange=lambda e: edited.update({"top_p": float(e.value)})).props('label-always').classes("flex flex-1").set_value(config.get("top_p"))
            with Row().classes("w-full"):
                Label("Max New Tokens").classes("w-fit font-bold text-lg")
                Slider(128, 8000, 1, onchange=lambda e: edited.update({"max_new_tokens": int(e.value)})).props('label-always').classes("flex flex-1").set_value(config.get("max_new_tokens"))
            with ui.expansion("Custom Instructions").classes("w-full justify-start"):
                TextArea(edited.get("custom_instructions", ""), max_h="600px").on_value_change(lambda e: edited.update({"custom_instructions": e.value})).classes("w-full")
        def save():
            config.update(edited)
            write_config(edited)
            settings_dialog.delete()
        with Row().classes("w-full justify-end"):
            Button("Cancel", settings_dialog.delete, color='negative')
            Button("Save", save)
    return settings_dialog

def docs():
    docs_dialog = Dialog()
    docs_dialog.props('persistent')
    with (docs_dialog.classes("w-full h-full max-w-[90vw] max-h-[90vh] sm:max-w-[50vw] sm:max-h-[50vh]")
    , Card().classes("w-full h-full")):
        with Row().classes("w-full"):
            Icon('book', "lg", "primary")
            Label("Docs").classes("text-2xl font-bold text-primary")
            AddSpace()
            Button(config={"icon":"developer_mode"}, color='primary', on_click=lambda:openLink("https://ansari-codes.github.io/portfolio")).tooltip("About the Developer")
            Button(config={"icon":"code"}, color='primary', on_click=lambda:openLink("https://github.com/Ansari-Codes/offline-assistant")).tooltip("Github Repo")
            Button(config={"icon":"close"}, color='negative', on_click=docs_dialog.delete).tooltip("Close")
        ui.markdown(doc_string).classes("w-full h-full max-h-full overflow-y-auto")
    docs_dialog.open()
    return docs_dialog
