import os
import shutil
import zipfile

from constants.enums import ZIP


class RepositoryBulletin:
    def __init__(self, path, logger=None):
        self.path = path
        self.logger = logger
        self.files = []

    def extract_bulletins(self, bulletins):
        result = []
        for bulletin in bulletins:
            try:
                target_dir = bulletin['name']
                bulletin_filepath = bulletin['path']
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)

                with zipfile.ZipFile(bulletin_filepath, 'r') as zip_ref:
                    zip_ref.extractall(target_dir)

                result.append({
                    'name': bulletin['name'],
                    'report_id': bulletin['report_id'],
                    'status': ZIP.extracted.value
                })
            except Exception as e:
                self.logger.critical(e)
                result.append({
                    'name': bulletin['name'],
                    'report_id': bulletin['report_id'],
                    'status': ZIP.error.value
                })

        return result

    def remove_bulletins(self, bulletins):
        result = []
        for bulletin in bulletins:
            if bulletin['status'] != ZIP.extracted.value:
                continue

            shutil.rmtree(bulletin['name'])

            result.append({
                'name': bulletin,
                'status': ZIP.deleted.value
            })

        return result
