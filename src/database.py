import os

import psycopg2
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


def get_connection():
    database_url = os.getenv("POSTGRES_URL")

    if database_url:
        return psycopg2.connect(database_url)

    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        database=os.getenv("POSTGRES_DB", "businesspulse"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    return connection