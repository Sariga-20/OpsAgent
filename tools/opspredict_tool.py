import json

import joblib
import pandas as pd
from langchain.tools import tool


MODEL_PATH = "models/ops_predict_xgboost.pkl"
METADATA_PATH = "models/model_metadata.json"


# Load the trained OpsPredict model
model = joblib.load(MODEL_PATH)


# Load model metadata
with open(METADATA_PATH, "r") as f:
    metadata = json.load(f)


FEATURES = metadata["features"]
THRESHOLD = metadata["threshold"]


@tool
def predict_delivery_risk(
    same_state: int,
    purchase_year: int,
    purchase_month: int,
    seller_previous_late_rate: float,
    unique_sellers: int,
    estimated_delivery_days: float,
    total_items: int,
    total_freight: float,
    purchase_day: int,
    seller_previous_late: int,
    average_product_volume_cm3: float,
    average_product_weight_g: float,
    seller_previous_orders: int,
    average_item_price: float,
    total_product_volume_cm3: float
) -> dict:
    """
    Predict the probability that an e-commerce order will be delivered late.
    """

    input_data = pd.DataFrame(
        [{
            "same_state": same_state,
            "purchase_year": purchase_year,
            "purchase_month": purchase_month,
            "seller_previous_late_rate": seller_previous_late_rate,
            "unique_sellers": unique_sellers,
            "estimated_delivery_days": estimated_delivery_days,
            "total_items": total_items,
            "total_freight": total_freight,
            "purchase_day": purchase_day,
            "seller_previous_late": seller_previous_late,
            "average_product_volume_cm3": average_product_volume_cm3,
            "average_product_weight_g": average_product_weight_g,
            "seller_previous_orders": seller_previous_orders,
            "average_item_price": average_item_price,
            "total_product_volume_cm3": total_product_volume_cm3
        }],
        columns=FEATURES
    )

    probability = float(
        model.predict_proba(input_data)[0][1]
    )

    prediction = int(
        probability >= THRESHOLD
    )

    risk = (
        "Late"
        if prediction == 1
        else "On Time / Early"
    )

    return {
        "late_delivery_probability": round(probability, 4),
        "prediction": prediction,
        "risk": risk,
        "threshold": THRESHOLD
    }