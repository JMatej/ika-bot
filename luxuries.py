from botapi import BotAPI


def groups_by_luxury():
    url = "https://s35-en.ikariam.gameforge.com"
    world = "s35-en.ikariam.gameforge.com"
    with open('emails') as f:
        content = f.readlines()
    content = [x.strip() for x in content]

    sulfur = []
    marble = []
    wine = []
    crystal = []

    for i in range(46):
        print(i)
        email = content[i]
        pwd = "matejko123"
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
                print('tento je vino')
                print(email)
            print(len(wine), len(crystal), len(marble), len(sulfur))
        except:
            print("failed")

    min_len = min(len(marble), len(sulfur), len(wine), len(crystal))
    for i in range(min_len):
        with open('groups', 'a') as f:
            f.write(marble[i] + ' ' + str(i) + '\n')
            f.write(sulfur[i] + ' ' + str(i) + '\n')
            f.write(wine[i] + ' ' + str(i) + '\n')
            f.write(crystal[i] + ' ' + str(i) + '\n')

groups_by_luxury()

# kdmqlgs0@gmail.com
# bottest1234@gmail.com
# bottest123@gmail.com
# Foreign Cultures –> Experiments –> Law of the Lever –> Letter Chute –> Spirit Level –> Canon Casting