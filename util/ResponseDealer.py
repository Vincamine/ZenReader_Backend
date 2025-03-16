import re


def process_llm_response(response):
    """
    Processes the response from the LLM service:
    - Extracts content from the first <p> to the last </p>.
    - Removes all newline characters.
    - Converts any **word** to <b>word</b>.

    Args:
        response (dict): The raw response from the LLM service.

    Returns:
        str: Clean HTML content with no newlines and bolded words.
    """
    if not response:
        return "<p>Error: No response received from LLM</p>"

    try:
        # Get the 'textResponse' field
        raw_text_response = response.get('textResponse', '')

        if not raw_text_response:
            return "<p>Error: textResponse field is missing</p>"

        # Remove all newline characters and strip whitespace
        cleaned_response = raw_text_response.replace('\n', '').strip()

        # Extract everything from the first <p> to the last </p>
        match = re.search(r'<p>.*</p>', cleaned_response, re.DOTALL)

        if match:
            html_content = match.group(0)
        else:
            return "<p>Error: No <p>...</p> block found in textResponse</p>"

        # Replace **word** with <b>word</b>
        html_with_bold = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', html_content)

        return html_with_bold

    except Exception as e:
        print(f"Error processing LLM response: {e}")
        return f"<p>Error processing response: {str(e)}</p>"
