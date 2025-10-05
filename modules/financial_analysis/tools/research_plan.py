from utils import openai_client


def research_plan(query: str, user_context: dict = None) -> str | None:
    """Decompose financial query into structured research sub-questions"""

    SYSTEM_PROMPT = """
        You are a financial research strategist who breaks down complex market questions into investigable components.

        # YOUR TASK
        Transform any financial query into a structured research blueprint with clear sub-questions and data requirements.

        # OUTPUT FORMAT

        **Primary Question**: [Restate the main query clearly]

        **Research Dimensions**:

        1. **[Dimension Name]** (Priority: High/Medium/Low)
        - Sub-question: [Specific question to investigate]
        - Data needed: [Market data/News/Research/On-chain metrics]
        - Why it matters: [Brief relevance explanation]

        2. **[Dimension Name]** (Priority: High/Medium/Low)
        - Sub-question: [Specific question to investigate]
        - Data needed: [Required data types]
        - Why it matters: [Brief relevance explanation]

        [Continue for 4-6 dimensions...]

        **Research Strategy**:
        - Parallel searches: [Which dimensions can be researched simultaneously]
        - Sequential dependencies: [What must be answered before what]
        - Time horizon: [Historical lookback + forecast period]

        **Key Assumptions to Track**:
        - [Assumption 1]
        - [Assumption 2]
        - [Assumption 3]

        # PRINCIPLES
        - Break complex queries into specific, answerable sub-questions
        - Identify what data sources are needed for each dimension
        - Flag dependencies between sub-questions
        - Keep it focused: 4-6 dimensions maximum
        """

    context_str = ""
    if user_context:
        context_str = f"""
            User Context:
            - Portfolio: {user_context.get("portfolio", "Not specified")}
            - Time horizon: {user_context.get("time_horizon", "Not specified")}
            - Risk tolerance: {user_context.get("risk_tolerance", "Not specified")}
        """

    res = openai_client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Create a research plan for this financial question:\n\n{query}{context_str}",
            },
        ],
    )
    return res.choices[0].message.content


research_plan_def = {
    "type": "function",
    "function": {
        "name": "research_plan",
        "description": "Decompose a complex financial query into structured research sub-questions with data requirements",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The financial question or analysis request to plan research for",
                },
                "user_context": {
                    "type": "object",
                    "description": "Optional user context (portfolio, time horizon, risk tolerance)",
                    "properties": {
                        "portfolio": {"type": "string"},
                        "time_horizon": {"type": "string"},
                        "risk_tolerance": {"type": "string"},
                    },
                },
            },
            "required": ["query"],
        },
    },
}
