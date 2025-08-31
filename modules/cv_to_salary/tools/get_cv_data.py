from agents import function_tool
from utils import cv_collection


@function_tool
def get_cv_data() -> str:
    """Get CV data from vector database collection"""
    try:
        results = cv_collection.get(include=["documents"])
        if results["documents"]:
            return "\n\n".join(results["documents"])
        return "No CV data found"
    except Exception as e:
        return f"Error retrieving CV data: {e}"
