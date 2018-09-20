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


class SStrategy:

    def run_user(self, email):
        bot = BotAPI(url, world, email, pwd)
        print(bot.get_state())
        print(1)

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
