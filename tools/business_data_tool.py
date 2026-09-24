from langchain.tools import tool

from src.database import get_connection


@tool
def get_business_metrics() -> dict:
    """
    Retrieve basic business metrics from the PostgreSQL database.
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        query = """
        SELECT
            COUNT(*) AS total_orders,
            COUNT(DISTINCT customer_id) AS unique_customers
        FROM orders;
        """

        cursor.execute(query)

        result = cursor.fetchone()

        return {
            "total_orders": result[0],
            "unique_customers": result[1]
        }

    finally:
        connection.close()


if __name__ == "__main__":
    result = get_business_metrics.invoke({})

    print("Business Metrics:")
    print(result)