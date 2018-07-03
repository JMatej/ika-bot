import time
import traceback

from botapi import BotAPI

world = "s35-en.ikariam.gameforge.com"
url = "https://s35-en.ikariam.gameforge.com"
pwd = "matejko123"


class TransportLuxury:
    def __init__(self, world, url, pwd):
        self.world = world
        self.url = url
        self.pwd = pwd
        self.lines = [line.rstrip() for line in open('groups.txt')]
        self.groups = self.get_groups()

    def get_groups(self):
        groups = {}
        master = self.lines[0].split(" ")[0]
        master_city_id = -1
        for idx, line in enumerate(self.lines):
            start = time.time()
            print(idx)
            email = line.split(" ")[0]
            group_id = int(line.split(" ")[1])
            bot = BotAPI(self.url, self.world, email, self.pwd)
            try:
                state = bot.get_state()
                city_id = state['city']['id']
                if idx == 0:
                    master_city_id = city_id
                if group_id not in groups:
                    groups[group_id] = [{'email': master, 'city_id': master_city_id}]
                groups[group_id].append({'email': email, 'city_id': city_id})
            except Exception as e:
                print("type error: " + str(e))
                print(traceback.format_exc())
            end = time.time()
            print('time: ', end - start)
        return groups

    def transport_from(self, email, group_id):
        bot = BotAPI(self.url, self.world, email, self.pwd)
        state = bot.get_state()
        luxury = state['town_hall']['luxury']
        for partner in self.groups[group_id]:
            if partner['email'] != email:
                marble = 0
                glass = 0
                sulfur = 0
                wine = 0
                if luxury == 'marble':
                    marble = state['city']['marble'] // 4
                elif luxury == 'crystal':
                    glass = state['city']['crystal'] // 4
                elif luxury == 'wine':
                    wine = state['city']['wine'] // 4
                elif luxury == 'sulfur':
                    sulfur = state['city']['sulfur'] // 4
                # destination_city_id, wood, wine, marble, glass, sulfur
                bot.transport(partner['city_id'], 0, wine, marble, glass, sulfur)

    def transport(self):
        for idx, line in enumerate(self.lines):
            print(idx)
            email = line.split(" ")[0]
            group_id = int(line.split(" ")[1])
            start = time.time()
            print('account:', idx, email, group_id)
            try:
                self.transport_from(email, group_id)
            except Exception as e:
                print("type error: " + str(e))
                print(traceback.format_exc())
            end = time.time()
            print('time: ', end - start)


inst = TransportLuxury(world, url, pwd)
inst.transport()
