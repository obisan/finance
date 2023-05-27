import os
import shutil
import zipfile

from constants.enums import DailyBulletinSection


class DailyBulletinAnalysis:

    def __init__(self, storage_db):
        self.storage_db = storage_db
        self.delete = False

    def analysis(self):
        for line in self.storage_db.get_dailybulletin_reports()[:1]:
            # r'\\xxx\storage\finance_storage\DailyBulletin\test\DailyBulletin_pdf_202301031.zip'
            zip_file_path = line[1]

            # Calculate the base directory from the ZIP file path
            base_dir = os.path.dirname(zip_file_path)

            # Calculate the target directory based on the ZIP file name
            zip_file_name = os.path.basename(zip_file_path)
            target_dir_name = os.path.splitext(zip_file_name)[0]
            target_dir = os.path.join(base_dir, target_dir_name)

            # Create the target directory if it doesn't exist
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(target_dir)

            sections = [DailyBulletinSection.EURO_DOLLAR_CALL.value, DailyBulletinSection.EURO_DOLLAR_PUT.value]

            for line in self.storage_db.get_dailybulletin_sections_by_id(sections)[:1]:
                pdf = '\\'.join([target_dir, line[1]]) + '.pdf'
                print(pdf)

            # Delete the target directory after use
            if self.delete:
                shutil.rmtree(target_dir)
