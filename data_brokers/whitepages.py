# data_brokers/whitepages.py
from .base import DataBroker
import time

class WhitepagesDataBroker(DataBroker):
    def __init__(self):
        super().__init__(
            name='Whitepages',
            search_url='https://www.whitepages.com/name',
            opt_out_url='https://www.whitepages.com/suppression_requests'
        )

    def search(self, page, personal_info):
        """Search for info on Whitepages."""
        print(f"Searching {self.name} for {personal_info['first_name']} {personal_info['last_name']}")
        page.goto(self.search_url)
        page.fill('input[name="first_name"]', personal_info['first_name'])
        page.fill('input[name="last_name"]', personal_info['last_name'])
        page.fill('input[name="address"]', personal_info['address'])
        page.click('button[type="submit"]')
        time.sleep(5)  # Wait for results to load
        return page.query_selector('.result-item') is not None

    def opt_out(self, page, personal_info):
        """Submit opt-out request on Whitepages."""
        print(f"Opting out from {self.name} for {personal_info['first_name']} {personal_info['last_name']}")
        page.goto(self.opt_out_url)
        page.fill('input[name="name"]', f"{personal_info['first_name']} {personal_info['last_name']}")
        page.fill('input[name="address"]', personal_info['address'])
        page.click('button[type="submit"]')
        time.sleep(5)  # Wait for submission to process