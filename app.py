# from flask import Flask, request, jsonify
# import re
# import json
# import os
# import requests
# import base64
#
# app = Flask(__name__)
#
# # Try to import PyMuPDF, but provide fallback if not available
# try:
#     import fitz  # PyMuPDF
#     HAS_PYMUPDF = True
# except ImportError:
#     HAS_PYMUPDF = False
#     print("WARNING: PyMuPDF not available. PDF extraction will be limited.")
#
# # AnythingLLM Configuration
# ANYTHING_LLM_ENABLED = os.environ.get('ANYTHING_LLM_ENABLED', 'true').lower() == 'true'
# ANYTHING_LLM_HOST = os.environ.get('ANYTHING_LLM_HOST', 'http://localhost:3001')
# ANYTHING_LLM_API_KEY = os.environ.get('ANYTHING_LLM_API_KEY', '')
# ANYTHING_LLM_MODEL = os.environ.get('ANYTHING_LLM_MODEL', 'mistral-7b')
#
# # Validate API key
# if ANYTHING_LLM_ENABLED and not ANYTHING_LLM_API_KEY:
#     print("WARNING: AnythingLLM enabled but no API key provided. Integration will fail.")
#     print("Set your API key in the .env file or environment variables.")
#
# class AnythingLLMClient:
#     """Client for interacting with AnythingLLM API"""
#
#     def __init__(self, host=ANYTHING_LLM_HOST, api_key=ANYTHING_LLM_API_KEY, model=ANYTHING_LLM_MODEL):
#         self.host = host
#         self.api_key = api_key
#         self.model = model
#         self.headers = {
#             'Content-Type': 'application/json',
#             'Authorization': f'Bearer {self.api_key}'
#         }
#
#     def is_available(self):
#         """Check if AnythingLLM is available"""
#         try:
#             response = requests.get(f"{self.host}/api/health", headers=self.headers, timeout=5)
#             return response.status_code == 200
#         except Exception as e:
#             print(f"AnythingLLM not available: {e}")
#             return False
#
#     def process_text(self, text, prompt=None):
#         """Process text with AnythingLLM"""
#         if not prompt:
#             prompt = """
#             Process the following text to identify:
#             1. Syllables in each word (for syllable-based highlighting to aid ADHD readers)
#             2. Key information (sentences containing important context or action items)
#             3. Important data (dates, numbers, proper names, organizations, locations)
#
#             Format your response as JSON with these fields:
#             - syllableEnhancements: A dictionary mapping words to syllables
#             - keyInfo: An array of sentences containing important information
#             - importantData: An object with categories for dates, numbers, people, organizations, locations
#             """
#
#         try:
#             endpoint = f"{self.host}/api/chat"
#             payload = {
#                 "message": prompt,
#                 "model": self.model,
#                 "context": text,
#                 "temperature": 0.1,  # Lower temperature for more deterministic outputs
#                 "responseFormat": "json"
#             }
#
#             response = requests.post(endpoint, json=payload, headers=self.headers, timeout=30)
#
#             if response.status_code != 200:
#                 print(f"AnythingLLM API error: {response.status_code} - {response.text}")
#                 return None
#
#             result = response.json()
#             return self._parse_llm_response(result, text)
#
#         except Exception as e:
#             print(f"Error processing with AnythingLLM: {e}")
#             return None
#
#     def _parse_llm_response(self, result, original_text):
#         """Parse the response from AnythingLLM"""
#         try:
#             # Extract the response content
#             if 'response' in result:
#                 content = result['response']
#
#                 # Try to parse JSON from the response
#                 try:
#                     # Extract JSON if the response contains it
#                     if isinstance(content, str):
#                         # Find the JSON portion if it's wrapped in markdown code blocks
#                         if '```json' in content and '```' in content.split('```json', 1)[1]:
#                             json_str = content.split('```json', 1)[1].split('```', 1)[0]
#                             parsed = json.loads(json_str)
#                         else:
#                             # Try to parse the whole response as JSON
#                             parsed = json.loads(content)
#                     else:
#                         parsed = content
#
#                     # If we got valid JSON data, process it
#                     if isinstance(parsed, dict):
#                         return self._structure_llm_data(parsed, original_text)
#
#                 except json.JSONDecodeError:
#                     print("Failed to parse JSON from llm response")
#                     print(f"Response: {content}")
#                     return None
#
#             return None
#         except Exception as e:
#             print(f"Error parsing llm response: {e}")
#             return None
#
#     def _structure_llm_data(self, parsed_data, original_text):
#         """Convert llm JSON data to the format expected by the frontend"""
#         result = {
#             'words': [],
#             'keyInfo': [],
#             'importantData': []
#         }
#
#         # Process syllables
#         if 'syllableEnhancements' in parsed_data:
#             syllables = parsed_data['syllableEnhancements']
#             # Create word objects with syllables
#             for word, word_syllables in syllables.items():
#                 result['words'].append({
#                     'word': word,
#                     'syllables': word_syllables if isinstance(word_syllables, list) else [word]
#                 })
#
#         # If no syllables were provided, fall back to basic word extraction
#         if len(result['words']) == 0:
#             # Extract words and use basic syllable detection
#             words = re.findall(r'\b\w+\b', original_text)
#             for word in words:
#                 result['words'].append({
#                     'word': word,
#                     'syllables': self._simple_syllable_split(word)
#                 })
#
#         # Key information
#         if 'keyInfo' in parsed_data and isinstance(parsed_data['keyInfo'], list):
#             result['keyInfo'] = parsed_data['keyInfo']
#
#         # Important data
#         important_data = []
#         if 'importantData' in parsed_data:
#             data = parsed_data['importantData']
#
#             # Add dates
#             if 'dates' in data and isinstance(data['dates'], list):
#                 important_data.extend(data['dates'])
#
#             # Add numbers
#             if 'numbers' in data and isinstance(data['numbers'], list):
#                 important_data.extend(data['numbers'])
#
#             # Add people
#             if 'people' in data and isinstance(data['people'], list):
#                 important_data.extend(data['people'])
#
#             # Add organizations
#             if 'organizations' in data and isinstance(data['organizations'], list):
#                 important_data.extend(data['organizations'])
#
#             # Add locations
#             if 'locations' in data and isinstance(data['locations'], list):
#                 important_data.extend(data['locations'])
#
#         result['importantData'] = important_data
#
#         return result
#
#     def _simple_syllable_split(self, word):
#         """Basic syllable splitting as fallback"""
#         vowels = 'aeiouy'
#         word = word.lower()
#         syllables = []
#         current = ""
#         prev_is_vowel = False
#
#         for char in word:
#             is_vowel = char in vowels
#             current += char
#
#             # Start a new syllable after a vowel followed by a consonant
#             if current and prev_is_vowel and not is_vowel:
#                 if len(current) > 1:
#                     syllables.append(current[:-1])
#                     current = current[-1]
#
#             prev_is_vowel = is_vowel
#
#         if current:
#             syllables.append(current)
#
#         # Handle edge cases
#         if len(syllables) == 0:
#             return [word]
#
#         return syllables
#
# # Create an instance of the AnythingLLM client
# llm_client = AnythingLLMClient() if ANYTHING_LLM_ENABLED else None
#
# @app.route('/extract', methods=['POST'])
# def extract_text():
#     data = request.json
#     pdf_path = data.get('pdfPath')
#     use_binary = data.get('useBinary', False)  # For handling binary PDF data
#     binary_data = data.get('binaryData')  # Base64 encoded PDF data
#
#     try:
#         extracted_text = ""
#
#         # Handle binary PDF data (useful for mobile/web uploads)
#         if use_binary and binary_data:
#             if HAS_PYMUPDF:
#                 # Decode base64 data
#                 pdf_bytes = base64.b64decode(binary_data)
#
#                 # Create a temporary file
#                 temp_path = os.path.join(os.path.dirname(__file__), 'temp.pdf')
#                 with open(temp_path, 'wb') as f:
#                     f.write(pdf_bytes)
#
#                 # Extract text using PyMuPDF
#                 doc = fitz.open(temp_path)
#                 for page in doc:
#                     extracted_text += page.get_text()
#
#                 # Clean up
#                 doc.close()
#                 if os.path.exists(temp_path):
#                     os.remove(temp_path)
#             else:
#                 return jsonify({
#                     'success': False,
#                     'error': 'PyMuPDF is required for binary PDF processing'
#                 })
#
#         # Handle file path-based PDF
#         elif pdf_path:
#             if HAS_PYMUPDF:
#                 # Extract with PyMuPDF
#                 doc = fitz.open(pdf_path)
#                 for page in doc:
#                     extracted_text += page.get_text()
#                 doc.close()
#             else:
#                 # Fallback for demo: just return example text
#                 extracted_text = """
#                 This is example text since PyMuPDF is not installed.
#
#                 ADHD, or Attention-Deficit/Hyperactivity Disorder, is a neurodevelopmental condition
#                 that affects approximately 5-10% of children and 2-5% of adults worldwide.
#
#                 People with ADHD often face challenges with attention, hyperactivity, and impulsivity
#                 that can impact various aspects of their lives. It is important to note that ADHD is
#                 a medical condition, not a character flaw or the result of poor discipline.
#
#                 Symptoms typically appear before the age of 12 and can continue into adulthood.
#                 On 11/15/2023, a new study found that reading difficulties affect about 45% of
#                 individuals with ADHD.
#                 """
#         else:
#             return jsonify({
#                 'success': False,
#                 'error': 'No PDF path or binary data provided'
#             })
#
#         return jsonify({
#             'success': True,
#             'text': extracted_text
#         })
#     except Exception as e:
#         print(f"Error extracting PDF: {e}")
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         })
#
# @app.route('/process', methods=['POST'])
# def process_text():
#     data = request.json
#     text = data.get('text', '')
#     use_llm = data.get('useLLM', True) and ANYTHING_LLM_ENABLED
#
#     try:
#         # Try to use AnythingLLM if enabled and requested
#         if use_llm and llm_client and llm_client.is_available():
#             print("Processing text with AnythingLLM...")
#             llm_result = llm_client.process_text(text)
#
#             if llm_result:
#                 return jsonify({
#                     'success': True,
#                     'processed': llm_result,
#                     'processor': 'anythingllm'
#                 })
#
#         # Fall back to basic processing if llm is not available or failed
#         print("Falling back to basic text processing...")
#         processed_data = basic_text_processing(text)
#
#         return jsonify({
#             'success': True,
#             'processed': processed_data,
#             'processor': 'basic'
#         })
#     except Exception as e:
#         print(f"Error processing text: {e}")
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         })
#
# def basic_text_processing(text):
#     """Basic text processing for ADHD-friendly formatting"""
#     processed_data = {
#         'words': [],
#         'keyInfo': [],
#         'importantData': []
#     }
#
#     # Process words for syllable information
#     words = re.findall(r'\b\w+\b', text)
#     for word in words:
#         processed_data['words'].append({
#             'word': word,
#             'syllables': split_into_syllables(word)
#         })
#
#     # Find key information (sentences with action words)
#     sentences = re.split(r'[.!?]', text)
#     action_words = ['must', 'should', 'need', 'important', 'required', 'essential', 'critical']
#     for sentence in sentences:
#         if any(action in sentence.lower() for action in action_words):
#             processed_data['keyInfo'].append(sentence.strip())
#
#     # Identify important data (dates, numbers, names)
#     # Find dates like MM/DD/YYYY
#     dates = re.findall(r'\d{1,2}/\d{1,2}/\d{2,4}', text)
#     # Find numbers
#     numbers = re.findall(r'\b\d+\.\d+\b|\b\d+\b', text)
#
#     # Simple named entity recognition
#     words_in_text = text.split()
#     capitalized_words = []
#     for word in words_in_text:
#         cleaned_word = word.strip('.,;:!?()"\'')
#         if len(cleaned_word) > 1 and cleaned_word[0].isupper():
#             capitalized_words.append(cleaned_word)
#
#     processed_data['importantData'].extend(dates)
#     processed_data['importantData'].extend(numbers)
#     processed_data['importantData'].extend(capitalized_words)
#
#     return processed_data
#
# def split_into_syllables(word):
#     """Basic syllable splitting algorithm"""
#     vowels = 'aeiouy'
#     word = word.lower()
#     syllables = []
#     current = ""
#     prev_is_vowel = False
#
#     for char in word:
#         is_vowel = char in vowels
#         current += char
#
#         # Start a new syllable after a vowel followed by a consonant
#         if current and prev_is_vowel and not is_vowel:
#             if len(current) > 1:
#                 syllables.append(current[:-1])
#                 current = current[-1]
#
#         prev_is_vowel = is_vowel
#
#     if current:
#         syllables.append(current)
#
#     # Handle edge cases
#     if len(syllables) == 0:
#         return [word]
#
#     return syllables
#
# # Route to check if AnythingLLM is available
# @app.route('/api/llm-status', methods=['GET'])
# def llm_status():
#     """Check if AnythingLLM is available"""
#     if not ANYTHING_LLM_ENABLED:
#         return jsonify({
#             'available': False,
#             'reason': 'AnythingLLM integration is disabled'
#         })
#
#     if not llm_client:
#         return jsonify({
#             'available': False,
#             'reason': 'AnythingLLM client is not initialized'
#         })
#
#     available = llm_client.is_available()
#     return jsonify({
#         'available': available,
#         'model': ANYTHING_LLM_MODEL if available else None
#     })
# ##  apiendpoint: post -> response
# ## sendrequest by service
# ## response by using response from service
#
#
# @app.after_request
# def after_request(response):
#     """Add CORS headers to allow frontend to access API"""
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
#     response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
#     return response
#
# if __name__ == '__main__':
#     app.run(port=5001, debug=True)
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from llm import service as llm_service

