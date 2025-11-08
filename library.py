import json
from datetime import datetime, timedelta
class LibrarySystem:
    def __init__(self):
        self.books = self.load_data('books.json')
        self.members = self.load_data('members.json')
        self.transactions = self.load_data('transactions.json')

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
            print("\n=== LIBRARY MANAGEMENT ===")
            print("1. Book Management")
            print("2. Member Management")
            print("3. Book Transactions")
            print("4. Reports")
            print("5. Exit")

            choice = input("Enter choice (1-5): ")

            if choice == '1':
                self.book_menu()
            elif choice == '2':
                self.member_menu()
            elif choice == '3':
                self.transaction_menu()
            elif choice == '4':
                self.report_menu()
            elif choice == '5':
                self.save_all()
                print("Data saved. Exiting...")
                break
            else:
                print("Invalid choice!")

    def save_all(self):
        self.save_data(self.books, 'books.json')
        self.save_data(self.members, 'members.json')
        self.save_data(self.transactions, 'transactions.json')

    def book_menu(self):
        while True:
            print("\n=== BOOK MANAGEMENT ===")
            print("1. Add Book")
            print("2. View All Books")
            print("3. Search Book")
            print("4. Update Book")
            print("5. Back")

            choice = input("Enter choice (1-5): ")

            if choice == '1':
                self.add_book()
            elif choice == '2':
                self.view_books()
            elif choice == '3':
                self.search_book()
            elif choice == '4':
                self.update_book()
            elif choice == '5':
                break
            else:
                print("Invalid choice!")

    def add_book(self):
        isbn = input("Enter ISBN: ")
        if isbn in self.books:
            print("Book already exists!")
            return

        self.books[isbn] = {
            'title': input("Title: "),
            'author': input("Author: "),
            'publisher': input("Publisher: "),
            'year': input("Year: "),
            'copies': int(input("Copies: ")),
            'available': int(input("Copies: "))  # Start with all copies available
        }
        print("Book added!")

    def view_books(self):
        if not self.books:
            print("No books in library!")
            return

        print("\n{:<15} {:<25} {:<20} {:<10} {:<6} {:<6}".format(
            "ISBN", "Title", "Author", "Year", "Total", "Avail."))
        print("-" * 85)

        for isbn, book in self.books.items():
            print("{:<15} {:<25} {:<20} {:<10} {:<6} {:<6}".format(
                isbn, book['title'], book['author'],
                book['year'], book['copies'], book['available']))

    def search_book(self):
        term = input("Enter ISBN, title or author: ").lower()
        found = False

        print("\n{:<15} {:<25} {:<20} {:<6}".format(
            "ISBN", "Title", "Author", "Avail."))
        print("-" * 70)

        for isbn, book in self.books.items():
            if (term in isbn.lower() or
                    term in book['title'].lower() or
                    term in book['author'].lower()):
                print("{:<15} {:<25} {:<20} {:<6}".format(
                    isbn, book['title'], book['author'], book['available']))
                found = True

        if not found: print("No matches found!")

    def update_book(self):
        isbn = input("Enter ISBN of book to update: ")
        if isbn not in self.books:
            print("Book not found!")
            return

        book = self.books[isbn]
        print("\nCurrent Details:")
        print(f"1. Title: {book['title']}")
        print(f"2. Author: {book['author']}")
        print(f"3. Publisher: {book['publisher']}")
        print(f"4. Year: {book['year']}")
        print(f"5. Total Copies: {book['copies']}")

        field = input("\nEnter field to update (1-5) or 0 to cancel: ")

        if field == '0':
            return
        elif field == '1':
            book['title'] = input("New title: ")
        elif field == '2':
            book['author'] = input("New author: ")
        elif field == '3':
            book['publisher'] = input("New publisher: ")
        elif field == '4':
            book['year'] = input("New year: ")
        elif field == '5':
            new_copies = int(input("New total copies: "))
            diff = new_copies - book['copies']
            book['copies'] = new_copies
            book['available'] += diff
        else:
            print("Invalid field!")

        print("Book updated!")

    def member_menu(self):
        while True:
            print("\n=== MEMBER MANAGEMENT ===")
            print("1. Add Member")
            print("2. View Members")
            print("3. Search Member")
            print("4. Back")

            choice = input("Enter choice (1-4): ")

            if choice == '1':
                self.add_member()
            elif choice == '2':
                self.view_members()
            elif choice == '3':
                self.search_member()
            elif choice == '4':
                break
            else:
                print("Invalid choice!")

    def add_member(self):
        mid = input("Enter member ID: ")
        if mid in self.members:
            print("Member ID already exists!")
            return

        self.members[mid] = {
            'name': input("Name: "),
            'email': input("Email: "),
            'phone': input("Phone: "),
            'join_date': datetime.now().strftime("%Y-%m-%d"),
            'books_borrowed': 0
        }
        print("Member added!")

    def view_members(self):
        if not self.members:
            print("No members!")
            return

        print("\n{:<10} {:<20} {:<15} {:<10}".format(
            "ID", "Name", "Phone", "Borrowed"))
        print("-" * 55)

        for mid, member in self.members.items():
            print("{:<10} {:<20} {:<15} {:<10}".format(
                mid, member['name'], member['phone'], member['books_borrowed']))

    def search_member(self):
        term = input("Enter ID or name: ").lower()
        found = False

        print("\n{:<10} {:<20} {:<15}".format("ID", "Name", "Phone"))
        print("-" * 45)

        for mid, member in self.members.items():
            if term in mid.lower() or term in member['name'].lower():
                print("{:<10} {:<20} {:<15}".format(mid, member['name'], member['phone']))
                found = True

        if not found: print("No matches found!")

    def transaction_menu(self):
        while True:
            print("\n=== BOOK TRANSACTIONS ===")
            print("1. Issue Book")
            print("2. Return Book")
            print("3. View Transactions")
            print("4. Back")

            choice = input("Enter choice (1-4): ")

            if choice == '1':
                self.issue_book()
            elif choice == '2':
                self.return_book()
            elif choice == '3':
                self.view_transactions()
            elif choice == '4':
                break
            else:
                print("Invalid choice!")

    def issue_book(self):
        mid = input("Enter member ID: ")
        if mid not in self.members:
            print("Invalid member ID!")
            return

        isbn = input("Enter ISBN: ")
        if isbn not in self.books:
            print("Invalid ISBN!")
            return

        if self.books[isbn]['available'] <= 0:
            print("No copies available!")
            return

        if self.members[mid]['books_borrowed'] >= 3:
            print("Member has reached borrowing limit (3 books)!")
            return

        tid = str(len(self.transactions) + 1).zfill(4)
        due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

        self.transactions[tid] = {
            'member': mid,
            'book': isbn,
            'issue_date': datetime.now().strftime("%Y-%m-%d"),
            'due_date': due_date,
            'return_date': "",
            'status': 'issued'
        }

        # Update counts
        self.books[isbn]['available'] -= 1
        self.members[mid]['books_borrowed'] += 1

        print(f"Book issued! Transaction ID: {tid}")
        print(f"Due date: {due_date}")

    def return_book(self):
        tid = input("Enter transaction ID: ")
        if tid not in self.transactions or self.transactions[tid]['status'] == 'returned':
            print("Invalid transaction ID or book already returned!")
            return

        trans = self.transactions[tid]
        trans['return_date'] = datetime.now().strftime("%Y-%m-%d")
        trans['status'] = 'returned'

        # Update counts
        self.books[trans['book']]['available'] += 1
        self.members[trans['member']]['books_borrowed'] -= 1

        # Check for late return
        return_date = datetime.strptime(trans['return_date'], "%Y-%m-%d")
        due_date = datetime.strptime(trans['due_date'], "%Y-%m-%d")

        if return_date > due_date:
            days_late = (return_date - due_date).days
            print(f"Book returned {days_late} days late! Fine: ${days_late * 0.50}")
        else:
            print("Book returned on time!")

    def view_transactions(self):
        if not self.transactions:
            print("No transactions!")
            return

        print("\n{:<5} {:<10} {:<15} {:<12} {:<12} {:<12} {:<8}".format(
            "ID", "Member", "Book", "Issued", "Due", "Returned", "Status"))
        print("-" * 80)

        for tid, trans in self.transactions.items():
            print("{:<5} {:<10} {:<15} {:<12} {:<12} {:<12} {:<8}".format(
                tid,
                trans['member'],
                trans['book'],
                trans['issue_date'],
                trans['due_date'],
                trans['return_date'] if trans['return_date'] else "N/A",
                trans['status']))

    def report_menu(self):
        while True:
            print("\n=== REPORTS ===")
            print("1. Books Available")
            print("2. Books Checked Out")
            print("3. Overdue Books")
            print("4. Member Borrowing History")
            print("5. Back")

            choice = input("Enter choice (1-5): ")

            if choice == '1':
                self.available_books()
            elif choice == '2':
                self.checked_out_books()
            elif choice == '3':
                self.overdue_books()
            elif choice == '4':
                self.member_history()
            elif choice == '5':
                break
            else:
                print("Invalid choice!")

    def available_books(self):
        print("\n=== AVAILABLE BOOKS ===")
        available = [b for b in self.books.values() if b['available'] > 0]

        if not available:
            print("No books available!")
            return

        print("\n{:<15} {:<25} {:<20}".format("ISBN", "Title", "Author"))
        print("-" * 60)

        for book in available:
            print("{:<15} {:<25} {:<20}".format(
                next(isbn for isbn, b in self.books.items() if b == book),
                book['title'], book['author']))

    def checked_out_books(self):
        print("\n=== CHECKED OUT BOOKS ===")
        checked_out = [t for t in self.transactions.values() if t['status'] == 'issued']

        if not checked_out:
            print("No books checked out!")
            return

        print("\n{:<15} {:<20} {:<10} {:<12} {:<12}".format(
            "Book", "Member", "Issued", "Due", "Days Left"))
        print("-" * 75)

        today = datetime.now()
        for trans in checked_out:
            due_date = datetime.strptime(trans['due_date'], "%Y-%m-%d")
            days_left = (due_date - today).days

            book = self.books[trans['book']]
            member = self.members[trans['member']]

            print("{:<15} {:<20} {:<10} {:<12} {:<12}".format(
                book['title'],
                member['name'],
                trans['issue_date'],
                trans['due_date'],
                days_left if days_left > 0 else "OVERDUE"))

    def overdue_books(self):
        print("\n=== OVERDUE BOOKS ===")
        today = datetime.now()
        overdue = [
            t for t in self.transactions.values()
            if t['status'] == 'issued' and
               datetime.strptime(t['due_date'], "%Y-%m-%d") < today
        ]

        if not overdue:
            print("No overdue books!")
            return

        print("\n{:<15} {:<20} {:<10} {:<12} {:<12}".format(
            "Book", "Member", "Issued", "Due", "Days Overdue"))
        print("-" * 75)

        for trans in overdue:
            due_date = datetime.strptime(trans['due_date'], "%Y-%m-%d")
            days_overdue = (today - due_date).days

            book = self.books[trans['book']]
            member = self.members[trans['member']]

            print("{:<15} {:<20} {:<10} {:<12} {:<12}".format(
                book['title'],
                member['name'],
                trans['issue_date'],
                trans['due_date'],
                days_overdue))

    def member_history(self):
        mid = input("Enter member ID: ")
        if mid not in self.members:
            print("Invalid member ID!")
            return

        history = [t for t in self.transactions.values() if t['member'] == mid]

        if not history:
            print("No borrowing history!")
            return

        print(f"\n=== BORROWING HISTORY FOR {self.members[mid]['name'].upper()} ===")
        print("\n{:<5} {:<15} {:<12} {:<12} {:<12} {:<8}".format(
            "ID", "Book", "Issued", "Due", "Returned", "Status"))
        print("-" * 70)

        for trans in history:
            book = self.books[trans['book']]

            print("{:<5} {:<15} {:<12} {:<12} {:<12} {:<8}".format(
                next(tid for tid, t in self.transactions.items() if t == trans),
                book['title'],
                trans['issue_date'],
                trans['due_date'],
                trans['return_date'] if trans['return_date'] else "N/A",
                trans['status']))


# Run the system
if __name__ == "__main__":
    library = LibrarySystem()
    library.main_menu()