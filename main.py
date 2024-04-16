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
    latest = requests.get('https://raw.githubusercontent.com/N3RDIUM/TimeGrid/main/.latest-version', timeout=1).text
    if __version__ != latest:
        logging.warning(f'An update is available! Please run `git pull`. (Your version: {__version__}) (Latest version: {latest})')
    else:
        logging.info(f'TimeGrid is already at the latest version. Great!')
except Exception as e:
    logging.warning(f"Failed to check for updates due to error: \"{e}\". The application will start normally anyway.")

# Production / Development
with open('.mode', 'r') as f:
    PRODUCTION = f.read().split('\n')[1] == "PRODUCTION"
    
if not PRODUCTION:
    logging.warn("Running in development mode! Please edit the .mode file if you are an end-user.")
else:
    logging.info("Running in production mode!")

# If you change this, make sure you change it at the end of .gitignore too.
DB_PATH = os.path.abspath('./db/')

# Database init
db = DB(DB_PATH)

# Create the dirs if they don't exist
os.makedirs(DB_PATH, exist_ok=True)
os.makedirs(os.path.join(DB_PATH, 'teachers'), exist_ok=True)
os.makedirs(os.path.join(DB_PATH, 'classes'), exist_ok=True)
os.makedirs(os.path.join(DB_PATH, 'bkp'), exist_ok=True)

# Create the app
app = flask.Flask(__name__)

@app.route('/')
def index():
    return "[Server Online]"


@app.route('/teachers')
def teachers():
    return flask.jsonify(list(db.teachers.keys()))

@app.route('/new-teacher', methods=['POST'])
def new_teacher():
    data = flask.request.get_json()
    id = data['id']
    del data['id']
    db.new_teacher(id, data)
    return 'OK'

@app.route('/update-teacher', methods=['POST'])
def update_teacher():
    data = flask.request.get_json()
    id = data['id']
    del data['id']
    db.update_teacher(id, data)
    return 'OK'

@app.route('/get-teacher', methods=['POST'])
def get_teacher():
    data = flask.request.get_json()
    return flask.jsonify(db.teachers[data['id']])

@app.route('/classes')
def classes():
    return flask.jsonify(list(db.classes.keys()))

@app.route('/new-class', methods=['POST'])
def new_class():
    data = flask.request.get_json()
    id = data['id']
    del data['id']
    db.new_class(id, data)
    return 'OK'

@app.route('/update-class', methods=['POST'])
def update_class():
    data = flask.request.get_json()
    id = data['id']
    del data['id']
    db.update_class(id, data)
    return 'OK'

# Driver code
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=not PRODUCTION)
