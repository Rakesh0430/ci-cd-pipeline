import os
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler

# Load environment variables
load_dotenv()

# Set up logging
LOG_DIR = os.getenv("LOG_DIR", "logs")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
MAX_LOG_FILE_SIZE = int(os.getenv("MAX_LOG_FILE_SIZE", 5 * 1024 * 1024))
BACKUP_LOG_COUNT = int(os.getenv("BACKUP_LOG_COUNT", 5))

app = Flask(__name__)

# Configure logging
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

log_file_path = os.path.join(LOG_DIR, "app.log")
handler = RotatingFileHandler(log_file_path, maxBytes=MAX_LOG_FILE_SIZE, backupCount=BACKUP_LOG_COUNT)
logging.basicConfig(handlers=[handler], level=LOG_LEVEL, format='[%(asctime)s] %(levelname)s: %(message)s')
logger = logging.getLogger("FinanceAppLogger")

@app.route('/')
def serve_index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/api/log_operation', methods=['POST'])
def log_operation():
    data = request.json
    operation = data.get('operation')
    amount = data.get('amount')
    
    logger.info(f"Operation: {operation}, Amount: {amount}")
    
    return jsonify({"message": "Operation logged successfully!"}), 200

if __name__ == "__main__":
    app.run(debug=True)
