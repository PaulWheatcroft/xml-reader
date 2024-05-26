from flask import Flask, request, jsonify, render_template
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from utils.book import get_xml_book_details

print(os.environ.get('VIRTUAL_ENV'))


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://admin:1AZwRsAH049P4132WG8Vmt2P@generally-busy-robin.a1.pgedge.io/perlego_interview?sslmode=require"
)

db.init_app(app)


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    product_id_type = db.Column(db.String(255))
    id_value = db.Column(db.String(255))
    title_text = db.Column(db.String(255))
    countries_included = db.relationship(
        'Country', secondary='book_country', backref='books'
    )

    def __init__(self, product_id_type, id_value, title_text):
        self.product_id_type = product_id_type
        self.id_value = id_value
        self.title_text = title_text


class Country(db.Model):
    __tablename__ = 'countries'
    id = db.Column(db.Integer, primary_key=True)
    country_short_code = db.Column(db.String(2))


book_country = db.Table(
    'book_country',
    db.Column('book_id', db.Integer, db.ForeignKey('books.id')),
    db.Column('country_id', db.Integer, db.ForeignKey('countries.id')),
)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        file = request.files['xml_file']
        if file:
            # Save the uploaded file to the data folder
            file.save('data/uploaded_file.xml')
            return 'File uploaded successfully!'
        else:
            return 'No file selected.'

    return '''
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="xml_file">
            <input type="submit" value="Upload">
        </form>
    '''


@app.route("/read_xml")
def read_xml():
    response = get_xml_book_details()
    book_details = response["book_details"]
    countries_included = response["countries_included"]
    book = Book.query.filter_by(
        id_value=response["book_details"]["id_value"]
    ).first()
    if book is None:
        print("Make a book")
        book = Book(
            book_details['id_value'],
            book_details['product_id_type'],
            book_details['title_text'],
        )
        db.session.add(book)
        db.session.commit()

    print(response["book_details"]["id_value"])
    print(book)
    return jsonify(response)


@app.route('/books')
def display_books():
    books = Book.query.all()
    return render_template('books.html', books=books)


if __name__ == "__main__":
    app.run()
