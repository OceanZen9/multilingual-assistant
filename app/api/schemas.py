from marshmallow import Schema, fields

class TranslationRequestSchema(Schema):
    text = fields.String(required=True)
    source_language = fields.String()
    target_language = fields.String(required=True)

class TranslationResponseSchema(Schema):
    translated_text = fields.String()
    detected_source_language = fields.String()

class ContentGenerationRequestSchema(Schema):
    prompt = fields.String(required=True)
    max_tokens = fields.Integer(missing=100)
    temperature = fields.Float(missing=0.7)

class ContentGenerationResponseSchema(Schema):
    generated_text = fields.String()
    prompt_used = fields.String()

class ErrorSchema(Schema):
    error_code = fields.String(required=True)
    message = fields.String(required=True)
    details = fields.Dict()
