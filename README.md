# YTune Backend

A Flask backend for YTune, a music streaming application that uses yt-dlp to stream songs from YouTube.

## Features

- Search for songs on YouTube using title and artist information
- Extract direct audio stream URLs from YouTube videos
- Get detailed metadata about YouTube videos
- Smart search algorithm to find the best match for Spotify tracks
- Audio-only streaming for efficient bandwidth usage

## Setup

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the development server:
   ```
   python main.py
   ```

## API Endpoints

### Search Song

- `POST /api/search-song` - Search for a song on YouTube based on title and artist
  ```json
  {
    "title": "song name",
    "artist": "artist name",
    "duration": 180  // optional, in seconds
  }
  ```
  Response:
  ```json
  {
    "video_id": "xyz",
    "title": "full title",
    "url": "youtube_url",
    "thumbnail": "thumbnail_url"
  }
  ```

### Get Stream URL

- `POST /api/get-stream-url` - Extract direct audio stream URL from YouTube video
  ```json
  {
    "video_id": "xyz"  // OR
    "youtube_url": "full_url"
  }
  ```
  Response:
  ```json
  {
    "stream_url": "direct_audio_url",
    "expires_at": "timestamp",
    "format": "audio format",
    "bitrate": 128
  }
  ```

### Get Song Info

- `GET /api/song-info/{video_id}` - Get metadata about a YouTube video
  
  Response:
  ```json
  {
    "title": "video title",
    "duration": 180,
    "thumbnail": "thumbnail_url",
    "uploader": "channel name",
    "view_count": 12345,
    "upload_date": "20240101",
    "description": "video description"
  }
  ```

### Health Check

- `GET /ping` - Check if the API is running
  
  Response:
  ```json
  {
    "status": "ok"
  }
  ```

## Deployment

This project is configured for deployment on Render. The `render.yaml` file contains the necessary configuration.

## Dependencies

- Flask - Web framework
- Flask-CORS - Cross-Origin Resource Sharing
- yt-dlp - YouTube downloader and metadata extractor
- youtube-search-python - YouTube search API
- gunicorn - WSGI HTTP Server
- python-dotenv - Environment variable management
- requests - HTTP client library

## Integration with Next.js Frontend

This backend is designed to work with a Next.js frontend that fetches user's Spotify data. The frontend can use these API endpoints to:

1. Search for YouTube equivalents of Spotify tracks
2. Get direct audio stream URLs for playback
3. Retrieve metadata for display in the UI

## Error Handling

All endpoints return consistent JSON responses with appropriate HTTP status codes:

- 200: Success
- 400: Bad request (missing parameters)
- 404: Resource not found
- 500: Server error

Error responses include an "error" field with a descriptive message.