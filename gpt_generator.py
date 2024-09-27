import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_answer(query, context):
    """
    Generate a response using GPT-3.5-turbo based on the user query and context.
    :param query: The user query.
    :param context: Relevant context (text chunks from the file or web).
    :return: The generated answer.
    """
    messages = [
        {"role": "system", "content": f"Context: {context}"},
        {"role": "user", "content": query}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use the correct model name
        messages=messages
    )

    return response.choices[0].message['content'].strip()
