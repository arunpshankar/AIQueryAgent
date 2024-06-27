
from typing import NoReturn

import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Static variables
BASE_URL = 'http://127.0.0.1:5000'


def get_all_accounts() -> NoReturn:
    """Fetch all accounts from the API and logs the results or errors."""
    try:
        response = requests.get(f'{BASE_URL}/api/accounts')
        response.raise_for_status()  # Raises an HTTPError for bad responses
        accounts = response.json()
        logging.info(f"All Accounts: {accounts}")
    except requests.exceptions.HTTPError as errh:
        logging.error(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        logging.error(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        logging.error(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        logging.error(f"Oops: Something Else: {err}")


def get_account_by_id(account_id: str) -> NoReturn:
    """Fetch a single account by its ID from the API and logs the results or errors."""
    try:
        response = requests.get(f'{BASE_URL}/api/accounts/{account_id}')
        response.raise_for_status()
        account = response.json()
        logging.info(f"Account {account_id}: {account}")
    except requests.exceptions.HTTPError:
        logging.error(f"Failed to fetch account {account_id}: {response.json()}")


def search_accounts_by_name(name: str) -> NoReturn:
    """Search for accounts that match a given name and logs the results or errors."""
    try:
        response = requests.get(f'{BASE_URL}/api/accounts/search', params={'name': name})
        response.raise_for_status()
        results = response.json()
        logging.info(f"Search Results for {name}: {results}")
    except requests.exceptions.HTTPError:
        logging.error(f"Failed to search accounts: {response.json()}")

# Example usage
if __name__ == '__main__':
    get_all_accounts()
    get_account_by_id('E0B3G6')  
    search_accounts_by_name('Bob')