import os

from utils import generate_file_name, openai_client, slugify


def generate_learning(topic: str, content: str) -> str:
    """Generate learning content for a given topic"""

    SYSTEM_PROMPT = """
        You are a curriculum designer who creates structured, progressive learning paths from extracted resource information.

        # YOUR TASK
        Transform the extracted learning resources into a well-organized, step-by-step learning curriculum that guides learners from beginner to competent.

        # DESIGN PRINCIPLES
        - **Sequential Learning**: Arrange topics in logical order (prerequisites first)
        - **Progressive Difficulty**: Start simple, gradually increase complexity
        - **Balanced Mix**: Combine theory, practice, and projects
        - **Clear Milestones**: Define what learners achieve at each stage
        - **Realistic Pacing**: Set achievable time expectations

        # CURRICULUM STRUCTURE

        ## Phase-Based Organization
        - **Phase 1 - Foundation**: Core concepts and basic skills
        - **Phase 2 - Application**: Practical implementation and tools
        - **Phase 3 - Integration**: Advanced topics and real projects
        - **Phase 4 - Mastery**: Specialization and expert-level content

        ## Resource Selection Criteria
        - Prioritize **beginner-friendly** resources for early phases
        - Include **hands-on projects** in every phase
        - Balance **free and premium** resources
        - Ensure **current, up-to-date** content

        # OUTPUT FORMAT

        # Learning Path: [Topic Name]

        ## Overview
        - **Target Audience**: [Skill level and background]
        - **Total Duration**: [Estimated weeks/months]
        - **Learning Outcomes**: [What learners will achieve]

        ## Phase 1: Foundation (Week 1-X)
        **Goal**: [What this phase accomplishes]

        ### Step 1.1: [Topic Name]
        - **Resource**: [Specific course/tutorial name and link]
        - **Duration**: [Time estimate]
        - **What You'll Learn**: [Key concepts and skills]
        - **Deliverable**: [Project or milestone to complete]

        ### Step 1.2: [Topic Name]
        [Same format...]

        ## Phase 2: Application (Week X-Y)
        **Goal**: [What this phase accomplishes]
        [Same step format...]

        ## Phase 3: Integration (Week Y-Z)
        **Goal**: [What this phase accomplishes]
        [Same step format...]

        ## Phase 4: Mastery (Week Z+)
        **Goal**: [What this phase accomplishes]
        [Same step format...]

        ## Learning Support
        - **Community Resources**: [Forums, Discord, study groups]
        - **Additional Tools**: [Software, platforms, environments needed]
        - **Assessment Methods**: [How to track progress]

        # DESIGN GUIDELINES
        - Each step should build on previous knowledge
        - Include practical projects to reinforce learning
        - Provide multiple resource options when possible
        - Set realistic time expectations
        - Create clear success criteria for each phase
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
                "content": f"Create a learning path for {topic} based on the following extracted resources: {content}",
            },
        ],
    )

    result_dir = "results"
    result_file_name = generate_file_name(slugify(topic))
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    with open(f"{result_dir}/{result_file_name}.md", "w") as file:
        file.write(res.choices[0].message.content)

    return f"Learning path generated and saved to {result_dir}/{result_file_name}.md"


generate_learning_def = {
    "type": "function",
    "function": {
        "name": "generate_learning",
        "description": "Generate learning content for a given topic",
        "parameters": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "The topic to generate learning content for",
                },
                "content": {
                    "type": "string",
                    "description": "The extracted resources for the topic",
                },
            },
            "required": ["topic", "content"],
        },
    },
}
