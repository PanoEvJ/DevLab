import os
from textwrap import dedent

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from pydantic import BaseModel, Field
from typing_extensions import Literal, TypedDict


# Schema for routing Logic
class RouterSchema(BaseModel):
    """Schema for routing logic"""

    step: Literal["joke", "story", "poem"] = Field(
        None, description="The next step to call in the routing workflow"
    )


# Graph state
class State(TypedDict):
    input: str
    decision: str
    output: str


# Instanciate the generator LLM
llm = ChatAnthropic(
    model="claude-3-5-haiku-latest", api_key=os.getenv("ANTHROPIC_API_KEY")
)

# Instanciate the router LLM
router = ChatAnthropic(
    model="claude-3-5-sonnet-latest", api_key=os.getenv("ANTHROPIC_API_KEY")
)
router = router.with_structured_output(RouterSchema)


# Nodes
def call_router(state: State) -> State:
    """Router the user input to the appropriate node"""

    # Run the LLM augmented with structured output to serve as the routing logic
    decision: RouterSchema = router.invoke(
        [
            SystemMessage(
                content="Route the input to story, joke, or poem based on the user's request"
            ),
            HumanMessage(content=state["input"]),
        ]
    )

    return {"decision": decision.step}


def generate_joke(state: State) -> State:
    """First LLM call to generate a joke"""
    msg = llm.invoke(f"Generate a joke about {state['input']}")
    return {"output": msg.content}


def generate_story(state: State) -> State:
    """Second LLM call to generate a story"""
    msg = llm.invoke(f"Generate a story about {state['input']}")
    return {"output": msg.content}


def generate_poem(state: State) -> State:
    """Third LLM call to generate a poem"""
    msg = llm.invoke(f"Generate a poem about {state['input']}")
    return {"output": msg.content}


def route_decision(state: State) -> Literal["joke", "story", "poem"]:
    """Route the decision to the appropriate node"""
    return state["decision"]


# Define the workflow
workflow = StateGraph(State)

# Add nodes to the workflow
workflow.add_node("call_router", call_router)
workflow.add_node("generate_joke", generate_joke)
workflow.add_node("generate_story", generate_story)
workflow.add_node("generate_poem", generate_poem)

# Add edges to the workflow
workflow.add_edge(START, "call_router")
workflow.add_conditional_edges(
    "call_router",
    route_decision,
    {"joke": "generate_joke", "story": "generate_story", "poem": "generate_poem"},
)
workflow.add_edge("generate_joke", END)
workflow.add_edge("generate_story", END)
workflow.add_edge("generate_poem", END)


# Compile the workflow
compiled_workflow: CompiledStateGraph = workflow.compile()

# Show workflow
with open("parallelized_workflow.png", "wb") as f:
    f.write(compiled_workflow.get_graph().draw_mermaid_png())

# Run the workflow
output_state: State = compiled_workflow.invoke({"input": "Write me a joke about cats"})
print(output_state)

print(output_state["output"])
