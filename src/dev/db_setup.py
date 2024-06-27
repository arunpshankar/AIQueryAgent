
from typing import NoReturn
import sqlite3
import logging
import csv
import sys


# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.getLevelName('INFO'),
                    handlers=[logging.StreamHandler(sys.stdout)],
                    format='%(asctime)s - %(module)s - %(levelname)s - %(message)s')

# Static variables
DATABASE_PATH = './data/sales.db'
CSV_PATH = './data/sales.csv'

def init_db() -> NoReturn:
    """
    Initializes the database by connecting to the SQLite database and creating a new table 'accounts'.
    It will drop the existing table if it exists and then create a new one.
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        c.execute('DROP TABLE IF EXISTS accounts')  # Drops the existing table if it exists
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
        logger.info("Database initialized and table 'accounts' created successfully.")
    except sqlite3.Error as e:
        logger.error(f"An error occurred while initializing the database: {e}")
    finally:
        conn.close()

def populate_db_from_csv() -> NoReturn:
    """
    Populates the 'accounts' table in the database from a CSV file.
    This function reads from 'sales.csv' and inserts each row into the 'accounts' table.
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        with open(CSV_PATH, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                c.execute('INSERT INTO accounts (id, name, industry, region, status) VALUES (?, ?, ?, ?, ?)', 
                          (row['id'], row['name'], row['industry'], row['region'], row['status']))
            conn.commit()
            logger.info("Database populated from CSV file successfully.")
    except sqlite3.Error as e:
        logger.error(f"An error occurred while populating the database from CSV: {e}")
    except FileNotFoundError:
        logger.error("The file 'sales.csv' was not found.")
    finally:
        conn.close()


if __name__ == '__main__':
    init_db()
    populate_db_from_csv()
