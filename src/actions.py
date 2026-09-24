def execute_operational_action(investigation: dict) -> dict:
    """
    Execute a controlled operational action after
    explicit human approval.
    """

    order_id = investigation["order_id"]

    action = {
        "action": "Create operational review",
        "order_id": order_id,
        "status": "Executed",
        "message": (
            f"Operational review created for order {order_id}."
        )
    }

    return action


if __name__ == "__main__":

    test_investigation = {
        "order_id": "e481f51cbdc54678b7cc49136f2d6af7"
    }

    result = execute_operational_action(
        test_investigation
    )

    print("\n========== OPERATIONAL ACTION ==========\n")
    print(result)