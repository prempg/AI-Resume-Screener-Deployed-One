import base64
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
    
def encode_image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def generate_vision_response(
    prompt: str,
    image_paths: list[str],
) -> str:
    content = [
        {
            "type": "text",
            "text": prompt,
        }
    ]

    for image_path in image_paths:
        image_base64 = encode_image_to_base64(image_path)

        content.append(
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image_base64}"
                },
            }
        )

    response = client.chat.completions.create(
        model=settings.GROQ_VISION_MODEL,
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
    )

    return response.choices[0].message.content

