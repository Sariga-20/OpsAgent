import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


# Groq configuration
GROQ_TEMPERATURE = float(
    os.getenv(
        "GROQ_TEMPERATURE",
        "0"
    )
)