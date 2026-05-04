from groq import Groq
from config.settings import GROQ_API_KEY, MODEL_NAME, TEMPERATURE

client = Groq(api_key=GROQ_API_KEY)

def call_llm(system_prompt: str, user_prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=TEMPERATURE
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"LLM Error: {str(e)}"