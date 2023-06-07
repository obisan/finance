import os
import shutil
import subprocess
import zipfile
from io import BytesIO

# import PyPDF2
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage

from constants.enums import DailyBulletinSection


class DailyBulletinAnalysis:

    def __init__(self, storage_db, logger=None):
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

            sections = [str(DailyBulletinSection.EURO_DOLLAR_CALL.value)]

            for section in self.storage_db.get_dailybulletin_sections_by_section(sections):
                section_name = section[1]
                # section_filename = '\\'.join([target_dir, section_name]) + '.pdf'
                section_filename_pdf = os.path.join(target_dir, section_name) + '.pdf'
                section_filename_txt = os.path.join(target_dir, section_name) + '.txt'
                if os.path.exists(section_filename_pdf):
                    print(section_filename_pdf)
                    # section_filename = os.path.join(output_directory, unzipped_file, pdf_filename)
                    output = subprocess.check_output(
                        "Rscript read_pdf.R {} {}".format(section_filename_pdf, section_filename_txt))
                    output = output.decode('utf-8')

                    os.remove(section_filename_txt)

                    # print(output)
                    # self.exec_analysis_pdf_1(section_filename_pdf)

            # Delete the target directory after use
            if self.delete:
                shutil.rmtree(target_dir)

    def exec_analysis_pdf_1(self, pdf_path):
        with open(pdf_path, 'rb') as file:
            resource_manager = PDFResourceManager()
            output_string = BytesIO()  # Use BytesIO for binary output
            converter = TextConverter(resource_manager, output_string, laparams=LAParams())
            interpreter = PDFPageInterpreter(resource_manager, converter)

            target_text = "SR1 FUT"
            # print(target_text)

            for page in PDFPage.get_pages(file):
                interpreter.process_page(page)
                # ss_extracted_text = output_string.getvalue().decode()  # Decode binary data to string
                ss_extracted_text = output_string.getvalue()

                if ss_extracted_text.find(target_text.encode()) != -1:
                    for line in ss_extracted_text.split("\n".encode()):
                        print(line.decode())
                    break

                output_string.truncate(0)
                output_string.seek(0)

            extracted_text = ""

            converter.close()
            output_string.close()

            return extracted_text
