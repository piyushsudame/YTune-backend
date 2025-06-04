from flask import Blueprint, request, jsonify
from app.services.youtube_service import YouTubeService
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create blueprint
youtube_bp = Blueprint('youtube', __name__, url_prefix='/api')

@youtube_bp.route('/search-song', methods=['POST'])
def search_song():
    """
    Search for a song on YouTube based on title and artist.
    
    Request JSON:
    {
        "title": "song name",
        "artist": "artist name",
        "duration": 180  # optional, in seconds
    }
    
    Response:
    {
        "video_id": "xyz",
        "title": "full title",
        "url": "youtube_url",
        "thumbnail": "thumbnail_url"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        title = data.get('title')
        artist = data.get('artist')
        duration = data.get('duration')
        
        if not title or not artist:
            return jsonify({"error": "Both title and artist are required"}), 400
            
        result = YouTubeService.search_song(title, artist, duration)
        
        if "error" in result:
            return jsonify(result), 404
            
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error in search-song endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@youtube_bp.route('/get-stream-url', methods=['POST'])
def get_stream_url():
    """
    Get direct audio stream URL from YouTube video.
    
    Request JSON:
    {
        "video_id": "xyz"  # OR
        "youtube_url": "full_url"
    }
    
    Response:
    {
        "stream_url": "direct_audio_url",
        "expires_at": "timestamp",
        "format": "audio format",
        "bitrate": 128
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        video_id = data.get('video_id')
        youtube_url = data.get('youtube_url')
        
        if not video_id and not youtube_url:
            return jsonify({"error": "Either video_id or youtube_url must be provided"}), 400
            
        result = YouTubeService.get_stream_url(video_id, youtube_url)
        
        if "error" in result:
            return jsonify(result), 404
            
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error in get-stream-url endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@youtube_bp.route('/song-info/<video_id>', methods=['GET'])
def get_song_info(video_id):
    """
    Get metadata about a YouTube video.
    
    Response:
    {
        "title": "video title",
        "duration": 180,
        "thumbnail": "thumbnail_url",
        "uploader": "channel name"
    }
    """
    try:
        if not video_id:
            return jsonify({"error": "Video ID is required"}), 400
            
        result = YouTubeService.get_song_info(video_id)
        
        if "error" in result:
            return jsonify(result), 404
            
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error in song-info endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500