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

    def _parse_search_results(self, page):
        """Parse the search results from the current page and return structured data, trying multiple selectors."""
        results = []
        # Try multiple possible selectors for result items, including class contains 'serp-card'
        selectors = [".serp-card.hide-scrollbar"]
        result_items = []
        for selector in selectors:
            items = page.query_selector_all(selector)
            if items:
                result_items.extend(items)
        seen = set()
        for item in result_items:
            try:
                name = ''
                address = ''
                phone = ''
                # Try multiple selectors for each field
                for name_sel in ["[class*='name-link-text']"]:
                    el = item.query_selector(name_sel)
                    if el:
                        name = el.evaluate("el => el.textContent.trim()") #workaround
                        break
                for addr_sel in ['.person-location']:
                    el = item.query_selector(addr_sel)
                    if el:
                        address = el.evaluate("el => el.textContent.trim()") #workaround
                        break
                # for phone_sel in ['.phone', '.person-phone', '.phone-number', '.card-phone']:
                #     el = item.query_selector(phone_sel)
                #     if el:
                #         phone = el.inner_text().strip()
                #         break
                # Avoid duplicates
                key = (name, address, phone)
                if key not in seen:
                    results.append({'name': name, 'address': address, 'phone': phone})
                    seen.add(key)
            except AttributeError as e:
                print(f"Error parsing result: {e}")
        return results

    def search(self, page, personal_info):
        """Search for info on Whitepages and return structured results."""
        print(f"Searching {self.name} for {personal_info['first_name']} {personal_info['last_name']}")
        page.goto(self.search_url)
        page.fill('#search-address', f"{personal_info['first_name']} {personal_info['last_name']}")
        page.click('button[type="submit"]')
        time.sleep(5)  # Wait for results to load
        return self._parse_search_results(page)


    def opt_out(self, page, personal_info):
        """Submit opt-out request on Whitepages."""
        print(f"Opting out from {self.name} for {personal_info['first_name']} {personal_info['last_name']}")
        page.goto(self.opt_out_url)
        page.fill('input[name="name"]', f"{personal_info['first_name']} {personal_info['last_name']}")
        page.fill('input[name="address"]', personal_info['address'])
        page.click('button[type="submit"]')
        time.sleep(5)  # Wait for submission to process