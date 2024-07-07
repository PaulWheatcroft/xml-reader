import os
from flask import (
    Flask,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Book, Country, book_country, db
from book import get_xml_book_details
import secrets

load_dotenv()

UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
ALLOWED_EXTENSIONS = os.getenv('ALLOWED_EXTENSIONS')
DB_URI = os.getenv('DB_URI')
USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')

app = Flask(__name__)

app.secret_key = secrets.token_hex(32)
if DB_URI:
    engine = create_engine(DB_URI)

app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db.init_app(app)


def allowed_file(filename):
    return (
        '.' in filename
        and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
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


def amend_countries_included(book_id, new_countries_included, filename):
    current_countries = set(
        row[0]
        for row in db.session.query(book_country.c.country_id)
        .filter_by(book_id=book_id)
        .all()
    )
    new_countries = []
    if new_countries_included[0] == "WORLD":
        new_countries = [country.id for country in Country.query.all()]
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
    os.rename(f"uploads/{filename}", f"uploads/archived_{filename}")


def read_xml(filename):
    response = get_xml_book_details(filename)
    book_details = response["book_details"]
    countries_included = response["countries_included"]

    book = Book.query.filter_by(id_value=book_details["id_value"]).first()
    if book is None:
        book = add_new_book(book_details)
    amend_countries_included(book.id, countries_included, filename)

    return make_response(response, 200)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_username = request.form.get('username')
    form_password = request.form.get('password')

    if form_username == USERNAME and form_password == PASSWORD:
        session['logged_in'] = True
        return redirect(url_for('upload_file'))
    else:
        return render_template('login.html', error='Invalid username or password')


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            if file.filename is not None:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                read_xml(filename)
                return render_template(
                    'upload_successful.html', title='Success'
                )
        return make_response('', 405)
    return render_template('upload.html', title='Home')


@app.route('/books')
def display_books():
    books = Book.query.all()
    return render_template('books.html', books=books)


if __name__ == "__main__":
    app.run()
