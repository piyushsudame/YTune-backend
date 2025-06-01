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
        print(f"Found {len(playlists) if playlists else 0} playlists")
        if playlists:
            print("First few playlists:", [p.get('title') for p in playlists[:3]])
        return playlists if playlists else []
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
        
        # First get all playlists to verify the ID
        all_playlists = ytmusic.get_library_playlists()
        print(f"Searching for playlist ID: {playlist_id}")
        print(f"Available playlists: {[p.get('playlistId') for p in all_playlists]}")
        
        # Try to get the playlist directly
        try:
            playlist = ytmusic.get_playlist(playlist_id)
            if not playlist:
                raise Exception("Playlist not found")
            return playlist
        except Exception as e:
            print(f"Error accessing playlist: {str(e)}")
            # Try getting it from library playlists
            for p in all_playlists:
                if p.get('playlistId') == playlist_id:
                    print(f"Found playlist in library: {p.get('title')}")
                    return ytmusic.get_playlist(p.get('playlistId'))
            raise Exception(f"Playlist not found in your library: {playlist_id}")
            
    except Exception as e:
        print(f"Error getting playlist details: {str(e)}")
        raise