import yt_dlp
import re
from datetime import datetime, timedelta
import logging
from youtubesearchpython import VideosSearch
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class YouTubeService:
    """Service for handling YouTube search and streaming operations."""
    
    @staticmethod
    def search_song(title, artist, duration=None):
        """
        Search for a song on YouTube based on title and artist.
        
        Args:
            title (str): The song title
            artist (str): The artist name
            duration (int, optional): The expected duration in seconds
            
        Returns:
            dict: Information about the best matching video
        """
        try:
            # Create search query by combining title and artist
            query = f"{title} {artist} official audio"
            
            # Use youtubesearchpython to search for videos
            search = VideosSearch(query, limit=5)
            results = search.result()['result']
            
            if not results:
                # Try a more generic search if no results found
                query = f"{title} {artist}"
                search = VideosSearch(query, limit=5)
                results = search.result()['result']
                
                if not results:
                    return {"error": "No videos found for the given song"}
            
            # Filter and score results to find the best match
            best_match = YouTubeService._find_best_match(results, title, artist, duration)
            
            if not best_match:
                return {"error": "No suitable match found"}
                
            return {
                "video_id": best_match["id"],
                "title": best_match["title"],
                "url": f"https://www.youtube.com/watch?v={best_match['id']}",
                "thumbnail": best_match.get("thumbnails", [{}])[0].get("url", ""),
                "duration": best_match.get("duration", {})
            }
            
        except Exception as e:
            logger.error(f"Error searching for song: {str(e)}")
            return {"error": f"Error searching for song: {str(e)}"}
    
    @staticmethod
    def _find_best_match(results, title, artist, target_duration=None):
        """
        Find the best matching video from search results.
        
        Args:
            results (list): List of search results
            title (str): The song title
            artist (str): The artist name
            target_duration (int, optional): The expected duration in seconds
            
        Returns:
            dict: The best matching video information
        """
        # Convert target duration to seconds if provided
        if target_duration and isinstance(target_duration, str):
            # If it's in MM:SS format
            if ":" in target_duration:
                parts = target_duration.split(":")
                target_duration = int(parts[0]) * 60 + int(parts[1])
            else:
                target_duration = int(target_duration)
        
        # Normalize strings for comparison
        title_lower = title.lower()
        artist_lower = artist.lower()
        
        scored_results = []
        
        for video in results:
            score = 0
            video_title = video.get("title", "").lower()
            
            # Check if both title and artist are in the video title
            if title_lower in video_title and artist_lower in video_title:
                score += 10
            elif title_lower in video_title:
                score += 5
            elif artist_lower in video_title:
                score += 3
                
            # Prefer official content
            if "official" in video_title or "official" in video.get("descriptionSnippet", "").lower():
                score += 3
                
            # Prefer audio content
            if "audio" in video_title:
                score += 2
                
            # Avoid live versions, remixes, covers unless specifically requested
            if "live" in video_title and "live" not in title_lower:
                score -= 5
            if "remix" in video_title and "remix" not in title_lower:
                score -= 3
            if "cover" in video_title and "cover" not in title_lower:
                score -= 3
                
            # Check duration if target_duration is provided
            if target_duration and video.get("duration"):
                # Convert video duration to seconds
                duration_str = video.get("duration")
                if duration_str:
                    try:
                        # Handle MM:SS format
                        if ":" in duration_str:
                            parts = duration_str.split(":")
                            if len(parts) == 2:  # MM:SS
                                video_duration = int(parts[0]) * 60 + int(parts[1])
                            elif len(parts) == 3:  # HH:MM:SS
                                video_duration = int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
                            else:
                                video_duration = 0
                                
                            # Calculate duration difference and adjust score
                            duration_diff = abs(video_duration - target_duration)
                            if duration_diff < 10:  # Within 10 seconds
                                score += 5
                            elif duration_diff < 30:  # Within 30 seconds
                                score += 3
                            elif duration_diff > 120:  # More than 2 minutes difference
                                score -= 5
                    except (ValueError, IndexError):
                        pass
            
            # Check the channel/uploader
            if video.get("channel", {}).get("name", "").lower() == artist_lower:
                score += 5
                
            scored_results.append((score, video))
        
        # Sort by score (highest first)
        scored_results.sort(key=lambda x: x[0], reverse=True)
        
        # Return the highest scored result, or None if no results
        return scored_results[0][1] if scored_results else None
    
    @staticmethod
    def get_stream_url(video_id=None, youtube_url=None):
        """
        Extract direct audio stream URL from YouTube video.
        
        Args:
            video_id (str, optional): YouTube video ID
            youtube_url (str, optional): Full YouTube URL
            
        Returns:
            dict: Stream URL and expiration information
        """
        try:
            if not video_id and not youtube_url:
                return {"error": "Either video_id or youtube_url must be provided"}
                
            url = youtube_url if youtube_url else f"https://www.youtube.com/watch?v={video_id}"
            
            # Configure yt-dlp options
            ydl_opts = {
                'format': 'bestaudio/best',
                'quiet': True,
                'no_warnings': True,
                'skip_download': True,
                'noplaylist': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                if not info:
                    return {"error": "Could not extract video information"}
                
                # Get the best audio format
                formats = info.get('formats', [])
                audio_formats = [f for f in formats if f.get('acodec') != 'none' and (f.get('vcodec') == 'none' or f.get('vcodec') is None)]
                
                if not audio_formats:
                    return {"error": "No audio format found"}
                
                # Sort by quality (bitrate)
                audio_formats.sort(key=lambda x: x.get('abr', 0) if x.get('abr') else 0, reverse=True)
                best_audio = audio_formats[0]
                
                # Estimate expiration time (YouTube URLs typically expire in 6 hours)
                expires_at = (datetime.now() + timedelta(hours=6)).isoformat()
                
                return {
                    "stream_url": best_audio['url'],
                    "expires_at": expires_at,
                    "format": best_audio.get('format_note', 'unknown'),
                    "bitrate": best_audio.get('abr', 0)
                }
                
        except Exception as e:
            logger.error(f"Error getting stream URL: {str(e)}")
            return {"error": f"Error getting stream URL: {str(e)}"}
    
    @staticmethod
    def get_song_info(video_id):
        """
        Get detailed information about a YouTube video.
        
        Args:
            video_id (str): YouTube video ID
            
        Returns:
            dict: Video metadata
        """
        try:
            url = f"https://www.youtube.com/watch?v={video_id}"
            
            # Configure yt-dlp options
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'skip_download': True,
                'noplaylist': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                if not info:
                    return {"error": "Could not extract video information"}
                
                return {
                    "title": info.get('title', ''),
                    "duration": info.get('duration', 0),
                    "thumbnail": info.get('thumbnail', ''),
                    "uploader": info.get('uploader', ''),
                    "view_count": info.get('view_count', 0),
                    "upload_date": info.get('upload_date', ''),
                    "description": info.get('description', '')[:500] if info.get('description') else '',  # Truncate long descriptions
                }
                
        except Exception as e:
            logger.error(f"Error getting song info: {str(e)}")
            return {"error": f"Error getting song info: {str(e)}"}