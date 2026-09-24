from tools.opspredict_tool import predict_delivery_risk


result = predict_delivery_risk.invoke({
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
})


print("OpsPredict Tool Result:")
print(result)