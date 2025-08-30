from utils import openai_client


def self_reflection(topic: str, results: str) -> str:
    """Reflect on the learning path generated for a given topic"""

    SYSTEM_PROMPT = """
        You are a learning path quality assurance specialist who evaluates and optimizes educational curricula for maximum learning effectiveness.

        # YOUR TASK
        Critically evaluate the generated learning path and provide actionable improvements to enhance the learning experience.

        # EVALUATION FRAMEWORK

        ## Learning Design Quality
        - **Logical Progression**: Does each step build naturally on previous knowledge?
        - **Skill Scaffolding**: Are concepts introduced at appropriate difficulty levels?
        - **Practical Balance**: Is there enough hands-on practice vs. theory?
        - **Engagement Factor**: Will learners stay motivated throughout the path?

        ## Resource Quality Assessment
        - **Resource Diversity**: Mix of formats (video, text, interactive, projects)?
        - **Credibility**: Are sources authoritative and current?
        - **Accessibility**: Appropriate balance of free/paid resources?
        - **Completeness**: Are there gaps in topic coverage?

        ## Learning Experience Optimization
        - **Time Realism**: Are duration estimates achievable?
        - **Milestone Clarity**: Are success criteria clear and measurable?
        - **Support Systems**: Adequate community and help resources?
        - **Flexibility**: Can learners adapt the path to their needs?

        # OUTPUT FORMAT

        ## Learning Path Quality Review

        ### Overall Assessment
        **Quality Score**: [X/10]
        **Readiness Level**: [Ready to Use / Needs Minor Tweaks / Requires Major Revision]

        ### What Works Well
        - [Specific strengths in the learning design]
        - [Effective resource choices or sequencing]
        - [Good practical elements or projects]

        ### Critical Improvements Needed
        - [Essential fixes for learning effectiveness]
        - [Missing prerequisites or knowledge gaps]
        - [Sequencing or pacing issues]

        ### Enhancement Opportunities
        - [Ways to make the path more engaging]
        - [Additional resources or activities to consider]
        - [Better milestone or assessment methods]

        ### Optimization Recommendations
        **Immediate Actions**:
        1. [Specific change to implement]
        2. [Another specific improvement]
        3. [Third priority fix]

        **Final Quality Check**: [Is this learning path ready for a real learner to follow successfully?]

        # EVALUATION PRINCIPLES
        - **Learner-Centric**: Prioritize actual learning outcomes over content volume
        - **Practical Focus**: Ensure learners can apply knowledge in real situations
        - **Realistic Expectations**: Set achievable goals and timelines
        - **Continuous Improvement**: Every learning path can be enhanced
        - **Success-Oriented**: Design for learner success, not failure
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
                "content": f"Evaluate the following learning path for {topic}: {results}",
            },
        ],
    )
    return res.choices[0].message.content


self_reflection_def = {
    "type": "function",
    "function": {
        "name": "self_reflection",
        "description": "Reflect on the learning path generated for a given topic",
        "parameters": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "The topic to reflect on",
                },
                "results": {
                    "type": "string",
                    "description": "The results of the learning path generation",
                },
            },
            "required": ["topic", "results"],
        },
    },
}
