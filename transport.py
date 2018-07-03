from botapi import BotAPI

world = "s35-en.ikariam.gameforge.com"
url = "https://s35-en.ikariam.gameforge.com"
pwd = "matejko123"


def get_groups():
    groups = {}
    lines = [line.rstrip() for line in open('groups.txt')]
    master = lines[0].split(" ")[0]
    master_city_id = -1
    for idx, line in enumerate(lines):
        print(idx)
        act_email = line.split(" ")[0]
        act_group_id = int(line.split(" ")[1])
        bot = BotAPI(url, world, act_email, pwd)
        state = bot.get_state()
        city_id = state['city']['id']
        if idx == 0:
            master_city_id = city_id
        if act_group_id not in groups:
            groups[act_group_id] = [{'email': master, 'city_id': master_city_id}]
        groups[act_group_id].append({'email': act_email, 'city_id': city_id})
    return groups


def transport_luxury():
    groups = get_groups()
    lines = [line.rstrip() for line in open('groups.txt')]
    for idx, line in enumerate(lines):
        print(idx)
        act_email = line.split(" ")[0]
        act_group_id = int(line.split(" ")[1])
        bot = BotAPI(url, world, act_email, pwd)
        state = bot.get_state()
        luxury = state['town_hall_info']['luxury']
        for partner in groups[act_group_id]:
            if partner['email'] != act_email:
                marble = 0
                glass = 0
                sulfur = 0
                wine = 0
                if luxury == 'marble':
                    marble = state['city_info']['marble'] // 4
                elif luxury == 'crystal':
                    glass = state['city_info']['crystal'] // 4
                elif luxury == 'wine':
                    wine = state['city_info']['wine'] // 4
                elif luxury == 'sulfur':
                    sulfur = state['city_info']['sulfur'] // 4
                # destination_city_id, wood, wine, marble, glass, sulfur
                bot.transport(partner['city_id'], 0, wine, marble, glass, sulfur)


transport_luxury()
