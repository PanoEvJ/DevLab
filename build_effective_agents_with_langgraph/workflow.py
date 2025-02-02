import os

from langchain_anthropic import ChatAnthropic
from pydantic import BaseModel, Field


class SearchQuery(BaseModel):
    search_query: str = Field(description="Query that is optimized for web search")
    justification: str = Field(
        description="Why is this query relevant to the user's request?"
    )


llm = ChatAnthropic(
    model="claude-3-5-haiku-latest", api_key=os.getenv("ANTHROPIC_API_KEY")
)

# LLM with a structured output
structured_llm = llm.with_structured_output(SearchQuery)

output = structured_llm.invoke("How does Calcium CT score relate to high cholesterol?")

print("-" * 10, "LLM with Structured Output", "-" * 10)
print(output.search_query)
print(output.justification)


# LLM with Tool Calling
def multiply(a: int, b: int) -> int:
    return a * b


llm_with_tool = llm.bind_tools([multiply])

output = llm_with_tool.invoke("What is 2 times 3?")

print("-" * 10, "LLM with Tool Calling", "-" * 10)
print(output.tool_calls)
