from flask import Blueprint, request, jsonify, Response, stream_with_context
import yt_dlp
import json
import os
import subprocess
import tempfile

ytdlp_bp = Blueprint('ytdlp', __name__, url_prefix='/api/ytdlp')

# YT-DLP options for audio extraction
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'quiet': True,
    'no_warnings': True,
}

@ytdlp_bp.route('/info/<video_id>', methods=['GET'])
def get_video_info(video_id):
    """Get metadata for a YouTube video without downloading it"""
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify(info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ytdlp_bp.route('/stream/<video_id>', methods=['GET'])
def stream_audio(video_id):
    """Stream audio from a YouTube video"""
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        
        # Get the best audio format URL
        with yt_dlp.YoutubeDL({'format': 'bestaudio', 'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = None
            
            # Find the audio URL from the formats
            for format in info.get('formats', []):
                if format.get('acodec') != 'none' and format.get('vcodec') == 'none':
                    audio_url = format['url']
                    break
            
            if not audio_url:
                # If no audio-only format, use the best format available
                audio_url = info['formats'][-1]['url']
            
            # Create a response that redirects to the audio URL
            # This avoids having to proxy the entire stream through our server
            return jsonify({
                'url': audio_url,
                'title': info.get('title', ''),
                'duration': info.get('duration', 0),
                'thumbnail': info.get('thumbnail', '')
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ytdlp_bp.route('/download/<video_id>', methods=['GET'])
def download_audio(video_id):
    """Download audio from a YouTube video and serve it as a file"""
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        
        # Create a temporary directory for the download
        with tempfile.TemporaryDirectory() as temp_dir:
            # Configure yt-dlp to download to the temp directory
            download_opts = ydl_opts.copy()
            download_opts['outtmpl'] = os.path.join(temp_dir, '%(title)s.%(ext)s')
            
            # Download the audio
            with yt_dlp.YoutubeDL(download_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                
                # Get the downloaded file path
                if 'entries' in info:  # It's a playlist
                    info = info['entries'][0]
                
                # The file will be named according to the title with .mp3 extension
                filename = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
                
                if not os.path.exists(filename):
                    # Try to find the file in the temp directory
                    for file in os.listdir(temp_dir):
                        if file.endswith('.mp3'):
                            filename = os.path.join(temp_dir, file)
                            break
                
                # Check if the file exists
                if not os.path.exists(filename):
                    return jsonify({'error': 'Failed to download the file'}), 500
                
                # Stream the file to the client
                def generate():
                    with open(filename, 'rb') as f:
                        while True:
                            chunk = f.read(4096)
                            if not chunk:
                                break
                            yield chunk
                
                response = Response(stream_with_context(generate()), 
                                   mimetype='audio/mpeg')
                response.headers['Content-Disposition'] = f'attachment; filename="{os.path.basename(filename)}"'
                return response
                
    except Exception as e:
        return jsonify({'error': str(e)}), 500