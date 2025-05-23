import logging
import sys

# Create a shared logger instance
logger = logging.getLogger("PrivacyPal")
logger.setLevel(logging.INFO)

# Formatter for log messages
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# File handler
file_handler = logging.FileHandler('privacypal.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Stream handler for stdout
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# Add a filter to automatically include the databroker field in all log messages
#logger.addFilter(lambda record: setattr(record, 'databroker', 'Main') or True)