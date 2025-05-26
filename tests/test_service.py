import pytest
from unittest.mock import patch, MagicMock
from flask import Flask # Needed to create a dummy app context for tests

from app.services.translation import translate_text, TranslationServiceError
from app.services.deepseek import generate_content, DeepSeekServiceError
# Assuming conftest.py provides an 'app' fixture for a configured Flask app

# Helper function to create a minimal app with specific config for service tests
def create_test_app(config_overrides=None):
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['DEEPSEEK_API_KEY'] = 'default_test_key'
    app.config['DEEPSEEK_API_BASE'] = 'https://api.testdeepseek.com'
    app.config['DEEPSEEK_MODEL_NAME'] = 'test-model'
    if config_overrides:
        app.config.update(config_overrides)
    return app

# --- Tests for Translation Service ---
def test_translate_text_success_placeholder(app): # Uses app from conftest
    with app.app_context(): # Services use current_app.config
        # Ensure the app context has a key, even if placeholder uses it or not
        # This is important if the conftest app doesn't guarantee this specific key
        if 'DEEPSEEK_API_KEY' not in app.config or app.config['DEEPSEEK_API_KEY'] is None:
             app.config['DEEPSEEK_API_KEY'] = 'dummy_key_for_translation_test_placeholder'
        
        result = translate_text("hello", "es", "en")
        assert result["translated_text"] == "Translated 'hello' to 'es' (placeholder)"
        assert result["detected_source_language"] == "en"

def test_translate_text_missing_api_key():
    app = create_test_app(config_overrides={"DEEPSEEK_API_KEY": None})
    with app.app_context():
        with pytest.raises(TranslationServiceError, match="DEEPSEEK_API_KEY not found"):
            translate_text("hello", "es")

# --- Tests for DeepSeek Service ---
MOCK_DEEPSEEK_URL = "https://api.testdeepseek.com/v1/chat/completions" # Expected URL based on helper/config

@patch('app.services.deepseek.requests.post')
def test_generate_content_success(mock_post, app): # Uses app from conftest
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "Generated story."}}],
        "model": "deepseek-test-model-from-api" # Model name returned by API
    }
    mock_post.return_value = mock_response

    with app.app_context(): # Ensure current_app.config is available
        # Override or ensure these specific config values for this test
        # This makes the test self-contained regarding config for deepseek service call
        app.config['DEEPSEEK_API_KEY'] = 'testkey123_for_success_test'
        app.config['DEEPSEEK_API_BASE'] = 'https://api.testdeepseek.com' # Must match MOCK_DEEPSEEK_URL base
        app.config['DEEPSEEK_MODEL_NAME'] = 'model-configured-for-success-test'
        
        result = generate_content("A story prompt")
        assert result["generated_text"] == "Generated story."
        assert result["model_used"] == "deepseek-test-model-from-api" # API response model takes precedence
        
        expected_payload = {
            "model": "model-configured-for-success-test", # This is what's sent to the API
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "A story prompt"},
            ],
            "max_tokens": 150, # Default
            "temperature": 0.7, # Default
        }
        mock_post.assert_called_once_with(
            MOCK_DEEPSEEK_URL, # Constructed from DEEPSEEK_API_BASE
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer testkey123_for_success_test",
            },
            json=expected_payload
        )

def test_generate_content_missing_api_key():
    # Using create_test_app for specific config manipulation
    app_instance = create_test_app(config_overrides={"DEEPSEEK_API_KEY": None})
    with app_instance.app_context():
        with pytest.raises(DeepSeekServiceError, match="DEEPSEEK_API_KEY not found"):
            generate_content("A prompt")

def test_generate_content_missing_api_base():
    app_instance = create_test_app(config_overrides={"DEEPSEEK_API_BASE": None})
    with app_instance.app_context():
        with pytest.raises(DeepSeekServiceError, match="DEEPSEEK_API_BASE not found"):
            generate_content("A prompt")

@patch('app.services.deepseek.requests.post')
def test_generate_content_api_http_error(mock_post):
    app_instance = create_test_app() # Has necessary config by default
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    import requests
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
    mock_post.return_value = mock_response

    with app_instance.app_context():
        with pytest.raises(DeepSeekServiceError, match="HTTP error 500: Internal Server Error"):
            generate_content("A prompt")

@patch('app.services.deepseek.requests.post')
def test_generate_content_api_request_exception(mock_post):
    app_instance = create_test_app()
    import requests
    mock_post.side_effect = requests.exceptions.Timeout("API timed out")

    with app_instance.app_context():
        with pytest.raises(DeepSeekServiceError, match="Error communicating with DeepSeek API: API timed out"):
            generate_content("A prompt")

@patch('app.services.deepseek.requests.post')
def test_generate_content_malformed_response_no_choices(mock_post):
    app_instance = create_test_app()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"error": "no choices here"} # Malformed
    mock_post.return_value = mock_response

    with app_instance.app_context():
        with pytest.raises(DeepSeekServiceError, match="Unexpected API response format: 'choices' missing or invalid"):
            generate_content("A prompt")

@patch('app.services.deepseek.requests.post')
def test_generate_content_malformed_response_no_message(mock_post):
    app_instance = create_test_app()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"choices": [{"something_else": "data"}]} # Malformed
    mock_post.return_value = mock_response

    with app_instance.app_context():
        with pytest.raises(DeepSeekServiceError, match="Unexpected API response format: 'message' or 'content' missing"):
            generate_content("A prompt")

@patch('app.services.deepseek.requests.post')
def test_generate_content_uses_default_model_if_not_in_config(mock_post, app): # uses conftest app
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "Generated with default model."}}],
        "model": "deepseek-chat" # API returns the model it used
    }
    mock_post.return_value = mock_response

    with app.app_context():
        # Ensure DEEPSEEK_MODEL_NAME is not in the app config for this test
        original_model_name = app.config.pop('DEEPSEEK_MODEL_NAME', None)
        
        # Ensure API key and base are present
        app.config['DEEPSEEK_API_KEY'] = 'testkey_default_model_test'
        app.config['DEEPSEEK_API_BASE'] = 'https://api.testdeepseek.com'

        result = generate_content("Prompt for default model")
        assert result["generated_text"] == "Generated with default model."
        assert result["model_used"] == "deepseek-chat"
        
        expected_payload = {
            "model": "deepseek-chat", # This is the DEFAULT_MODEL from app.services.deepseek
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Prompt for default model"},
            ],
            "max_tokens": 150,
            "temperature": 0.7,
        }
        mock_post.assert_called_once_with(
            MOCK_DEEPSEEK_URL,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer testkey_default_model_test",
            },
            json=expected_payload
        )
        
        # Restore model name if it was originally there
        if original_model_name is not None:
            app.config['DEEPSEEK_MODEL_NAME'] = original_model_name
