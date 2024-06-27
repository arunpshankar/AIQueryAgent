from typing import List
from typing import Dict 
import logging
import sqlite3
import sys


# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.getLevelName('INFO'),
                    handlers=[logging.StreamHandler(sys.stdout)],
                    format='%(asctime)s - %(module)s - %(levelname)s - %(message)s')

# Static variables
DATABASE_PATH = './data/sales.db'

def connect_db():
    """
    Establishes a database connection with the SQLite database.
    Sets the row factory to sqlite3.Row to allow column access by name.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def test_query_by_id(account_id: str) -> Dict:
    """
    Queries the database for an account by ID and returns the result as a dictionary.
    """
    try:
        conn = connect_db()
        c = conn.cursor()
        c.execute('SELECT * FROM accounts WHERE id = ?', (account_id,))
        result = c.fetchone()
        return dict(result) if result else {}
    finally:
        conn.close()

def test_query_by_name_exact(name: str) -> List[Dict]:
    """
    Queries the database for accounts with an exact name match and returns the results as a list of dictionaries.
    """
    try:
        conn = connect_db()
        c = conn.cursor()
        c.execute('SELECT * FROM accounts WHERE name = ?', (name,))
        results = c.fetchall()
        return [dict(result) for result in results] if results else []
    finally:
        conn.close()

def test_query_by_name_fuzzy(name: str) -> List[Dict]:
    """
    Queries the database for accounts with a name that includes the search term and returns the results as a list of dictionaries.
    """
    try:
        conn = connect_db()
        c = conn.cursor()
        c.execute("SELECT * FROM accounts WHERE name LIKE '%' || ? || '%'", (name,))
        results = c.fetchall()
        return [dict(result) for result in results] if results else []
    finally:
        conn.close()

def test_query_by_industry(industry: str) -> List[Dict]:
    """
    Queries the database for accounts in a specific industry and returns the results as a list of dictionaries.
    """
    try:
        conn = connect_db()
        c = conn.cursor()
        c.execute('SELECT * FROM accounts WHERE industry = ?', (industry,))
        results = c.fetchall()
        return [dict(result) for result in results] if results else []
    finally:
        conn.close()

def test_query_by_region(region: str) -> List[Dict]:
    """
    Queries the database for accounts in a specific region and returns the results as a list of dictionaries.
    """
    try:
        conn = connect_db()
        c = conn.cursor()
        c.execute('SELECT * FROM accounts WHERE region = ?', (region,))
        results = c.fetchall()
        return [dict(result) for result in results] if results else []
    finally:
        conn.close()

def test_query_by_status(status: str) -> List[Dict]:
    """
    Queries the database for accounts with a specific status and returns the results as a list of dictionaries.
    """
    try:
        conn = connect_db()
        c = conn.cursor()
        c.execute('SELECT * FROM accounts WHERE status = ?', (status,))
        results = c.fetchall()
        return [dict(result) for result in results] if results else []
    finally:
        conn.close()


if __name__ == '__main__':
    print("Testing retrieval by Account ID:")
    for k, v in test_query_by_id('Z3P6G9').items():
        print(f"{k}: {v}")

    print("\nTesting retrieval by Name (Exact Match):")
    for record in test_query_by_name_exact('Alice Inc'):
        for k, v in record.items():
            print(f"{k}: {v}")
        print()  

    print("Testing retrieval by Name (Fuzzy):")
    for record in test_query_by_name_fuzzy('Bob'):
        for k, v in record.items():
            print(f"{k}: {v}")
        print() 

    print("Testing by Industry:")
    for record in test_query_by_industry('Healthcare'):
        for k, v in record.items():
            print(f"{k}: {v}")
        print() 
