from flask import request
from flask import jsonify
from flask import Flask
import logging
import sqlite3
import flask 
import sys 


app = Flask(__name__)

# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.getLevelName('INFO'),
                    handlers=[logging.StreamHandler(sys.stdout)],
                    format='%(asctime)s - %(module)s - %(levelname)s - %(message)s')

# Log versions of dependencies 
logger.info(f'Using openai=={flask.__version__}')


@app.route('/')
def home():
    return "Welcome to the API!"

@app.route('/api/accounts', methods=['GET'])
def get_accounts():
    conn = sqlite3.connect('salesforce_mock.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT id, name, industry, region, status FROM accounts')
    accounts = c.fetchall()
    conn.close()
    return jsonify([dict(account) for account in accounts]), 200

@app.route('/api/accounts/<account_id>', methods=['GET'])
def get_account(account_id):
    conn = sqlite3.connect('salesforce_mock.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM accounts WHERE id = ?', (account_id,))
    account = c.fetchone()
    conn.close()
    if account:
        return jsonify(dict(account)), 200
    else:
        return jsonify({'error': 'Account not found'}), 404

@app.route('/api/accounts/search', methods=['GET'])
def search_accounts():
    search_query = request.args.get('name', '')
    conn = sqlite3.connect('salesforce_mock.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM accounts WHERE name LIKE '%' || ? || '%'", (search_query,))
    accounts = c.fetchall()
    conn.close()
    return jsonify([dict(account) for account in accounts]), 200