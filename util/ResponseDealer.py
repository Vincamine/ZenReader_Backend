def process_llm_response(response):
    """
    Processes the response from the LLM service.
    
    Args:
        response (dict): The raw response from the LLM service
        
    Returns:
        str: Processed HTML content 
    """
    if not response:
        return "<p>Error: No response received from LLM</p>"
        
    # Extract HTML content from response
    try:
        # The structure of the response depends on the specific LLM service
        # This assumes a structure where the response is in a 'response' field
        if 'response' in response:
            return response['response']
        else:
            # If the response has a different structure, modify this accordingly
            return str(response)
    except Exception as e:
        print(f"Error processing LLM response: {e}")
        return f"<p>Error processing response: {str(e)}</p>"