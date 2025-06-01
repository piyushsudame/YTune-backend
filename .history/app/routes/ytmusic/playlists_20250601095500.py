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
        if not playlists:
            return []
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
        
        # Try to get the playlist directly
        try:
            # For public playlists, we need to use the full URL format
            if not playlist_id.startswith('http'):
                playlist_id = f'https://music.youtube.com/playlist?list={playlist_id}'
            
            playlist = ytmusic.get_playlist(playlist_id)
            if not playlist:
                raise Exception("Playlist not found")
            return playlist
        except Exception as e:
            if "singleColumnBrowseResultsRenderer" in str(e):
                # Try alternative method for public playlists
                try:
                    playlist = ytmusic.get_playlist(playlist_id, limit=None)
                    if not playlist:
                        raise Exception("Playlist not found")
                    return playlist
                except Exception as inner_e:
                    raise Exception(f"Playlist not found or is not accessible: {str(inner_e)}")
            raise Exception(f"Error accessing playlist: {str(e)}")
            
    except Exception as e:
        print(f"Error getting playlist details: {str(e)}")
        raise