import unittest
from unittest.mock import patch, Mock
from models import Country, db, book_country
from app import add_new_book, amend_countries_included, Session, engine
import os


class TestAddNewBook(unittest.TestCase):

    @patch('app.db.session')
    def test_add_new_book(self):
        book_details = {
            'id_value': '123',
            'product_id_type': '15',
            'title_text': 'Test Book',
        }

        new_book = add_new_book(book_details)
        print(new_book.title_text)
        assert new_book.id_value is book_details['id_value']
        assert new_book.product_id_type is book_details['product_id_type']
        assert new_book.title_text is book_details['title_text']
