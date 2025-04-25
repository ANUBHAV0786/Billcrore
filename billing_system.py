import sqlite3
from datetime import datetime

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

def add_product(name, price):
    try:
        price = float(price)
        if price <= 0:
            print("❌ Price must be greater than zero.")
            return
    except ValueError:
        print("❌ Invalid price. Please enter a numeric value.")
        return

    name_lower = name.strip().lower()
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Products WHERE LOWER(name) = ?', (name_lower,))
        if cursor.fetchone():
            print(f"❌ Product '{name}' already exists.")
        else:
            cursor.execute('INSERT INTO Products (name, price) VALUES (?, ?)', (name, price))
            conn.commit()
            print(f"✅ Product '{name}' added successfully.")

def list_products():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Products')
        products = cursor.fetchall()

    if not products:
        print("📭 No products available.")
    else:
        print("\n🛒 Available Products:")
        for p in products:
            print(f"ID: {p[0]} | Name: {p[1]} | Price: ₹{p[2]}")

def create_invoice(product_id_input, quantity_input):
    try:
        product_id = int(product_id_input)
        quantity = int(quantity_input)
        if quantity <= 0:
            print("❌ Quantity must be greater than zero.")
            return
    except ValueError:
        print("❌ Invalid input. Product ID and quantity must be integers.")
        return

    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT price FROM Products WHERE id = ?', (product_id,))
        product = cursor.fetchone()

        if product:
            price = product[0]
            total = price * quantity
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute('INSERT INTO Invoices (product_id, quantity, total, timestamp) VALUES (?, ?, ?, ?)',
                           (product_id, quantity, total, timestamp))
            conn.commit()
            print(f"🧾 Invoice created. Total: ₹{total:.2f} | Timestamp: {timestamp}")
        else:
            print("❌ Product ID does not exist.")

def list_invoices():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT Invoices.id, Products.name, Invoices.quantity, Invoices.total, Invoices.timestamp
                          FROM Invoices JOIN Products ON Invoices.product_id = Products.id''')
        invoices = cursor.fetchall()

    if not invoices:
        print("📭 No invoices found.")
    else:
        print("\n📄 All Invoices:")
        for inv in invoices:
            print(f"Invoice ID: {inv[0]} | Product: {inv[1]} | Qty: {inv[2]} | Total: ₹{inv[3]:.2f} | Date: {inv[4]}")

def filter_invoices_by_date(start_date, end_date):
    try:
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        print("❌ Invalid date format. Please use YYYY-MM-DD.")
        return

    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT Invoices.id, Products.name, Invoices.quantity, Invoices.total, Invoices.timestamp
                          FROM Invoices JOIN Products ON Invoices.product_id = Products.id
                          WHERE timestamp BETWEEN ? AND ?''',
                       (start_date + " 00:00:00", end_date + " 23:59:59"))
        filtered = cursor.fetchall()

    if not filtered:
        print("📭 No invoices found in the given date range.")
    else:
        print("\n📄 Filtered Invoices:")
        for inv in filtered:
            print(f"Invoice ID: {inv[0]} | Product: {inv[1]} | Qty: {inv[2]} | Total: ₹{inv[3]:.2f} | Date: {inv[4]}")

def export_invoices_to_pdf():
    conn = sqlite3.connect('billing_system.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT Invoices.id, Products.name, Invoices.quantity, Invoices.total, Invoices.timestamp
        FROM Invoices
        JOIN Products ON Invoices.product_id = Products.id
        ORDER BY Invoices.timestamp DESC
    ''')
    invoices = cursor.fetchall()
    conn.close()

    if not invoices:
        print("⚠️ No invoices to export.")
        return

    # Create PDF file
    filename = f"invoices_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "🧾 Invoice Report")

    c.setFont("Helvetica", 10)
    y = height - 80
    headers = ["Invoice ID", "Product", "Qty", "Total (₹)", "Date"]
    c.drawString(50, y, "{:<12} {:<20} {:<8} {:<12} {:<20}".format(*headers))
    y -= 20
    c.line(50, y, width - 50, y)
    y -= 20

    for inv in invoices:
        if y < 100:
            c.showPage()
            c.setFont("Helvetica", 10)
            y = height - 50

        line = "{:<12} {:<20} {:<8} {:<12} {:<20}".format(
            inv[0], inv[1], inv[2], f"{inv[3]:.2f}", inv[4]
        )
        c.drawString(50, y, line)
        y -= 20

    c.save()
    print(f"✅ Invoices exported successfully to '{filename}'")

def billing_menu():
    while True:
        print("\n📋 Billing Menu:")
        print("1. Add Product")
        print("2. List Products")
        print("3. Create Invoice")
        print("4. List Invoices")
        print("5. Filter Invoices by Date")
        print("6. Export Invoices to PDF")
        print("7. Exit")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            name = input("Enter product name: ").strip()
            price = input("Enter product price: ").strip()
            add_product(name, price)
        elif choice == "2":
            list_products()
        elif choice == "3":
            list_products()
            product_id = input("Enter product ID: ").strip()
            quantity = input("Enter quantity: ").strip()
            create_invoice(product_id, quantity)
        elif choice == "4":
            list_invoices()
        elif choice == "5":
            start_date = input("Enter start date (YYYY-MM-DD): ").strip()
            end_date = input("Enter end date (YYYY-MM-DD): ").strip()
            filter_invoices_by_date(start_date, end_date)
        elif choice == "6":
            export_invoices_to_pdf()
        elif choice == "7":
            print("👋 Exiting Billing System. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter a number between 1 and 7.")

# Initialize
create_tables()
billing_menu()
