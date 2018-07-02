import re
import json
import requests
from bs4 import BeautifulSoup
from proxxy import get_proxy
from slimit.parser import Parser
from slimit.visitors import nodevisitor


class BotAPI:
    def __init__(self, url, world, email, pwd):
        self.url = url
        self.world = world
        self.email = email
        self.pwd = pwd
        self.city_id = 0
        self.island_id = 0
        self.last_token = ""

    def get_logged(self):
        s = requests.Session()
        proxies = {"http": get_proxy()}
        s.proxies.update(proxies)
        r = s.post(
            self.url + "/index.php?action=loginAvatar&function=login",
            data={
                'uni_url': self.world,
                'name': self.email,
                'password': self.pwd,
            },
        )
        print(r)
        content = r.content.decode('utf-8')
        html = BeautifulSoup(content, 'html.parser')
        self.last_token = html.select_one('#js_ChangeCityActionRequest').attrs['value']
        return s

    def get_city_info(self):
        sess = self.get_logged()
        r = sess.get(self.url)
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

    def get_town_hall(self):
        sess = self.get_logged()
        r = sess.get(self.url + "/index.php?view=townHall&cityId=" + str(self.city_id) + "&position=0")
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

    def get_island_info(self):
        sess = self.get_logged()
        r = sess.get(self.url + "/?view=island")
        content = r.content.decode('utf-8')
        html = BeautifulSoup(content, 'html.parser')
        self.island_id = int(html.select_one('input[name="currentIslandId"]').attrs['value'])
        return {'island_id': self.island_id}

    def get_state(self):
        city_info = self.get_city_info()
        self.city_id = city_info['id']
        town_hall_info = self.get_town_hall()
        island_info = self.get_island_info()
        return {
            'city': city_info,
            'island': island_info,
            'town_hall': town_hall_info,
        }

    def build(self, position, building):
        sess = self.get_logged()
        r = sess.post(
            self.url + "/index.php",
            data={
                'action': 'CityScreen',
                'function': 'build',
                'cityId': self.city_id,
                'currentCityId': self.city_id,
                'position': position,
                'building': building,
                'actionRequest': self.last_token,
                'ajax': 1,
            },
        )
        return True

    def upgrade(self, position, level):
        sess = self.get_logged()
        r = sess.post(
            self.url + "/index.php",
            data={
                'action': 'CityScreen',
                'function': 'upgradeBuilding',
                'cityId': self.city_id,
                'currentCityId': self.city_id,
                'position': position,
                'level': level,
                'actionRequest': self.last_token,
                'ajax': 1,
            },
        )
        return True

    def set_workers(self, number, wood=True):
        sess = self.get_logged()
        typ = 'resource'
        if not wood:
            typ = 'tradegood'
        r = sess.post(
            self.url + "/index.php",
            data={
                'action': 'IslandScreen',
                'function': 'workerPlan',
                'type': typ,
                'islandId': self.island_id,
                'screen': typ,
                'cityId': self.city_id,
                'currentIslandId': self.island_id,
                'rw': number,
                'tw': number,
                'actionRequest': self.last_token,
                'ajax': 1,
            },
        )
        return True

    def buy_merchant_ship(self, position):
        sess = self.get_logged()
        r = sess.post(
            self.url + "/index.php",
            data={
                'action': 'CityScreen',
                'function': 'increaseTransporter',
                'type': 'resource',
                'position': position,
                'islandId': self.island_id,
                'screen': 'resource',
                'cityId': self.city_id,
                'currentCityId': self.city_id,
                'actionRequest': self.last_token,
            },
        )
        return True

    def transport(self, destination_city_id, wood, wine, marble, glass, sulfur):
        sess = self.get_logged()
        r = sess.post(
            self.url + "/index.php",
            data={
                'action': 'transportOperations',
                'function': 'loadTransportersWithFreight',
                'cargo_resource': wood,
                'cargo_tradegood1': wine,
                'cargo_tradegood2': marble,
                'cargo_tradegood3': glass,
                'cargo_tradegood4': sulfur,
                'islandId': self.island_id,
                'destinationCityId': destination_city_id,
                'cityId': self.city_id,
                'currentIslandId': self.island_id,
                'actionRequest': self.last_token,
            },
        )
        return True

    # seafaring, economy, science, military
    def research(self, typ):
        sess = self.get_logged()
        r = sess.post(
            self.url + "/index.php",
            data={
                'action': 'Advisor',
                'function': 'doResearch',
                'type': typ,
                'currentIslandId': self.island_id,
                'actionRequest': self.last_token,
            },
        )
        return True
