import pytest
from models import Base


@pytest.fixture(scope="function")
def sqlalchemy_declarative_base():
    return Base


@pytest.fixture(scope="function")
def sqlalchemy_mock_books():
    return [
        (
            "books",
            [
                {
                    "id": 1,
                    "product_id_type": "15",
                    "id_value": "111",
                    "title_text": "First",
                },
                {
                    "id": 2,
                    "product_id_type": "15",
                    "id_value": "222",
                    "title_text": "Second",
                },
            ],
        )
    ]
