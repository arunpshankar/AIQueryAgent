from flask.wrappers import Request
from flask import jsonify
from flask import request
from typing import Union
from typing import Tuple
from flask import Flask
from typing import Dict 
from typing import List
import logging
import sqlite3
import flask 
import json 
import sys


app = Flask(__name__)

# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    handlers=[logging.StreamHandler(sys.stdout)],
                    format='%(asctime)s - %(module)s - %(levelname)s - %(message)s')

# Log versions of dependencies 
logger.info(f'Using flask=={flask.__version__}')


@app.route('/')
def home() -> str:
    """
    Home route to check if the API is running.

    Returns:
        str: Welcome message.
    """
    return "Welcome to the Sales API!"


@app.route('/api/accounts', methods=['GET'])
def get_accounts() -> Tuple[Dict[str, Union[str, List[Dict[str, Union[str, int]]]]], int]:
    """
    Retrieve all accounts from the database.

    Returns:
        Tuple[Dict[str, Union[str, List[Dict[str, Union[str, int]]]]], int]: JSON response with accounts and status code.
    """
    try:
        conn = sqlite3.connect('sales.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('SELECT id, name, industry, region, status FROM accounts')
        accounts = c.fetchall()
        conn.close()
        return jsonify([dict(account) for account in accounts]), 200
    except Exception as e:
        logger.error(f"Error retrieving accounts: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500


@app.route('/api/accounts/<account_id>', methods=['GET'])
def get_account(account_id: str) -> Tuple[Dict[str, Union[str, Dict[str, Union[str, int]]]], int]:
    """
    Retrieve a specific account by ID.

    Args:
        account_id (str): The ID of the account to retrieve.

    Returns:
        Tuple[Dict[str, Union[str, Dict[str, Union[str, int]]]], int]: JSON response with the account and status code.
    """
    try:
        conn = sqlite3.connect('sales.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('SELECT * FROM accounts WHERE id = ?', (account_id,))
        account = c.fetchone()
        conn.close()
        if account:
            return jsonify(dict(account)), 200
        else:
            return jsonify({'error': 'Account not found'}), 404
    except Exception as e:
        logger.error(f"Error retrieving account {account_id}: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500


@app.route('/api/accounts/search', methods=['GET'])
def search_accounts() -> Tuple[Dict[str, Union[str, List[Dict[str, Union[str, int]]]]], int]:
    """
    Search for accounts by name (partial or exact string match).

    Returns:
        Tuple[Dict[str, Union[str, List[Dict[str, Union[str, int]]]]], int]: JSON response with the accounts and status code.
    """
    try:
        search_query = request.args.get('name', '')
        conn = sqlite3.connect('sales.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM accounts WHERE name LIKE '%' || ? || '%'", (search_query,))
        accounts = c.fetchall()
        conn.close()
        return jsonify([dict(account) for account in accounts]), 200
    except Exception as e:
        logger.error(f"Error searching for accounts with query '{search_query}': {e}")
        return jsonify({'error': 'Internal Server Error'}), 500


@app.route('/api/accounts/url', methods=['POST'])
def generate_account_url() -> Tuple[Dict, int]:
    """ 
    Generate a URL for the given account ID and type.
    
    Returns:
        A JSON object with the generated URL and a HTTP status code.
    """
    try:
        # Log the incoming request for debugging purposes
        app.logger.info('Received request: %s', request.data)
        app.logger.info('Request headers: %s', request.headers)

        # Parse JSON data from the request
        data = request.get_json(force=True)

        # Log parsed data for debugging purposes
        app.logger.info('Parsed data: %s', data)

        # Extract account_id and account_type
        account_id = data.get('account_id')
        account_type = data.get('account_type')

        # Validate input
        if not account_id or not account_type:
            return jsonify({'error': 'account_id and account_type are required'}), 400

        # Define base URL parts
        base_urls = {
            'portfolio': 'https://sales.com/portfolio/accounts/',
            'sales': 'https://sales.com/sales/accounts/',
            'activity': 'https://sales.com/activity/accounts/'
        }

        # Get the appropriate base URL
        base_url = base_urls.get(account_type.lower())
        if not base_url:
            return jsonify({'error': 'Invalid account_type'}), 400

        # Generate the full URL
        full_url = f"{base_url}{account_id}"

        # Log generated URL for debugging purposes
        app.logger.info('Generated URL: %s', full_url)

        return jsonify({'url': full_url}), 200

    except Exception as e:
        app.logger.error('Error generating URL: %s', str(e))
        return jsonify({'error': str(e)}), 500


def sales(request: Request) -> Tuple[Dict[str, str], int]:
    """
    Entry point for the Cloud Function to process a request and return a response.

    Args:
        request (Request): The Flask request object.

    Returns:
        Tuple[Dict[str, str], int]: JSON response and status code.
    """
    logger.info(f'Request method: {request.method}')
    logger.info(f'Request headers: {request.headers}')
    logger.info(f'Request data: {request.data}')

    with app.test_request_context(path=request.full_path, method=request.method, data=request.data):
        try:
            # Manually dispatch the Flask request
            response = app.dispatch_request()
            logger.info(f'Response: {response}')
            return response
        except Exception as e:
            # Handle exceptions that might occur during dispatch
            logger.error(f"Error processing request: {e}")
            return jsonify({'error': str(e)}), 500

# No app.run() needed; Cloud Functions handle the server setup.