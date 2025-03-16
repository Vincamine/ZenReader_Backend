import json

def generate_llm_query(text):
    """
    Takes input text and formats it into a JSON request for the LLM service,
    requesting ONLY key words as the output.

    Args:
        text (str): The input text to be processed

    Returns:
        dict: A formatted query dictionary ready to be sent to the LLM service
    """

    query = {
        "message": (
            f"Extract and return only the key words from the following text: {text} text end. "
            "Follow these rules: 1. Key words should be returned as plain text, separated by commas. "
            "2. Do not include any explanations, HTML tags, or additional formatting. "
            "3. Output ONLY the key words. Do not include any extra text before or after the list."
        ),
        "mode": "chat",
        "sessionId": "identifier-to-partition-chats-by-external-id",
        "attachments": []
    }

    return query
