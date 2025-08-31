import os
import re
import time

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


def slugify(text: str) -> str:
    """Convert a string to a slug"""
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    return text


def generate_file_name(text: str) -> str:
    """Generate a file name with a timestamp"""
    current_date = str(int(round(time.time() * 1000)))
    return f"{text}-{current_date}"
