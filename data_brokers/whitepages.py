# data_brokers/whitepages.py
from .base import DataBroker
from modules.util import logger
import time

# Set up a logger for the WhitepagesDataBroker class
#logger = MyLogger('whitepages_logger', 'whitepages.log')



class WhitepagesDataBroker(DataBroker):
    def __init__(self):
        super().__init__(
            name='Whitepages',
            search_url='https://www.whitepages.com/name',
            opt_out_url='https://www.whitepages.com/suppression_requests'
        )

    def _parse_search_results(self, page):
        """Parse the search results from the current page and return structured data, trying multiple selectors."""
        logger.info("Parsing search results")
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
                addresses = []
                age = ''
                may_go_by = []
                related_to = []
                email = ''
                phone = ''
                work = ''
                link = ''

                # Try multiple selectors for each field
                for name_sel in ["[class*='name-link-text']"]:
                    el = item.query_selector(name_sel)
                    if el:
                        name = el.evaluate("el => el.textContent.trim()") #workaround
                        break
                for addr_sel in ['.locations-list']:
                    el = item.query_selector(addr_sel)
                    if el:
                        address_txt = el.evaluate("el => el.textContent.trim()") #workaround
                        cleaned_address_txt = address_txt.replace('\xa0', '').replace('•', '')
                        addresses = [location.strip() for location in cleaned_address_txt.split('  ') if location.strip()]
                        break
                for mgb_sel in ['.aka-list']:
                    el = item.query_selector(mgb_sel)
                    if el:
                        mgb_txt = el.evaluate("el => el.textContent.trim()") #workaround
                        cleaned_mgb_txt = mgb_txt.replace('\xa0', '').replace('•', '')
                        may_go_by = [location.strip() for location in cleaned_mgb_txt.split('  ') if location.strip()]
                        break

                for email_sel in [".family-title:has-text('email')"]:
                    el = item.query_selector(email_sel)
                    if el:
                        next_sibling = el.query_selector("xpath=following-sibling::*[1]")
                        if next_sibling:
                            # Get the text content of the next sibling
                            email = next_sibling.evaluate("el => el.textContent.trim()")
                            break
                      
 
                for relatedto_sel in [".family-title:has-text('Related To')"]:
                    el = item.query_selector(relatedto_sel)
                    if el:
                        next_sibling = el.query_selector("xpath=following-sibling::*[1]")
                        if next_sibling:
                            # Get the text content of the next sibling
                            related_to_txt = next_sibling.evaluate("el => el.textContent.trim()")
                            cleaned_relatedto_txt = related_to_txt.replace('\xa0', '').replace('•', '')
                            related_to = [location.strip() for location in cleaned_relatedto_txt.split('  ') if location.strip()]
                            break
                
                for phone_sel in [".family-title:has-text('Phone Number')"]:
                    el = item.query_selector(phone_sel)
                    if el:
                        next_sibling = el.query_selector("xpath=following-sibling::*[1]")
                        if next_sibling:
                            # Get the text content of the next sibling
                            phone = next_sibling.evaluate("el => el.textContent.trim()")
                            break

                for age_sel in [".person-age"]:
                    el = item.query_selector(age_sel)
                    if el:
                        # Get the text content of the next sibling
                        age = el.evaluate("el => el.textContent.trim()")
                        break

                for work_sel in [".job-title"]:
                    el = item.query_selector(work_sel)
                    if el:
                        # Get the text content of the next sibling
                        work = el.evaluate("el => el.textContent.trim()")
                        break

                link = f"https://www.whitepages.com{item.evaluate("el => el.getAttribute('href')")}"


                # Avoid duplicates
                # key = (name, tuple(addresses), age, tuple(may_go_by), tuple(related_to), email, phone, work)
                # if key not in seen:
                results.append({'name': name, 
                                'addresses': addresses, 
                                'age': age, 
                                'may_go_by': may_go_by, 
                                'related_to': related_to, 
                                'email': email, 
                                'phone': phone, 
                                'work': work,
                                'link': link})
                    # seen.add(key)
            except AttributeError as e:
                print(f"Error parsing result: {e}")
        logger.info("Parsed %d results", len(results))
        return results

    def search(self, page, personal_info):
        """Search for info on Whitepages and return structured results."""
        #print(f"Searching {self.name} for {personal_info['first_name']} {personal_info['last_name']}")
        logger.info("Searching for %s %s %s", personal_info['first_name'], personal_info.get('middle_name','') , personal_info['last_name'])
        page.goto(self.search_url)
        page.fill('#search-address', f"{personal_info['first_name']} {personal_info.get('middle_name','')} {personal_info['last_name']}")
        page.click('button[type="submit"]')
        time.sleep(2)  # Wait for results to load
        return self._parse_search_results(page)


    def opt_out(self, page, personal_info):
        """Submit opt-out request on Whitepages."""
        print(f"Opting out from {self.name} for {personal_info['first_name']} {personal_info['last_name']}")
        page.goto(self.opt_out_url)
        page.fill('input[name="name"]', f"{personal_info['first_name']} {personal_info['last_name']}")
        page.fill('input[name="address"]', personal_info['address'])
        page.click('button[type="submit"]')
        time.sleep(5)  # Wait for submission to process