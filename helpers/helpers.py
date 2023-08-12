from bs4 import BeautifulSoup


class Helper:

    @staticmethod
    def get_settings(xml_data):
        soup = BeautifulSoup(xml_data, "xml")

        result = {
            'filename': soup.find("config").find("connect").text,
            'mode': soup.find("config").find("mode").text,
            'repository': soup.find("config").find("repository").text}
        return result
