import requests
from lxml.html import fromstring
import random

def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    # maximum 20 proxies
    for i in parser.xpath('//tbody/tr')[:20]:
        # if i.xpath('.//td[7][contains(text(),"yes")]'):
        proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
        proxies.add(proxy)
    return proxies


def get_proxy():
    proxies = get_proxies()
    return random.choice(list(proxies))
