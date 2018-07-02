import random
import math
import traceback
import time

from botapi import BotAPI

url = "https://s35-en.ikariam.gameforge.com"
world = "s35-en.ikariam.gameforge.com"
pwd = "matejko123"

# users = ["kfjawoj1@gmail.com"]
# users = ["bottest0@centrum.sk"]
# users = ["bottest123@centrum.sk"]
users = []

with open('emails.txt') as f:
    for line in f:
        line = line.strip()
        users.append(line)


def gen_ran(n):
    numbers = [random.uniform(0, 1) for _ in range(4)]
    sm = sum(numbers)
    return [math.floor(x/sm*n) for x in numbers]


class SStrategy:

    def run_user(self, email):
        bot = BotAPI(url, world, email, pwd)
        print(bot.get_state())
        bot.build(1, 3)  # build trading port
        bot.build(3, 4)  # build academy
        bot.build(4, 7)  # build academy
        lvls = bot.state['city']['buildings']
        to_upgrade = []
        buildings = [('position0', 0), ('position1', 1), ('position3', 3), ('position4', 4)]
        for b in buildings:
            if len(lvls[b[0]][1]) > 5 and lvls[b[0]][1][:5] == 'level':
                lvl = int(lvls[b[0]][1][5:])
                to_upgrade.append((b[1], lvl))
        random.shuffle(to_upgrade)
        for b in to_upgrade:
            bot.upgrade(b[0], b[1])  # position, level
        bot.buy_merchant_ship(1)
        research_areas = ['seafaring', 'economy', 'science', 'military']
        random.shuffle(research_areas)
        for area in research_areas:
            bot.research(area)
        i = 0
        while True:
            print('try', i)
            rn = gen_ran(bot.state['town_hall']['people'])
            bot.set_workers(rn[0])
            bot.set_workers(rn[1], False)
            bot.set_scientists(rn[2])
            net_gold = bot.get_town_hall()['net_gold']
            print('net_gold:', net_gold)
            if 0 < net_gold < 50 or i >= 3:
                break
            i += 1

    def run(self):
        while 1:
            for idx, email in enumerate(users):
                start = time.time()
                print('account:', idx, email)
                try:
                    self.run_user(email)
                except Exception as e:
                    print("type error: " + str(e))
                    print(traceback.format_exc())
                end = time.time()
                print('time: ', end - start)


s = SStrategy()
s.run()

# print(bot.research('military'))
# print(get_state())
# print(build(city_id=42663, position=12, building=4))
# print(set_workers(1))
# print(buy_merchant_ship(1))
# print(upgrade(42663, 1, 1))
# print(transport(42139, 1, 2, 3, 4, 5))
