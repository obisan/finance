import os
import zipfile

import requests


class Downloader_cot:

    def __init__(self, settings, target_year, reload=False):

        path = settings['path']
        extension1 = settings['extension1']
        extension2 = settings['extension2']
        scr_file = settings['scr_file']
        param1 = settings['param1']
        url = settings['url']

        self.reload = reload

        self.year = target_year
        self.root_path = path
        self.url = url + param1 + str(target_year) + "." + extension2

        self.zip_path = path + param1 + str(target_year) + '.' + extension2
        self.annual_old = path + scr_file + '.' + extension1
        self.annual_new = path + scr_file + str(target_year) + '.' + extension1

    def download_by_year(self):
        if not self.reload:
            if os.path.isfile(self.annual_new):
                return 0

        print('Beginning download the massive of ' + str(self.year) + ' year\n')

        r = requests.get(self.url)
        with open(self.zip_path, 'wb') as f:
            f.write(r.content)

        # Retrieve HTTP meta-data
        print('status       = ' + str(r.status_code))
        print('content-type = ' + r.headers['content-type'])
        print('encoding     = ' + str(r.encoding))

        with zipfile.ZipFile(self.zip_path, 'r') as l_zip:
            l_zip.extractall(self.root_path)

        os.rename(r'' + self.annual_old, r'' + self.annual_new)

        os.remove(self.zip_path)

        return 0
