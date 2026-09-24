from langchain.tools import tool
from src.database import get_connection


@tool
def get_order_features(order_id: str) -> dict:
    """
    Retrieve the features required by OpsPredict for a specific order.
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        query = """
        SELECT
            o.order_id,
            o.customer_id,
            o.order_purchase_timestamp,
            o.order_delivered_customer_date,
            o.order_estimated_delivery_date,
            c.customer_state
        FROM orders o
        JOIN customers c
            ON o.customer_id = c.customer_id
        WHERE o.order_id = %s;
        """

        cursor.execute(query, (order_id,))
        result = cursor.fetchone()

        if result is None:
            return {
                "error": f"Order {order_id} was not found."
            }

        return {
            "order_id": result[0],
            "customer_id": result[1],
            "purchase_timestamp": str(result[2]),
            "delivered_date": str(result[3]),
            "estimated_delivery_date": str(result[4]),
            "customer_state": result[5]
        }

    finally:
        connection.close()


if __name__ == "__main__":

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT order_id
            FROM orders
            LIMIT 1;
        """)

        order_id = cursor.fetchone()[0]

    finally:
        connection.close()

    result = get_order_features.invoke({
        "order_id": order_id
    })

    print("\nOrder Information:")
    print(result)