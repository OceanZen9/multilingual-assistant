from flask import Flask
from config import get_config # From root config.py
# Ensure load_dotenv is called early, though config.py might also do it
from dotenv import load_dotenv
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Load configuration from root config.py
    app_config = get_config()
    app.config.from_object(app_config)

    # Configure logging level from app config
    log_level = app.config.get('LOG_LEVEL', 'INFO').upper()
    app.logger.setLevel(log_level)
    app.logger.info(f"Flask app '{__name__}' created with environment: {app_config.__class__.__name__}")
    app.logger.info(f"Debug mode: {app.debug}")
    # Log the DEEPSEEK_API_BASE to ensure it's loaded (it might be None if not set)
    app.logger.info(f"DeepSeek API Base (from config): {app.config.get('DEEPSEEK_API_BASE')}")


    # Import and register blueprints
    from app.api.routes import api_bp
    app.register_blueprint(api_bp)
    
    app.logger.info("API blueprint registered.")

    return app
