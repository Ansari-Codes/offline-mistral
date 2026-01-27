![preview](https://github.com/Ansari-Codes/offline-assistant/blob/main/images/Capture3.PNG?raw=true)
![preview2](https://github.com/Ansari-Codes/offline-assistant/blob/main/images/Capture.PNG?raw=true)

# 🤖 Qwen On Desktop (QOD)

This software was created with one question in mind: **"Can we create an offline chatbot utility?"**

Companies like OpenAI, Google, or DeepSeek run **massive, multi-billion parameter models** on high-end hardware. Running such models on a regular PC is challenging as the result is shown in fig:

![GIF SHOWING BLAST](https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExcmkyeDN2empjcjhocGZtdDNidmI1c3l6aW5uZ2h0cGdwY3lpNWJidiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/XrNry0aqYWEhi/giphy.gif) 😥😯

So, I used:

1. **Qwen2.5-0.5B**: [HuggingFace](https://huggingface.co/Qwen/Qwen2.5-0.5B)

   * Small enough to run on **16GB RAM** and general CPU machines.
   * Tested and working -- trust me!

2. **NiceGUI**: [Website](https://nicegui.io)

   * Provides a **modern, lightweight UI** for the model.

## Developer

I am **Muhammad Abubakar Siddique Ansari**, passionate about **Data Science and AI**. I love creating utilities and solving problems.

I am currently (2026) a **1st Year ICS student at KIPS College**, Punjab - Pakistan. You can learn more about me at my portfolio: [Portfolio](https://ansari-codes.github.io/portfolio).

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

![settigns](https://github.com/Ansari-Codes/offline-assistant/blob/main/images/Capture2.PNG?raw=true)

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

| Use Case                          | Temperature | Top_p      | Max New Tokens | Notes                           |
| --------------------------------- | ----------- | ---------- | -------------- | ------------------------------- |
| Quick & Precise Answers           | 0.1 – 0.3   | 0.8        | 50 – 100       | Factual answers or coding help  |
| Casual Chat / Fun                 | 0.6 – 0.8   | 0.9        | 100 – 200      | Adds personality and variety    |
| Creative Writing / Brainstorming  | 0.8 – 1.0   | 0.95 – 1.0 | 200 – 500      | Explore ideas freely            |
| Detailed Explanations / Summaries | 0.3 – 0.5   | 0.9        | 200 – 300      | Balanced creativity and clarity |

**Tip:** Adjust **temperature**, **top_p**, and **max_new_tokens** together to get the exact style and length you want.


## Help

If you encounter problems or find a bug, please **open an issue on the repo**: [GitHub Issues](https://github.com/Ansari-Codes/offline-assistant/issues). 

**Contact me at email: ansaricodes@gmail.com**
