import xml.etree.ElementTree as ET
from flask import Flask, Response, request

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
    print("****")
    xml_content = None
    xml_file_path = "sample_data/1.xml"
    with open(xml_file_path, "r") as file:
        xml_content = file.read()

    root = ET.fromstring(xml_content)
    print("root", root)
    response_content = "Wot u looking at"

    return Response(response_content, mimetype="text/plain")


if __name__ == "__main__":
    app.run()
