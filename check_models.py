from google import genai
import os
from dotenv import load_dotenv

# Load your .env variables
load_dotenv()

# Initialize the client
client = genai.Client()

# List all models your API key is allowed to access
print("--- Available Models for your API Key ---")
for m in client.models.list():
    print(f"Model Name: {m.name}")