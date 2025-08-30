import json

from utils import openai_client, tavily_client


def resource_search(query: str) -> str:
    """Internet search for resources related to a given topic"""
    res = tavily_client.search(query, include_raw_content="markdown")
    search_results = res.get("results", [])

    SYSTEM_PROMPT = """
        You are an information extraction specialist who identifies and extracts key facts from web search results and documents.

        # YOUR TASK
        Extract the most important and relevant information from the provided text, organizing it into clear, concise bullet points for learning resource identification.

        # EXTRACTION FOCUS
        Look for and extract:
        - **Course/Tutorial Names**: Specific titles and platforms
        - **Learning Resources**: Books, documentation, guides, tools
        - **Skill Levels**: Beginner, intermediate, advanced indicators
        - **Time Estimates**: Duration, hours, weeks mentioned
        - **Prerequisites**: Required knowledge or skills
        - **Key Topics Covered**: Main concepts and skills taught
        - **Format Types**: Video, text, interactive, hands-on projects
        - **Access Information**: Free, paid, pricing details
        - **Quality Indicators**: Ratings, reviews, author credentials

        # EXTRACTION RULES
        - Extract facts as stated, don't interpret or summarize
        - Include specific names, numbers, and details
        - Note contradictory information if found
        - Skip promotional language, focus on factual content
        - Preserve important technical terms and concepts

        # OUTPUT FORMAT

        ## Extracted Learning Resources

        ### Resource Category: [Type of resources found]
        - **Resource Name**: [Exact title] | Platform: [Platform name]
        - **Level**: [Skill level] | Format: [Type] | Access: [Free/Paid]
        - **Content**: [Key topics/skills covered]
        - **Details**: [Duration, prerequisites, special features]

        ### Resource Category: [Next type]
        [Same format...]

        ## Key Facts Extracted
        - [Important learning-related facts found]
        - [Time estimates and requirements]
        - [Prerequisites and skill dependencies]
        - [Quality and credibility indicators]

        ## Information Gaps
        - [Topics mentioned but lacking detail]
        - [Missing information that would be useful]

        # EXTRACTION PRINCIPLES
        - **Accuracy**: Extract exactly as written, no interpretation
        - **Relevance**: Focus on learning and educational content
        - **Completeness**: Don't miss important details
        - **Organization**: Group similar information together
        """

    res = openai_client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": json.dumps(search_results),
            },
        ],
    )
    return res.choices[0].message.content


resource_search_def = {
    "type": "function",
    "function": {
        "name": "resource_search",
        "description": "Internet search for resources related to a given topic",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The query to search the internet for",
                },
            },
            "required": ["query"],
        },
    },
}
