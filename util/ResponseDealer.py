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

        # Clean raw_text_response: remove commas, periods, and extra punctuation
        cleaned_keywords = re.sub(r'[,.]', '', raw_text_response)

        # Convert cleaned response into a set of keywords (optional: normalize case)
        keywords_list = cleaned_keywords.strip().split()
        keywords_set = set(word.lower() for word in keywords_list)

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
        clean_word = re.sub(r'[^\w]', '', word).lower()

        # Bold the first two letters (preserve punctuation)
        if len(word) > 2:
            bolded_word = f"<b>{word[:2]}</b>{word[2:]}"
        else:
            bolded_word = f"<b>{word}</b>"

        # If the cleaned word matches a keyword, wrap it with underline and color
        if clean_word in keywords_set:
            formatted_word = (
                f'<span style="text-decoration: underline; color: red;">{bolded_word}</span>'
            )
        else:
            formatted_word = bolded_word

        html_words.append(formatted_word)

    # Combine the words into an HTML paragraph
    html_content = "<p>" + " ".join(html_words) + "</p>"

    return html_content
