from flask import Blueprint, request, jsonify
from app.services.youtube_service import YouTubeService
import logging
import yt_dlp
from datetime import datetime, timedelta

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

@youtube_bp.route('/get-song-stream', methods=['POST'])
def get_song_stream():
    """
    Search for a song on YouTube and return its streamable URL.
    
    Request JSON:
    {
        "song_name": "song name by artist"
    }
    
    Response:
    {
        "stream_url": "direct_audio_url",
        "expires_at": "timestamp",
        "title": "video title",
        "thumbnail": "thumbnail_url"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        song_name = data.get('song_name')
        
        if not song_name:
            return jsonify({"error": "Song name is required"}), 400
        
        # Use yt-dlp to search for the song and get the stream URL
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'noplaylist': True,
            'default_search': 'ytsearch1',  # Search YouTube and get first result
        }
        
        logger.info(f"Searching for song: {song_name}")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Search for the song
            info = ydl.extract_info(song_name, download=False)
            
            if not info or 'entries' not in info or not info['entries']:
                return jsonify({"error": "No results found for the song"}), 404
            
            # Get the first result
            video_info = info['entries'][0]
            
            # Get the best audio format
            formats = video_info.get('formats', [])
            audio_formats = [f for f in formats if f.get('acodec') != 'none' and (f.get('vcodec') == 'none' or f.get('vcodec') is None)]
            
            if not audio_formats:
                return jsonify({"error": "No audio format found"}), 404
            
            # Sort by quality (bitrate)
            audio_formats.sort(key=lambda x: x.get('abr', 0) if x.get('abr') else 0, reverse=True)
            best_audio = audio_formats[0]
            
            # Estimate expiration time (YouTube URLs typically expire in 6 hours)
            expires_at = (datetime.now() + timedelta(hours=6)).isoformat()
            
            return jsonify({
                "stream_url": best_audio['url'],
                "expires_at": expires_at,
                "title": video_info.get('title', ''),
                "thumbnail": video_info.get('thumbnail', '')
            }), 200
        
    except Exception as e:
        logger.error(f"Error in get-song-stream endpoint: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500