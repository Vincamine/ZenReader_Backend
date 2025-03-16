"""
Integration with AnythingLLM for enhanced text processing.
This module provides functions for connecting to and utilizing AnythingLLM.
"""

import json
import re
import os
import requests
from typing import Dict, List, Any, Optional, Union

# Default configuration - in production, this would be loaded from environment variables
DEFAULT_CONFIG = {
    "api_url": "http://localhost:3000/api", # Default AnythingLLM API URL
    "api_key": "your_api_key_here",         # Would be loaded securely in production
    "model": "default"                       # The model to use in AnythingLLM
}

class AnythingLLMClient:
    """Client for interacting with AnythingLLM."""
    
    def __init__(self, config: Optional[Dict[str, str]] = None):
        """Initialize the AnythingLLM client with configuration."""
        self.config = config or DEFAULT_CONFIG
        self.api_url = self.config["api_url"]
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config['api_key']}"
        }
        
    def test_connection(self) -> bool:
        """Test the connection to AnythingLLM."""
        try:
            # This is a placeholder - you would use the actual API endpoints
            response = requests.get(f"{self.api_url}/status", headers=self.headers)
            return response.status_code == 200
        except Exception as e:
            print(f"Failed to connect to AnythingLLM: {e}")
            return False
    
    def process_text(self, text: str) -> Dict[str, Any]:
        """
        Process text using AnythingLLM to extract enhanced information.
        
        Args:
            text: The text to process
            
        Returns:
            A dictionary containing processed data
        """
        # This is a placeholder implementation
        # In a real implementation, you would send the text to AnythingLLM
        # and parse the response
        
        try:
            # Simulate AnythingLLM processing
            processed_data = self._simulate_llm_processing(text)
            return processed_data
        except Exception as e:
            print(f"Error processing text with AnythingLLM: {e}")
            return self._fallback_processing(text)
    
    def split_into_syllables(self, word: str) -> List[str]:
        """
        Split a word into syllables using AnythingLLM.
        
        Args:
            word: The word to split
            
        Returns:
            A list of syllables
        """
        # This would call AnythingLLM in a real implementation
        # For now, use a simple heuristic
        
        try:
            # Prompt for AnythingLLM (would be used in the actual implementation)
            prompt = f"Split the word '{word}' into syllables. Return only the syllables as a JSON array."
            
            # Simple syllable splitting algorithm as fallback
            vowels = 'aeiouy'
            word = word.lower()
            syllables = []
            current = ""
            prev_is_vowel = False
            
            for char in word:
                is_vowel = char in vowels
                current += char
                
                # Start a new syllable after a vowel followed by a consonant
                # This is a simplified rule and not perfect
                if current and prev_is_vowel and not is_vowel:
                    if len(current) > 1:
                        syllables.append(current[:-1])
                        current = current[-1]
                
                prev_is_vowel = is_vowel
            
            if current:
                syllables.append(current)
            
            # If no syllables were found, treat the whole word as one syllable
            if not syllables:
                return [word]
                
            return syllables
        except Exception as e:
            print(f"Error splitting word into syllables: {e}")
            return [word]  # Return the entire word as a fallback
    
    def _simulate_llm_processing(self, text: str) -> Dict[str, Any]:
        """
        Simulate AnythingLLM processing for development purposes.
        
        In a real implementation, this would send the text to AnythingLLM
        and parse the response.
        """
        # Process text to extract sentences
        sentences = re.split(r'[.!?]', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Extract words
        words = re.findall(r'\b\w+\b', text)
        
        # Process words for syllable information
        processed_words = []
        for word in words:
            syllables = self.split_into_syllables(word)
            processed_words.append({
                "word": word,
                "syllables": syllables
            })
        
        # Identify key information (sentences with action words)
        action_words = ['must', 'should', 'need', 'important', 'required', 'critical', 'essential']
        key_info = []
        for sentence in sentences:
            if any(action in sentence.lower() for action in action_words):
                key_info.append(sentence)
        
        # Find important data (dates, numbers, names)
        # Dates like MM/DD/YYYY
        dates = re.findall(r'\d{1,2}/\d{1,2}/\d{2,4}', text)
        # Numbers
        numbers = re.findall(r'\b\d+\.\d+\b|\b\d+\b', text)
        
        # Simulate entity recognition (would be done by AnythingLLM)
        # This is a very basic simulation
        people = []
        organizations = []
        locations = []
        
        # Simple heuristics for entities
        for word in words:
            if word[0].isupper() and len(word) > 1:
                # This is a very naive approach - just for demonstration
                if len(word) > 7:
                    organizations.append(word)
                elif word.endswith(('ville', 'town', 'city', 'land')):
                    locations.append(word)
                else:
                    people.append(word)
        
        # Combine all important data
        important_data = dates + numbers + people + organizations + locations
        
        # Generate a simple summary (would be done by AnythingLLM)
        word_count = len(words)
        sentence_count = len(sentences)
        summary = f"This document contains {word_count} words in {sentence_count} sentences."
        
        return {
            "words": processed_words,
            "keyInfo": key_info,
            "importantData": important_data,
            "entities": {
                "people": people,
                "organizations": organizations,
                "locations": locations,
                "dates": dates,
                "numbers": numbers
            },
            "summary": summary
        }
    
    def _fallback_processing(self, text: str) -> Dict[str, Any]:
        """
        Fallback processing method if AnythingLLM is unavailable.
        """
        # Very basic processing as a fallback
        words = re.findall(r'\b\w+\b', text)
        processed_words = [{"word": w, "syllables": [w]} for w in words]
        
        return {
            "words": processed_words,
            "keyInfo": [],
            "importantData": [],
            "entities": {
                "people": [],
                "organizations": [],
                "locations": [],
                "dates": [],
                "numbers": []
            },
            "summary": "Processing was done without AnythingLLM due to an error."
        }


# Utility function to get a client instance
def get_client() -> AnythingLLMClient:
    """Get an instance of the AnythingLLM client."""
    # In a real application, you might load configuration from environment variables
    config = {
        "api_url": os.environ.get("ANYTHING_LLM_API_URL", DEFAULT_CONFIG["api_url"]),
        "api_key": os.environ.get("ANYTHING_LLM_API_KEY", DEFAULT_CONFIG["api_key"]),
        "model": os.environ.get("ANYTHING_LLM_MODEL", DEFAULT_CONFIG["model"])
    }
    return AnythingLLMClient(config)


# Sample usage
if __name__ == "__main__":
    # This is just for testing/demonstration
    client = get_client()
    
    if client.test_connection():
        print("Successfully connected to AnythingLLM")
    else:
        print("Failed to connect to AnythingLLM, will use fallback methods")
    
    sample_text = """
    ADHD, or Attention-Deficit/Hyperactivity Disorder, is a neurodevelopmental condition that affects approximately 5-10% of children and 2-5% of adults worldwide. People with ADHD often face challenges with attention, hyperactivity, and impulsivity that can impact various aspects of their lives. It is important to note that ADHD is a medical condition, not a character flaw or the result of poor discipline.
    
    Symptoms typically appear before the age of 12 and can continue into adulthood. On 11/15/2023, a new study found that reading difficulties affect about 45% of individuals with ADHD. The study was conducted at Harvard University.
    """
    
    result = client.process_text(sample_text)
    print(json.dumps(result, indent=2))