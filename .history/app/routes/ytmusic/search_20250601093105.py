from ytmusicapi import YTMusic

def search_song(query):
    """
    Search for a song on YouTube Music
    
    Args:
        query (str): The search query (e.g., "Oasis Wonderwall")
        
    Returns:
        list: Search results
    """
    ytmusic = YTMusic()
    search_results = ytmusic.search(query, filter="songs")
    return search_results

def get_top_song_video_id(query):
    """
    Get the top song's videoId from a query.
    
    Args:
        query (str): The search query
        
    Returns:
        str: Video ID of the top result, or None if not found
    """
    ytmusic = YTMusic()
    results = ytmusic.search(query, filter="songs")
    
    if results and 'videoId' in results[0]:
        return results[0]['videoId']
    return None 