import os

import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from dotenv import load_dotenv
from mistralai import Mistral
from openai import OpenAI
from tavily import TavilyClient

load_dotenv()

mistral_client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
chroma_client = chromadb.PersistentClient(path="data")
ef = OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"), model_name="text-embedding-3-small"
)

try:
    cv_collection = chroma_client.get_collection(name="cv_data", embedding_function=ef)
except Exception:
    cv_collection = chroma_client.create_collection(
        name="cv_data", embedding_function=ef
    )
