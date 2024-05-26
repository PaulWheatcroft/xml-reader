# from sqlalchemy import Integer, String
# from sqlalchemy.orm import Mapped, mapped_column


# class Book(db.Model):
#     __tablename__ = 'books'
#     id = db.Column(db.Integer, primary_key=True)
#     product_id_type = db.Column(db.String(255))
#     id_value = db.Column(db.String(255))
#     title_text = db.Column(db.String(255))
#     countries_included = db.relationship(
#         'Country', secondary='book_country', backref='books'
#     )


# class Country(db.Model):
#     __tablename__ = 'countries'
#     id = db.Column(db.Integer, primary_key=True)
#     country_short_code = db.Column(db.String(2))


# book_country = db.Table(
#     'book_country',
#     db.Column('book_id', db.Integer, db.ForeignKey('books.id')),
#     db.Column('country_id', db.Integer, db.ForeignKey('countries.id')),
# )
