import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
llm1 = "openai/gpt-4o-mini"
llm2 = "meta-llama/llama-3.3-70b-instruct"