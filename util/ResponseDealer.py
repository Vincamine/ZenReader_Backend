import re

def process_llm_response(response):
    """
    Processes the response from the LLM service and extracts content from the first <p> to the last </p>,
    and removes all newline characters.

    Args:
        response (dict): The raw response from the LLM service.

    Returns:
        str: Clean HTML content starting from the first <p> to the last </p> with no newlines.
    """
    if not response:
        return "<p>Error: No response received from LLM</p>"

    try:
        # Get the 'textResponse' field
        raw_text_response = response.get('textResponse', '')

        if not raw_text_response:
            return "<p>Error: textResponse field is missing</p>"

        # Remove all newline characters
        cleaned_response = raw_text_response.replace('\n', '').strip()

        # You can still extract the content from <p>...</p> if needed
        # match = re.search(r'<p>.*</p>', cleaned_response, re.DOTALL)
        #
        # if match:
        #     return match.group(0)
        # else:
        #     return "<p>Error: No <p>...</p> block found in textResponse</p>"

        return cleaned_response

    except Exception as e:
        print(f"Error processing LLM response: {e}")
        return f"<p>Error processing response: {str(e)}</p>"
