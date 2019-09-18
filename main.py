import sys, logging, os, json

version = (3,7)
assert sys.version_info >= version, "This script requires at least Python {0}.{1}".format(version[0],version[1])

logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)




# Game loop functions
def render(room,maxHealth,Health):
    ''' Displays the current room, moves, and points '''

    print('\n\nMax Health: {mH}, CurrentHealth: {cH}'.format(mH=maxHealth, cH=Health))
    print('\n\nYou are in the {name}'.format(name=room['name']))
    print(room['desc'])


def getInput(verbs):
    ''' Asks the user for input and normalizes the inputted value. Returns a list of commands '''

    response = input('\nWhat would you like to do? ').strip().upper().split()
    if (len(response)):
        #assume the first word is the verb
        response[0] = normalizeVerb(response[0],verbs)
    return response


def update(response,room,current,inventory,game):
    ''' Process the input and update the state of the world '''
    s = list(response)[0]  #We assume the verb is the first thing typed
    if s == "":
        print("\nSorry, I don't understand.")
        return current
    elif s == 'HELP':
        printVerbs(room)
        return current
    elif s == 'INVENT':
        printInvent(inventory)
        return current
    elif s == 'TAKE' :
        noitem = True
        for e in room['exits']:
            if s == e['verb']:
                InventFill(inventory,room)
                noitem = False
                return current
        if noitem:
            print('There is nothing to take.')
            return current
    elif s == 'ATTACK' :
        for e in room['exits']:
            if s == e['verb']:
                return Battle(inventory,room,current,game)
    else:
        for e in room['exits']:
            if s == e['verb'] and e['target'] != 'NoExit':
                print(e['condition'])
                return e['target']
    print("\nYou can't go that way!")
    return current


# Helper functions

def printVerbs(room):
    e = ", ".join(str(x['verb']) for x in room['exits'])
    print('\nYou can take the following actions: {directions}'.format(directions = e))
    print('INVENT')

def printInvent(invent):
    for e in invent:
        print(e)

def Battle(invent,room,current,game):
    playerstrength = 0
    for e in invent:
        if e == "Sword":
            if playerstrength < 1:
                playerstrength =1
        if e == "Sharpened Sword":
            if playerstrength < 2:
                playerstrength =2
        if e == "Dwarven Axe":
            if playerstrength < 3:
                playerstrength =3
        if e == "Sharpened Dwarven Axe":
            if playerstrength < 4:
                playerstrength = 4
        if e == "Dragon's Flame":
            playerstrength = 5
    for e in room['exits']:
            if "ATTACK" == e['verb'] and e['target'] != 'NoExit':
                print(e['condition'])
                print(playerstrength)
                game['rooms']['CHARACTER']['health'] = game['rooms']['CHARACTER']['health'] - (e['strength'])
                e['health'] = e['health'] - playerstrength
                if e ['health'] <= 0:
                    print(e['onkill'])
                    return e['target']
                else:
                    return current

def InventFill(invent,room):
    for e in room['exits']:
            if "TAKE" == e['verb'] and e['target'] != 'NoExit':
                print(e['condition'])
                invent.append(e['item'])
                e['verb'] = "TAKEN"

def normalizeVerb(selection,verbs):
    for v in verbs:
        if selection == v['v']:
            return v['map']
    return ""

def end_game(winning,points,moves):
    if winning:
        print('\n\nYou have won! Congratulations')
        print('\nYou scored {points} points in {moves} moves! Nicely done!'.format(moves=moves, points=points))
    else:
        print('\n\nThanks for playing!')
        print('\nYou scored {points} points in {moves} moves. See you next time!'.format(moves=moves, points=points))





def main():

    # Game name, game file, starting location, winning location(s), losing location(s)
    games = [
        (   'My Game',          'game.json',    'THRONEROOM',    ['END'],    [])
        ,(  'Zork I',           'zork.json',    'WHOUS',    ['NIRVA'],  [])
        ,(  'A Nightmare',      'dream.json',    'START',   ['AWAKE'],  ['END'])
    ]

    inventory = []

    # Ask the player to choose a game
    game = {}
    while not game:
        print('\n\nWhich game would you like to play?\n')
        for i,g in enumerate(games):
            print("{i}. {name}".format(i=i+1, name=g[0]))
        try:
            choice = int(input("\nPlease select an option: "))
            game = games[choice-1]
        except:
            continue
            
    name,gameFile,current,win,lose = game





    with open(gameFile) as json_file:
        game = json.load(json_file)

    moves = 0
    points = 0
    health = 10
    maxHealth = 10
    inventory = []

    print("\n\n\n\nWelcome to {name}!\n\n".format(name=name))
    while True:
        if choice == 1:
            render(game['rooms'][current],game['rooms']['CHARACTER']['maxhealth'],game['rooms']['CHARACTER']['health'])
        else:
            render(game['rooms'][current],health,maxHealth)

        response = getInput(game['verbs'])

        if response[0] == 'QUIT':
            end_game(False,points,moves)
            break

        current = update(response,game['rooms'][current],current,inventory,game)

        moves = moves + 1

        if current in win:
            end_game(True,points,moves)
            break
        if current in lose:
            end_game(False,points,moves)
            break






if __name__ == '__main__':
	main()