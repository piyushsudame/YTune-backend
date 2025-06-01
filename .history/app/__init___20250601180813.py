from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import yt_dlp

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

    @app.route('/api/stream', methods=['POST'])
    def get_stream_url():
        data = request.get_json()
        query = data.get('query')
        if not query:
            return jsonify({'error': 'No query provided'}), 400

        try:
            # Configure yt-dlp options
            ydl_opts = {
                'format': 'bestaudio/best',
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # If the query is a URL, use it directly
                if query.startswith(('http://', 'https://')):
                    info = ydl.extract_info(query, download=False)
                else:
                    # Search for the video
                    search_results = ydl.extract_info(f"ytsearch:{query}", download=False)
                    if not search_results or not search_results.get('entries'):
                        return jsonify({'error': 'No results found'}), 404
                    info = search_results['entries'][0]

                # Get the best audio URL
                formats = info.get('formats', [])
                audio_formats = [f for f in formats if f.get('acodec') != 'none' and f.get('vcodec') == 'none']
                
                if not audio_formats:
                    return jsonify({'error': 'No audio format found'}), 404

                # Get the best audio format
                best_audio = audio_formats[-1]  # Usually the last one is the best quality
                
                return jsonify({
                    'audio_url': best_audio['url'],
                    'title': info.get('title'),
                    'duration': info.get('duration'),
                    'thumbnail': info.get('thumbnail')
                })

        except Exception as e:
            return jsonify({'error': f'Error processing request: {str(e)}'}), 500

    # Health check endpoint
    @app.route('/ping')
    def ping():
        return {'status': 'ok'}

    return app