import re


def process_llm_response(response, text):
    """
    Processes the JSON response from the LLM service and formats the text.

    Args:
        response (dict): The raw JSON response from the LLM service.
        text (str): The original text to be formatted.

    Returns:
        str: The formatted HTML content.
    """
    if not response:
        return "<p>Error: No response received from LLM</p>"

    try:
        # Retrieve the 'textResponse' field (a long string with keywords separated by spaces)
        raw_text_response = response.get('textResponse', '')

        if not raw_text_response:
            return "<p>Error: textResponse field is missing or empty</p>"

        # Convert raw_text_response into a set of keywords
        keywords_set = set(raw_text_response.strip().split())

        # Generate formatted HTML content from the original text and keywords
        formatted_html = generate_html_from_text(text, keywords_set)

        return formatted_html

    except Exception as e:
        print(f"Error processing LLM response: {e}")
        return f"<p>Error processing response: {str(e)}</p>"


def generate_html_from_text(text, keywords_set):
    """
    Helper function to generate HTML format from text and keywords.

    Args:
        text (str): The original input text.
        keywords_set (set): A set of keyword strings.

    Returns:
        str: HTML-formatted string.
    """
    words = text.strip().split()

    html_words = []
    for word in words:
        # Clean the word for keyword matching (remove punctuation)
        clean_word = re.sub(r'[^\w]', '', word)

        # Bold the first two letters
        if len(word) > 2:
            bolded_word = f"<b>{word[:2]}</b>{word[2:]}"
        else:
            bolded_word = f"<b>{word}</b>"

        # If word matches a keyword, add underline and red color
        if clean_word in keywords_set:
            # Wrap in a span for underline and color, keeping the bold intact
            formatted_word = (
                f'<span style="text-decoration: underline; color: red;">{bolded_word}</span>'
            )
        else:
            formatted_word = bolded_word

        html_words.append(formatted_word)

    # Combine the words into an HTML paragraph
    html_content = "<p>" + " ".join(html_words) + "</p>"

    return html_content
