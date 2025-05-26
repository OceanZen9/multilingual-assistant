import requests
from flask import current_app

class DeepSeekServiceError(Exception):
    pass

# Model name can still be a default here, or also moved to config if it varies by environment
DEFAULT_MODEL = "deepseek-chat" 

def generate_content(prompt: str, max_tokens: int = 150, temperature: float = 0.7):
    api_key = current_app.config.get("DEEPSEEK_API_KEY")
    api_base_url = current_app.config.get("DEEPSEEK_API_BASE")

    if not api_key:
        raise DeepSeekServiceError("DEEPSEEK_API_KEY not found in Flask app configuration.")
    if not api_base_url:
        raise DeepSeekServiceError("DEEPSEEK_API_BASE not found in Flask app configuration.")

    actual_api_url = f"{api_base_url.rstrip('/')}/v1/chat/completions"
    
    current_app.logger.debug(f"Using DeepSeek API URL: {actual_api_url}")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    payload = {
        "model": current_app.config.get("DEEPSEEK_MODEL_NAME", DEFAULT_MODEL), # Use model from config or default
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
        # Add other parameters as needed, e.g., stream, presence_penalty, etc.
        # These could also be configurable if desired.
    }

    try:
        response = requests.post(actual_api_url, headers=headers, json=payload)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)
        
        data = response.json()
        
        # Safely access the generated text
        # Check if 'choices' is present, is a list, and has at least one element
        if not data.get("choices") or not isinstance(data["choices"], list) or not data["choices"]:
            raise DeepSeekServiceError("Unexpected API response format: 'choices' missing or invalid.")
        
        choice = data["choices"][0]
        if not choice.get("message") or not choice["message"].get("content"):
            raise DeepSeekServiceError("Unexpected API response format: 'message' or 'content' missing.")
            
        generated_text = choice["message"]["content"]
        # Attempt to get model from response, fallback to requested model, then default
        model_used = data.get("model", payload.get("model", DEFAULT_MODEL))


        return {"generated_text": generated_text.strip(), "model_used": model_used}

    except requests.exceptions.HTTPError as e:
        # More specific error for HTTP errors, includes response content if possible
        error_details = f"HTTP error {e.response.status_code}: {e.response.text}"
        raise DeepSeekServiceError(f"DeepSeek API request failed: {error_details}")
    except requests.exceptions.RequestException as e:
        # For network issues, timeout, etc.
        raise DeepSeekServiceError(f"Error communicating with DeepSeek API: {e}")
    except (KeyError, TypeError, IndexError) as e:
        # Handles cases where the expected keys/structure are not in the response
        raise DeepSeekServiceError(f"Malformed response from DeepSeek API: {e}")
    except Exception as e:
        # Catch any other unexpected errors
        raise DeepSeekServiceError(f"An unexpected error occurred: {e}")
