import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.getenv('FLASK_RUN_PORT', 5000))
    # Use app.debug from loaded config, host='0.0.0.0' to be accessible externally
    app.run(host='0.0.0.0', port=port, debug=app.debug)
