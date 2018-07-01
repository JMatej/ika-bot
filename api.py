import re

import requests
from bs4 import BeautifulSoup

url = "https://s35-en.ikariam.gameforge.com"
world = "s35-en.ikariam.gameforge.com"
email = "bottest0@centrum.sk"
pwd = "matejko123"
city_id = 42663
island_id = 589
last_token = ""


def get_logged(world, email, pwd):
    s = requests.Session()
    r = s.post(
        url + "/index.php?action=loginAvatar&function=login",
        data={
            'uni_url': world,
            'name': email,
            'password': pwd,
        },
    )
    print(r)
    content = r.content.decode('utf-8')
    html = BeautifulSoup(content, 'html.parser')
    global last_token
    last_token = html.select_one('#js_ChangeCityActionRequest').attrs['value']
    return s


def get_city_info():
    sess = get_logged(world, email, pwd)
    r = sess.get(url)
    content = r.content.decode('utf-8')
    html = BeautifulSoup(content, 'html.parser')
    gold = int(html.select_one('.gold a').text.replace(",", ""))
    wood = int(html.select_one('.wood span').text.replace(",", ""))
    wine = int(html.select_one('.wine span').text.replace(",", ""))
    marble = int(html.select_one('.marble span').text.replace(",", ""))
    glass = int(html.select_one('.glass span').text.replace(",", ""))
    sulfur = int(html.select_one('.sulfur span').text.replace(",", ""))
    population = int(html.select_one('.population span').text.replace(",", ""))
    resources = {
        'wood': wood, 'wine': wine, 'marble': marble, 'glass': glass, 'sulfur': sulfur, 'population': population,
    }
    onclick_txt = html.select_one('.expandable').attrs['onclick']
    pattern = r'cityId=[0-9]*'
    city_id = int(re.search(pattern, onclick_txt).group()[7:])
    buildings = {}
    for elem in html.select("div[id^='position']"):
        cls = elem.attrs['class']
        buildings[cls[0]] = [cls[2], cls[3]]
    return {'gold': gold, 'resources': resources, 'buildings': buildings, 'id': city_id}


def get_town_hall(city_id):
    sess = get_logged(world, email, pwd)
    r = sess.get(url + "/?view=island&cityId=" + str(city_id))
    content = r.content.decode('utf-8')
    html = BeautifulSoup(content, 'html.parser')
    # print(html)
    return None


def get_island_info(city_id):
    sess = get_logged(world, email, pwd)
    r = sess.get(url + "/?view=island")
    content = r.content.decode('utf-8')
    html = BeautifulSoup(content, 'html.parser')
    island_id = int(html.select_one('input[name="currentIslandId"]').attrs['value'])
    return {'island_id': island_id}


def get_state():
    city_info = get_city_info()
    city_id = city_info['id']
    get_town_hall(city_id)
    island_info = get_island_info(city_id)
    return {'city': city_info, 'island': island_info}


def build(city_id, position, building):
    sess = get_logged(world, email, pwd)
    r = sess.post(
        url + "/index.php",
        data={
            'action': 'CityScreen',
            'function': 'build',
            'cityId': city_id,
            'currentCityId': city_id,
            'position': position,
            'building': building,
            'actionRequest': last_token,
            'ajax': 1,
        },
    )
    return True


def set_workers(number):
    sess = get_logged(world, email, pwd)
    r = sess.post(
        url + "/index.php",
        data={
            'action': 'IslandScreen',
            'function': 'workerPlan',
            'type': 'resource',
            'islandId': island_id,
            'screen': 'resource',
            'cityId': city_id,
            'currentIslandId': island_id,
            'rw': number,
            'actionRequest': last_token,
            'ajax': 1,
        },
    )
    return True


# print(get_state())
# print(build(city_id=42663, position=12, building=4))
print(set_workers(15))

# sess = get_logged(world, email, pwd)
# r = sess.get(url)
# content = r.content.decode('utf-8')
# html = BeautifulSoup(content, 'html.parser')
# print(html.select_one('.gold a').text)
