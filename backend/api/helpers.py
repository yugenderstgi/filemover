import xmltodict
import json





def convert_dict_to_xml(data_dict):
    xml_str = xmltodict.unparse(data_dict, pretty=True )
    xml_str = xml_str.replace('<?xml version="1.0" encoding="utf-8"?>', '')

    xml_str = xml_str.strip()  # Remove leading/trailing whitespace
    if xml_str.startswith('\n'):
        xml_str = xml_str[1:]     # Remove leading newline character
    return xml_str

