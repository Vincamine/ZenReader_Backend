import re

def process_llm_response(response):
    """
    Processes the response from the LLM service and extracts keywords.

    Args:
        response (dict): The raw response from the LLM service.

    Returns:
        list: List of keywords extracted from the response.
    """
    if not response:
        return []

    try:
        # Get the 'textResponse' field
        raw_text_response = response.get('textResponse', '')

        if not raw_text_response:
            print("Error: textResponse field is missing")
            return []

        # Extract keywords (comma-separated)
        # Remove any HTML tags if present
        clean_response = re.sub(r'<.*?>', '', raw_text_response)
        
        # Split by commas and strip whitespace
        keywords = [keyword.strip() for keyword in clean_response.split(',') if keyword.strip()]
        
        return keywords

    except Exception as e:
        print(f"Error processing LLM response: {e}")
        return []
