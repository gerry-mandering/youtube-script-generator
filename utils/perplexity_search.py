import requests
import os

from dotenv import load_dotenv
from utils.utils import logger

load_dotenv()

PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

def perplexity_search(keyword):
    logger.info(f"Starting Perplexity search for keyword: {keyword}")
    url = "https://api.perplexity.ai/chat/completions"
    
    payload = {
        "model": "llama-3.1-sonar-large-128k-online",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant providing concise and accurate information."
            },
            {
                "role": "user",
                "content": f"Provide a brief summary of key information about: {keyword}"
            }
        ]
    }
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {PERPLEXITY_API_KEY}"
    }

    try:
        logger.info("Sending request to Perplexity API")
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        data = response.json()
        if 'choices' in data and len(data['choices']) > 0:
            result = data['choices'][0]['message']['content']
            logger.info(f"Successfully retrieved information for: {keyword}")
            logger.info(f"Perplexity API Result: {result}")
            return result
        else:
            logger.warning(f"No relevant information found for: {keyword}")
            return f"No relevant information found for: {keyword}"
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred while querying Perplexity API: {e}")
        return f"Error occurred while searching for: {keyword}"