from langchain.tools import tool
from src.database import get_connection


@tool
def get_order_prediction_features(order_id: str) -> dict:
    """
    Retrieve the 15 features required by the OpsPredict model
    for a specific order using information available before
    the order was purchased.
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        query = """
        WITH target_order AS (
            SELECT
                o.order_id,
                o.order_purchase_timestamp,
                o.order_estimated_delivery_date,
                c.customer_state
            FROM orders o
            JOIN customers c
                ON o.customer_id = c.customer_id
            WHERE o.order_id = %s
        ),

        target_sellers AS (
            SELECT DISTINCT
                oi.seller_id
            FROM order_items oi
            WHERE oi.order_id = %s
        ),

        order_base AS (
            SELECT
                oi.order_id,
                COUNT(*) AS total_items,
                COUNT(DISTINCT oi.seller_id) AS unique_sellers,
                SUM(oi.price) AS total_product_price,
                SUM(oi.freight_value) AS total_freight,
                AVG(oi.price) AS average_item_price
            FROM order_items oi
            WHERE oi.order_id = %s
            GROUP BY oi.order_id
        ),

        product_features AS (
            SELECT
                oi.order_id,

                AVG(
                    COALESCE(
                        p.product_length_cm *
                        p.product_height_cm *
                        p.product_width_cm,
                        0
                    )
                ) AS average_product_volume_cm3,

                AVG(
                    COALESCE(p.product_weight_g, 0)
                ) AS average_product_weight_g,

                SUM(
                    COALESCE(
                        p.product_length_cm *
                        p.product_height_cm *
                        p.product_width_cm,
                        0
                    )
                ) AS total_product_volume_cm3

            FROM order_items oi
            JOIN products p
                ON oi.product_id = p.product_id
            WHERE oi.order_id = %s
            GROUP BY oi.order_id
        ),

        seller_info AS (
            SELECT
                oi.order_id,
                BOOL_AND(
                    s.seller_state = t.customer_state
                ) AS same_state

            FROM order_items oi

            JOIN sellers s
                ON oi.seller_id = s.seller_id

            CROSS JOIN target_order t

            WHERE oi.order_id = %s

            GROUP BY oi.order_id
        ),

        historical_seller_orders AS (
            SELECT
                oi.seller_id,
                COUNT(DISTINCT oi.order_id) AS previous_orders,

                COUNT(
                    DISTINCT CASE
                        WHEN o.order_delivered_customer_date
                             > o.order_estimated_delivery_date
                        THEN o.order_id
                    END
                ) AS previous_late_orders

            FROM order_items oi

            JOIN orders o
                ON oi.order_id = o.order_id

            JOIN target_order t
                ON o.order_purchase_timestamp
                   < t.order_purchase_timestamp

            JOIN target_sellers ts
                ON oi.seller_id = ts.seller_id

            WHERE o.order_status = 'delivered'

            GROUP BY oi.seller_id
        ),

        seller_history AS (
            SELECT
                COALESCE(
                    SUM(previous_orders),
                    0
                ) AS seller_previous_orders,

                COALESCE(
                    SUM(previous_late_orders),
                    0
                ) AS seller_previous_late,

                CASE
                    WHEN COALESCE(
                        SUM(previous_orders), 0
                    ) = 0
                    THEN 0.0

                    ELSE
                        SUM(previous_late_orders)::numeric
                        /
                        SUM(previous_orders)
                END AS seller_previous_late_rate

            FROM historical_seller_orders
        )

        SELECT
            t.order_id,

            CASE
                WHEN si.same_state
                THEN 1
                ELSE 0
            END AS same_state,

            EXTRACT(
                YEAR FROM t.order_purchase_timestamp
            )::int AS purchase_year,

            EXTRACT(
                MONTH FROM t.order_purchase_timestamp
            )::int AS purchase_month,

            sh.seller_previous_late_rate,

            ob.unique_sellers,

           GREATEST(
               (
               t.order_estimated_delivery_date
               - t.order_purchase_timestamp::date
               ),
               0
            )::numeric AS estimated_delivery_days,
            ob.total_items,

            ob.total_freight,

            EXTRACT(
                DAY FROM t.order_purchase_timestamp
            )::int AS purchase_day,

            CASE
                WHEN sh.seller_previous_late > 0
                THEN 1
                ELSE 0
            END AS seller_previous_late,

            pf.average_product_volume_cm3,

            pf.average_product_weight_g,

            sh.seller_previous_orders,

            ob.average_item_price,

            pf.total_product_volume_cm3

        FROM target_order t

        CROSS JOIN order_base ob

        CROSS JOIN product_features pf

        CROSS JOIN seller_info si

        CROSS JOIN seller_history sh;
        """

        cursor.execute(
            query,
            (
                order_id,
                order_id,
                order_id,
                order_id,
                order_id
            )
        )

        result = cursor.fetchone()

        if result is None:
            return {
                "error": (
                    f"Could not build prediction features "
                    f"for order {order_id}."
                )
            }

        columns = [
            description[0]
            for description in cursor.description
        ]

        return dict(zip(columns, result))

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

    result = get_order_prediction_features.invoke(
        {
            "order_id": order_id
        }
    )

    print("\nPrediction Features:\n")
    print(result)