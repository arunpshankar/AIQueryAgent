import sqlite3

def test_query_by_id(account_id):
    conn = sqlite3.connect('./data/sales.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM accounts WHERE id = ?', (account_id,))
    result = c.fetchone()
    conn.close()
    return dict(result) if result else 'Account not found'

def test_query_by_name_exact(name):
    conn = sqlite3.connect('./data/sales.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM accounts WHERE name = ?', (name,))
    results = c.fetchall()
    conn.close()
    return [dict(result) for result in results] if results else 'No accounts found with exact name'

def test_query_by_name_fuzzy(name):
    conn = sqlite3.connect('./data/sales.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM accounts WHERE name LIKE '%' || ? || '%'", (name,))
    results = c.fetchall()
    conn.close()
    return [dict(result) for result in results] if results else 'No accounts found with matching name'

def test_query_by_industry(industry):
    conn = sqlite3.connect('./data/sales.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM accounts WHERE industry = ?', (industry,))
    results = c.fetchall()
    conn.close()
    return [dict(result) for result in results]

def test_query_by_region(region):
    conn = sqlite3.connect('./data/sales.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM accounts WHERE region = ?', (region,))
    results = c.fetchall()
    conn.close()
    return [dict(result) for result in results]

def test_query_by_status(status):
    conn = sqlite3.connect('./data/sales.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM accounts WHERE status = ?', (status,))
    results = c.fetchall()
    conn.close()
    return [dict(result) for result in results]

# Example usage
if __name__ == '__main__':
    print("Testing retrieval by Account ID:")
    print(test_query_by_id('1'))

    print("Testing retrieval by Name (Exact Match):")
    print(test_query_by_name_exact('Alice Inc'))

    print("Testing retrieval by Name (Fuzzy):")
    print(test_query_by_name_fuzzy('Al'))

    print("Testing by Industry:")
    print(test_query_by_industry('Technology'))
