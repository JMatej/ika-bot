from botapi import BotAPI

url = "https://s35-en.ikariam.gameforge.com"
world = "s35-en.ikariam.gameforge.com"
email = "bottest0@centrum.sk"
pwd = "matejko123"

bot = BotAPI(url, world, email, pwd)
print(bot.get_state())
# print(bot.research('military'))
# print(get_state())
# print(build(city_id=42663, position=12, building=4))
# print(set_workers(1))
# print(buy_merchant_ship(1))
# print(upgrade(42663, 1, 1))
# print(transport(42139, 1, 2, 3, 4, 5))
