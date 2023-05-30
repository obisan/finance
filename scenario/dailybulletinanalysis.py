import os
import shutil
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

            for section in self.storage_db.get_dailybulletin_sections_by_id(sections)[:1]:
                pdf = '\\'.join([target_dir, section[1]]) + '.pdf'
                self.exec_analysis_pdf_1(pdf)

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

        # def exec_analysis_pdf_2(self, pdf_path):
        #     with open(pdf_path, 'rb') as file:
        #         pdf_reader = PyPDF2.PdfFileReader(file)
        #         num_pages = pdf_reader.numPages
        #         extracted_text = ''
        #
        #         target_line = 'EURO DOLLAR CALL OPTIONS'
        #
        #         for page_number in range(num_pages)[:1]:
        #             page = pdf_reader.getPage(page_number)
        #             content = page.extract_text()
        #
        #             if target_line in content:
        #                 lines = content.split('\n')
        #                 for line in lines:
        #                     print(line)
        #
        #             # extracted_text += page.extract_text()
        #
        #         return extracted_text
