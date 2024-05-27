import os
from flask import (
    Flask,
    flash,
    request,
    jsonify,
    render_template,
    redirect,
    make_response,
    url_for,
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session
from book import get_xml_book_details
import secrets

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'xml'}


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)


app.secret_key = secrets.token_hex(32)

engine = create_engine(
    "postgresql://admin:1AZwRsAH049P4132WG8Vmt2P@generally-busy-robin.a1.pgedge.io/perlego_interview?sslmode=require"
)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://admin:1AZwRsAH049P4132WG8Vmt2P@generally-busy-robin.a1.pgedge.io/perlego_interview?sslmode=require"
)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db.init_app(app)


def allowed_file(filename):
    return (
        '.' in filename
        and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    )


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


def add_new_book(book_details):
    new_book = Book(
        id_value=book_details['id_value'],
        product_id_type=book_details['product_id_type'],
        title_text=book_details['title_text'],
    )
    db.session.add(new_book)
    db.session.commit()
    return new_book


def amend_countries_included(book_id, new_countries_included):
    current_countries = set(
        row[0]
        for row in db.session.query(book_country.c.country_id)
        .filter_by(book_id=book_id)
        .all()
    )
    new_countries = []
    if new_countries_included[0] == "WORLD":
        new_countries = Country.query.all()
    else:
        for country in new_countries_included:
            include_country = Country.query.filter_by(
                country_short_code=country
            ).first()
            if include_country:
                new_countries.append(include_country.id)
            else:
                print(f'Country code {country} does not exist')
    countries_to_add = set(new_countries) - current_countries
    countries_to_remove = current_countries - set(new_countries)
    for country_id in countries_to_add:
        with Session(engine) as session:
            session.execute(
                book_country.insert().values(
                    book_id=book_id, country_id=country_id
                )
            )
            session.commit()
    for country_id in countries_to_remove:
        with Session(engine) as session:
            session.execute(
                book_country.delete().where(
                    book_country.c.book_id == book_id,
                    book_country.c.country_id == country_id,
                )
            )
            session.commit()


# @app.route("/read_xml")
def read_xml(filename):
    response = get_xml_book_details(filename)
    book_details = response["book_details"]
    countries_included = response["countries_included"]

    book = Book.query.filter_by(id_value=book_details["id_value"]).first()
    if book is None:
        book = add_new_book(book_details)
    amend_countries_included(book.id, countries_included)

    return make_response(response, 200)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            if file.filename is not None:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                read_xml(filename)
                return make_response(
                    'File uploaded',
                    200,
                )
            else:
                return make_response('File name not supported', 400)
        return make_response('', 405)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/books')
def display_books():
    books = Book.query.all()
    return render_template('books.html', books=books)


if __name__ == "__main__":
    app.run()