app = FastAPI()

# Request model
class ExecuteRequest(BaseModel):
    text: str

# Response model
class ExecuteResponse(BaseModel):
    HTML: str

@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=404,
        content={"detail": "Resource not found"}
    )

@app.exception_handler(400)
async def bad_request_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=400,
        content={"detail": "Bad request: " + exc.detail if exc.detail else "Invalid input"}
    )
@app.post("/api/execute", response_model=ExecuteResponse)
async def execute(request: ExecuteRequest):
    try:
        input_text = request.text.strip()

        # Validate input (basic example)
        if not input_text:
            raise HTTPException(status_code=400, detail="Input 'text' cannot be empty")

        # Process the text using your LLM service function.
        # Replace 'process_text' with your actual function in llm/service.py
        html_result = llm_service.process_text(input_text)

        # If the result is None or empty, you can throw 404 as an example (optional logic)
        if not html_result:
            raise HTTPException(status_code=404, detail="No result found from LLM processing")

        return ExecuteResponse(HTML=html_result)

    except HTTPException as http_exc:
        # Reraise HTTPExceptions to be handled by FastAPI
        raise http_exc

    except Exception as e:
        # Catch unexpected exceptions and return as 500 Internal Server Error
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=5000, reload=True)

    uvicorn.run("app:app", host="127.0.0.1", port=5000, reload=True)