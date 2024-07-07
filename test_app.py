from models import Book


def test_new_book_filter_is_none(mocked_session):
    book_id_value = "333"
    book = mocked_session.query(Book).filter_by(id_value=book_id_value).first()
    assert book is None
