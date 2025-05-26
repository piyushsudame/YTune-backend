import json
from ytmusicapi import YTMusic
import yt_dlp

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

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        for f in info_dict.get('formats', []):
            if f.get('acodec') != 'none' and f.get('vcodec') == 'none':
                return f.get('url')
    return None

def main():
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
    main()
