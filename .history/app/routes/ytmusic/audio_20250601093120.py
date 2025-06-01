from yt_dlp import YoutubeDL

def get_audio_url(video_id):
    """
    Get the best audio URL for the given YouTube video ID.
    
    Args:
        video_id (str): The YouTube video ID
        
    Returns:
        str: Audio URL or None if not found
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