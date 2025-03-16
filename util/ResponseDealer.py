import re

def process_llm_response(response):
    """
    Processes the response from the LLM service and extracts content between <p>...</p>.

    Args:
        response (dict): The raw response from the LLM service.

    Returns:
        str: Clean HTML content between <p> and </p>.
    """
    if not response:
        return "<p>Error: No response received from LLM</p>"

    try:
        # Get the 'textResponse' field
        raw_text_response = response.get('textResponse', '')

        if not raw_text_response:
            return "<p>Error: textResponse field is missing</p>"

        # Extract content between <p> and </p> using regex
        match = re.search(r'<p>.*?</p>', raw_text_response, re.DOTALL)

        if match:
            return match.group(0)
        else:
            return "<p>Error: No <p>...</p> content found in textResponse</p>"

    except Exception as e:
        print(f"Error processing LLM response: {e}")
        return f"<p>Error processing response: {str(e)}</p>"
