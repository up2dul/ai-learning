import os
import re
import time

from dotenv import load_dotenv
from langfuse.openai import openai
from tavily import TavilyClient

load_dotenv()

openai_client = openai
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


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
