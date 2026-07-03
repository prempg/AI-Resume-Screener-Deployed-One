from ..db.collections.files import files_collection
from bson import ObjectId
import os
from pdf2image import convert_from_path
from app.analyzers.resume_analyzer import analyze_resume
import base64
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


async def process_file(id: str, file_path: str):
    await files_collection.update_one({"_id": ObjectId(id)}, {
        "$set": {"status": "processing"}
    })

    await files_collection.update_one({"_id": ObjectId(id)}, {
        "$set": {"status": "converting to images"}
    })

    # Step 1: Convert PDF to Images
    pages = convert_from_path(file_path)
    images = []

    for i, page in enumerate(pages):
        image_save_path = f"/mnt/uploads/images/{id}/image-{i}.jpg"
        os.makedirs(os.path.dirname(image_save_path), exist_ok=True)
        page.save(image_save_path, 'JPEG')
        images.append(image_save_path)

    await files_collection.update_one({"_id": ObjectId(id)}, {
        "$set": {"status": "converting to images success"}
    })

    # Step 2: Encode first page to base64
    images_base64 = [encode_image(img) for img in images]

    # Step 3: Send to Groq Vision Model
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Based on the resume below, roast this resume"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{images_base64[0]}"
                        }
                    }
                ]
            }
        ]
    )
    result_text = response.choices[0].message.content

async def process_resume_analysis(
    id: str,
    resume_path: str,
    job_description: str,
):
    await files_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"status": "processing"}}
    )

    try:
        result_text = analyze_resume(
            resume_path=resume_path,
            job_description=job_description,
        )

        await files_collection.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "status": "processed",
                    "result": result_text,
                }
            },
        )

    except Exception as e:
        await files_collection.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "status": "failed",
                    "result": str(e),
                }
            },
        )
    
    # Step 4: Save result to DB
    await files_collection.update_one({"_id": ObjectId(id)}, {
        "$set": {
            "status": "processed",
            "result": result_text
        }
    })

    # queue: Email Queue - Your file is ready










# from ..db.collections.files import files_collection
# from bson import ObjectId
# import os
# from pdf2image import convert_from_path
# import base64
# from openai import OpenAI


# client = OpenAI()


# def encode_image(image_path):
#     with open(image_path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode("utf-8")


# async def process_file(id: str, file_path: str):
#     await files_collection.update_one({"_id": ObjectId(id)}, {
#         "$set": {
#             "status": "processing"
#         }
#     })

#     await files_collection.update_one({"_id": ObjectId(id)}, {
#         "$set": {
#             "status": "converting to images"
#         }
#     })

#     # Step1: Convert the PDF - Image
#     pages = convert_from_path(file_path)
#     images = []

#     for i, page in enumerate(pages):
#         image_save_path = f"/mnt/uploads/images/{id}/image-{i}.jpg"
#         os.makedirs(os.path.dirname(image_save_path), exist_ok=True)
#         page.save(image_save_path, 'JPEG')
#         images.append(image_save_path)

#     await files_collection.update_one({"_id": ObjectId(id)}, {
#         "$set": {
#             "status": "converting to images successs"
#         }
#     })

#     images_base64 = [encode_image(img) for img in images]

#     result = client.responses.create(
#         model="gpt-4.1",
#         input=[
#             {
#                 "role": "user",
#                 "content": [
#                     {"type": "input_text",
#                         "text": "Based on the resume below, Roast this resume"},
#                     {
                        # flake8: noqa
#                         "type": "input_image",
#                         "image_url": f"data:image/jpeg;base64,{images_base64[0]}",
#                     },
#                 ],
#             }
#         ],
#     )

#     await files_collection.update_one({"_id": ObjectId(id)}, {
#         "$set": {
#             "status": "processed",
#             "result": result.output_text
#         }
#     })

#     # queue: Email Queue - Your file is ready
