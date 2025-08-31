import json

from agents import function_tool
from loguru import logger
from utils import tavily_client


@function_tool
def search_salary_info(job_role: str) -> str:
    """Search for salary information for a specific job role"""
    try:
        query = f"{job_role} salary range compensation currently"
        results = tavily_client.search(
            query, include_raw_content="markdown", max_results=5
        )
        search_results = results.get("results", [])
        logger.info(f"Found {len(search_results)} salary results for {job_role}")
        return json.dumps(search_results)
    except Exception as e:
        return f"Error searching salary data: {e}"
