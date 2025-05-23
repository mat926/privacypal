# PrivacyPal

**PrivacyPal** is a Python-based automation tool designed to help you remove your personal information from data brokers' websites. It uses undetected Playwright to search for your data, verify its accuracy, and submit opt-out requests, minimizing manual effort. The tool supports searching for multiple name variations and relatives to ensure comprehensive coverage.

## Features
- **Automated Search**: Searches data brokers for your personal information.
- **Result Verification**: Uses fuzzy matching to reduce false positives by verifying search results against your provided details.
<!-- - **Automatic Email Verification**: Handles email verification for opt-out requests. -->
- **Multi-Name Support**: Handles name variations (e.g., aliases, maiden names) and relatives.
- **Modular Design**: Easily extendable to support additional data brokers.
- **Logging**: Saves detailed logs of all actions for transparency and debugging.


## Supported Data Brokers
- Whitepages ✅

Currently, PrivacyPal supports **Whitepages**, with a framework to add more data brokers like Spokeo or BeenVerified.

## Prerequisites
- Python 3.8+
- [Patched Playwright](https://github.com/Kaliiiiiiiiii-Vinyzu/patchright) for web automation
- [fuzzywuzzy](https://github.com/seatgeek/fuzzywuzzy) for result verification
- A modern web browser (installed automatically by Playwright)

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/mat926/PrivacyPal.git
   cd PrivacyPal