import logging
import os

# Create logs folder if not exists
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/system.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_info(message: str):
    logging.info(message)

def log_error(message: str):
    logging.error(message)