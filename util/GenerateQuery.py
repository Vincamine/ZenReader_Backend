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
        "message": f"Here is the text: {text} text end. please make the first two letter bold in text and underline the key words, output to html format, no need explaination, only html details",
        "mode": "chat",
        "sessionId": "identifier-to-partition-chats-by-external-id",
        "attachments": []
    }
    
    return query

