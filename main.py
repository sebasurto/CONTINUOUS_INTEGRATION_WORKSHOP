import csv
from datetime import datetime, timedelta

class Book:
    def __init__(self, title, author, available_quantity):
        self.title = title
        self.author = author
        self.available_quantity = available_quantity

def load_books_from_csv(file_path):
    books = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            book = Book(row['Title'], row['Author'], row['Quantity'])
            books.append(book)
    return books

def display_catalog(books):
    print("Catalog of Available Books:")
    print("{:<40} {:<30} {:<20}".format("Title", "Author", "Available Quantity"))
    for book in books:
        print("{:40} {:<30} {:<20}".format(book.title, book.author, book.available_quantity))


def select_books(books, selected_titles):
    selected_books = []
    for book_title in selected_titles:
        found_book = next((book for book in books if book.title.lower() == book_title.lower() and book.available_quantity > 0), None)
        if found_book:
            quantity = 1  # Assuming 1 copy by default for simplicity in testing
            if quantity <= found_book.available_quantity:
                selected_books.append((found_book, quantity))
                found_book.available_quantity -= quantity
    if len(selected_books) > 10:
        return -1
    return selected_books


def calculate_due_date(current_date):
    return current_date + timedelta(days=14)

def calculate_late_fee(due_date):
    today = datetime.now()
    if today > due_date:
        return (today - due_date).days * 1
    return 0

def checkout(selected_books):
    if selected_books == -1:
        return -1

    print("\nSelected Books for Checkout:")
    print("Title\t\tQuantity\tDue Date\tLate Fee")
    for book, quantity in selected_books:
        due_date = calculate_due_date(datetime.now())
        late_fee = calculate_late_fee(due_date)
        print(f"{book.title}\t{quantity}\t\t{due_date.strftime('%Y-%m-%d')}\t{late_fee}")

def return_books(books):
    returned_books = []
    while True:
        book_title = input("Enter the title of the book you are returning (or type 'done' to finish): ")
        if book_title.lower() == 'done':
            break
        found_book = next((book for book in books if book.title.lower() == book_title.lower()), None)
        if found_book:
            quantity = input(f"How many copies of '{found_book.title}' are you returning? Enter quantity: ")
            if quantity.isdigit() and int(quantity) > 0:
                quantity = int(quantity)
                found_book.available_quantity += quantity
                returned_books.append((found_book, quantity))
            else:
                print("Invalid quantity. Please enter a positive integer greater than zero.")
        else:
            print(f"'{book_title}' is not a valid book to return.")

    total_late_fees = sum(calculate_late_fee(calculate_due_date(datetime.now())) for book, _ in returned_books)
    print(f"\nTotal late fees for returned books: ${total_late_fees}")

def main():
    books = load_books_from_csv('books.csv')
    display_catalog(books)

    action = input("What would you like to do? (checkout/return): ")
    if action.lower() == 'checkout':
        selected_books = select_books(books)
        checkout(selected_books)
    elif action.lower() == 'return':
        return_books(books)
    else:
        print("Invalid action. Please choose either 'checkout' or 'return'.")

if __name__ == "__main__":
    main()
