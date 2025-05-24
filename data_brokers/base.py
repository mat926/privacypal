# data_brokers/base.py
import re
from fuzzywuzzy import fuzz
from modules import util

logger = util.logger

# Abstract base class for data brokers
class DataBroker:
    def __init__(self, name, search_url, opt_out_url):
        self.name = name
        self.search_url = search_url
        self.opt_out_url = opt_out_url

        # Add a filter to automatically include the databroker field in all log messages
        #logger.addFilter(lambda record: setattr(record, 'databroker', self.name) or True)

    def search(self, page, personal_info):
        """Search for personal info on the data broker's website."""
        raise NotImplementedError

    def opt_out(self, page, personal_info):
        """Complete the opt-out process on the data broker's website."""
        raise NotImplementedError

    def verify_results(self, search_results, name, config):
        """Verify if search results match personal info to avoid false positives."""
        logger.info("Verifying search results")



        for result in search_results:
            # Check if the name in the result matches any name in the config names
            is_name_match = self.check_name_match(result, name)
            is_address_match = self.check_address_match(result, config)
            # is_email_match = self.check_email_match(search_results, config)
            if is_name_match and is_address_match:
                logger.info("Result: %s", result)


        logger.info("No matches found in search results")
        return False
    
    def check_name_match(self, search_result, name):
        """Check if the name in the result matches any name in the config names."""
        #TODO handle middle names/initials

        # Check if the name in the result matches the config names
        result_name = search_result['name']
        if name['first_name'] in result_name and name['last_name'] in result_name:
            # Check if the middle name or initial is in the result name
            if 'middle_name' in name:
                middle_initial = name['middle_name'][0]  # Infer middle initial
                # Use regex to check if the middle initial is a whole word
                if name['middle_name'] in result_name or re.search(rf'\b{middle_initial}\b', result_name):
                    return True
            else:
                # If no middle name or initial is provided, just check first and last names
                return True
        return False
        

    def check_address_match(self, search_result, config):
        """Check if the address in the result matches any address in the config addresses."""
        # Load addresses and related names from the config
        address_list = config.get('addresses', [])

        # Check if any address in the result matches the config addresses
        result_addresses = search_result.get('addresses', [])
        for result_address in result_addresses:
            if self.is_state_match(result_address, address_list) and self.is_city_match(result_address, address_list):
                return True
        return False


    def is_state_match(self, result_address, config_addresses):
        """Check if the state in the result address matches any state in the config addresses."""
        for address in config_addresses:
            if address['state'] in result_address:
                return True
        return False
    
    def is_city_match(self, result_address, config_addresses):
        """Check if the city in the result address matches any city in the config addresses."""
        for address in config_addresses:
            if address['city'] in result_address:
                return True
        return False
