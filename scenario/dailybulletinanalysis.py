import os

from cme import Euro_FX
from cme.bulletin import Globex
from constants.enums import DailyBulletinSection
from convert.converter import ConverterPDFtoTXT


class DailyBulletinAnalysis:

    def __init__(self, storage_db, repository=None, logger=None):
        self.storage_db = storage_db
        self.repository = repository
        self.logger = logger
        self.globex = Globex(storage_db)

        sections = [str(DailyBulletinSection.EURO_FX.value)]
        self.sections = \
            list(map(lambda x: {
                'section': x[0],
                'name': x[1]
            }, self.storage_db.get_dailybulletin_sections_by_section(sections)))

    def exec_analysis(self, bulletins):
        dailybulletin_reports_data = []
        for bulletin in bulletins:
            target_dir_zip = os.path.join(os.curdir, bulletin['name'])
            for section in self.sections:
                section_filename_pdf = os.path.join(target_dir_zip, section['name']) + '.pdf'
                section_filename_txt = os.path.join(target_dir_zip, section['name']) + '.txt'

                section_content = \
                    ConverterPDFtoTXT(section_filename_pdf, section_filename_txt, self.logger).get_string()

                euro_fx = Euro_FX(globex=self.globex)
                section_data = euro_fx.exec(section_content)
                dailybulletin_reports_data.append({
                    'bulletin': bulletin['name'],
                    'report_id': bulletin['report_id'],
                    'section': section['section'],
                    'data': section_data
                })

        self.storage_db.insert_dailybulletin_reports_data(dailybulletin_reports_data)

    def analysis(self):
        bulletins_extracted = \
            self.repository.extract_bulletins(
                list(map(lambda x: {
                    'name': x[0],
                    'report_id': x[1],
                    'path': x[2]
                }, self.storage_db.get_dailybulletin_reports()[-1:])))

        self.exec_analysis(bulletins_extracted)

        self.repository.remove_bulletins(bulletins_extracted)
