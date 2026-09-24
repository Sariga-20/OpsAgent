import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


# Ollama configuration
OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2:3b"
)

OLLAMA_TEMPERATURE = float(
    os.getenv(
        "OLLAMA_TEMPERATURE",
        "0"
    )
)