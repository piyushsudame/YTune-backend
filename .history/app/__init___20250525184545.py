from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv

def create_app(test_config=None):
    # Load environment variables from .env file if it exists
    load_dotenv()
    
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    # Enable CORS for all routes
    CORS(app)
    
    # Set default configuration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        # Add other configuration settings as needed
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register blueprints
    from app.routes.ytmusic_routes import ytmusic_bp
    from app.routes.yt_dlp import ytdlp_bp
    
    app.register_blueprint(ytmusic_bp, url_prefix='/api/ytmusic')
    app.register_blueprint(ytdlp_bp, url_prefix='/api/ytdlp')

    # Health check endpoint
    @app.route('/ping')
    def ping():
        return {'status': 'ok'}

    return app