from src.agent_graph import ops_agent_graph


if __name__ == "__main__":

    order_id = "e481f51cbdc54678b7cc49136f2d6af7"

    initial_state = {
        "order_id": order_id
    }

    result = ops_agent_graph.invoke(
        initial_state
    )

    print("\n========== LANGGRAPH RESULT ==========\n")

    print("Order ID:")
    print(result["order_id"])

    print("\nStatus:")
    print(result.get("status"))

    print("\nLLM Analysis:")
    print(result.get("analysis"))

    print("\nApproved:")
    print(result.get("approved"))

    print("\nAction Result:")
    print(result.get("action_result"))