from ytmusicapi import YTMusic

def get_playlists():
    """
    Get all playlists from the authenticated user's YouTube Music account
    
    Returns:
        list: List of playlists with their details
    """
    try:
        ytmusic = YTMusic('oauth.json')
        playlists = ytmusic.get_library_playlists()
        return playlists
    except Exception as e:
        print(f"Error getting playlists: {str(e)}")
        raise

def get_playlist_details(playlist_id):
    """
    Get detailed information about a specific playlist
    
    Args:
        playlist_id (str): The playlist ID
        
    Returns:
        dict: Playlist details including all tracks
    """
    try:
        ytmusic = YTMusic('oauth.json')
        playlist = ytmusic.get_playlist(playlist_id)
        return playlist
    except Exception as e:
        print(f"Error getting playlist details: {str(e)}")
        raise