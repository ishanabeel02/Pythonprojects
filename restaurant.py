import json
from datetime import datetime


class RestaurantSystem:
    def __init__(self):
        self.menu = self.load_data('menu.json')
        self.orders = self.load_data('orders.json')
        self.tables = self.load_data('tables.json')
        self.staff = self.load_data('staff.json')

        # Initialize default tables if none exist
        if not self.tables:
            self.tables = {str(i): {'capacity': 4, 'status': 'Available'} for i in range(1, 11)}

    def load_data(self, filename):
        try:
            with open(filename) as f:
                return json.load(f)
        except:
            return {}

    def save_data(self, data, filename):
        with open(filename, 'w') as f:
            json.dump(data, f)

    def main_menu(self):
        while True:
            print("\n=== RESTAURANT MANAGEMENT ===")
            print("1. Menu Management")
            print("2. Table Management")
            print("3. Order Management")
            print("4. Staff Management")
            print("5. Reports")
            print("6. Exit")

            choice = input("Enter choice (1-6): ")

            if choice == '1':
                self.menu_management()
            elif choice == '2':
                self.table_management()
            elif choice == '3':
                self.order_management()
            elif choice == '4':
                self.staff_management()
            elif choice == '5':
                self.reports_menu()
            elif choice == '6':
                self.save_all()
                print("Data saved. Exiting...")
                break
            else:
                print("Invalid choice!")

    def save_all(self):
        self.save_data(self.menu, 'menu.json')
        self.save_data(self.orders, 'orders.json')
        self.save_data(self.tables, 'tables.json')
        self.save_data(self.staff, 'staff.json')

    def menu_management(self):
        while True:
            print("\n=== MENU MANAGEMENT ===")
            print("1. Add Menu Item")
            print("2. View Menu")
            print("3. Update Menu Item")
            print("4. Delete Menu Item")
            print("5. Back")

            choice = input("Enter choice (1-5): ")

            if choice == '1':
                self.add_menu_item()
            elif choice == '2':
                self.view_menu()
            elif choice == '3':
                self.update_menu_item()
            elif choice == '4':
                self.delete_menu_item()
            elif choice == '5':
                break
            else:
                print("Invalid choice!")

    def add_menu_item(self):
        item_id = input("Enter item ID: ")
        if item_id in self.menu:
            print("Item ID already exists!")
            return

        self.menu[item_id] = {
            'name': input("Item name: "),
            'category': input("Category (Appetizer/Main/Dessert/Drink): ").capitalize(),
            'price': float(input("Price: $")),
            'description': input("Description: "),
            'available': True
        }
        print("Menu item added!")

    def view_menu(self):
        if not self.menu:
            print("Menu is empty!")
            return

        print("\n{:<8} {:<20} {:<15} {:<10} {:<10}".format(
            "ID", "Name", "Category", "Price", "Available"))
        print("-" * 65)

        for item_id, item in self.menu.items():
            print("{:<8} {:<20} {:<15} ${:<9.2f} {:<10}".format(
                item_id, item['name'], item['category'],
                item['price'], "Yes" if item['available'] else "No"))

    def update_menu_item(self):
        item_id = input("Enter item ID to update: ")
        if item_id not in self.menu:
            print("Item not found!")
            return

        item = self.menu[item_id]
        print("\nCurrent Details:")
        print(f"1. Name: {item['name']}")
        print(f"2. Category: {item['category']}")
        print(f"3. Price: ${item['price']:.2f}")
        print(f"4. Description: {item['description']}")
        print(f"5. Available: {'Yes' if item['available'] else 'No'}")

        field = input("\nEnter field to update (1-5) or 0 to cancel: ")

        if field == '0':
            return
        elif field == '1':
            item['name'] = input("New name: ")
        elif field == '2':
            item['category'] = input("New category: ").capitalize()
        elif field == '3':
            item['price'] = float(input("New price: $"))
        elif field == '4':
            item['description'] = input("New description: ")
        elif field == '5':
            item['available'] = input("Available? (y/n): ").lower() == 'y'
        else:
            print("Invalid field!")

        print("Menu item updated!")

    def delete_menu_item(self):
        item_id = input("Enter item ID to delete: ")
        if item_id not in self.menu:
            print("Item not found!")
            return

        confirm = input(f"Delete {self.menu[item_id]['name']}? (y/n): ").lower()
        if confirm == 'y':
            del self.menu[item_id]
            print("Item deleted!")

    def table_management(self):
        while True:
            print("\n=== TABLE MANAGEMENT ===")
            print("1. View Tables")
            print("2. Update Table Status")
            print("3. Back")

            choice = input("Enter choice (1-3): ")

            if choice == '1':
                self.view_tables()
            elif choice == '2':
                self.update_table_status()
            elif choice == '3':
                break
            else:
                print("Invalid choice!")

    def view_tables(self):
        print("\n{:<8} {:<10} {:<15}".format("Table", "Capacity", "Status"))
        print("-" * 35)

        for table_num, table in self.tables.items():
            print("{:<8} {:<10} {:<15}".format(
                table_num, table['capacity'], table['status']))

    def update_table_status(self):
        table_num = input("Enter table number: ")
        if table_num not in self.tables:
            print("Table not found!")
            return

        print(f"\nCurrent status: {self.tables[table_num]['status']}")
        print("1. Available")
        print("2. Occupied")
        print("3. Reserved")
        print("4. Cleaning")

        choice = input("Enter new status (1-4): ")

        if choice == '1':
            self.tables[table_num]['status'] = 'Available'
        elif choice == '2':
            self.tables[table_num]['status'] = 'Occupied'
        elif choice == '3':
            self.tables[table_num]['status'] = 'Reserved'
        elif choice == '4':
            self.tables[table_num]['status'] = 'Cleaning'
        else:
            print("Invalid choice!")

        print("Table status updated!")

    def order_management(self):
        while True:
            print("\n=== ORDER MANAGEMENT ===")
            print("1. Create New Order")
            print("2. View Active Orders")
            print("3. Update Order Status")
            print("4. View Order History")
            print("5. Back")

            choice = input("Enter choice (1-5): ")

            if choice == '1':
                self.create_order()
            elif choice == '2':
                self.view_active_orders()
            elif choice == '3':
                self.update_order_status()
            elif choice == '4':
                self.view_order_history()
            elif choice == '5':
                break
            else:
                print("Invalid choice!")

    def create_order(self):
        if not self.menu:
            print("Menu is empty! Add items first.")
            return

        # Find available tables
        available_tables = [t for t, info in self.tables.items()
                            if info['status'] in ['Available', 'Reserved']]

        if not available_tables:
            print("No tables available!")
            return

        print("\nAvailable Tables:")
        for table in available_tables:
            print(f"Table {table} (Capacity: {self.tables[table]['capacity']})")

        table_num = input("\nEnter table number: ")
        if table_num not in available_tables:
            print("Invalid table selection!")
            return

        staff_id = input("Enter staff ID: ")
        if staff_id not in self.staff:
            print("Staff not found!")
            return

        # Show menu
        print("\nMenu Items:")
        self.view_menu()

        order_items = []
        while True:
            item_id = input("\nEnter item ID to add (or 'done' to finish): ")
            if item_id.lower() == 'done':
                break

            if item_id not in self.menu:
                print("Invalid item ID!")
                continue

            if not self.menu[item_id]['available']:
                print("Item not available!")
                continue

            quantity = int(input("Enter quantity: "))
            order_items.append({
                'item_id': item_id,
                'name': self.menu[item_id]['name'],
                'price': self.menu[item_id]['price'],
                'quantity': quantity
            })
            print(f"{quantity}x {self.menu[item_id]['name']} added to order")

        if not order_items:
            print("Order cancelled - no items added")
            return

        order_id = str(len(self.orders) + 1).zfill(4)
        total = sum(item['price'] * item['quantity'] for item in order_items)

        self.orders[order_id] = {
            'table': table_num,
            'staff': staff_id,
            'items': order_items,
            'total': total,
            'status': 'Pending',
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        # Update table status
        self.tables[table_num]['status'] = 'Occupied'

        print(f"\nOrder created! ID: {order_id}")
        print(f"Table: {table_num}")
        print(f"Total: ${total:.2f}")

    def view_active_orders(self):
        active_orders = [o for o in self.orders.values()
                         if o['status'] in ['Pending', 'Preparing', 'Served']]

        if not active_orders:
            print("No active orders!")
            return

        print("\n{:<8} {:<8} {:<15} {:<10} {:<10}".format(
            "Order", "Table", "Staff", "Status", "Total"))
        print("-" * 55)

        for order_id, order in self.orders.items():
            if order['status'] in ['Pending', 'Preparing', 'Served']:
                print("{:<8} {:<8} {:<15} {:<10} ${:<9.2f}".format(
                    order_id, order['table'], order['staff'],
                    order['status'], order['total']))

    def update_order_status(self):
        order_id = input("Enter order ID: ")
        if order_id not in self.orders:
            print("Order not found!")
            return

        order = self.orders[order_id]
        print(f"\nCurrent status: {order['status']}")
        print("1. Pending")
        print("2. Preparing")
        print("3. Served")
        print("4. Completed")
        print("5. Cancelled")

        choice = input("Enter new status (1-5): ")

        statuses = ['Pending', 'Preparing', 'Served', 'Completed', 'Cancelled']
        if choice in ['1', '2', '3', '4', '5']:
            new_status = statuses[int(choice) - 1]
            order['status'] = new_status

            # If order is completed or cancelled, free the table
            if new_status in ['Completed', 'Cancelled']:
                self.tables[order['table']]['status'] = 'Available'

            print(f"Order status updated to {new_status}")
        else:
            print("Invalid choice!")

    def view_order_history(self):
        if not self.orders:
            print("No order history!")
            return

        print("\n{:<8} {:<8} {:<15} {:<10} {:<15} {:<10}".format(
            "Order", "Table", "Staff", "Status", "Time", "Total"))
        print("-" * 75)

        for order_id, order in self.orders.items():
            print("{:<8} {:<8} {:<15} {:<10} {:<15} ${:<9.2f}".format(
                order_id, order['table'], order['staff'],
                order['status'], order['timestamp'], order['total']))

    def staff_management(self):
        while True:
            print("\n=== STAFF MANAGEMENT ===")
            print("1. Add Staff Member")
            print("2. View Staff")
            print("3. Update Staff Details")
            print("4. Back")

            choice = input("Enter choice (1-4): ")

            if choice == '1':
                self.add_staff()
            elif choice == '2':
                self.view_staff()
            elif choice == '3':
                self.update_staff()
            elif choice == '4':
                break
            else:
                print("Invalid choice!")

    def add_staff(self):
        staff_id = input("Enter staff ID: ")
        if staff_id in self.staff:
            print("Staff ID already exists!")
            return

        self.staff[staff_id] = {
            'name': input("Full name: "),
            'role': input("Role (Waiter/Chef/Manager): ").capitalize(),
            'phone': input("Phone: "),
            'hire_date': datetime.now().strftime("%Y-%m-%d")
        }
        print("Staff member added!")

    def view_staff(self):
        if not self.staff:
            print("No staff members!")
            return

        print("\n{:<10} {:<20} {:<15} {:<12}".format(
            "ID", "Name", "Role", "Hire Date"))
        print("-" * 60)

        for sid, staff in self.staff.items():
            print("{:<10} {:<20} {:<15} {:<12}".format(
                sid, staff['name'], staff['role'], staff['hire_date']))

    def update_staff(self):
        staff_id = input("Enter staff ID: ")
        if staff_id not in self.staff:
            print("Staff not found!")
            return

        staff = self.staff[staff_id]
        print("\nCurrent Details:")
        print(f"1. Name: {staff['name']}")
        print(f"2. Role: {staff['role']}")
        print(f"3. Phone: {staff['phone']}")

        field = input("\nEnter field to update (1-3) or 0 to cancel: ")

        if field == '0':
            return
        elif field == '1':
            staff['name'] = input("New name: ")
        elif field == '2':
            staff['role'] = input("New role: ").capitalize()
        elif field == '3':
            staff['phone'] = input("New phone: ")
        else:
            print("Invalid field!")

        print("Staff details updated!")

    def reports_menu(self):
        while True:
            print("\n=== REPORTS ===")
            print("1. Sales Report")
            print("2. Popular Items")
            print("3. Table Utilization")
            print("4. Back")

            choice = input("Enter choice (1-4): ")

            if choice == '1':
                self.sales_report()
            elif choice == '2':
                self.popular_items()
            elif choice == '3':
                self.table_utilization()
            elif choice == '4':
                break
            else:
                print("Invalid choice!")

    def sales_report(self):
        if not self.orders:
            print("No orders to report!")
            return

        total_sales = sum(order['total'] for order in self.orders.values())
        completed_orders = [o for o in self.orders.values() if o['status'] == 'Completed']
        completed_sales = sum(order['total'] for order in completed_orders)

        print("\n=== SALES REPORT ===")
        print(f"Total Orders: {len(self.orders)}")
        print(f"Total Sales: ${total_sales:.2f}")
        print(f"Completed Orders: {len(completed_orders)}")
        print(f"Completed Sales: ${completed_sales:.2f}")

    def popular_items(self):
        if not self.orders:
            print("No orders to analyze!")
            return

        item_counts = {}
        for order in self.orders.values():
            for item in order['items']:
                if item['name'] not in item_counts:
                    item_counts[item['name']] = 0
                item_counts[item['name']] += item['quantity']

        if not item_counts:
            print("No items ordered!")
            return

        sorted_items = sorted(item_counts.items(), key=lambda x: x[1], reverse=True)

        print("\n=== POPULAR ITEMS ===")
        print("{:<25} {:<10}".format("Item", "Quantity Sold"))
        print("-" * 35)

        for item, count in sorted_items[:10]:  # Show top 10
            print("{:<25} {:<10}".format(item, count))

    def table_utilization(self):
        if not self.orders:
            print("No orders to analyze!")
            return

        table_usage = {}
        for table_num in self.tables:
            table_usage[table_num] = 0

        for order in self.orders.values():
            if order['status'] != 'Cancelled':
                table_usage[order['table']] += 1

        print("\n=== TABLE UTILIZATION ===")
        print("{:<8} {:<15}".format("Table", "Orders Served"))
        print("-" * 25)

        for table, count in sorted(table_usage.items()):
            print("{:<8} {:<15}".format(table, count))


# Run the system
if __name__ == "__main__":
    restaurant = RestaurantSystem()
    restaurant.main_menu()