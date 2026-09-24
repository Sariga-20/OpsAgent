def request_human_approval(investigation: dict) -> bool:
    """
    Request explicit human approval before a consequential
    operational action can be taken.
    """

    print("\n========== HUMAN APPROVAL REQUIRED ==========\n")

    print(
        f"Order: {investigation['order_id']}"
    )

    print(
        f"Delivery Risk: "
        f"{investigation['model_prediction']['risk']}"
    )

    print(
        f"Late Delivery Probability: "
        f"{investigation['model_prediction']['late_delivery_probability']}"
    )

    print(
        "\nNo operational action will be executed "
        "without explicit human approval."
    )

    response = input(
        "\nApprove operational action? (yes/no): "
    )

    return response.strip().lower() == "yes"


if __name__ == "__main__":

    test_investigation = {
        "order_id": "e481f51cbdc54678b7cc49136f2d6af7",

        "model_prediction": {
            "late_delivery_probability": 0.1185,
            "prediction": 0,
            "risk": "On Time / Early",
            "threshold": 0.7
        }
    }

    approved = request_human_approval(
        test_investigation
    )

    print(
        "\nApproval result:",
        approved
    )