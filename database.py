import sqlite3

def connect_db():
    return sqlite3.connect('billing_system.db')

def create_tables():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Products (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT UNIQUE COLLATE NOCASE,
                            price REAL)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS Invoices (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            product_id INTEGER,
                            quantity INTEGER,
                            total REAL,
                            timestamp TEXT,
                            FOREIGN KEY (product_id) REFERENCES Products(id))''')
        print("✅ Database initialized.")
