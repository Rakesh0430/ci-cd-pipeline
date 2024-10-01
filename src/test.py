import logging
import os
import shutil
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Constants for logging
LOG_DIR = os.getenv("LOG_DIR", "logs")  # Log directory from environment variable or default to "logs"
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

# Function to get log file name
def get_log_file_name():
    return f"log_{TIMESTAMP}.log"

LOG_FILE_NAME = get_log_file_name()

# Clean up previous logs if they exist
if os.path.exists(LOG_DIR):
    shutil.rmtree(LOG_DIR)

# Create log directory
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE_NAME)

# Configure logging
logging.basicConfig(
    filename=LOG_FILE_PATH,
    filemode="w",
    format='[%(asctime)s] \t%(levelname)s \t%(lineno)d \t%(filename)s \t%(funcName)s() \t%(message)s',
    level=logging.INFO
)

logger = logging.getLogger("FinanceComplaint")

class FinanceException(Exception):
    """Custom exception for finance-related errors."""
    
    def __init__(self, error_message: Exception, error_detail: sys, error_code: int = 1000):
        super().__init__(error_message)
        self.error_message = self.get_detailed_error_message(
            error_message=error_message,
            error_detail=error_detail,
            error_code=error_code
        )

    @staticmethod
    def get_detailed_error_message(error_message: Exception, error_detail: sys, error_code: int) -> str:
        """Formats a detailed error message with file name, line number, and a unique error code."""
        _, _, exec_tb = error_detail.exc_info()  # Get traceback object
        line_number = exec_tb.tb_lineno  # Get line number of the error
        file_name = exec_tb.tb_frame.f_code.co_filename  # Get the file where the error occurred

        # Format the error message with detailed information
        detailed_message = (
            f"Error Code: [{error_code}] "
            f"Error occurred in script: [{file_name}] "
            f"at line number: [{line_number}] "
            f"error message: [{error_message}]"
        )
        return detailed_message

    def __str__(self):
        return self.error_message

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.error_message}')"


class FinanceProcessor:
    """Class to process financial transactions."""

    def __init__(self, initial_balance: float):
        self.balance = initial_balance

    def process_transaction(self, withdrawal_amount: float) -> float:
        """Process a financial transaction (withdrawal)."""
        try:
            if withdrawal_amount > self.balance:
                raise ValueError("Insufficient funds for the withdrawal")  # Custom error if balance is insufficient
            
            # Process the transaction
            self.balance -= withdrawal_amount
            logger.info(f"Transaction successful! New balance: {self.balance}")
            return self.balance

        except Exception as e:
            # Raise the custom FinanceException with detailed error information
            raise FinanceException(e, sys)


def main():
    """Main function to execute the finance processing."""
    initial_balance = float(os.getenv("INITIAL_BALANCE", 500.0))  # Get initial balance from environment variable
    withdrawal_amount = float(os.getenv("WITHDRAWAL_AMOUNT", 600.0))  # Get withdrawal amount from environment variable

    finance_processor = FinanceProcessor(initial_balance)

    try:
        logger.info(f"Attempting to withdraw {withdrawal_amount} from an account balance of {initial_balance}.")
        finance_processor.process_transaction(withdrawal_amount)

    except FinanceException as fe:
        # Log the error details to the log file
        logger.error(fe)
        
        # Catch and print the detailed FinanceException
        print(f"Handled FinanceException: {fe}")

    finally:
        logger.info("Transaction processing completed.")


if __name__ == "__main__":
    main()
