import os
from dotenv import load_dotenv
from google import genai

# Load .env file
load_dotenv()

# Get API key from .env (use GEMINI_API_KEY)
api_key = os.getenv("GEMINI_API_KEY")

# Create client with key from .env
client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-3-flash-preview",  # Updated model name (gemini-3-flash-preview may not exist)
    contents="Who is elon musk"
)
print(response.text)
