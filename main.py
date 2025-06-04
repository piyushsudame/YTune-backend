import os
from app import create_app
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create the Flask application
app = create_app()

if __name__ == "__main__":
    # Get port from environment variable or use default
    port = int(os.environ.get("PORT", 5000))
    
    # Determine debug mode from environment
    debug_mode = os.environ.get("FLASK_ENV", "production") == "development"
    
    logger.info(f"Starting YTune backend server on port {port}")
    logger.info(f"Debug mode: {debug_mode}")
    
    # Run the application
    app.run(
        host="0.0.0.0",  # Listen on all available interfaces
        port=port,
        debug=debug_mode
    )
