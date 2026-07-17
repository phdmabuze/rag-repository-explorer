from pydantic_ai import Agent

from shared.config import settings

agent = Agent(
    f"ollama:{settings.llm_model}",
    system_prompt="""
You are a coding assistant.
Answer questions using only the provided context.
If context is insufficient, say that you don't know.
""",
)


async def answer_question(
    question: str,
    context: str,
) -> str:
    result = await agent.run(
        f"""
Context:

{context}

Question:

{question}
"""
    )

    return result.output
