from database import create_tables
from product import add_product, list_products
from invoice import create_invoice, list_invoices, filter_invoices_by_date, export_invoices_to_pdf

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

        choice = input("Enter your choice (1-7): ").strip()

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

if __name__ == "__main__":
    create_tables()
    billing_menu()
