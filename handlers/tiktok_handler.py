import os
import re
import requests


class TTHandler:
    _headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Cookie': os.getenv('cookie', '').encode('utf-8'),
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Sec-GPC': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache'
    }
    _html = None

    # dunderline == double under line == magic methods
    def __init__(self, link):
        self._get_page(link)

    # public
    def is_captcha(self):
        pattern = f'.*tiktok-verify-page.*'
        if re.match(pattern, self._html):
            return True
        return False

    # public
    def get_video_link(self, link_name='playAddr'):
        pattern = f'{link_name}":"(.*?)"'
        link = re.findall(pattern, self._html)
        if link:
            return link[0].encode().decode('unicode_escape')

    # private
    def _get_page(self, link):
        response = requests.request("GET", link, headers=self._headers)
        self._html = response.text

    def debug(self):
        with open('out.html', 'w') as f:
            f.write(self._html)
