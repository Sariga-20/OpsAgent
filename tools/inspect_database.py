from src.database import get_connection


connection = get_connection()

try:
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            table_name,
            column_name
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position;
    """)

    rows = cursor.fetchall()

    current_table = None

    print("\nDatabase Tables and Columns:\n")

    for table_name, column_name in rows:

        if table_name != current_table:
            print(f"\n--- {table_name} ---")
            current_table = table_name

        print(column_name)

finally:
    connection.close()