import json
import joblib
import pandas as pd


MODEL_PATH = "models/ops_predict_xgboost.pkl"
METADATA_PATH = "models/model_metadata.json"


# Load model
model = joblib.load(MODEL_PATH)

# Load metadata
with open(METADATA_PATH, "r") as f:
    metadata = json.load(f)

features = metadata["features"]
threshold = metadata["threshold"]


print("Model loaded successfully!")
print("Number of features:", len(features))
print("Threshold:", threshold)
print("Features:")
for feature in features:
    print("-", feature)


# Sample input
sample_data = {
    "same_state": 0,
    "purchase_year": 2018,
    "purchase_month": 8,
    "seller_previous_late_rate": 0.40,
    "unique_sellers": 3,
    "estimated_delivery_days": 8.0,
    "total_items": 5,
    "total_freight": 120.0,
    "purchase_day": 25,
    "seller_previous_late": 40,
    "average_product_volume_cm3": 5000.0,
    "average_product_weight_g": 2500.0,
    "seller_previous_orders": 100,
    "average_item_price": 150.0,
    "total_product_volume_cm3": 25000.0
}

input_data = pd.DataFrame(
    [sample_data],
    columns=features
)

probability = float(
    model.predict_proba(input_data)[0][1]
)

prediction = int(
    probability >= threshold
)

print("\nPrediction test:")
print("Late-delivery probability:", round(probability, 4))
print("Prediction:", prediction)

if prediction == 1:
    print("Risk: Late")
else:
    print("Risk: On Time / Early")