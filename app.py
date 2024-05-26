from flask import Flask, request, jsonify
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
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
    return jsonify(response)


if __name__ == "__main__":
    app.run()
