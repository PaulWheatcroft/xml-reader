import pytest
from pytest_mock import mocker
from unittest.mock import MagicMock
from app import app, add_new_book, DB_URI
from models import Book, db

@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            yield client

@pytest.fixture
def mock_test_database(monkeypatch):
    """Set the DEFAULT_CONFIG database to test_db."""
    monkeypatch.setitem(db, "database", "test_db")

def test_add_new_book_to_existing_database(client, mock_test_database):
    print("^^^^^^^^", mock_test_database)
    book = {'id_value': '789', 'product_id_type': 'book', 'title_text': 'Book 3'}
    
    # Call the add_new_book function with the mocked db session
    new_book = add_new_book(book, mock_test_database)

    # Assertion statements for the new book
    assert isinstance(new_book, Book)
    assert new_book.id_value == '789'
    assert new_book.product_id_type == 'book'
    assert new_book.title_text == 'Book 3'
