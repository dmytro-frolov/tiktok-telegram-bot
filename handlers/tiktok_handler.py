import re
import requests

socks_proxy = "socks5://localhost:4444"

PROXY = {
    "http": socks_proxy,
    "https": socks_proxy,
}


class TTHandler:
    _users_cookie = {}
    _headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
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

    def __init__(self, link):
        self._get_page(link)

    def is_captcha(self):
        if self._html.find('tiktok-verify-page') > 0:
            return True
        return False

        pattern = f'.*tiktok-verify-page.*'
        if re.match(pattern, self._html):
            return True
        return False

    def get_video_link(self, link_name='playAddr'):
        pattern = f'{link_name}":"(.*?)"'
        link = re.findall(pattern, self._html)
        if link:
            return link[0].encode().decode('unicode_escape')

    def _get_page(self, link):
        response = requests.request("GET", link, headers=self._headers,
                                    timeout=15, cookies=self._users_cookie) #proxies=PROXY)
        self._html = response.text
        # self.debug()

    def debug(self):
        with open('out.html', 'w') as f:
            f.write(self._html)

    @classmethod
    def set_cookie(cls, cookie):
        cls._users_cookie = {}
        for cookie in cookie.split(';'):
            k, v = cookie.split('=', 1)
            cls._users_cookie[k] = v.strip()
