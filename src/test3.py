import logging
import os
import shutil
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from datetime import datetime

class LoggerConfig:
    def __init__(self, log_dir='logs', log_level='INFO', max_log_file_size=5 * 1024 * 1024, backup_log_count=5):
        self.log_dir = log_dir
        self.log_level = log_level
        self.max_log_file_size = max_log_file_size
        self.backup_log_count = backup_log_count
        self.logger = self.configure_logging()

    def setup_log_directory(self):
        """Create a log directory."""
        try:
            if os.path.exists(self.log_dir):
                shutil.rmtree(self.log_dir)  # Remove the existing log directory and its contents
            os.makedirs(self.log_dir, exist_ok=True)  # Create the log directory
        except Exception as e:
            logging.error(f"Failed to create log directory: {e}")

    def configure_logging(self):
        """Configure the logging settings."""
        self.setup_log_directory()  # Setup the log directory

        # Log file name with a timestamp
        log_file_name = f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        log_file_path = os.path.join(self.log_dir, log_file_name)

        # Create a rotating file handler
        handler = RotatingFileHandler(
            log_file_path,
            maxBytes=self.max_log_file_size,
            backupCount=self.backup_log_count,
            encoding='utf-8'
        )

        # Set up logging format
        formatter = logging.Formatter(
            '[%(asctime)s] \t%(levelname)s \t%(lineno)d \t%(filename)s \t%(funcName)s() \t%(message)s'
        )
        handler.setFormatter(formatter)

        # Create and configure logger
        logger = logging.getLogger("FinanceAppLogger")
        logger.setLevel(self.log_level)
        logger.addHandler(handler)

        return logger

    def log_finance_operation(self, operation, amount):
        """Log a finance operation."""
        self.logger.info(f"Operation: {operation}, Amount: {amount}")

class EnvironmentConfig:
    @staticmethod
    def load_environment_variables():
        """Load environment variables from the .env file."""
        load_dotenv()

    @staticmethod
    def get_logging_configuration():
        """Get logging configuration from environment variables."""
        log_dir = os.getenv("LOG_DIR", "logs")
        log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        max_log_file_size = int(os.getenv("MAX_LOG_FILE_SIZE", 5 * 1024 * 1024))
        backup_log_count = int(os.getenv("BACKUP_LOG_COUNT", 5))
        return log_dir, log_level, max_log_file_size, backup_log_count

# Main application logic
if __name__ == "__main__":
    # Load environment variables
    EnvironmentConfig.load_environment_variables()

    # Get logging configuration
    log_dir, log_level, max_log_file_size, backup_log_count = EnvironmentConfig.get_logging_configuration()

    # Create a logger configuration instance
    logger_config = LoggerConfig(log_dir, log_level, max_log_file_size, backup_log_count)
    logger_config.logger.info("Application started.")

    # Example logging operations
    logger_config.log_finance_operation("Deposit", 1000)
    logger_config.log_finance_operation("Withdrawal", 500)

    logger_config.logger.info("Application finished.")
