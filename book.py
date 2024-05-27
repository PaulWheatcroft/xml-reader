import xml.etree.ElementTree as ET
import re

book_details = {"product_id_type": "", "id_value": "", "title_text": ""}
countries_included = []


def extract_book_details_from_xml(xml_content):
    root = ET.fromstring(xml_content)
    book_details = {}
    countries_included = []

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
            countries_included.extend(re.split(r'\s+', string_countries))

    return {
        "book_details": book_details,
        "countries_included": countries_included,
    }


def get_xml_book_details(filename):
    xml_content = None
    xml_file_path = f"uploads/{filename}"

    with open(xml_file_path, "r") as file:
        xml_content = file.read()

    book_details = extract_book_details_from_xml(xml_content)

    return book_details
