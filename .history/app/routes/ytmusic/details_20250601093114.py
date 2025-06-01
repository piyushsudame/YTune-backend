from ytmusicapi import YTMusic

def get_song_details(video_id):
    """
    Get detailed information about a song
    
    Args:
        video_id (str): The YouTube video ID
        
    Returns:
        dict: Song details
    """
    ytmusic = YTMusic()
    song_details = ytmusic.get_song(video_id)
    return song_details 