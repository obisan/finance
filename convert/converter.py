import os
import subprocess


class ConverterPDFtoTXT:

    def __init__(self, filename_pdf, filename_txt, logger=None):
        self.filename_pdf = filename_pdf
        self.filename_txt = filename_txt
        self.logger = logger
        self.delete = False

    def convert(self):
        if os.path.exists(self.filename_pdf):
            try:
                output = subprocess.check_output(
                    ["Rscript", "./read_pdf.R", self.filename_pdf, self.filename_txt],
                    stderr=subprocess.STDOUT)
                output = output.decode('utf-8')
                if output.find('error') == -1:
                    return 0
                else:
                    self.logger.error(output)
            except Exception as e:
                print(e)
        else:
            return 0

    def save(self):
        self.convert()

    def get_string(self):
        self.convert()
        if os.path.exists(self.filename_pdf):
            with open(self.filename_txt, 'r') as file:
                result = file.read().splitlines()
        if self.delete:
            os.remove(self.filename_txt)
        return result
