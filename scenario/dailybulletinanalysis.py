import os
import shutil
import zipfile

from cme import Euro_FX
from constants.enums import DailyBulletinSection
from convert.converter import ConverterPDFtoTXT


class DailyBulletinAnalysis:

    def __init__(self, storage_db, repository=None, logger=None):
        self.storage_db = storage_db
        self.logger = logger
        self.delete = False

    def analysis(self):
        for line in self.storage_db.get_dailybulletin_reports()[1:2]:
            # r'\\xxx\storage\finance_storage\DailyBulletin\test\DailyBulletin_pdf_202301031.zip'
            bulletin_name = line[0]
            bulletin_filepath = line[1]

            # Calculate the base directory from the ZIP file path
            bulletin_dir = os.path.dirname(bulletin_filepath)

            # Calculate the target directory based on the ZIP file name
            target_dir = os.path.join(bulletin_dir, bulletin_name)

            # Create the target directory if it doesn't exist
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

            with zipfile.ZipFile(bulletin_filepath, 'r') as zip_ref:
                zip_ref.extractall(target_dir)

            sections = [str(DailyBulletinSection.EURO_FX.value)]

            for section in self.storage_db.get_dailybulletin_sections_by_section(sections):
                section_name = section[1]
                section_filename_pdf = os.path.join(target_dir, section_name) + '.pdf'
                section_filename_txt = os.path.join(target_dir, section_name) + '.txt'

                section_content = \
                    ConverterPDFtoTXT(section_filename_pdf, section_filename_txt, self.logger).get_string()

                euro_fx = Euro_FX()
                euro_fx.exec(section_content)

            # Delete the target directory after use
            if self.delete:
                shutil.rmtree(target_dir)
