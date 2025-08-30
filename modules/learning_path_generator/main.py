import json

from tools.broadcast import broadcast, broadcast_def
from tools.generate_learning import generate_learning, generate_learning_def
from tools.research_plan import research_plan, research_plan_def
from tools.resource_search import resource_search, resource_search_def
from tools.self_reflection import self_reflection, self_reflection_def
from utils import openai_client

tools_defs = [
    research_plan_def,
    generate_learning_def,
    resource_search_def,
    broadcast_def,
    self_reflection_def,
]
tools_dict = {
    "research_plan": research_plan,
    "generate_learning": generate_learning,
    "resource_search": resource_search,
    "broadcast": broadcast,
    "self_reflection": self_reflection,
}


def execute_func(func_name: str, func_args: dict) -> str:
    func = tools_dict[func_name]
    if not func:
        return {
            "error": f"Function {func_name} not found.",
        }
    return func(**func_args)


def main_process(topic: str) -> None:
    """Main process for the Learning Path Generator"""

    SYSTEM_PROMPT = """
        You are an AI Learning Path Generator that creates comprehensive, structured learning curricula for any topic or skill.

        # YOUR MISSION
        Transform any learning request into a complete, actionable learning path with curated resources, clear progression, and realistic timelines.

        # LEARNING PATH CREATION PROCESS
        1. **Research Planning** - Analyze the learning topic and create strategic research blueprint
        2. **Resource Internet Search** - Extract key learning resources and information from web search results
        3. **Learning Path Generation** - Build structured curriculum with progressive phases and deliverables
        4. **Self-Reflection & Optimization** - Evaluate and improve the learning path for maximum effectiveness

        # EXECUTION STANDARDS
        - **Always use available tools** - Leverage web search and structured analysis capabilities
        - **Provide clear progress updates** - Announce each phase as you begin it
        - **Focus on learner success** - Design paths that real people can follow and complete
        - **Ensure educational quality** - Prioritize credible, current, and practical resources

        # COMMUNICATION PROTOCOL
        Before each major step, announce your progress:
        - "📋 **PLANNING**: Analyzing learning request and creating research strategy..."
        - "🔍 **EXTRACTING**: Gathering and organizing learning resources from search results..."
        - "🎯 **BUILDING**: Creating structured learning path with phases and milestones..."
        - "🔧 **OPTIMIZING**: Reviewing and refining the learning path for quality..."
        - "✅ **COMPLETE**: Learning path delivered as markdown document"

        # SUCCESS CRITERIA
        - **Comprehensive Coverage**: All essential topics and skills included
        - **Logical Progression**: Clear learning sequence from beginner to competent
        - **Actionable Resources**: Specific courses, tutorials, and materials with links
        - **Realistic Timeline**: Achievable milestones and time estimates
        - **Professional Quality**: Ready-to-use curriculum suitable for actual learning
        """

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": f"""
                Topic: {topic}
                
                # IMPORTANT
                - You MUST use the self_reflection tool to evaluate your research process before concluding
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
    input_topic = input("Enter the topic you want to learn about: ")
    print("---" * 10)
    main_process(input_topic)
