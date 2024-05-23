import xml.etree.ElementTree as ET


def clear_xml_file():
    root = ET.Element("users")

    tree = ET.ElementTree(root)

    tree.write("users.xml")


class Registry:
    def __init__(self):
        self.message_status = {}
        self.user_id = []
        self.user_mail = None
        self.broadcast_status = False
        self.register_status = False

    @staticmethod
    def write_to_xml(name, id_user, email):
        try:
            tree = ET.parse('users.xml')
            root = tree.getroot()
        except FileNotFoundError:
            root = ET.Element("users")
            tree = ET.ElementTree(root)

        for existing_user in root.findall('user'):
            user_id = existing_user.find('id').text
            if user_id == id_user:
                print(f"Пользователь с email {email} уже существует.")
                return

        user_element = ET.SubElement(root, "user")

        name_element = ET.SubElement(user_element, "name")
        name_element.text = name

        email_element = ET.SubElement(user_element, "email")
        email_element.text = email

        id_element = ET.SubElement(user_element, "id")
        id_element.text = id_user

        tree = ET.ElementTree(root)
        tree.write("users.xml", encoding="utf-8", xml_declaration=True)

    @staticmethod
    def get_xml_field(field):
        tree = ET.parse('users.xml')
        root = tree.getroot()

        user_fields = []

        for user in root.findall('user'):
            name = user.find(field).text
            user_fields.append(name)

        return user_fields
