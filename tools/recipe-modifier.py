from pinecone import Pinecone
from dotenv import load_dotenv
import os
from langchain_community.vectorstores import pinecone
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import requests
import re
from bs4 import BeautifulSoup
import tiktoken
from openai import OpenAI

load_dotenv()  
pinecone_index = "emp-2024"
namespace = "recipes"
pinecone_api_key = os.getenv("PINECONE_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)
embeddings = OpenAIEmbeddings(openai_api_type=openai_api_key)
pc = Pinecone(api_key = pinecone_api_key)
index = pc.Index(pinecone_index)


def get_website_content(url):

    response = requests.get(url)

    if response.status_code == 200:
    
        soup = BeautifulSoup(response.text, 'html.parser')

      
        content = soup.get_text()

        return content
    else:
        print(f"Failed to retrieve content. Status code: {response.status_code}")
        return None

def upload_url(url: str):
    content = get_website_content(url)
    print(f"cleaned {content}")
    print("done1")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap=150)

    texts = text_splitter.split_text(content)

    print(f"split {texts}")
    print("Done")
    
    count = 0
    for text in texts:
        print("hi")
        embed_vector = embeddings.embed_query(text)
        print(f"embed {embed_vector}")
        index.upsert(
            vectors=[
                {
                    'id':str(count),
                    'values':embed_vector,
                    'metadata':{
                    'text': text
                    }
                }
            ], 
            namespace=namespace
        )
        print(f"upserted {text}")
        count+=1



def modify_recipe(query:str):
    embed_vector = embeddings.embed_query(query)
    query_response = index.query(
        namespace=namespace, 
        vector=embed_vector,
        top_k=8,
        include_values=True,
        include_metadata=True
    )
    matches = query_response["matches"]
    print(matches)
    texts = []
    for match in matches:
        # print(match)
        result_id = match["id"]
        similarity_score = match["score"]
        text_value = match["metadata"]["text"]  
        texts.append(text_value)

    generate_recipes(texts, query)
    print(texts)

def generate_recipes(contents: list[str], query:str):
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
    {"role": "system", "content": f"""You are a helpful smart home cook. You have the following premade recipe {contents}. 
     You will take this recipe and adjust it based on the user's needs. Give a detailed recipe which the user can easily follow to cook. Output to the user in
     a clear and concise format."""},
    {"role": "user", "content": query}
    ]
    )
    print(response.choices[0].message.content)

url = 'https://www.indianhealthyrecipes.com/paneer-tikka-on-stove-top/'

# website_content = upload_url(url)
#modify_recipe("Replace the paneer with tofu")


