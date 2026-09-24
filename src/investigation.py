from tools.order_risk_tool import investigate_order_delivery_risk
from tools.rag_tool import search_delivery_policy
from src.policy_evaluator import evaluate_policy_indicators


def investigate_order(order_id: str) -> dict:
    """
    Perform a controlled investigation of an order.

    The workflow:
    1. Retrieve ML delivery-risk prediction.
    2. Retrieve relevant delivery-policy evidence.
    3. Return structured facts for the agent/application.
    """

    # Step 1: ML investigation
    risk_result = investigate_order_delivery_risk.invoke(
        {
            "order_id": order_id
        }
    )

    if "error" in risk_result:
        return risk_result

    # Step 2: Retrieve policy evidence
    policy_result = search_delivery_policy.invoke(
        {
            "query": (
                "delivery risk seller performance "
                "high risk orders operational actions "
                "human approval"
            )
        }
    )
    policy_evaluation = evaluate_policy_indicators({
        "prediction_features": risk_result["features"]
    })

    # Step 3: Build structured result
    investigation = {
        "order_id": order_id,

        "model_prediction": {
            "late_delivery_probability":
                risk_result["late_delivery_probability"],

            "prediction":
                risk_result["prediction"],

            "risk":
                risk_result["risk"],

            "threshold":
                risk_result["threshold"]
        },

        "prediction_features":
            risk_result["features"],

        "policy_evidence":
            policy_result,

        "policy_evaluation": 
            policy_evaluation,
        "human_approval_required": True
    }

    return investigation


if __name__ == "__main__":

    order_id = "e481f51cbdc54678b7cc49136f2d6af7"

    result = investigate_order(order_id)

    print("\n========== STRUCTURED INVESTIGATION ==========\n")

    print("Order ID:")
    print(result["order_id"])

    print("\nModel Prediction:")
    print(result["model_prediction"])

    print("\nHuman Approval Required:")
    print(result["human_approval_required"])

    print("\nPolicy Evidence:")
    print(result["policy_evidence"])

    print("\nPolicy Evaluation:")
    print(result["policy_evaluation"])