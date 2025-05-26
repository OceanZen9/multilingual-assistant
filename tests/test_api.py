import json
import pytest
from unittest.mock import patch, MagicMock

# Assuming conftest.py provides a 'client' fixture for the Flask test client.
# Schemas for expected error structure (simplified for tests, or import actual ErrorSchema if complex)
# For simplicity, we'll check key fields in error responses.

VALIDATION_ERROR_CODE = "VALIDATION_ERROR"
TRANSLATION_SERVICE_ERROR_CODE = "TRANSLATION_SERVICE_ERROR"
DEEPSEEK_SERVICE_ERROR_CODE = "DEEPSEEK_SERVICE_ERROR"
BAD_REQUEST_ERROR_CODE = "BAD_REQUEST"

# Tests for /api/translate
def test_translate_success(client):
    with patch('app.api.routes.translate_text') as mock_translate:
        mock_translate.return_value = {
            "translated_text": "Hola mundo",
            "detected_source_language": "en"
        }
        response = client.post('/api/translate', json={
            "text": "Hello world",
            "target_language": "es",
            "source_language": "en"
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data["translated_text"] == "Hola mundo"
        assert data["detected_source_language"] == "en"
        mock_translate.assert_called_once_with(text="Hello world", target_language="es", source_language="en")

def test_translate_validation_error(client):
    response = client.post('/api/translate', json={
        "text": "Hello world" # Missing target_language
    })
    assert response.status_code == 400
    data = response.get_json()
    assert data["error_code"] == VALIDATION_ERROR_CODE
    assert "target_language" in data["details"]

def test_translate_service_error(client):
    with patch('app.api.routes.translate_text') as mock_translate:
        from app.services.translation import TranslationServiceError
        mock_translate.side_effect = TranslationServiceError("Test translation error")
        response = client.post('/api/translate', json={
            "text": "Hello world",
            "target_language": "es"
        })
        assert response.status_code == 502 # As defined in the route
        data = response.get_json()
        assert data["error_code"] == TRANSLATION_SERVICE_ERROR_CODE
        assert "Test translation error" in data["message"]

def test_translate_no_json(client):
    response = client.post('/api/translate', data="not json", content_type="text/plain")
    assert response.status_code == 400
    data = response.get_json()
    assert data["error_code"] == BAD_REQUEST_ERROR_CODE
    assert "No input data provided" in data["message"]


# Tests for /api/generate
def test_generate_success(client):
    with patch('app.api.routes.generate_content') as mock_generate:
        mock_generate.return_value = {
            "generated_text": "This is a story.",
            "model_used": "deepseek-chat" # service returns this
        }
        response = client.post('/api/generate', json={
            "prompt": "Tell me a story",
            "max_tokens": 50
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data["generated_text"] == "This is a story."
        assert data["prompt_used"] == "Tell me a story" # Schema maps this
        mock_generate.assert_called_once_with(prompt="Tell me a story", max_tokens=50, temperature=0.7) # 0.7 is default

def test_generate_validation_error(client):
    response = client.post('/api/generate', json={
        "max_tokens": 50 # Missing prompt
    })
    assert response.status_code == 400
    data = response.get_json()
    assert data["error_code"] == VALIDATION_ERROR_CODE
    assert "prompt" in data["details"]

def test_generate_service_error(client):
    with patch('app.api.routes.generate_content') as mock_generate:
        from app.services.deepseek import DeepSeekServiceError
        mock_generate.side_effect = DeepSeekServiceError("Test generation error")
        response = client.post('/api/generate', json={
            "prompt": "Tell me a story"
        })
        assert response.status_code == 502 # As defined in the route
        data = response.get_json()
        assert data["error_code"] == DEEPSEEK_SERVICE_ERROR_CODE
        assert "Test generation error" in data["message"]

def test_generate_no_json(client):
    response = client.post('/api/generate', data="not json", content_type="text/plain")
    assert response.status_code == 400
    data = response.get_json()
    assert data["error_code"] == BAD_REQUEST_ERROR_CODE
    assert "No input data provided" in data["message"]
