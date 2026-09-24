from src.investigation import investigate_order
from src.approval import request_human_approval
from src.actions import execute_operational_action


def run_ops_workflow(order_id: str):
    """
    Run the complete OpsAgent investigation workflow.

    Investigation → Human Approval → Controlled Action
    """

    print("\n========== OPSAGENT WORKFLOW ==========\n")

    # Step 1: Investigate the order
    print("Step 1: Investigating order...")

    investigation = investigate_order(order_id)

    if "error" in investigation:
        print(investigation["error"])
        return investigation

    print("Investigation completed.")

    print(
        "\nModel Prediction:",
        investigation["model_prediction"]
    )

    # Step 2: Request human approval
    print("\nStep 2: Requesting human approval...")

    approved = request_human_approval(
        investigation
    )

    # Step 3: Execute only after approval
    if not approved:

        print(
            "\nAction cancelled."
            "\nNo operational action was executed."
        )

        return {
            "order_id": order_id,
            "status": "Cancelled",
            "reason": "Human approval denied"
        }

    print("\nStep 3: Executing approved action...")

    action_result = execute_operational_action(
        investigation
    )

    print("\nAction completed.")

    return {
        "order_id": order_id,
        "status": "Completed",
        "investigation": investigation,
        "action": action_result
    }


if __name__ == "__main__":

    order_id = "e481f51cbdc54678b7cc49136f2d6af7"

    result = run_ops_workflow(order_id)

    print("\n========== FINAL RESULT ==========\n")
    print(result)