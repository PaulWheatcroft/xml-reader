from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()
db = SQLAlchemy(model_class=Base)


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    product_id_type = Column(String(255))
    id_value = Column(String(255))
    title_text = Column(String(255))
    countries_included = db.relationship(
        'Country', secondary='book_country', backref='books'
    )

    def __init__(self, product_id_type, id_value, title_text):
        self.product_id_type = product_id_type
        self.id_value = id_value
        self.title_text = title_text


class Country(db.Model):
    __tablename__ = 'countries'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    country_short_code = Column(String(2))

    def __init__(self, country_short_code, name):
        self.name = name
        self.country_short_code = country_short_code


book_country = db.Table(
    'book_country',
    db.Column('book_id', db.Integer, db.ForeignKey('books.id')),
    db.Column('country_id', db.Integer, db.ForeignKey('countries.id')),
)
