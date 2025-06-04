import os
import logging
from app import create_app

# Configure logging for production
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create the Flask application
app = create_app()

# Log application startup
logger.info("YTune backend application initialized")

if __name__ == "__main__":
    # This block will be executed if the script is run directly
    # but not when imported by Gunicorn
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)