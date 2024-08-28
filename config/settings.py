import os

from dotenv import load_dotenv

load_dotenv()

# OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Model settings
MODEL_NAME = os.getenv("MODEL_NAME")