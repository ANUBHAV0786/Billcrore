from database import connect_db

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
