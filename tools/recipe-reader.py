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

load_dotenv()  
url = "https://pub.dev/packages/dart_openai"
content = requests.get(url)

soup = BeautifulSoup(content, 'html.parser')

