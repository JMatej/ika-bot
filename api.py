import re
import json
import requests
from bs4 import BeautifulSoup
from proxxy import get_proxy
from slimit.parser import Parser
from slimit.visitors import nodevisitor

url = "https://s35-en.ikariam.gameforge.com"
world = "s35-en.ikariam.gameforge.com"
email = "bottest0@centrum.sk"
pwd = "matejko123"
city_id = 42663
island_id = 589
last_token = ""


def get_logged(world, email, pwd):
    s = requests.Session()
    proxies = {"http": get_proxy()}
    s.proxies.update(proxies)
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
    r = sess.get(url + "/index.php?view=townHall&cityId=" + str(city_id) + "&position=0")
    content = r.content.decode('utf-8')
    html = BeautifulSoup(content, 'html.parser')
    parser = Parser()
    tree = parser.parse(html.select('script')[-1].text)
    arr = list(nodevisitor.visit(tree))[16].to_ecma()
    js_data = json.loads(arr)[0][1][1]
    ht = BeautifulSoup(js_data, 'html.parser')
    woodworkers = int(ht.select_one('.woodworkers span').text.replace(",", ""))
    specialworkers = int(ht.select_one('.specialworkers span').text.replace(",", ""))
    scientists = int(ht.select_one('.scientists span').text.replace(",", ""))
    priests = int(ht.select_one('.priests span').text.replace(",", ""))
    citizens = int(ht.select_one('.citizens span').text.replace(",", ""))

    wood_production = int(ht.select_one('.WoodProduction').text.replace(",", ""))
    luxury_production = int(ht.select_one('.LuxuryProduction').text.replace(",", ""))
    scientists_cost = int(ht.select_one('.ScientistsCost').text.replace(",", ""))
    scientists_production = int(ht.select_one('.ScientistsProduction').text.replace(",", ""))
    priests_production = int(ht.select_one('.PriestsProduction').text.replace(",", ""))
    citizens_production = int(ht.select_one('.CitizensProduction').text.replace(",", ""))
    luxury = ht.select("div[class^='icon_']")[1].attrs['class'][0][5:]
    return {
        'woodworkers': woodworkers,
        'specialworkers': specialworkers,
        'scientists': scientists,
        'priests': priests,
        'citizens': citizens,
        'wood_production': wood_production,
        'luxury_production': luxury_production,
        'scientists_cost': scientists_cost,
        'scientists_production': scientists_production,
        'priests_production': priests_production,
        'citizens_production': citizens_production,
        'luxury': luxury,
    }


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
    town_hall_info = get_town_hall(city_id)
    island_info = get_island_info(city_id)
    return {
        'city': city_info,
        'island': island_info,
        'town_hall': town_hall_info,
    }


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


def set_workers(number, wood=True):
    sess = get_logged(world, email, pwd)
    typ = 'resource'
    if not wood:
        typ = 'tradegood'
    r = sess.post(
        url + "/index.php",
        data={
            'action': 'IslandScreen',
            'function': 'workerPlan',
            'type': typ,
            'islandId': island_id,
            'screen': typ,
            'cityId': city_id,
            'currentIslandId': island_id,
            'rw': number,
            'tw': number,
            'actionRequest': last_token,
            'ajax': 1,
        },
    )
    return True


def buy_merchant_ship(position):
    sess = get_logged(world, email, pwd)
    r = sess.post(
        url + "/index.php",
        data={
            'action': 'CityScreen',
            'function': 'increaseTransporter',
            'type': 'resource',
            'position': position,
            'islandId': island_id,
            'screen': 'resource',
            'cityId': city_id,
            'currentCityId': city_id,
            'actionRequest': last_token,
        },
    )
    return True

# print(get_state())
# print(build(city_id=42663, position=12, building=4))
# print(set_workers(1))
# print(buy_merchant_ship(1))

# sess = get_logged(world, email, pwd)
# r = sess.get(url)
# content = r.content.decode('utf-8')
# html = BeautifulSoup(content, 'html.parser')
# print(html.select_one('.gold a').text)
