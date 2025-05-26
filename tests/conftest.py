import pytest
import os
from app import create_app # From app/__init__.py
from config import TestingConfig

@pytest.fixture(scope='module')
def app():
    # Save the original FLASK_ENV
    original_flask_env = os.environ.get("FLASK_ENV")
    # Set FLASK_ENV to 'test' to ensure TestingConfig is loaded by create_app
    os.environ["FLASK_ENV"] = "test"
    
    flask_app = create_app() # create_app will use get_config() which respects FLASK_ENV

    # After app creation, restore original FLASK_ENV
    if original_flask_env is None:
        del os.environ["FLASK_ENV"]
    else:
        os.environ["FLASK_ENV"] = original_flask_env

    # Double check if TestingConfig was indeed loaded and update if necessary.
    # This is more of a safeguard; ideally, create_app() with FLASK_ENV='test' is sufficient.
    # However, app.config is a Flask Config object, not our original config class instance.
    # We can check app.config['ENV'] or specific test values.
    if flask_app.config.get('ENV') != 'test' or not flask_app.config.get('TESTING'):
        # If create_app didn't pick up TestingConfig (e.g., if FLASK_ENV was overridden internally)
        # or if TestingConfig wasn't fully applied, force load TestingConfig.
        # This is a fallback.
        flask_app.config.from_object(TestingConfig) # This will override previous settings
        flask_app.config.update({"TESTING": True, "ENV": "test"})


    # Establish an application context before running the tests.
    with flask_app.app_context():
        yield flask_app # Yield the app for use in tests

@pytest.fixture
def client(app):
    # Create a test client using the app fixture
    return app.test_client()
