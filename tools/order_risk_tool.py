import json
import joblib
import pandas as pd

from langchain.tools import tool

from tools.order_prediction_data import get_order_prediction_features


MODEL_PATH = "models/ops_predict_xgboost.pkl"
METADATA_PATH = "models/model_metadata.json"


# Load model
model = joblib.load(MODEL_PATH)

# Load metadata
with open(METADATA_PATH, "r") as f:
    metadata = json.load(f)

FEATURES = metadata["features"]
THRESHOLD = metadata["threshold"]


@tool
def investigate_order_delivery_risk(order_id: str) -> dict:
    """
    Investigate a specific order and predict its late-delivery risk.

    The tool retrieves the required prediction features from PostgreSQL
    and sends them to the OpsPredict XGBoost model.
    """

    # Get features from PostgreSQL
    feature_data = get_order_prediction_features.invoke(
        {
            "order_id": order_id
        }
    )

    # Handle missing order
    if "error" in feature_data:
        return feature_data

    # Keep only model features
    model_input = {
        feature: feature_data[feature]
        for feature in FEATURES
    }

    # Convert PostgreSQL Decimal values to numeric floats
    input_data = pd.DataFrame(
        [model_input],
        columns=FEATURES
    ).astype(float)

    # Predict probability
    probability = float(
        model.predict_proba(input_data)[0][1]
    )

    # Apply model threshold
    prediction = int(
        probability >= THRESHOLD
    )

    risk = (
        "Late"
        if prediction == 1
        else "On Time / Early"
    )

    return {
        "order_id": order_id,
        "late_delivery_probability": round(
            probability,
            4
        ),
        "prediction": prediction,
        "risk": risk,
        "threshold": THRESHOLD,
        "features": model_input
    }


if __name__ == "__main__":

    # Test with the same order we have been using
    order_id = "e481f51cbdc54678b7cc49136f2d6af7"

    result = investigate_order_delivery_risk.invoke(
        {
            "order_id": order_id
        }
    )

    print("\n========== ORDER RISK INVESTIGATION ==========\n")
    print(result)