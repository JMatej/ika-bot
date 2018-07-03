from botapi import BotAPI

world = "s35-en.ikariam.gameforge.com"
url = "https://s35-en.ikariam.gameforge.com"
pwd = "matejko123"

def get_groups():
    groups = {}
    lines = [line.rstrip('\n') for line in open('groups')]
    for line in lines:
        act_email = line.split(" ")[0]
        act_group_id = int(line.split(" ")[1])
        bot = BotAPI(url, world, act_email, pwd)
        state = bot.get_state()
        city_id = state['city_id']
        # city_id = 4
        if act_group_id not in groups:
            groups[act_group_id] = []
        groups[act_group_id].append({'emial':act_email, 'city_id':city_id})
    return groups

def transport_luxury():
    groups = get_groups()
    lines = [line.rstrip('\n') for line in open('groups')]
    for line in lines:
        act_email = line.split(" ")[0]
        act_group_id = int(line.split(" ")[1])
        bot = BotAPI(url, world, act_email, pwd)
        state = bot.get_state()
        luxury = state['town_hall_info']['luxury']
        amount = 0
        for partner in groups[act_group_id]:
            if partner['emial'] is not act_email:
                marble = 0
                glass = 0
                sulfur = 0
                wine = 0
                if luxury == 'marble':
                    amount = state['city_info']['marble']
                    marble = amount
                elif luxury == 'crystal':
                    amount = state['city_info']['crystal']
                    glass = amount
                elif luxury == 'wine':
                    amount = state['city_info']['wine']
                    wine = amount
                elif luxury == 'sulfur':
                    amount = state['city_info']['sulfur']
                    sulfur = amount
                #destination_city_id, wood, wine, marble, glass, sulfur
                bot.transport(partner['city_id'], 0, wine, marble, glass, sulfur)



transport_luxury()