import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = (
    "Ти — досвідчений автор статей, який створює чіткі, змістовні та цікаві тексти "
    "на будь-яку тему. Пиши одразу по суті, без зайвих вступів чи пояснень. "
    "Твоя мета — дати корисний і повний текст, який легко читається." 
    "Роби це українською"
)

def generate_text_by_prompt(prompt: str, model: str = "gpt-4.1-mini") -> str:
    response = openai.chat.completions.create(
        model=model,
        messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ],
    )
    return response.choices[0].message.content