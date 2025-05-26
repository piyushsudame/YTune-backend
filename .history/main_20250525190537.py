from flask import Flask, request, jsonify
from app.routes.use_main_api import search_song, get_song_details
from app.routes.get_song_url import get_top_song_video_id, get_audio_url

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
    
    video_id = get_top_song_video_id(query)
    if not video_id:
        return jsonify({'error': 'No video found'}), 404
    
    audio_url = get_audio_url(video_id)
    if not audio_url:
        return jsonify({'error': 'Could not get audio URL'}), 404
    
    return jsonify({'audio_url': audio_url})

if __name__ == "__main__":
    app.run(debug=True)