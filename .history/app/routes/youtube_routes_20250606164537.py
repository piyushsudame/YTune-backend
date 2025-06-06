from flask import Flask, request, jsonify
from yt_dlp import YoutubeDL
import traceback

app = Flask(__name__)

@app.route('/api/get-stream-url', methods=['POST'])
def get_stream_url():
    data = request.get_json()
    song_name = data.get('song_name')

    ydl_opts = {
        'quiet': True,
        'format': 'bestaudio[ext=m4a]/bestaudio/best',
        'default_search': 'ytsearch1',
        'noplaylist': True,
        'skip_download': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(song_name, download=False)

            # if it's a search result list
            if 'entries' in info:
                info = info['entries'][0]  # grab first result

            stream_url = info.get('url')
            if not stream_url:
                raise Exception("No stream URL found.")

            return jsonify({ "stream_url": stream_url })

    except Exception as e:
        return jsonify({ "error": f"Error getting stream URL: {str(e)}" }), 500
