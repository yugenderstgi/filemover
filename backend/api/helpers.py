import xmltodict
import json

# import xml.etree.ElementTree as ET

# import xml.etree.ElementTree as ET

def convert_dict_to_xml(data_dict):
    xml_str = xmltodict.unparse(data_dict, pretty=True )
    xml_str = xml_str.replace('<?xml version="1.0" encoding="utf-8"?>', '')

    xml_str = xml_str.strip()  # Remove leading/trailing whitespace
    if xml_str.startswith('\n'):
        xml_str = xml_str[1:]     # Remove leading newline character
    return xml_str

def xml_to_json(xml_input):
    # Parse the XML input into a dictionary
    xml_bytes = xml_input.encode('utf-8')
    xml_dict = xmltodict.parse(xml_input, force_list=False)
    
    json_output = json.dumps(xml_dict)
    
    return json_output

# def get_transform_name(action_parms):
#         if action_parms:
#             try:
#                 root = ET.fromstring(action_parms)
#                 transform_name = root.find('transform_name').text
#                 return transform_name
#             except (ET.ParseError, AttributeError):
#                 pass
#         return None

# def get_action_parms(xml_data):
#         # xml_data = obj.action_parms
#         print("xml :",xml_data)
#         dict_data = xmltodict.parse(xml_data)
#         print("???",dict_data)
#         if obj.action_type=='Unzip':
#             return dict_data
#         transform_params = dict_data['params']['transform_params']
#         print("$$$",transform_params)
#         if transform_params:
#             # Preprocess the transform_params XML content
#             preprocess_xml = f"<root>{transform_params}</root>"

#             # Parse the preprocessed XML content
#             parsed_data = xmltodict.parse(preprocess_xml)

#             # Extract the transformed parameters
#             transform_params = parsed_data['root']
        
#         dict_data['params']['transform_params'] = transform_params
#         return dict_data






# import xml.etree.ElementTree as ET

# def dict2xml(data_dict):
#     root = ET.Element('params')
#     for key, value in data_dict.items():
#         if isinstance(value, dict):
#             sub_element = ET.SubElement(root, key)
#             for k, v in value.items():
#                 element = ET.SubElement(sub_element, k)
#                 element.text = str(v)
#         else:
#             element = ET.SubElement(root, key)
#             element.text = str(value)
#     xml_str = ET.tostring(root).decode('utf-8')
#     return xml_str








# def convert_nested_dict_to_xml(data_dict):
#         for key, value in data_dict.items():
#             if isinstance(value, dict):
#                 if all(isinstance(v, (str, bool, int, float)) for v in value.values()):
#                     data_dict[key] = xmltodict.unparse({key: value}, pretty=True)
#         return data_dict
    









# def convert_dict_to_xml(data_dict):
#     root = convert_dict_to_xml_recursive(data_dict)
#     xml_string = ET.tostring(root, encoding='unicode', method='xml')
#     return xml_string

# def convert_dict_to_xml_recursive(data_dict):
#     root = None
#     for key, value in data_dict.items():
#         if isinstance(value, dict):
#             element = convert_dict_to_xml_recursive(value)
#             if root is None:
#                 root = element
#             else:
#                 root.append(element)
#         else:
#             element = ET.Element(key)
#             element.text = str(value)
#             if root is None:
#                 root = element
#             else:
#                 root.append(element)
#     return root

# class help:



    def convert_nested_dict_to_xml(self, data_dict):
        for key, value in data_dict.items():
            if isinstance(value, dict):
                if all(isinstance(v, (str, bool, int, float)) for v in value.values()):
                    data_dict[key] = xmltodict.unparse({key: value}, pretty=True)
        return data_dict
    
# object=help()