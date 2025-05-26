import json
from ytmusicapi import YTMusic
from yt_dlp import YoutubeDL
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_top_song_video_id(query):
    """
    Use ytmusicapi to get the top song's videoId from a query.
    """
    ytmusic = YTMusic()
    results = ytmusic.search(query, filter="songs")
    
    if results and 'videoId' in results[0]:
        return results[0]['videoId']
    return None

def get_audio_url(video_id):
    """
    Use yt-dlp to get the best audio URL for the given YouTube video ID.
    """
    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': True,
        'extract_flat': False,
        'skip_download': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            for f in info_dict.get('formats', []):
                if f.get('acodec') != 'none' and f.get('vcodec') == 'none':
                    return f.get('url')
            
            # Fallback: if no audio-only format is found, return any URL
            if info_dict.get('formats'):
                for f in info_dict.get('formats', []):
                    if f.get('url'):
                        return f.get('url')
    except Exception as e:
        print(f"Error in get_audio_url: {str(e)}")
    return None

def get_video_url_from_json():
    """
    Read video ID from song_details.json and return its URL
    """
    try:
        with open('song_details.json', 'r') as f:
            data = json.load(f)
            video_id = data.get('videoDetails', {}).get('videoId')
            if video_id:
                return f"https://www.youtube.com/watch?v={video_id}"
    except FileNotFoundError:
        print("song_details.json not found")
    except json.JSONDecodeError:
        print("Error reading song_details.json")
    return None

@app.route('/get-audio-url', methods=['GET'])
def get_audio_url_endpoint():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400
    
    video_id = get_top_song_video_id(query)
    if not video_id:
        return jsonify({'error': 'Could not find a valid song'}), 404
    
    audio_url = get_audio_url(video_id)
    if not audio_url:
        return jsonify({'error': 'Failed to extract audio URL'}), 500
    
    return jsonify({
        'video_id': video_id,
        'audio_url': audio_url
    })

def main():
    # First try to get URL from song_details.json
    video_url = get_video_url_from_json()
    
    if video_url:
        print(f"Found video URL from song_details.json: {video_url}")
        video_id = video_url.split('v=')[1]
        audio_url = get_audio_url(video_id)
        if audio_url:
            print(f"\nAudio URL:\n{audio_url}")
        else:
            print("Failed to extract audio URL.")
    else:
        # Fallback to manual search if json not found
        query = input("Enter a song name: ")
        video_id = get_top_song_video_id(query)

        if not video_id:
            print("Couldn't find a valid song.")
            return

        print(f"Video ID found: {video_id}")
        audio_url = get_audio_url(video_id)

        if audio_url:
            print(f"\nAudio URL:\n{audio_url}")
        else:
            print("Failed to extract audio URL.")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
