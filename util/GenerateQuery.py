import json

def generate_llm_query(text):
    """
    Takes input text and formats it into a JSON request for the LLM service.

    Args:
        text (str): The input text to be processed

    Returns:
        dict: A formatted query dictionary ready to be sent to the LLM service
    """
    query = {
        "message": f"Here is the text: {text} text end. "
                   "Please make the first two letters bold in text and underline the key words. "
                   "Output to HTML format, no need for explanation, only HTML details.",
        "mode": "chat",
        "sessionId": "identifier-to-partition-chats-by-external-id",
        "attachments": []
    }

    return query

