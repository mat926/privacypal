import os
#from playwright.sync_api import sync_playwright
from patchright.sync_api import sync_playwright
import time
from fuzzywuzzy import fuzz
from modules.util import logger
from modules.config import Config
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
    # personal_info = {
    #     'first_name': 'John', # os.getenv('FIRST_NAME'),
    #     'last_name': 'Smith', #os.getenv('LAST_NAME'),
    #     'address':  '17255 W Via De Luna Dr' # os.getenv('ADDRESS')
    # }

    # # Load name variations and relatives
    # name_variations = os.getenv('NAME_VARIATIONS', '').split(', ')
    # relatives = os.getenv('RELATIVES', '').split(', ')

    # # Validate primary personal info
    # if not all(personal_info.values()):
    #     logger.error("Please set FIRST_NAME, LAST_NAME, and ADDRESS as environment variables.")
    #     print("Error: Please set FIRST_NAME, LAST_NAME, and ADDRESS as environment variables.")
    #     return

    try:
        # Load configuration from YAML file
        config = Config()
    except Exception as e:
        logger.error(f"Error loading config file: {e}")
        print(f"Error loading config file: {e}")
        return

    logger.info("Starting PrivacyPal Data Broker Removal Process")
    # Create list of all names to search (primary + variations + relatives)
    all_names = config.config['names']
    
    

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

        for name in all_names:
            f_name = name['first_name']
            m_name = name.get('middle_name', '')
            l_name = name['last_name']
            logger.info("Processing searches for %s %s %s", f_name, m_name , l_name)

            for data_broker in data_brokers:
                # Update the databroker field dynamically
                #logger.addFilter(lambda record: setattr(record, 'databroker', data_broker.name) or True)

                try:
                    search_results = data_broker.search(page, name)
                    if search_results:
                        filtered_results = data_broker.verify_results(search_results, name, config.config)
                        # print(f"Verified information found on {data_broker.name} for {f_name} {l_name}")
                        data_broker.opt_out(page, filtered_results, name)
                        #     #logger.info(f"Opt-out request submitted for {data_broker.name} - {first_name} {last_name}")
                        #     print(f"Opt-out request submitted for {data_broker.name} - {f_name} {l_name}")
                        # else:
                        #     #logger.info(f"Results on {data_broker.name} for {first_name} {last_name} did not match closely enough")
                        #     print(f"Results on {data_broker.name} for {f_name} {l_name} did not match closely enough")
                    else:
                        #logger.info(f"No information found on {data_broker.name} for {first_name} {last_name}")
                        print(f"No information found on {data_broker.name} for {f_name} {l_name}")
                except Exception as e:
                    #logger.error(f"Error processing {data_broker.name} for {first_name} {last_name}: {e}")
                    print(f"Error processing {data_broker.name} for {f_name} {l_name}: {e}")
                time.sleep(2)  # Delay to avoid rate limiting

        browser.close()
        logger.info("Process completed.")
        print("Process completed. Check data_broker_removal.log for details.")

if __name__ == "__main__":
    main()