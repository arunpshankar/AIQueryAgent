from flask import request 
from flask import jsonify
from typing import Tuple
from flask import Flask
from typing import List
from typing import Dict 
import logging
import sqlite3
import flask 
import sys


app = Flask(__name__)

# Static variable for database path
DATABASE_PATH = './data/sales.db'

# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    handlers=[logging.StreamHandler(sys.stdout)],
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger.info(f'Using Flask=={flask.__version__}')


@app.route('/')
def home() -> str:
    """ Root endpoint to welcome users.
    Returns:
        A welcome message.
    """
    return "Welcome to the Sales API!"


@app.route('/api/accounts', methods=['GET'])
def get_accounts() -> Tuple[List[Dict], int]:
    """ Retrieve all accounts from the database.
    Returns:
        A JSON list of accounts and a HTTP status code.
    """
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute('SELECT id, name, industry, region, status FROM accounts')
            accounts = c.fetchall()
            return jsonify([dict(account) for account in accounts]), 200
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        return jsonify({'error': 'Unable to fetch accounts'}), 500


@app.route('/api/accounts/<account_id>', methods=['GET'])
def get_account(account_id: str) -> Tuple[Dict, int]:
    """ Retrieve a single account by ID.
    Args:
        account_id: The ID of the account to retrieve.
    Returns:
        A JSON object of the account and a HTTP status code.
    """
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute('SELECT * FROM accounts WHERE id = ?', (account_id,))
            account = c.fetchone()
            if account:
                return jsonify(dict(account)), 200
            else:
                return jsonify({'error': 'Account not found'}), 404
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        return jsonify({'error': 'Unable to fetch account'}), 500


@app.route('/api/accounts/search', methods=['GET'])
def search_accounts() -> Tuple[List[Dict], int]:
    """ Search for accounts by name.
    Returns:
        A JSON list of accounts and a HTTP status code.
    """
    search_query = request.args.get('name', '')
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("SELECT * FROM accounts WHERE name LIKE '%' || ? || '%'", (search_query,))
            accounts = c.fetchall()
            return jsonify([dict(account) for account in accounts]), 200
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        return jsonify({'error': 'Unable to search accounts'}), 500


if __name__ == '__main__':
    app.run(debug=True)