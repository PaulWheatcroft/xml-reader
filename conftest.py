import pytest
from models import Base, Book


@pytest.fixture(scope="function")
def sqlalchemy_declarative_base():
    return Base

book1 = Book(1, 111, "first")
book2 = Book(2, 222, "second")


@pytest.fixture(scope="function")
def sqlalchemy_mock_books():
    return [book1, book2]
