# YTune Backend

A Flask backend for YTune, a music streaming application that uses ytmusicapi to fetch playlist and account data and yt-dlp to stream songs.

## Features

- Search for songs, albums, artists, and playlists using YouTube Music API
- Fetch playlist details and user library data
- Stream audio from YouTube videos
- Download audio files
- Authentication with YouTube Music

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

### YTMusic API

- `GET /api/ytmusic/search?q=<query>&filter=<filter>&limit=<limit>` - Search YouTube Music
- `GET /api/ytmusic/playlist/<playlist_id>` - Get playlist details
- `GET /api/ytmusic/song/<song_id>` - Get song details
- `GET /api/ytmusic/library/playlists` - Get user's library playlists
- `POST /api/ytmusic/auth/setup` - Setup authentication

### YT-DLP API

- `GET /api/ytdlp/info/<video_id>` - Get video information
- `GET /api/ytdlp/stream/<video_id>` - Stream audio from a video
- `GET /api/ytdlp/download/<video_id>` - Download audio from a video

## Authentication

To use authenticated features, you need to set up authentication with YouTube Music:

1. OAuth Authentication (Recommended):
   ```
   curl -X POST http://localhost:5000/api/ytmusic/auth/setup -H "Content-Type: application/json" -d '{"oauth": true}'
   ```
   Follow the instructions to complete the OAuth flow.

2. Manual Headers Authentication:
   ```
   curl -X POST http://localhost:5000/api/ytmusic/auth/setup -H "Content-Type: application/json" -d '{"headers": {...}}'
   ```
   Replace `{...}` with your YouTube Music request headers.

## Deployment

This project is configured for deployment on Render. The `render.yaml` file contains the necessary configuration.

## Dependencies

- Flask - Web framework
- Flask-CORS - Cross-Origin Resource Sharing
- ytmusicapi - YouTube Music API client
- yt-dlp - YouTube downloader
- gunicorn - WSGI HTTP Server
- python-dotenv - Environment variable management