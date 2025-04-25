from database import connect_db
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas

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
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''SELECT Invoices.id, Products.name, Invoices.quantity, Invoices.total, Invoices.timestamp
                      FROM Invoices JOIN Products ON Invoices.product_id = Products.id
                      ORDER BY Invoices.timestamp DESC''')
    invoices = cursor.fetchall()
    conn.close()

    if not invoices:
        print("⚠️ No invoices to export.")
        return

    filename = f"invoices_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    c = Canvas(filename, pagesize=A4)
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
