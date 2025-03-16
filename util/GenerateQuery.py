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
                   "Extract 3-5 key words or short phrases from this text that capture the main concepts. "
                   "Don't explain anything - only return the keywords separated by commas. "
                   "For example, return: keyword1, keyword2, keyword3",
        "mode": "chat",
        "sessionId": "identifier-to-partition-chats-by-external-id",
        "attachments": []
    }

    return query

