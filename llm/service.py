import requests
import os
from util.GenerateQuery import generate_llm_query
from util.ResponseDealer import process_llm_response

from dotenv import load_dotenv

load_dotenv()
# LLM endpoint configuration
LLM_API_ENDPOINT = os.environ.get('LLM_API_ENDPOINT', 'http://localhost:5000/api/v1/workspace/hackathon/chat')
LLM_API_KEY = os.environ.get('LLM_API_KEY', '')

def send_to_llm(query):
    """
    Sends a query to the LLM endpoint and returns the response.

    Args:
        query (dict): The query generated by generate_llm_query()

    Returns:
        dict: The response from the LLM
    """
    headers = {
        'Content-Type': 'application/json'
    }

    if LLM_API_KEY:
        headers['Authorization'] = f'Bearer {LLM_API_KEY}'

    try:
        response = requests.post(
            LLM_API_ENDPOINT,
            json=query,
            headers=headers,
            timeout=30
        )

        if response.status_code != 200:
            print(f"LLM API error: {response.status_code} - {response.text}")
            return None

        return response.json()

    except Exception as e:
        print(f"Error sending request to LLM: {e}")
        return None


def process_text(text):
    """
    End-to-end function to take input text, send to LLM, and return processed HTML.

    Args:
        text (str): The text to process

    Returns:
        str: HTML string from LLM response
    """
    query = generate_llm_query(text)

    llm_raw_response = send_to_llm(query)

    html_output = process_llm_response(llm_raw_response)

    return html_output
