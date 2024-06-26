
from flask.wrappers import Request
from flask import Flask, request, jsonify
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


def init_db():
    conn = sqlite3.connect('salesforce_mock.db')
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS accounts')  # Add this line to drop the existing table
    c.execute('''
        CREATE TABLE accounts (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            industry TEXT NOT NULL,
            region TEXT NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Pre-populate the database with mock data
def populate_db():
    conn = sqlite3.connect('salesforce_mock.db')
    c = conn.cursor()
    c.executemany('INSERT INTO accounts (id, name, industry, region, status) VALUES (?, ?, ?, ?, ?)', [
        ('1', 'Alice Inc', 'Technology', 'North America', 'Active'),
        ('2', 'Bob LLC', 'Healthcare', 'Europe', 'Inactive'),
        ('3', 'Charlie Corp', 'Retail', 'Asia', 'Active'),
    ])
    conn.commit()
    conn.close()

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


def sales_mock_002(request):
    logger.info(f'Request: {request.__dict__}')
    with app.test_request_context(path=request.full_path, method=request.method):
        try:
            # Manually dispatch the Flask request
            response = app.dispatch_request()
            logger.info(f'Response: {response}')
            return response
        except Exception as e:
            # Handle exceptions that might occur during dispatch
            return jsonify({'error': str(e)}), 500

# No app.run() needed; Cloud Functions handle the server setup.