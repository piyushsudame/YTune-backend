"""
Basic script to fetch song information using ytmusicapi library by sigma67
"""
from ytmusicapi import YTMusic
import json

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

def main():
    # Example usage
    search_query = input("Enter a song to search for: ")
    
    # Search for the song
    print(f"Searching for: {search_query}")
    results = search_song(search_query)
    
    # Display the top 5 results
    print("\nTop 5 search results:")
    for i, result in enumerate(results[:5]):
        print(f"{i+1}. {result.get('title', 'Unknown')} by {result.get('artists', [{'name': 'Unknown'}])[0]['name']}")
    
    # Ask user to select a song
    selection = int(input("\nSelect a song (1-5): ")) - 1
    if 0 <= selection < len(results[:5]):
        selected_song = results[selection]
        video_id = selected_song.get('videoId')
        
        if video_id:
            # Get detailed information about the selected song
            print(f"\nFetching details for: {selected_song.get('title')}")
            details = get_song_details(video_id)
            
            # Print formatted details
            print("\nSong Details:")
            print(f"Title: {details.get('videoDetails', {}).get('title', 'Unknown')}")
            print(f"Artist: {details.get('videoDetails', {}).get('author', 'Unknown')}")
            print(f"Video ID: {video_id}")
            print(f"Duration: {details.get('videoDetails', {}).get('lengthSeconds', 'Unknown')} seconds")
            
            # Save the full details to a JSON file
            with open('song_details.json', 'w') as f:
                json.dump(details, f, indent=4)
            print("\nFull details saved to song_details.json")
        else:
            print("Could not find video ID for the selected song.")
    else:
        print("Invalid selection.")

if __name__ == "__main__":
    main()