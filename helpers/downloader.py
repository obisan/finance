import requests


class Downloader:

    def __init__(self, url, target):
        self.url = url
        self.target = target

    @property
    def download_by_year(self):
        print('Beginning download the massive of ' + '\n')

        request = requests.get(self.url)
        with open(self.target, 'wb') as f:
            f.write(request.content)

        # Retrieve HTTP meta-data
        print('status       = ' + str(request.status_code))
        print('content-type = ' + request.headers['content-type'])
        print('encoding     = ' + str(request.encoding))

        return 0
