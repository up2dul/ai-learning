import os
import time

from loguru import logger
from utils import cv_collection, mistral_client, openai_client


def create_conversion_prompt(markdown_content) -> str:
    """Create a prompt for the OpenAI conversion model"""
    return f"""
            Convert the following CV markdown content into structured bullet points for salary analysis.

            Focus on extracting:
            1. Specific technical skills and experience levels
            2. Job titles and career progression
            3. Geographic information
            4. Quantifiable achievements
            5. Education and certifications

            CV Content:
            {markdown_content}

            Please extract and organize this information following the specified format, ensuring all technical terms are properly normalized for job market analysis.
            """


def process_cv_ocr(file_path: str, file_name: str = "cv.pdf") -> None:
    """Main function for the OCR to Structured CV Data script"""
    logger.info("Uploading file to storage...")
    uploaded_pdf = mistral_client.files.upload(
        file={
            "file_name": file_name,
            "content": open(file_path, "rb"),
        },
        purpose="ocr",
    )

    signed_url = mistral_client.files.get_signed_url(file_id=uploaded_pdf.id)

    logger.info("Processing OCR...")
    ocr_response = mistral_client.ocr.process(
        model="mistral-ocr-latest",
        document={
            "type": "document_url",
            "document_url": signed_url.url,
        },
    )

    pages = ocr_response.model_dump().get("pages")

    SYSTEM_PROMPT = """
        You are an expert CV data extractor specialized in preparing resumes for salary prediction analysis.

        Your task is to extract and structure CV information into clear, searchable bullet points optimized for job market research and salary benchmarking.

        EXTRACTION PRINCIPLES:
        1. Focus on salary-relevant information: skills, experience duration, job titles, locations, achievements
        2. Normalize all technical terms to industry-standard names (e.g., "JavaScript" not "JS", "Amazon Web Services" not "AWS")
        3. Extract quantifiable metrics wherever possible (years, percentages, team sizes, budget amounts)
        4. Maintain consistent formatting for easy parsing and retrieval

        CRITICAL REQUIREMENTS:
        - Extract EXACT job titles as they appear (these are crucial for salary matching)
        - Include precise employment durations (start/end dates or total years)
        - List technical skills with experience levels when mentioned
        - Capture geographic information (current location, work locations)
        - Note company types/sizes if indicated (startup, enterprise, consulting, etc.)
        - Extract measurable accomplishments (revenue impact, performance gains, project scale)

        OUTPUT FORMAT:
        Structure as organized bullet points under these categories:

        ## Personal Information
        - Name: [Full name]
        - Location: [Current city, state/country]
        - Contact: [Email/phone if present]

        ## Professional Summary
        - Current Role: [Most recent job title]
        - Total Experience: [X years in field]
        - Industry Focus: [Primary industry/sector]
        - Seniority Level: [Junior/Mid/Senior/Lead/Principal based on experience]

        ## Technical Skills
        - Programming Languages: [List with years of experience if mentioned]
        - Frameworks/Libraries: [Specific framework names]
        - Tools & Technologies: [Development tools, IDEs, etc.]
        - Cloud & Infrastructure: [AWS, Azure, GCP, Docker, Kubernetes, etc.]
        - Databases: [SQL, NoSQL, specific database names]
        - Other Technical: [DevOps, testing frameworks, methodologies]

        ## Work Experience
        For each role:
        - Position: [Job Title] at [Company Name]
        - Duration: [Start Date - End Date] ([X years Y months])
        - Industry: [Company industry if clear]
        - Key Technologies: [Technologies used in this role]
        - Achievements: [Quantified accomplishments]
        - Team/Project Scale: [Team size, budget, users affected, etc.]

        ## Education & Certifications
        - Education: [Degree] in [Field] from [Institution] ([Year])
        - Certifications: [Professional certifications with issuing body]
        - Relevant Training: [Bootcamps, courses, specializations]

        ## Quantified Achievements
        - [Specific measurable accomplishments across all roles]
        - [Revenue impact, performance improvements, cost savings]
        - [Awards, recognition, publications]

        FORMATTING RULES:
        - Use consistent bullet point structure
        - Include "Not specified" for missing critical information
        - Separate multiple items with commas within bullet points
        - Use standard date formats (MM/YYYY or "X years")
        - Normalize all skill names to full, searchable terms
        """

    all_cv_data = ""

    for page_num, page in enumerate(pages, start=1):
        markdown = page.get("markdown")

        if not markdown or markdown.strip() == "":
            logger.warning(f"Empty content on page {page_num}, skipping...")
            continue

        logger.info(f"Processing page {page_num}...")

        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": create_conversion_prompt(markdown)},
            ],
        )
        result = response.choices[0].message.content
        all_cv_data += result + "\n\n"

        # Store each page with enhanced metadata
        # Store with enhanced metadata for better retrieval
        cv_collection.add(
            documents=[result],
            metadatas=[
                {
                    "document_type": "cv_extraction",
                    "page_number": page_num,
                    "content_category": "structured_cv_data",
                    "extraction_date": time.strftime("%Y-%m-%d"),
                    "suitable_for": "salary_analysis",
                }
            ],
            ids=[f"cv_extraction_page_{page_num}"],
        )

    timestamp = int(time.time() * 1000)
    result_file_name = f"cv_data-{timestamp}.md"
    result_file_path = f"results/cv/{result_file_name}"

    os.makedirs("results", exist_ok=True)
    with open(result_file_path, "w", encoding="utf-8") as file:
        file.write("# Structured CV Data for Salary Analysis\n\n")
        file.write(all_cv_data)

    logger.info("CV processing complete!")
