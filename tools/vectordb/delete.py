from pinecone import Pinecone
import os
from dotenv import load_dotenv


load_dotenv()

pinecone_index = "emp-2024"
namespace = "recipes"
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_environment = os.getenv("PINECONE_ENVIRONEMT")


def delete(namespace:str):
    pc = Pinecone(api_key=pinecone_api_key)
    index = pc.Index(pinecone_index)

    index.delete(delete_all=True)

delete(namespace)