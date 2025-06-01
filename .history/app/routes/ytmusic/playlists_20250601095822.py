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
        
        # Try to get the playlist directly with the clean ID
        try:
            playlist = ytmusic.get_playlist(playlist_id, limit=None)
            if not playlist:
                raise Exception("Playlist not found")
            return playlist
        except Exception as e:
            print(f"First attempt error: {str(e)}")
            
            # If the first attempt fails, try with the full URL format
            try:
                full_url = f'https://music.youtube.com/playlist?list={playlist_id}'
                playlist = ytmusic.get_playlist(full_url, limit=None)
                if not playlist:
                    raise Exception("Playlist not found")
                return playlist
            except Exception as inner_e:
                print(f"Second attempt error: {str(inner_e)}")
                
                # One more attempt with VL prefix (sometimes needed for public playlists)
                try:
                    if not playlist_id.startswith('VL'):
                        vl_id = f'VL{playlist_id}'
                        playlist = ytmusic.get_playlist(vl_id, limit=None)
                        if not playlist:
                            raise Exception("Playlist not found")
                        return playlist
                    raise Exception("All attempts failed")
                except Exception as vl_e:
                    print(f"Third attempt error: {str(vl_e)}")
                    raise Exception(f"Playlist not found or is not accessible. ID: {playlist_id}")
            
    except Exception as e:
        print(f"Error getting playlist details: {str(e)}")
        raise