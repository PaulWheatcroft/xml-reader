import xml.etree.ElementTree as ET
from flask import jsonify
import re


book_details = {"product_id_type": "", "id_value": "", "title_text": ""}
countries_included = []


def get_book_details():
    xml_content = None
    xml_file_path = "sample_data/4.xml"

    with open(xml_file_path, "r") as file:
        xml_content = file.read()

    root = ET.fromstring(xml_content)
    for element in root.iter():
        if element.tag in ['ProductIDType', 'b221'] and element.text:
            book_details['product_id_type'] = element.text
        if element.tag in ['IDValue', 'b244'] and element.text:
            book_details['id_value'] = element.text
        if element.tag in ['TitleText', 'b203'] and element.text:
            book_details['title_text'] = element.text
        if (
            element.tag in ['x450', 'x449', 'CountriesIncluded']
            and element.text
        ):
            string_countries = element.text
            countries_included.append(re.split(r'\s+', string_countries))

    response_data = {
        "book_details": book_details,
        "countries_included": countries_included,
    }

    return response_data
