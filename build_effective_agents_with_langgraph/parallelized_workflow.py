import os
from textwrap import dedent

from langchain_anthropic import ChatAnthropic
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from typing_extensions import TypedDict


# Graph state
class State(TypedDict):
    topic: str
    joke: str
    story: str
    poem: str
    combined_output: str


# Instanciate the LLM
llm = ChatAnthropic(
    model="claude-3-5-haiku-latest", api_key=os.getenv("ANTHROPIC_API_KEY")
)


# Nodes
def generate_joke(state: State) -> State:
    """First LLM call to generate a joke"""
    msg = llm.invoke(f"Generate a joke about {state['topic']}")
    return {"joke": msg.content}


def generate_story(state: State) -> State:
    """Second LLM call to generate a story"""
    msg = llm.invoke(f"Generate a story about {state['topic']}")
    return {"story": msg.content}


def generate_poem(state: State) -> State:
    """Third LLM call to generate a poem"""
    msg = llm.invoke(f"Generate a poem about {state['topic']}")
    return {"poem": msg.content}


def aggregate_outputs(state: State) -> State:
    """Aggregate the outputs of the three LLM calls"""
    return {
        "combined_output": dedent(
            f"""
            Here's a joke, story, and poem about {state["topic"]}\n\n
            JOKE: {state["joke"]}\n\n
            STORY: {state["story"]}\n\n
            POEM: {state["poem"]}\n\n
            """
        )
    }


# Define the workflow
workflow = StateGraph(State)

# Add nodes to the workflow
workflow.add_node("generate_joke", generate_joke)
workflow.add_node("generate_story", generate_story)
workflow.add_node("generate_poem", generate_poem)
workflow.add_node("aggregate_outputs", aggregate_outputs)

# Add edges to the workflow
workflow.add_edge(START, "generate_joke")
workflow.add_edge(START, "generate_story")
workflow.add_edge(START, "generate_poem")
workflow.add_edge("generate_joke", "aggregate_outputs")
workflow.add_edge("generate_story", "aggregate_outputs")
workflow.add_edge("generate_poem", "aggregate_outputs")
workflow.add_edge("aggregate_outputs", END)

# Compile the workflow
compiled_workflow: CompiledStateGraph = workflow.compile()

# Show workflow
with open("parallelized_workflow.png", "wb") as f:
    f.write(compiled_workflow.get_graph().draw_mermaid_png())

# Run the workflow
output_state: State = compiled_workflow.invoke({"topic": "cats"})

print(output_state["combined_output"])
