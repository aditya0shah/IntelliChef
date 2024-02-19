from openai import OpenAI
from dotenv import load_dotenv
import os
import requests
import re
import json
from bs4 import BeautifulSoup

load_dotenv()  

openai_key = os.getenv("OPENAI_API_KEY") 

client = OpenAI(api_key=openai_key)


def create_recipe(ingrediants: str):
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_format={ "type": "json_object" },
    messages=[
    {"role": "system", "content": """You are a helpful smart home cook. You will take a set of ingrediants as input and will output, as a json file, 4 recipes.
     These must be detailed recipes with quantities and detailed steps in which someone can cook this meals. Output 4 parts to this JSON file. Each part 1 is one recipe and each element
     of that JSON file contains a recipe, number of calories in that recipe, and dietary restrictions it conforms to (such as gluten free or vegetarian). The JSON should follow this format:
     
     { 
       'recipe1': {'name': Insert Name Here, 'calories': Insert Calorie Count Here, 
                   'dietary_restrictions':[restriction1, restriction2, restriction3, etc.], 
                   'ingredients':{'ingredient1': Amount Needed,
                                 'ingredient2': Amount Needed, etc. },
                    'instructions': [Insert Instruction 1, Insert Instruction 2, Insert Instruction 3, etc.] 
        }, 'recipe2': {'name': Insert Name Here, 'calories': Insert Calorie Count Here, 
                   'dietary_restrictions':[restriction1, restriction2, restriction3, etc.], 
                   'ingredients':{'ingredient1': Amount Needed,
                                 'ingredient2': Amount Needed, etc. },
                    'instructions': [Insert Instruction 1, Insert Instruction 2, Insert Instruction 3, etc.] 
        }, etc.
     } """},
    {"role": "user", "content": ingrediants}
    ]
    )
    r = response.choices[0].message.content
    r = json.loads(r)
    imgs = []
    imgs.append(recipe_image(r["recipe1"]["name"]))
    imgs.append(recipe_image(r["recipe2"]["name"]))
    imgs.append(recipe_image(r["recipe3"]["name"]))
    imgs.append(recipe_image(r["recipe4"]["name"]))
    # for recipe in response.choices[0].message.content:
    #     recipe_image(recipe)
    return response.choices[0].message.content, imgs

def recipe_image(name:str):
    
    response = client.images.generate(
        model="dall-e-2",
        prompt=name,
        n=1,
    )
    return response.data[0].url
    # print(f"response {response} \n")
    # print(f"image_url {response.data[0].url}")

# create_recipe("Bacon, Salt, Tomato, Paneer, Onion, Sugar, Milk, Coca Cola") 