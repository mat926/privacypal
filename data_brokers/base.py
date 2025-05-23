# data_brokers/base.py
from fuzzywuzzy import fuzz
import logging

# Abstract base class for data brokers
class DataBroker:
    def __init__(self, name, search_url, opt_out_url):
        self.name = name
        self.search_url = search_url
        self.opt_out_url = opt_out_url

    def search(self, page, personal_info):
        """Search for personal info on the data broker's website."""
        raise NotImplementedError

    def opt_out(self, page, personal_info):
        """Complete the opt-out process on the data broker's website."""
        raise NotImplementedError

    def verify_result(self, page, personal_info):
        """Verify if search results match personal info to avoid false positives."""
        try:
            # Extract name and address from the first result (adjust selector as needed)
            result_name = page.query_selector('.result-item .name').inner_text().strip()
            result_address = page.query_selector('.result-item .address').inner_text().strip()

            # Combine first and last name for comparison
            full_name = f"{personal_info['first_name']} {personal_info['last_name']}"

            # Fuzzy matching for name and address
            name_similarity = fuzz.token_set_ratio(full_name.lower(), result_name.lower())
            address_similarity = fuzz.token_set_ratio(personal_info['address'].lower(), result_address.lower())

            # Log the verification details
            logging.info(f"Verifying {self.name}: Name similarity={name_similarity}, Address similarity={address_similarity}")

            # Consider a match if both name and address have high similarity
            return name_similarity > 90 and address_similarity > 85
        except Exception as e:
            logging.error(f"Error verifying results for {self.name}: {e}")
            return False