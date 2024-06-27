import sqlite3
import csv

def init_db():
    conn = sqlite3.connect('./data/sales.db')
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS accounts')  # This line drops the existing table if it exists
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

def populate_db_from_csv():
    conn = sqlite3.connect('./data/sales.db')
    c = conn.cursor()
    with open('./data/sales.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            c.execute('INSERT INTO accounts (id, name, industry, region, status) VALUES (?, ?, ?, ?, ?)', 
                      (row['id'], row['name'], row['industry'], row['region'], row['status']))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    populate_db_from_csv()
