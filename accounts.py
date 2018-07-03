from random import choice
from string import ascii_lowercase
import requests
from itertools import cycle
import proxxy


def create_emails(amount):
    emails = []
    for i in range(0, amount):
        part = ''.join(choice(ascii_lowercase) for i in range(7))
        mail = '@gmail.com'
        part += str(i)
        email = part + mail
        emails.append({'email': email, 'name': part})
    return emails


def create_accounts(urla, amount):
    emails = create_emails(amount)
    url = 'https://' + urla + '-en.ikariam.gameforge.com/index.php?action=newPlayer&function=createAvatar'
    proxies = proxxy.get_proxies()
    proxy_pool = cycle(proxies)
    for i in range(0, amount):
        proxy = next(proxy_pool)
        payload = {'email': emails[i]['email'], 'name': emails[i]['name'], 'agb': 'on', 'password': 'matejko123',
                   'uni_url': urla + '-en.ikariam.gameforge.com'}
        try:
            response = requests.post(url, data=payload, proxies={"http": proxy, "https": proxy})
            print(emails[i]['email'], emails[i]['name'])
        except:
            print("Skipping. Connnection error")


def invite_friends(fh, player_id):
    url = 'https://s35-en.ikariam.gameforge.com/index.php'
    proxies = proxxy.get_proxies()
    emails = create_emails(20)
    proxy_pool = cycle(proxies)
    for i in range(0, 10):
        print(emails[i]['email'], emails[i]['name'])
        proxy = next(proxy_pool)
        payload = {
            'action': 'newPlayer',
            'friendId': player_id,  # '29969',
            'fh': fh,  # '4f158c4f36d1dfbf022ee3b08ec69d82',
            'function': 'createAvatar',
            'email': emails[i]['email'],
            'name': emails[i]['name'],
            'agb': 'on',
            'password': 'matejko123'
        }
        try:
            response = requests.post(url, data=payload, proxies={"http": proxy, "https": proxy})
            with open('emails.txt', 'a') as f:
                f.write(emails[i]['email'] + '\n')
        except:
            print("Skipping. Connnection error")


invite_friends('a65e7006d322c14428247b672885492c', '16352')
