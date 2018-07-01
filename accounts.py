import random
import string
from random import choice
from string import ascii_lowercase
import requests
from lxml.html import fromstring
from itertools import cycle
import traceback
import proxxy


def create_accounts(urla, amount):
    emails = []
    url = urla + 'https://' + urla + '-en.ikariam.gameforge.com/index.php?action=newPlayer&function=createAvatar'
    for i in range(0, amount):
        part = ''.join(choice(ascii_lowercase) for i in range(7))
        mail = '@gmail.com'
        part += str(i)
        email = part + mail
        emails.append({'email': email, 'name': part})
    proxies = proxxy.get_proxies()
    proxy_pool = cycle(proxies)
    for i in range(0, 20):
        proxy = next(proxy_pool)
        payload = {'email': emails[i]['email'], 'name': emails[i]['name'], 'agb': 'on', 'password': 'matejko123',
                   'uni_url': urla + '-en.ikariam.gameforge.com'}
        try:
            response = requests.post(url, data=payload, proxies={"http": proxy, "https": proxy})
        except:
            print("Skipping. Connnection error")
