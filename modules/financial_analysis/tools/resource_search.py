import json

from loguru import logger
from utils import openai_client, tavily_client


def resource_search(query: str, context: str = None) -> str | None:
    """Internet search for financial data, research, and market intelligence"""

    # Execute Tavily search with financial context
    search_params = {
        "query": query,
        "include_raw_content": "markdown",
        "max_results": 10,
    }

    # Add date filtering for time-sensitive queries
    if any(
        term in query.lower()
        for term in ["recent", "latest", "current", "2024", "2025"]
    ):
        search_params["days"] = 30  # Last 30 days for recent queries

    res = tavily_client.search(**search_params)
    search_results = res.get("results", [])

    logger.info(
        f"Successfully retrieved {len(search_results)} financial search results"
    )

    # Pre-process search results to reduce token count
    processed_results = []
    for idx, result in enumerate(search_results[:8], 1):  # Limit to top 8 results
        # Truncate raw_content to first 1500 characters if it exists
        raw_content = result.get("raw_content") or result.get("content") or ""
        truncated_content = (
            raw_content[:1500] + "..." if len(raw_content) > 1500 else raw_content
        )

        processed_results.append(
            {
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "content": truncated_content,
                "score": result.get("score", 0),
            }
        )

    logger.info("Processed and truncated search results for analysis")

    SYSTEM_PROMPT = """
        You are a financial intelligence analyst extracting key insights from web sources.

        # TASK
        Extract critical financial information and organize it for investment analysis.

        # EXTRACT
        - Market data: prices, volumes, metrics
        - Policy info: regulations, government actions
        - Expert opinions and forecasts
        - Historical context and precedents
        - Quantitative claims with dates
        - Contradicting views

        # OUTPUT FORMAT

        ## Key Findings
        ### [Insight Headline]
        - **Claim**: [Specific fact/data]
        - **Source**: [Publication] | [Date]
        - **Type**: [Data/Opinion/Research/News]

        ## Market Data
        - [Metric]: [Value] | [Date]

        ## Perspectives
        **Bullish**: [Claims with sources]
        **Bearish**: [Claims with sources]
        **Consensus**: [Common views]

        ## Quality
        - Tier 1 (Institutional): [count/list]
        - Tier 2 (Media/analysts): [count/list]

        # RULES
        - Cite all sources
        - Note dates explicitly
        - Include multiple perspectives
        - Flag opinion vs. data
        - Be concise but precise
        """

    context_str = f"\n\nContext: {context}" if context else ""

    res = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"""
                    Query: {query}{context_str}

                    Search Results:
                    {json.dumps(processed_results, indent=2)}
                    """,
            },
        ],
        temperature=0.3,
        max_tokens=2000,
    )

    logger.info("Successfully generated financial search results")
    return res.choices[0].message.content


resource_search_def = {
    "type": "function",
    "function": {
        "name": "resource_search",
        "description": "Search the internet for financial data, market research, policy information, and analytical perspectives",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query optimized for finding financial information (be specific, include dates if relevant)",
                },
                "context": {
                    "type": "string",
                    "description": "Optional context about what research dimension this search supports",
                },
            },
            "required": ["query"],
        },
    },
}
