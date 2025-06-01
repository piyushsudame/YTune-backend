from flask import Flask, request, jsonify
from app.routes.ytmusic.search import search_song, get_top_song_video_id
from app.routes.ytmusic.details import get_song_details
from app.routes.ytmusic.audio import get_audio_url

app = Flask(__name__)

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    query = data.get('query')
    if not query:
        return jsonify({'error': 'No query provided'}), 400

    results = search_song(query)
    return jsonify(results)

@app.route('/song-details/<video_id>', methods=['GET'])
def song_details(video_id):
    details = get_song_details(video_id)
    return jsonify(details)

@app.route('/get-audio-url', methods=['POST'])
def get_audio():
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

if __name__ == "__main__":
    app.run(debug=True)
