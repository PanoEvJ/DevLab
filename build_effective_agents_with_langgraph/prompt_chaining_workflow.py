import os

from langchain_anthropic import ChatAnthropic
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from typing_extensions import Literal, TypedDict

llm = ChatAnthropic(
    model="claude-3-5-haiku-latest", api_key=os.getenv("ANTHROPIC_API_KEY")
)


# Graph state
class State(TypedDict):
    topic: str
    joke: str  # output of the 1st call
    improved_joke: str  # output of the 2nd call
    final_joke: str  # output of the 3rd call


# Nodes
def generate_joke(state: State) -> State:
    """First LLM call to generate a initial joke"""
    msg = llm.invoke(f"Generate a joke about {state['topic']}")
    return {"joke": msg.content}


def improve_joke(state: State) -> State:
    """Second LLM call to improve the joke"""
    msg = llm.invoke(f"Make this joke funnier by adding wordplay: {state['joke']}")
    return {"improved_joke": msg.content}


def polish_joke(state: State) -> State:
    """Third LLM call to generate the final joke"""
    msg = llm.invoke(f"Add a surprising twist to this joke: {state['improved_joke']}")
    return {"final_joke": msg.content}


# Conditional edge function to check if the joke has a punchline
def check_punchline(state: State) -> Literal["Pass", "Fail"]:
    """Gate function to check if the joke has a punchline"""

    # Simpe check: does the joke contain "?" or "!"
    if "?" in state["joke"] or "!" in state["joke"]:
        return "Pass"
    return "Fail"


# Build workflow
workflow = StateGraph(State)

# Add nodes
workflow.add_node("generate_joke", generate_joke)
workflow.add_node("improve_joke", improve_joke)
workflow.add_node("polish_joke", polish_joke)

# Add edges to connect nodes
workflow.add_edge(START, "generate_joke")
workflow.add_conditional_edges(
    "generate_joke", check_punchline, {"Pass": "improve_joke", "Fail": END}
)
workflow.add_edge("improve_joke", "polish_joke")
workflow.add_edge("polish_joke", END)

# Compile the graph
chain: CompiledStateGraph = workflow.compile()

# Show workflow
with open("prompt_chaining.png", "wb") as f:
    f.write(chain.get_graph().draw_mermaid_png())

# Invoke the workflow
state: State = chain.invoke({"topic": "cats"})

print("Initial joke:")
print(state["joke"])
print("\n--- --- ---\n")
if "improved_joke" in state:
    print("Improved joke:")
    print(state["improved_joke"])
    print("\n--- --- ---\n")

    print("Final joke:")
    print(state["final_joke"])
else:
    print("Joke failed quality gate - no punchline detected")
