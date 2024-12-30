import xml.etree.ElementTree as ET

def parse_xml_to_dict(xml_data):
    """
    Parses XML data into a Python dictionary.
    """
    tree = ET.ElementTree(ET.fromstring(xml_data))
    root = tree.getroot()
    return {root.tag: root.attrib}
