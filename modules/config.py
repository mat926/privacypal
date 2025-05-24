# config.py
import yaml
from modules import util

logger = util.logger

class Config:
    def __init__(self, config_path='config.yaml'):
        """Initialize the Config class by loading and validating the YAML config file."""
        self.config = self._load_config(config_path)
        self._validate_config()

    def _load_config(self, config_path):
        """Load the YAML configuration file."""
        try:
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            logger.error(f"Config file '{config_path}' not found.")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Error parsing config file: {e}")
            print(f"Error parsing config file: {e}")
            raise

    def _validate_config(self):
        """Validate the structure and required fields of the config file."""
        if not self.config:
            raise ValueError("Config file is empty or invalid")

        # Validate names section
        if 'names' not in self.config or not isinstance(self.config['names'], list):
            raise ValueError("Config file must contain a 'names' section with a list of names")
        for name in self.config['names']:
            if not all(key in name for key in ['first_name', 'last_name']):
                raise ValueError("Each entry in 'names' must contain 'first_name' and 'last_name'")

        # Validate addresses section
        if 'addresses' not in self.config or not isinstance(self.config['addresses'], list):
            raise ValueError("Config file must contain an 'addresses' section with a list of addresses")
        for address in self.config['addresses']:
            if not all(key in address for key in ['street', 'city', 'state', 'zip']):
                raise ValueError("Each entry in 'addresses' must contain 'street', 'city', 'state', and 'zip'")

        # Validate emails section
        if 'emails' not in self.config or not isinstance(self.config['emails'], list):
            raise ValueError("Config file must contain an 'emails' section with a list of emails")
        for email in self.config['emails']:
            if not isinstance(email, str):
                raise ValueError("Each entry in 'emails' must be a string")

    # def get_primary_info(self):
    #     """Return the primary personal info as a dictionary."""
    #     return {
    #         'first_name': self.config['primary_name']['first_name'],
    #         'last_name': self.config['primary_name']['last_name'],
    #         'address': self.config['primary_name']['address']
    #     }

    # def get_all_names(self):
    #     """Return a list of tuples containing all names to search (primary + variations + relatives)."""
    #     all_names = []
    #     for name in self.config['names']:
    #         all_names.append((name['first_name'], name['last_name']))
    #     return all_names