import json

from tools.broadcast import broadcast, broadcast_def
from tools.generate_analysis import generate_analysis, generate_analysis_def
from tools.research_plan import research_plan, research_plan_def
from tools.resource_search import resource_search, resource_search_def
from tools.self_reflection import self_reflection, self_reflection_def
from utils import openai_client

tools_defs = [
    research_plan_def,
    generate_analysis_def,
    resource_search_def,
    broadcast_def,
    self_reflection_def,
]
tools_dict = {
    "research_plan": research_plan,
    "generate_analysis": generate_analysis,
    "resource_search": resource_search,
    "broadcast": broadcast,
    "self_reflection": self_reflection,
}


def execute_func(func_name: str, func_args: dict) -> str:
    func = tools_dict[func_name]
    if not func:
        return f"Function {func_name} not found."
    return func(**func_args)


def main_process(query: str) -> None:
    """Main process for the Financial Analysis System"""

    SYSTEM_PROMPT = """
        You are an AI Financial Analysis System that generates comprehensive, multi-dimensional market analysis with transparent reasoning chains and actionable insights.

        # YOUR MISSION
        Transform complex financial queries into structured, source-backed analysis with clear reasoning, scenario modeling, and confidence-scored conclusions.

        # FINANCIAL ANALYSIS PROCESS
        1. **Research Planning** - Decompose the financial query into structured research sub-questions with data requirements
        2. **Resource Internet Search** - Gather real-time market data, news, research, and expert opinions from web sources
        3. **Analysis Generation** - Synthesize findings into logical reasoning chains with scenario modeling and actionable insights
        4. **Self-Reflection & Validation** - Audit analysis quality, identify gaps, and ensure logical consistency

        # EXECUTION STANDARDS
        - **Always use available tools** - Leverage research planning, web search, and structured analysis capabilities
        - **Provide clear progress updates** - Announce each phase as you begin it using the broadcast tool
        - **Focus on transparency** - Show reasoning work, flag uncertainties, and track assumptions
        - **Ensure analytical rigor** - Source all claims, quantify confidence, and present balanced perspectives

        # COMMUNICATION PROTOCOL
        Before each major step, announce your progress using the broadcast tool:
        - "📋 **PLANNING**: Decomposing financial query into research dimensions..."
        - "🔍 **RESEARCHING**: Gathering market data, news, and expert analysis from web sources..."
        - "🎯 **ANALYZING**: Synthesizing findings into causal logic and scenario models..."
        - "🔧 **VALIDATING**: Auditing analysis quality and logical consistency..."
        - "✅ **COMPLETE**: Financial analysis delivered with transparent reasoning chains"

        # SUCCESS CRITERIA
        - **Comprehensive Coverage**: All key dimensions of the financial question addressed
        - **Transparent Reasoning**: Clear causal logic from evidence to conclusions
        - **Source-Backed Claims**: All major findings attributed to credible sources
        - **Scenario Modeling**: Multiple plausible outcomes with probability assessments
        - **Actionable Insights**: Specific positioning, monitoring, and risk management recommendations
        - **Confidence Calibration**: Honest assessment of certainty levels with supporting rationale
        """

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": f"""
                Financial Query: {query}
                
                # IMPORTANT
                - You MUST use the self_reflection tool to evaluate your analysis quality before concluding
                - You MUST use the broadcast tool to communicate your progress to the user
                """,
        },
    ]

    while True:
        res = openai_client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            tools=tools_defs,
            tool_choice="auto",
        )

        message = res.choices[0].message
        messages.append(message)

        if message.tool_calls:
            for tool_call in message.tool_calls:
                func_name = tool_call.function.name
                func_args = json.loads(tool_call.function.arguments)

                func_response = execute_func(func_name, func_args)
                messages.append(
                    {
                        "role": "tool",
                        "content": func_response,
                        "tool_call_id": tool_call.id,
                    }
                )
        else:
            break


if __name__ == "__main__":
    print("---" * 10)
    input_topic = input("Enter the financial question you want to analyze: ")
    print("---" * 10)
    main_process(input_topic)
