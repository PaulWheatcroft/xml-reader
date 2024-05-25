import xml.etree.ElementTree as ET
from flask import Flask, Response, request, jsonify
import re

from utils.book import get_book_details

app = Flask(__name__)


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
    response = get_book_details()
    return jsonify(response)


if __name__ == "__main__":
    app.run()
