from utils import openai_client


def self_reflection(analysis: str, quality_threshold: float = 8.0) -> str | None:
    """Validate analysis quality and identify gaps before delivery"""

    SYSTEM_PROMPT = """
        You are a quality assurance analyst who validates financial research for completeness and logical consistency.

        # YOUR TASK
        Audit the analysis for gaps, contradictions, and quality issues. Suggest improvements.

        # VALIDATION CHECKLIST

        ## Completeness Audit
        - ✓/✗ All sub-questions addressed
        - ✓/✗ Sources cited for major claims
        - ✓/✗ Scenarios cover probability space (sum to ~100%)
        - ✓/✗ Actionable insights provided
        - ✓/✗ Assumptions explicitly stated

        ## Logical Consistency Check
        - Are there contradictions between different sections?
        - Do probability weights make sense?
        - Are time horizons consistent throughout?
        - Does scenario logic align with evidence?

        ## Source Quality Review
        - Tier 1 sources (Fed, BIS, top journals): [count]
        - Tier 2 sources (major media, established analysts): [count]  
        - Tier 3 sources (blogs, unverified): [count]
        - Data sources (APIs, databases): [count]
        - **Quality score**: [0-10]

        ## Confidence Calibration
        - Claims with 80%+ confidence: [count]
        → Do they have strong empirical support?
        - Claims with 40-60% confidence: [count]
        → Are uncertainties properly explained?
        - **Calibration assessment**: [Well-calibrated/Overconfident/Underconfident]

        ## Gap Analysis
        - Missing elements: [What's not covered that should be]
        - Weak areas: [Where analysis needs strengthening]
        - Expansion opportunities: [Optional deeper dives to offer]

        ## Bias Check
        - Recency bias: [Over-weighting recent events?]
        - Confirmation bias: [Did we seek disconfirming evidence?]
        - Anchoring: [Too tied to initial hypothesis?]

        # OUTPUT FORMAT

        **Overall Quality Score**: [0-10]

        **Strengths**:
        - [What's done well]

        **Issues Flagged**:
        - 🔴 Critical: [Must fix before delivery]
        - 🟡 Moderate: [Should improve if possible]
        - 🟢 Minor: [Nice to have enhancements]

        **Recommendations**:
        1. [Specific action to improve quality]
        2. [Specific action to improve quality]

        **Deliver Analysis?**: [Yes / Refine first / Major revisions needed]

        # PRINCIPLES
        - Be specific about what's wrong and how to fix it
        - Prioritize issues by severity
        - Validate logic, not just check formatting
        - Ensure confidence levels match evidence strength
        """

    res = openai_client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"""
                    Validate this financial analysis for quality and completeness:
                    {analysis}
                    
                    Quality threshold: {quality_threshold}/10
                    """,
            },
        ],
    )
    return res.choices[0].message.content


self_reflection_def = {
    "type": "function",
    "function": {
        "name": "self_reflection",
        "description": "Validate analysis quality by checking completeness, logical consistency, source quality, and identifying gaps",
        "parameters": {
            "type": "object",
            "properties": {
                "analysis": {
                    "type": "string",
                    "description": "The generated financial analysis to validate",
                },
                "quality_threshold": {
                    "type": "number",
                    "description": "Minimum quality score required (0-10 scale). Default 8.0",
                },
            },
            "required": ["analysis"],
        },
    },
}
