from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session
from utils.book import get_xml_book_details


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)

engine = create_engine(
    "postgresql://admin:1AZwRsAH049P4132WG8Vmt2P@generally-busy-robin.a1.pgedge.io/perlego_interview?sslmode=require"
)

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
    name = db.Column(db.String(255))
    country_short_code = db.Column(db.String(2))

    def __init__(self, country_short_code, name):
        self.name = name
        self.country_short_code = country_short_code


book_country = db.Table(
    'book_country',
    db.Column('book_id', db.Integer, db.ForeignKey('books.id')),
    db.Column('country_id', db.Integer, db.ForeignKey('countries.id')),
)


@app.route('/', methods=['GET', 'POST'])
def home_page():
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

    book = Book.query.filter_by(id_value=book_details["id_value"]).first()
    if book is None:
        new_book = Book(
            id_value=book_details['id_value'],
            product_id_type=book_details['product_id_type'],
            title_text=book_details['title_text'],
        )
        db.session.add(new_book)
        db.session.commit()
        book_id = new_book.id
    else:
        book_id = book.id

    for country_short_code in countries_included:
        if country_short_code == "WORLD":
            break
        country = Country.query.filter_by(
            country_short_code=country_short_code
        ).first()
        if country:
            with Session(engine) as session:
                stmt = book_country.insert().values(
                    book_id=book_id, country_id=country.id
                )
                session.execute(stmt)
                session.commit()

    return jsonify(response)


@app.route('/books')
def display_books():
    books = Book.query.all()
    return render_template('books.html', books=books)


if __name__ == "__main__":
    app.run()
