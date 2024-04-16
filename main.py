# Imports
from database import DB
import logging
import flask
import os

# Metadata
__version__ = 'v0.1-dev'
__author__ = 'N3RDIUM'

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Update notifier
try:
    import requests 
    latest = requests.get('https://raw.githubusercontent.com/N3RDIUM/TimeGrid/main/latest-version').text
    if __version__ != latest:
        logging.warning(f'An update is available! Please run `git pull`. (Your version: {__version__}) (Latest version: {latest})')
    else:
        logging.info(f'TimeGrid is already at the latest version. Great!')
except Exception as e:
    logging.warning(f"Failed to check for updates due to error: \"{e}\". The application will start normally anyway.")

# Production / Development
with open('mode', 'r') as f:
    PRODUCTION = f.read().split('\n')[1] == "PRODUCTION"
    
if not PRODUCTION:
    logging.warn("Running in development mode! Please edit the mode file.")
else:
    logging.info("Running in production mode!")

# If you change this, make sure you change it at the end of .gitignore too.
DB_PATH = os.path.abspath('./db/')

# Create the dirs if they don't exist
os.makedirs(DB_PATH, exist_ok=True)
os.makedirs(os.path.join(DB_PATH, 'teachers'), exist_ok=True)
os.makedirs(os.path.join(DB_PATH, 'classes'), exist_ok=True)
os.makedirs(os.path.join(DB_PATH, 'bkp'), exist_ok=True)

# Create the app
app = flask.Flask(__name__)

# Driver code
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=not PRODUCTION)
