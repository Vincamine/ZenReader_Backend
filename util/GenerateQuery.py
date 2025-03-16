import json

def generate_llm_query(text):
    """
    Takes input text and formats it into a JSON request for the LLM service,
    generating HTML <p> tags without additional styling.

    Args:
        text (str): The input text to be processed

    Returns:
        dict: A formatted query dictionary ready to be sent to the LLM service
    """

    query = {
        "message": (
            f"Here is the text: {text} text end. Please process the text with the following rules: 1. use bold at the first two letter for every key word 2. Format the output in HTML using only <p> tags. 3. Do not include any CSS styles like background color, font size, font family, or padding. 4. Do not include '*', '**', or use markdown. Key word is not and "
            "Output only the final HTML. Do not include explanations or additional text—just the raw HTML content wrapped in <p> tags."
        ),
        "mode": "chat",
        "sessionId": "identifier-to-partition-chats-by-external-id",
        "attachments": []
    }

    return query
