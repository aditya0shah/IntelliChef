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

load_dotenv()  
pinecone_index = "emp-2024"
namespace = "recipes"
pinecone_api_key = os.getenv("PINECONE_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

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
    result = index.query(
        namespace=namespace, 
        vector=embed_vector,
        top_k=10,
        include_values=True,
        include_metadata=True
    )
    texts=[]
    for item in result:
        text = item['metadata']['text']
        texts.append(text)
        print(text)
    


url = 'https://www.indianhealthyrecipes.com/paneer-tikka-on-stove-top/'

# website_content = upload_url(url)
modify_recipe("Replace the paneer with tofu")


