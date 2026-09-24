from langgraph.graph import StateGraph, START, END

from src.graph_state import OpsAgentState
from src.graph_nodes import (
    investigation_node,
    analysis_node,
    approval_node,
    action_node,
)


def route_after_approval(state):
    """
    Decide whether to execute the action or stop
    based on human approval.
    """

    if state.get("approved", False):
        return "approved"

    return "rejected"


# Create the graph
builder = StateGraph(OpsAgentState)


# Add nodes
builder.add_node(
    "investigation",
    investigation_node
)

builder.add_node(
    "analysis",
    analysis_node
)

builder.add_node(
    "approval",
    approval_node
)

builder.add_node(
    "action",
    action_node
)


# Start → Investigation
builder.add_edge(
    START,
    "investigation"
)


# Investigation → Approval
builder.add_edge(
    "investigation",
    "analysis"
)

builder.add_edge(
    "analysis",
    "approval"
)

# Approval → Conditional routing
builder.add_conditional_edges(
    "approval",
    route_after_approval,
    {
        "approved": "action",
        "rejected": END,
    }
)


# Action → End
builder.add_edge(
    "action",
    END
)


# Compile the graph
ops_agent_graph = builder.compile()