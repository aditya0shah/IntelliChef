from openai import OpenAI
from dotenv import load_dotenv
import base64
import os

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY") 

client = OpenAI(api_key=openai_key)

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')




def get_ingrediants_from_pic(image_path:str):
  base64_image = encode_image(image_path)
  response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
      {
        "role": "user",
        "content": [
          {"type": "text", "text": "Name every ingredient you see in this image. "},
          {
            "type": "image_url",
            "image_url": {
              "url": f"data:image/jpeg;base64,{base64_image}"
            },
          },
        ],
      }
    ]
  )
  return response
print(get_ingrediants_from_pic("../files/source-pics/fridge3.jpeg"))