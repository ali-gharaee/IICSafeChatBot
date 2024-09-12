import logging
import configparser
import os

# Load configuration from the properties file
config = configparser.ConfigParser(interpolation=None)  # Disable interpolation to prevent issues with '%'
config_file_path = os.path.join(os.path.dirname(__file__), '../config/logging_config.properties')

if not os.path.exists(config_file_path):
    raise FileNotFoundError(f"Configuration file not found: {config_file_path}")

config.read(config_file_path)

# Print available sections for debugging
print(f"Available sections: {config.sections()}")

# Get logging configuration from config file
log_file = config.get('logging_config', 'log_file')
log_mode = config.get('logging_config', 'log_mode')
log_format = config.get('logging_config', 'log_format')
log_level = config.get('logging_config', 'log_level').upper()
log_datefmt = config.get('logging_config', 'log_datefmt')

# Map log level strings to logging module levels
log_level_map = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

# Configure logging
logging.basicConfig(
    filename=log_file,
    filemode=log_mode,
    format=log_format,
    level=log_level_map.get(log_level, logging.INFO),  # Default to INFO if invalid level
    datefmt=log_datefmt
)

logging.info("Logging configuration successfully initialized.")
