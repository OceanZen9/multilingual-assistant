from flask import Blueprint, request, jsonify, current_app
from marshmallow import ValidationError

from app.api.schemas import (
    TranslationRequestSchema, TranslationResponseSchema,
    ContentGenerationRequestSchema, ContentGenerationResponseSchema,
    ErrorSchema
)
from app.services.translation import translate_text, TranslationServiceError
from app.services.deepseek import generate_content, DeepSeekServiceError

# Create a Flask Blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Instantiate Schemas
translation_request_schema = TranslationRequestSchema()
translation_response_schema = TranslationResponseSchema()
content_generation_request_schema = ContentGenerationRequestSchema()
content_generation_response_schema = ContentGenerationResponseSchema()
error_schema = ErrorSchema()

@api_bp.route('/translate', methods=['POST'])
def handle_translate():
    json_data = request.get_json()
    if not json_data:
        return jsonify(error_schema.dump({
            "error_code": "BAD_REQUEST",
            "message": "No input data provided"
        })), 400
    
    try:
        data = translation_request_schema.load(json_data)
        result = translate_text(
            text=data['text'],
            target_language=data['target_language'],
            source_language=data.get('source_language') # .get() for optional field
        )
        return jsonify(translation_response_schema.dump(result)), 200

    except ValidationError as err:
        current_app.logger.warning(f"Validation error in /translate: {err.messages}")
        return jsonify(error_schema.dump({
            "error_code": "VALIDATION_ERROR",
            "message": "Invalid input provided.",
            "details": err.messages
        })), 400
    except TranslationServiceError as err:
        current_app.logger.error(f"TranslationServiceError in /translate: {str(err)}")
        return jsonify(error_schema.dump({
            "error_code": "TRANSLATION_SERVICE_ERROR",
            "message": str(err)
        })), 502 # 502 Bad Gateway for upstream service errors
    except Exception as err:
        current_app.logger.error(f"Unhandled exception in /translate: {str(err)}", exc_info=True)
        return jsonify(error_schema.dump({
            "error_code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected internal error occurred."
        })), 500

@api_bp.route('/generate', methods=['POST'])
def handle_generate():
    json_data = request.get_json()
    if not json_data:
        return jsonify(error_schema.dump({
            "error_code": "BAD_REQUEST",
            "message": "No input data provided"
        })), 400

    try:
        data = content_generation_request_schema.load(json_data)
        result = generate_content(
            prompt=data['prompt'],
            max_tokens=data.get('max_tokens', 150), # Use .get() with default for optional fields
            temperature=data.get('temperature', 0.7) # Use .get() with default for optional fields
        )
        # The service returns a dict like {"generated_text": "...", "model_used": "..."}
        # The ContentGenerationResponseSchema expects "generated_text" and "prompt_used"
        # Aligning the response to the schema.
        response_data = {
            "generated_text": result["generated_text"],
            "prompt_used": data['prompt'] 
        }
        return jsonify(content_generation_response_schema.dump(response_data)), 200

    except ValidationError as err:
        current_app.logger.warning(f"Validation error in /generate: {err.messages}")
        return jsonify(error_schema.dump({
            "error_code": "VALIDATION_ERROR",
            "message": "Invalid input provided.",
            "details": err.messages
        })), 400
    except DeepSeekServiceError as err:
        current_app.logger.error(f"DeepSeekServiceError in /generate: {str(err)}")
        return jsonify(error_schema.dump({
            "error_code": "DEEPSEEK_SERVICE_ERROR",
            "message": str(err)
        })), 502 # 502 Bad Gateway for upstream service errors
    except Exception as err:
        current_app.logger.error(f"Unhandled exception in /generate: {str(err)}", exc_info=True)
        return jsonify(error_schema.dump({
            "error_code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected internal error occurred."
        })), 500
