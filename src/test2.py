import logging
import os
import shutil
from logging.handlers import RotatingFileHandler
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Constants for logging
LOG_DIR = os.getenv("LOG_DIR", "logs")  # Log directory from environment variable or default to "logs"
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

def get_log_file_name():
    """Generate the log file name based on the current timestamp."""
    return f"log_{TIMESTAMP}.log"

LOG_FILE_NAME = get_log_file_name()
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE_NAME)

# Clean up previous logs if they exist
if os.path.exists(LOG_DIR):
    shutil.rmtree(LOG_DIR)

# Create log directory
os.makedirs(LOG_DIR, exist_ok=True)

# Configure logging
try:
    # Create a rotating file handler
    handler = RotatingFileHandler(
        LOG_FILE_PATH,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=5,              # Keep last 5 log files
        encoding='utf-8'
    )

    # Set up logging format
    formatter = logging.Formatter(
        '[%(asctime)s] \t%(levelname)s \t%(lineno)d \t%(filename)s \t%(funcName)s() \t%(message)s'
    )
    handler.setFormatter(formatter)

    # Get the logger and set the level
    logger = logging.getLogger("FinanceComplaint")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    logger.info("Logging is configured successfully.")
except Exception as e:
    print(f"Failed to configure logging: {e}")

# Example function to log finance-related operations
def log_finance_operation(operation, amount):
    """Log a finance operation."""
    logger.info(f"Operation: {operation}, Amount: {amount}")

# Example usage
if __name__ == "__main__":
    log_finance_operation("Deposit", 1000)
    log_finance_operation("Withdrawal", 500)
