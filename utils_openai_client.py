import os
from dotenv import load_dotenv
from openai import OpenAI

# Setup OpenAI API clien using the API key

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_client():
    return client
