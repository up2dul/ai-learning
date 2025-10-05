import os

from utils import generate_file_name, openai_client


def generate_analysis(
    research_plan: str,
    search_results: list,
    reasoning_depth: str = "standard",
    allow_checkpoints: bool = True,
) -> str | None:
    """Synthesize research findings into structured financial analysis with transparent reasoning"""

    SYSTEM_PROMPT = """
        You are a financial analyst who synthesizes research into clear, actionable insights with transparent reasoning.

        # YOUR TASK
        Build a logical analysis by connecting research findings into causal chains and scenario models.

        # OUTPUT FORMAT

        ## Executive Summary
        [2-3 sentence bottom-line conclusion]

        ## Analytical Framework

        ### Finding 1: [Key Insight]
        **Evidence**: [What the data shows]
        **Source**: [Where this comes from]
        **Confidence**: [High/Medium/Low - with reasoning]

        **Causal Logic**:
        [Event/Condition] → [Mechanism] → [Market Impact]
        ↳ Supporting evidence: [Specific data points]
        ↳ Contradicting signals: [Alternative interpretations if any]

        ### Finding 2: [Key Insight]
        [Repeat structure...]

        ## Scenario Analysis

        **Base Case** (Probability: X%)
        - Scenario: [What happens in most likely path]
        - Market impact: [Specific price/direction expectations]
        - Key assumptions: [What needs to be true]
        - Invalidation signals: [What would prove this wrong]

        **Alternative Scenarios**
        [2-3 other plausible outcomes with probabilities]

        ## Actionable Implications
        - Positioning: [Specific recommendations]
        - Monitoring: [What metrics to watch]
        - Risk management: [Hedge considerations]
        - Rebalance triggers: [When to adjust]

        ## Confidence Assessment
        | Component | Confidence | Reasoning |
        |-----------|-----------|-----------|
        [Table showing confidence in each conclusion]

        ## Assumption Tracker
        ✓ [Assumption 1 - currently valid]
        ⚠ [Assumption 2 - monitor closely]
        ✗ [Assumption 3 - invalidated]

        ## Sources
        [Categorized list with links]

        # CHECKPOINT RULES (if allow_checkpoints=True)
        When reasoning has significant uncertainty or conflicting evidence:
        - Flag the ambiguity explicitly
        - Present both interpretations fairly
        - Ask: "Which framework seems more applicable given current conditions?"
        - Wait for user input before proceeding

        # PRINCIPLES
        - Show your reasoning work, don't just state conclusions
        - Quantify confidence levels with evidence
        - Flag contradictions rather than hiding them
        - Connect analysis to actionable decisions
        - Be precise about time horizons and magnitudes
        """

    search_summary = "\n\n".join(
        [f"**Source {i + 1}**: {result}" for i, result in enumerate(search_results)]
    )

    checkpoint_instruction = (
        "\n\nIMPORTANT: Include human checkpoints at points of high uncertainty."
        if allow_checkpoints
        else ""
    )

    res = openai_client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"""
                    Synthesize these research findings into a structured analysis:
                    
                    **Research Plan**:
                    {research_plan}
                    
                    **Search Results**:
                    {search_summary}
                    
                    Reasoning depth: {reasoning_depth}{checkpoint_instruction}
                    """,
            },
        ],
    )

    result_dir = "results/financial"
    result_file_name = generate_file_name("financial")
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    with open(f"{result_dir}/{result_file_name}.md", "w") as file:
        content = res.choices[0].message.content
        if content is not None:
            file.write(content)

    return res.choices[0].message.content


generate_analysis_def = {
    "type": "function",
    "function": {
        "name": "generate_analysis",
        "description": "Synthesize research findings into structured financial analysis with transparent reasoning chains and scenario models",
        "parameters": {
            "type": "object",
            "properties": {
                "research_plan": {
                    "type": "string",
                    "description": "The original research plan with sub-questions",
                },
                "search_results": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of research findings from searches",
                },
                "reasoning_depth": {
                    "type": "string",
                    "enum": ["quick", "standard", "comprehensive"],
                    "description": "How deep to go with causal chain analysis",
                },
                "allow_checkpoints": {
                    "type": "boolean",
                    "description": "Whether to include human-in-loop validation points",
                },
            },
            "required": ["research_plan", "search_results"],
        },
    },
}
