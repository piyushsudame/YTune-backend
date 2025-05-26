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

    # Register routes
    from flask import Blueprint
    
    # Create blueprints
    ytmusic_bp = Blueprint('ytmusic', __name__)
    ytdlp_bp = Blueprint('ytdlp', __name__)
    
    # Import route functions
    from app.routes.use_main_api import search_song, get_song_details
    from app.routes.get_song_url import get_top_song_video_id, get_audio_url
    
    # Define routes for ytmusic blueprint
    @ytmusic_bp.route('/search', methods=['POST'])
    def search():
        from flask import request, jsonify
        data = request.get_json()
        query = data.get('query')
        if not query:
            return jsonify({'error': 'No query provided'}), 400
        
        results = search_song(query)
        return jsonify(results)
    
    @ytmusic_bp.route('/song-details/<video_id>', methods=['GET'])
    def song_details(video_id):
        from flask import jsonify
        details = get_song_details(video_id)
        return jsonify(details)
    
    # Define routes for ytdlp blueprint
    @ytdlp_bp.route('/get-audio-url', methods=['POST'])
    def get_audio():
        from flask import request, jsonify
        data = request.get_json()
        query = data.get('query')
        if not query:
            return jsonify({'error': 'No query provided'}), 400
        
        # Check if the query looks like a YouTube video ID (typically 11 characters)
        if len(query) == 11 and all(c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_' for c in query):
            # Use the query directly as a video ID
            video_id = query
        else:
            # Use the query to search for a video
            video_id = get_top_song_video_id(query)
            if not video_id:
                return jsonify({'error': 'No video found'}), 404
        
        try:
            audio_url = get_audio_url(video_id)
            if not audio_url:
                return jsonify({'error': 'Could not get audio URL'}), 404
            
            return jsonify({'audio_url': audio_url})
        except Exception as e:
            return jsonify({'error': f'Error processing request: {str(e)}'}), 500
    
    # Register blueprints
    app.register_blueprint(ytmusic_bp, url_prefix='/api/ytmusic')
    app.register_blueprint(ytdlp_bp, url_prefix='/api/ytdlp')

    # Health check endpoint
    @app.route('/ping')
    def ping():
        return {'status': 'ok'}

    return app