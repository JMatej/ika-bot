import traceback

from botapi import BotAPI


def groups_by_luxury():
    url = "https://s35-en.ikariam.gameforge.com"
    world = "s35-en.ikariam.gameforge.com"
    pwd = "matejko123"
    with open('emails.txt') as f:
        content = f.readlines()
    content = [x.strip() for x in content]

    sulfur = []
    marble = []
    wine = []
    crystal = []

    for i, email in enumerate(content):
        print(i)
        bot = BotAPI(url, world, email, pwd)
        try:
            state = bot.get_state()
            print(state['town_hall']['luxury'])
            if state['town_hall']['luxury'] == 'marble':
                marble.append(email)
            elif state['town_hall']['luxury'] == 'sulfur':
                sulfur.append(email)
            elif state['town_hall']['luxury'] == 'crystal':
                crystal.append(email)
            elif state['town_hall']['luxury'] == 'wine':
                wine.append(email)
        except Exception as e:
            print(traceback.format_exc())

    print(len(wine), len(crystal), len(marble), len(sulfur))
    max_len = max(len(marble), len(sulfur), len(wine), len(crystal))
    arr_cities = []
    for i in range(max_len):
        if i < len(marble):
            arr_cities.append(marble[i])
        if i < len(sulfur):
            arr_cities.append(sulfur[i])
        if i < len(crystal):
            arr_cities.append(crystal[i])
        if i < len(wine):
            arr_cities.append(wine[i])

    with open('groups.txt', 'a') as f:
        for idx, email in enumerate(arr_cities):
            f.write(email + ' ' + str(idx // 4) + '\n')
    print('end')


groups_by_luxury()

# kdmqlgs0@gmail.com
# bottest1234@gmail.com
# bottest123@gmail.com
# Foreign Cultures –> Experiments –> Law of the Lever –> Letter Chute –> Spirit Level –> Canon Casting
