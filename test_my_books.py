import pytest
from datetime import datetime, timedelta
from main import (
    Book,
    load_books_from_csv,
    select_books,
    calculate_due_date,
    calculate_late_fee
)
# Mock data for testing
mock_books = [
    Book("Book1", "Author1", 5),
    Book("Book2", "Author2", 10),
    Book("Book3", "Author3", 0),
    Book("Book4", "Author4", 3)
]

def test_load_books_from_csv():
    file_path = 'books.csv'
    books = load_books_from_csv(file_path)
    assert len(books) > 0  # Assuming the test CSV file contains at least one book entry

def test_select_books():
    selected_books = select_books(mock_books)
    assert selected_books != -1  # Asserts that selected_books is not -1, indicating a successful selection

def test_select_books_max_limit():
    too_many_books = [
        Book(f"Book{i}", f"Author{i}", 1) for i in range(15)
    ]
    selected_books = select_books(too_many_books)
    assert selected_books == -1  # Asserts that -1 is returned for exceeding the maximum limit

def test_calculate_due_date():
    current_date = datetime.now()
    due_date = calculate_due_date(current_date)
    assert due_date == current_date + timedelta(days=14)  # Asserts due date calculation

def test_calculate_late_fee():
    current_date = datetime.now()
    past_date = current_date - timedelta(days=5)
    late_fee = calculate_late_fee(past_date)
    assert late_fee == 5  # Assuming $1 per day for 5 days, late fee should be 5

if __name__ == '__main__':
    pytest.main()
