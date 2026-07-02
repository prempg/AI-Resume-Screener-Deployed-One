from groq import Groq
from app.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)


def generate_text_response(prompt: str) -> str:
    response = client.chat.completions.create(
        model=settings.GROQ_TEXT_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response.choices[0].message.content
