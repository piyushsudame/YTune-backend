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
        
        # Clean the playlist ID - remove any URL parts if present
        if playlist_id.startswith('http'):
            # Extract the ID from the URL
            import re
            match = re.search(r'list=([A-Za-z0-9_-]+)', playlist_id)
            if match:
                playlist_id = match.group(1)
        
        # For YouTube playlists (not YouTube Music playlists), we need to use a different approach
        # The singleColumnBrowseResultsRenderer error often happens with YouTube playlists
        
        # First, let's try to search for the playlist
        search_results = ytmusic.search(playlist_id, filter="playlists")
        
        # Check if we found any playlists
        if search_results and len(search_results) > 0:
            # Try each result until we find one that works
            for result in search_results:
                if 'browseId' in result:
                    try:
                        browse_id = result['browseId']
                        print(f"Trying browse ID: {browse_id}")
                        playlist = ytmusic.get_playlist(browse_id, limit=None)
                        if playlist:
                            return playlist
                    except Exception as search_e:
                        print(f"Search result attempt error: {str(search_e)}")
                        continue
        
        # If search didn't work, try direct methods
        try:
            # Try with the raw ID
            print(f"Trying with raw ID: {playlist_id}")
            playlist = ytmusic.get_playlist(playlist_id, limit=None)
            if playlist:
                return playlist
        except Exception as e:
            print(f"Raw ID attempt error: {str(e)}")
            
            # Try with the full URL format
            try:
                full_url = f'https://music.youtube.com/playlist?list={playlist_id}'
                print(f"Trying with full URL: {full_url}")
                playlist = ytmusic.get_playlist(full_url, limit=None)
                if playlist:
                    return playlist
            except Exception as url_e:
                print(f"Full URL attempt error: {str(url_e)}")
                
                # Try with VL prefix (sometimes needed for public playlists)
                try:
                    if not playlist_id.startswith('VL'):
                        vl_id = f'VL{playlist_id}'
                        print(f"Trying with VL prefix: {vl_id}")
                        playlist = ytmusic.get_playlist(vl_id, limit=None)
                        if playlist:
                            return playlist
                except Exception as vl_e:
                    print(f"VL prefix attempt error: {str(vl_e)}")
                    
                    # Last resort - try to use a different method to get the playlist
                    try:
                        # Try to get the playlist using the YouTube API directly
                        # This is a workaround for the singleColumnBrowseResultsRenderer error
                        from ytmusicapi.parsers.browsing import parse_playlist_items
                        
                        # Get the library playlists to check if this is one of them
                        library_playlists = ytmusic.get_library_playlists(limit=50)
                        for lib_playlist in library_playlists:
                            if lib_playlist.get('playlistId') == playlist_id:
                                return ytmusic.get_playlist(lib_playlist.get('browseId'), limit=None)
                        
                        raise Exception("Playlist not found in library")
                    except Exception as direct_e:
                        print(f"Direct API attempt error: {str(direct_e)}")
                        raise Exception(f"Playlist not found or is not accessible. ID: {playlist_id}")
            
    except Exception as e:
        print(f"Error getting playlist details: {str(e)}")
        raise