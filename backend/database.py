import sqlite3
import os

DB_FILE = "sales_data.db"

def create_database():
    """Creates the SQLite database and populates it with sample data."""
    # Delete old database file if it exists
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create the sales table
    cursor.execute('''
    CREATE TABLE sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT NOT NULL,
        category TEXT NOT NULL,
        region TEXT NOT NULL,
        sale_date DATE NOT NULL,
        quantity INTEGER NOT NULL,
        unit_price REAL NOT NULL,
        total_price REAL NOT NULL
    );
    ''')

    # Sample data
    sales_data = [
        ('Laptop', 'Electronics', 'North', '2025-08-15', 10, 1200.00, 12000.00),
        ('Keyboard', 'Electronics', 'North', '2025-08-15', 50, 75.00, 3750.00),
        ('Desk Chair', 'Furniture', 'West', '2025-08-16', 20, 150.00, 3000.00),
        ('Monitor', 'Electronics', 'South', '2025-08-17', 30, 300.00, 9000.00),
        ('Laptop', 'Electronics', 'West', '2025-08-18', 15, 1200.00, 18000.00),
        ('Mouse', 'Electronics', 'North', '2025-08-19', 100, 25.00, 2500.00),
        ('Desk Chair', 'Furniture', 'East', '2025-08-20', 25, 150.00, 3750.00),
        ('Monitor', 'Electronics', 'North', '2025-08-21', 20, 300.00, 6000.00)
    ]

    # Insert data into the table
    cursor.executemany('''
    INSERT INTO sales (product_name, category, region, sale_date, quantity, unit_price, total_price)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', sales_data)

    conn.commit()
    conn.close()
    print(f"Database '{DB_FILE}' created successfully with sample data.")

if __name__ == "__main__":
    create_database()
