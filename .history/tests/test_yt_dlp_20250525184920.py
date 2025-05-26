import unittest
from app import create_app
import json
import os
import tempfile

class TestYTDlpRoutes(unittest.TestCase):
    def setUp(self):
        """Set up test client and other test variables"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        # Test video ID (using a short, reliable video)
        self.test_video_id = "dQw4w9WgXcQ"  # Rick Astley - Never Gonna Give You Up
        
    def test_get_video_info(self):
        """Test the /info/<video_id> endpoint"""
        response = self.client.get(f'/api/ytdlp/info/{self.test_video_id}')
        data = json.loads(response.data)
        
        # Check if response is successful
        self.assertEqual(response.status_code, 200)
        
        # Check if essential fields are present
        self.assertIn('title', data)
        self.assertIn('duration', data)
        self.assertIn('formats', data)
        
    def test_stream_audio(self):
        """Test the /stream/<video_id> endpoint"""
        response = self.client.get(f'/api/ytdlp/stream/{self.test_video_id}')
        data = json.loads(response.data)
        
        # Check if response is successful
        self.assertEqual(response.status_code, 200)
        
        # Check if essential fields are present
        self.assertIn('url', data)
        self.assertIn('title', data)
        self.assertIn('duration', data)
        self.assertIn('thumbnail', data)
        
        # Check if URL is valid
        self.assertTrue(data['url'].startswith('http'))
        
    def test_download_audio(self):
        """Test the /download/<video_id> endpoint"""
        response = self.client.get(f'/api/ytdlp/download/{self.test_video_id}')
        
        # Check if response is successful
        self.assertEqual(response.status_code, 200)
        
        # Check if response has correct headers
        self.assertEqual(response.mimetype, 'audio/mpeg')
        self.assertIn('Content-Disposition', response.headers)
        self.assertTrue(response.headers['Content-Disposition'].startswith('attachment; filename='))
        
        # Check if response has content
        self.assertTrue(len(response.data) > 0)
        
    def test_invalid_video_id(self):
        """Test behavior with invalid video ID"""
        invalid_id = "invalid_video_id"
        
        # Test info endpoint
        response = self.client.get(f'/api/ytdlp/info/{invalid_id}')
        self.assertEqual(response.status_code, 500)
        
        # Test stream endpoint
        response = self.client.get(f'/api/ytdlp/stream/{invalid_id}')
        self.assertEqual(response.status_code, 500)
        
        # Test download endpoint
        response = self.client.get(f'/api/ytdlp/download/{invalid_id}')
        self.assertEqual(response.status_code, 500)

if __name__ == '__main__':
    unittest.main() 