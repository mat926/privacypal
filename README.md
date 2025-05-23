# PrivacyPal

**PrivacyPal** is a Python-based automation tool designed to help you remove your personal information from data brokers' websites. It uses Playwright to search for your data, verify its accuracy, and submit opt-out requests, minimizing manual effort. The tool supports searching for multiple name variations and relatives to ensure comprehensive coverage.

## Features
- **Automated Search**: Searches data brokers for your personal information.
- **Result Verification**: Uses fuzzy matching to reduce false positives by verifying search results against your provided details.
- **Multi-Name Support**: Handles name variations (e.g., aliases, maiden names) and relatives.
- **Modular Design**: Easily extendable to support additional data brokers.
- **Logging**: Saves detailed logs of all actions for transparency and debugging.

Currently, PrivacyPal supports **Whitepages**, with a framework to add more data brokers like Spokeo or BeenVerified.

## Prerequisites
- Python 3.8+
- [Playwright](https://playwright.dev/python/) for web automation
- [fuzzywuzzy](https://github.com/seatgeek/fuzzywuzzy) for result verification
- A modern web browser (installed automatically by Playwright)

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/PrivacyPal.git
   cd PrivacyPal