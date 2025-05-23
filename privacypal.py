import os
#from playwright.sync_api import sync_playwright
from patchright.sync_api import sync_playwright
import time
from fuzzywuzzy import fuzz
from modules.util import logger
from data_brokers import DataBroker, WhitepagesDataBroker

# Import additional data brokers here, e.g., from data_brokers.spokeo import SpokeoDataBroker

# Set up logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )

# Set up the main logger
#logger = util.logger
#logger = MyLogger('PrivacyPal', 'data_broker_removal.log', logging.INFO)


# Main function to run the app
def main():
    # Load personal info from environment variables
    personal_info = {
        'first_name': 'John', # os.getenv('FIRST_NAME'),
        'last_name': 'Smith', #os.getenv('LAST_NAME'),
        'address':  '17255 W Via De Luna Dr' # os.getenv('ADDRESS')
    }

    # Load name variations and relatives
    name_variations = os.getenv('NAME_VARIATIONS', '').split(', ')
    relatives = os.getenv('RELATIVES', '').split(', ')

    # Validate primary personal info
    if not all(personal_info.values()):
        logger.error("Please set FIRST_NAME, LAST_NAME, and ADDRESS as environment variables.")
        print("Error: Please set FIRST_NAME, LAST_NAME, and ADDRESS as environment variables.")
        return

    logger.info("Starting PrivacyPal Data Broker Removal Process")
    # Create list of all names to search (primary + variations + relatives)
    all_names = [(personal_info['first_name'], personal_info['last_name'])]
    for variation in name_variations:
        if variation.strip():
            first, last = variation.strip().split(' ', 1)
            all_names.append((first, last))
    for relative in relatives:
        if relative.strip():
            first, last = relative.strip().split(' ', 1)
            all_names.append((first, last))

    # List of data brokers
    data_brokers = [
        WhitepagesDataBroker(),
        # Add more data brokers here, e.g., SpokeoDataBroker()
    ]

    # Start Playwright and process each data broker
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir="./user_data",
            channel="chrome",
            headless=False,
            no_viewport=True,
            # do NOT add custom browser headers or user_agent
        )
        page = browser.new_page()

        for first_name, last_name in all_names:
            current_info = {
                'first_name': first_name,
                'last_name': last_name,
                'address': personal_info['address']
            }
            logger.info("Processing searches for %s %s", first_name, last_name)

            for data_broker in data_brokers:
                # Update the databroker field dynamically
                logger.addFilter(lambda record: setattr(record, 'databroker', data_broker.name) or True)

                try:
                    if data_broker.search(page, current_info):
                        if data_broker.verify_result(page, current_info):
                            print(f"Verified information found on {data_broker.name} for {first_name} {last_name}")
                            data_broker.opt_out(page, current_info)
                            #logger.info(f"Opt-out request submitted for {data_broker.name} - {first_name} {last_name}")
                            print(f"Opt-out request submitted for {data_broker.name} - {first_name} {last_name}")
                        else:
                            #logger.info(f"Results on {data_broker.name} for {first_name} {last_name} did not match closely enough")
                            print(f"Results on {data_broker.name} for {first_name} {last_name} did not match closely enough")
                    else:
                        #logger.info(f"No information found on {data_broker.name} for {first_name} {last_name}")
                        print(f"No information found on {data_broker.name} for {first_name} {last_name}")
                except Exception as e:
                    #logger.error(f"Error processing {data_broker.name} for {first_name} {last_name}: {e}")
                    print(f"Error processing {data_broker.name} for {first_name} {last_name}: {e}")
                time.sleep(2)  # Delay to avoid rate limiting

        browser.close()
        logger.info("Process completed.")
        print("Process completed. Check data_broker_removal.log for details.")

if __name__ == "__main__":
    main()