def evaluate_policy_indicators(investigation: dict) -> dict:
    """
    Evaluate policy indicators using deterministic rules.

    This function does not use the LLM.
    It only compares investigation data with
    explicitly defined policy indicators.
    """

    features = investigation["prediction_features"]

    indicators = {
        "high_seller_late_rate": (
            features["seller_previous_late_rate"] > 0
        ),

        "short_estimated_delivery": (
            features["estimated_delivery_days"] < 7
        ),

        "high_freight_cost": (
            features["total_freight"] > 50
        ),

        "multiple_items": (
            features["total_items"] > 1
        ),

        "multiple_sellers": (
            features["unique_sellers"] > 1
        ),

        "cross_state": (
            features["same_state"] == 0
        )
    }

    return {
        "policy_indicators": indicators
    }


if __name__ == "__main__":

    test_investigation = {
        "prediction_features": {
            "seller_previous_late_rate": 0,
            "estimated_delivery_days": 16,
            "total_freight": 8.72,
            "total_items": 1,
            "unique_sellers": 1,
            "same_state": 1
        }
    }

    result = evaluate_policy_indicators(
        test_investigation
    )

    print("\n========== POLICY EVALUATION ==========\n")
    print(result)