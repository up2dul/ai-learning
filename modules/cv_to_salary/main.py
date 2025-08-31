import os
import time

from agents import Agent, Runner
from loguru import logger
from tools.get_cv_data import get_cv_data
from tools.process_cv_ocr import process_cv_ocr
from tools.search_salary_info import search_salary_info
from utils import cv_collection


SYSTEM_PROMPT = """
You are a CV to Salary Analysis Agent.

WORKFLOW:
1. Use get_cv_data to retrieve CV information
2. Extract the primary job role from the CV data  
3. Use search_salary_info to find salary data for that role
4. Provide a focused salary analysis with:
    - Primary salary range with currency and location
    - Experience level alignment
    - Key salary factors from CV skills
    - Source links for verification

RULES:
- Always get CV data first
- Focus on concrete salary figures
- Include source URLs
- Keep analysis concise and actionable
"""

salary_agent = Agent(
    name="CV Salary Analyzer",
    instructions=SYSTEM_PROMPT,
    model="gpt-4o-mini",
    tools=[get_cv_data, search_salary_info],
)


def check_cv_data(cv_file_name: str) -> None:
    """Ensure CV data is available in the collection, process PDF if needed"""
    try:
        results = cv_collection.get()
        if not results["documents"]:
            logger.info("No CV data found, processing PDF...")
            if os.path.exists(cv_file_name):
                process_cv_ocr(cv_file_name)
                logger.info("✅ CV processed successfully")
            else:
                logger.error("❌ cv.pdf not found")
    except Exception as e:
        logger.error(f"Error checking/processing CV: {e}")


async def main() -> None:
    """Main function to run CV to salary analysis"""
    logger.info("🚀 Starting CV to Salary Analysis")
    cv_file_name = "cv.pdf"

    check_cv_data(cv_file_name)

    runner = await Runner.run(
        starting_agent=salary_agent,
        input="Analyze my CV and provide salary insights for my role",
    )

    result = runner.final_output
    timestamp = int(time.time() * 1000)
    result_file_name = f"salary-analysis-{timestamp}.md"
    result_file_path = f"results/{result_file_name}"

    os.makedirs("results", exist_ok=True)
    with open(result_file_path, "w") as f:
        f.write(f"# CV to Salary Analysis\n\n{result}")

    logger.info(f"✅ Analysis complete! Saved to: {result_file_path}")
    print("\n" + "=" * 60)
    print("📊 CV TO SALARY ANALYSIS COMPLETE")
    print("=" * 60)
    print(f"📁 Report saved to: {result_file_path}")
    print("-" * 40)


if __name__ == "__main__":
    import asyncio
    import time

    asyncio.run(main())
