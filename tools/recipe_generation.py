from openai import OpenAI
from dotenv import load_dotenv
import os
import requests
import re
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
        }
     } """},
    {"role": "user", "content": ingrediants}
    ]
    )
    print(response.choices[0].message.content)z


<<<<<<< HEAD
print(create_recipe("Sugar, Salt, Tomato, Butter, Paneer, Onion"))
=======
create_recipe("Bacon, Salt, Tomato, Paneer, Onion, Sugar, Milk, Coca Cola") 
>>>>>>> a96434ee67e0c6b350e4e7c39ee3e0c75e69f3fa
