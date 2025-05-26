from flask import Blueprint, request, jsonify
from ytmusicapi import YTMusic
import os
import json

ytmusic_bp = Blueprint('ytmusic', __name__, url_prefix='/api/ytmusic')

# Initialize YTMusic with OAuth or headers
def get_ytmusic():
    # Check if we have OAuth credentials
    if os.path.exists('oauth.json'):
        return YTMusic('oauth.json')
    
    # Check if we have headers file
    if os.path.exists('headers_auth.json'):
        return YTMusic('headers_auth.json')
    
    # If no auth is available, use non-authenticated client
    return YTMusic()

@ytmusic_bp.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    filter_param = request.args.get('filter', 'songs')
    limit = request.args.get('limit', 20, type=int)
    
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400
    
    try:
        ytmusic = get_ytmusic()
        results = ytmusic.search(query, filter=filter_param, limit=limit)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ytmusic_bp.route('/playlist/<playlist_id>', methods=['GET'])
def get_playlist(playlist_id):
    try:
        ytmusic = get_ytmusic()
        playlist = ytmusic.get_playlist(playlist_id)
        return jsonify(playlist)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ytmusic_bp.route('/song/<song_id>', methods=['GET'])
def get_song(song_id):
    try:
        ytmusic = get_ytmusic()
        song = ytmusic.get_song(song_id)
        return jsonify(song)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ytmusic_bp.route('/auth/setup', methods=['POST'])
def setup_auth():
    try:
        # For browser authentication
        if request.json.get('oauth', False):
            YTMusic.setup_oauth()
            return jsonify({'message': 'OAuth setup complete. Check oauth.json file.'})
        
        # For manual headers setup
        headers = request.json.get('headers')
        if headers:
            with open('headers_auth.json', 'w') as f:
                json.dump(headers, f)
            return jsonify({'message': 'Headers authentication setup complete'})
        
        return jsonify({'error': 'Invalid request. Specify oauth=true or provide headers.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ytmusic_bp.route('/library/playlists', methods=['GET'])
def get_library_playlists():
    try:
        ytmusic = get_ytmusic()
        playlists = ytmusic.get_library_playlists()
        return jsonify(playlists)
    except Exception as e:
        return jsonify({'error': str(e)}), 