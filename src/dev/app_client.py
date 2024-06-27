from typing import Optional
from typing import Dict
from typing import List 
import requests
import logging


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Static variables
BASE_URL = 'http://127.0.0.1:5000'


def get_all_accounts() -> Optional[List[Dict]]:
    """
    Fetch all accounts from the API and log the results or errors.

    Returns a list of accounts if successful, None otherwise.
    """
    try:
        response = requests.get(f'{BASE_URL}/api/accounts')
        response.raise_for_status()  # Will raise an exception for HTTP errors
        accounts = response.json()
        logging.info("All Accounts: %s", accounts)
        return accounts
    except requests.exceptions.RequestException as e:
        logging.error("Error retrieving accounts: %s", e)
        return None


def get_account_by_id(account_id: str) -> Optional[Dict]:
    """
    Fetch a single account by its ID and log the results or errors.

    Returns the account if successful, None otherwise.
    """
    try:
        response = requests.get(f'{BASE_URL}/api/accounts/{account_id}')
        response.raise_for_status()
        account = response.json()
        logging.info("Account %s: %s", account_id, account)
        return account
    except requests.exceptions.RequestException as e:
        logging.error("Failed to fetch account %s: %s", account_id, e)
        return None


def search_accounts_by_name(name: str) -> Optional[List[Dict]]:
    """
    Search for accounts by name and log the results or errors.

    Returns a list of matching accounts if successful, None otherwise.
    """
    try:
        response = requests.get(f'{BASE_URL}/api/accounts/search', params={'name': name})
        response.raise_for_status()
        results = response.json()
        logging.info("Search Results for %s: %s", name, results)
        return results
    except requests.exceptions.RequestException as e:
        logging.error("Failed to search accounts by name %s: %s", name, e)
        return None


if __name__ == '__main__':
    get_all_accounts()
    get_account_by_id('E0B3G6')  
    search_accounts_by_name('Bob')