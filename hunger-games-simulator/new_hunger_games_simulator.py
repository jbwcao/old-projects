import random

class Tribute:
    is_career = False
    strength_range = (20,80)
    def __init__(self,name): 
        self.name = name
        self.available_targets = None
        self.is_alive = True
        self.kills = 0
        self.strength = random.randint(*Tribute.strength_range)
        score = round(random.uniform(0.8,1.5)*(self.strength/10))
        if score > 13:
            score = 13
        self.gamemaker_score = score
    def attack(self,target):
        roll = random.randint(1,10)
        if self.strength < target.strength:     
            if roll < 9:
                self.is_alive = False
                target.kills += 1
            else:
                target.is_alive = False
                self.kills += 1
        else:
            if roll < 3:
                self.is_alive = False
                target.kills += 1
            else:
                target.is_alive = False
                self.kills += 1
    def self_kill(self):
        self.is_alive = False
        
class CarrerTribute(Tribute):
    is_career = True
    strength_range = (60,100)
    def __init__(self,name):
        super().__init__(name)
        self.strength = random.randint(*CarrerTribute.strength_range)
        score = round(random.uniform(0.8,1.5)*(self.strength/10))
        if score > 13:
            score = 13
        self.gamemaker_score = score

def get_lines(file_name):
    with open(file_name) as f:
        names = f.readlines()
        return [name.rstrip() for name in names]

def create_tributes(names_of_tributes,percent_career):
    tributes_ = []
    num_of_tributes = len(names_of_tributes)
    num_of_careers = round((percent_career/100)*num_of_tributes)
    random.shuffle(names_of_tributes)
    for i, name in enumerate(names_of_tributes):
        if i < num_of_careers:
            tributes_.append(CarrerTribute(name))
        else:
            tributes_.append(Tribute(name))  
    return tributes_

def update_targets(alive_tributes_):
    for t in alive_tributes_:
        t.available_targets = []
        for potential_target in alive_tributes_:
            if t.name != potential_target.name:
                t.available_targets.append(potential_target)

#for debugging purposes only
def debug_show_info(tributes_to_show):
    for tribute in tributes_to_show:
        info = vars(tribute)
        info.update({'career': tribute.is_career})
        print(info)

def debug_show_available_targets(t):
    print(f'{t.name} targets')
    for tribute in t.available_targets:
        print(tribute.name,end= ', ')

def combat_event(alive_tributes_):
    current_tribute = random.choice(alive_tributes_)
    tribute_target = random.choice(current_tribute.available_targets)
    current_tribute.attack(tribute_target)
    if current_tribute.is_alive:
        print(f'{current_tribute.name} kills {tribute_target.name}')
        dead_tribute = tribute_target
    else:
        print(f'{tribute_target.name} kills {current_tribute.name}')
        dead_tribute = current_tribute
    alive_tributes_.remove(dead_tribute)
    update_targets(alive_tributes_)
    return dead_tribute.name
    
def self_kill_event(alive_tributes_):
        current_tribute = random.choice(alive_tributes_)
        current_tribute.is_alive = False
        event = random.randint(1,5)
        match event:
            case 1:
                print(f'{current_tribute.name} falls out of a tree and dies')
            case 2:
                print(f'{current_tribute.name} is eaten by crocodiles trying to cross a river')
            case 3:
                print(f'{current_tribute.name} dies to poisonous berries')
            case 4:
                print(f'{current_tribute.name} bids farewell to this cruel cruel world')
            case 5:
                print(f'{current_tribute.name} dies to exposure')
        alive_tributes_.remove(current_tribute)
        update_targets(alive_tributes_)
        return current_tribute.name

def flavor_text_event(alive_tributes_):
    alive_tributes_copy = [tribute for tribute in alive_tributes_]
    t1 = random.choice(alive_tributes_copy)
    alive_tributes_copy.remove(t1)
    t2 = random.choice(alive_tributes_copy)
    alive_tributes_copy.remove(t2)
    if len(alive_tributes_) > 5: 
        t3 = random.choice(alive_tributes_copy)
        event = random.randint(1,15)
    elif len(alive_tributes_) == 2:
        event = random.randint(10,14)
    else:
        event = random.randint(6,15)
    match event:
        case 1:
            print(f'{t1.name} cries themself to sleep')
        case 2:
            print(f'{t1.name} recieves supplies from an unknown sponsor')
        case 3:
            print(f'{t1.name} finds a fresh water source')
        case 4:
            print(f'{t1.name} stargazes with {t2.name} and {t3.name}')
        case 5:
            print(f'{t1.name} and {t2.name} hunt for other tributes')
        case 6:
            print(f'{t1.name} hunts for other tributes')
        case 7:
            print(f'{t1.name} gives {t2.name} a hug')
        case 8: 
            print(f'{t1.name} and {t2.name} hold hands')
        case 9:
            print(f'{t1.name} wounds {t2.name}, but decides to spare their life')
        case 10:
            print(f'{t1.name} climbs a tree for safety')
        case 11:
            berries = ['boysenberries', 'blueberries', 'mulberries', 'unknown berries']
            berry = random.choice(berries)
            print(f'{t1.name} picks {berry}')
        case 12:
            print(f'{t1.name} comtemplates life decisions')
        case 13:
            print(f'{t1.name} thinks about home')
        case 14:
            print(f'{t1.name} sees smoke rising in the distance')
        case 15:
            print(f'{t1.name} thinks about {t2.name}')

def intro():
    print('Welcome to the Hunger Games Simulator')
    print("Background: The Hunger Games is a dystopian novel written by Suzanne Collins set in the fictional nation of Panem. Panem is composed of 12 poor districts and a Capitol. Early in Panem's history, a rebillion by the districts resulted in the destruction of the 13th district and the creation of an annual televised event known as the Hunger Games. To remind the districts of the Capitol's power and how the districts are completely at its mercy, one boy and one girl between the ages of 12 and 18 are selected to participate in the games. The ‘tributes’ are chosen through a lottery system known as the Reaping and are forced to fight to the death, leaving the last survivor as the victor.")
    print()

def show_scores(alive_tributes_):
    print("The gamemakers give the following scores(out of 13) for the tributes. It is the gamemakers' evaluation on how well they think each person will do for bets")
    for t in alive_tributes_:
        if t.is_career:
            print(f'{t.name}*: {t.gamemaker_score}')
        else:
            print(f'{t.name}: {t.gamemaker_score}')
    print('*denotes career tributes')
    print()

def bloodbath(alive_tributes_):
    if len(alive_tributes_) < 5:
        offset = 0
    else:
        offset = random.randint(-2,2)
    print('The bloodbath begins!')
    bloodbath_casualites = []
    for i in range(round(len(alive_tributes_)/3) + offset):
        bloodbath_casualites.append(combat_event(alive_tributes_))
    print(f'The bloodbath ends with {len(bloodbath_casualites)} casualities')
    print()
    return bloodbath_casualites

def show_kill_counts(tributes_):
    print('Kill Counts')
    for t in tributes_:
        print(f'{t.name}: {t.kills}')
    
def get_placement(num):
    placement_name = {
        1: "st",
        2: "nd",
        3: "rd"
    }.get(num % 10 if num not in (11, 12, 13) else 0, "th")
    return placement_name

def get_names():
    while True:
            print('How should the tributes be selected? (Enter an option 1-3)')
            print('1. using a .txt file')
            print('2. entering names manually')
            print('3. use the default names')
            selection = input()
            match selection:
                case '1':
                    return get_lines(input('Enter a file path: '))
                case '2':
                    names = []
                    tribute_num = 1
                    while True:
                        name = input(f'Enter the name of the {tribute_num}{get_placement(tribute_num)} tribute(leave blank to end): ')
                        tribute_num += 1
                        if name == '':
                            break
                        else:
                            names.append(name) 
                    return names
                case '3':
                    return  ['Johanna Mason', 'Marvel', 'Glimmer', 'Cato', 'Clove', 'Foxface', 'Thresh', 'Rue', 'Peeta Mellark', 'Katniss Everdeen', 'Gloss', 'Cashmere', 'Brutus', 'Enobaria', 'Beetee', 'Wiress', 'Finnick Odair', 'Mags', 'Blight', 'Cecelia', 'Chaff', 'Seeder', 'Facet', 'Velvereen', 'Marcus', 'Sabyn', 'Circ', 'Teslee', 'Mizzen Coral', 'Hy', 'Sol', 'Otto', 'Ginnee', 'Treech', 'Lamina', 'Bobbin', 'Wovey', 'Panlo', 'Sheaf', 'Tanner', 'Brandy', 'Reaper Ash', 'Dill', 'Jessup Diggs', 'Lucy Gray Baird']
                case _:
                    print('Invalid input, please enter a number from 1 to 3')

def get_dead_tributes(deaths_):
    if len(deaths_) == 0:
        return 'No cannons were heard throughout the night'
    elif len(deaths_) == 1:
        return '1 cannon shot was heard through the night, the face of ' + str(deaths_[0]) + ' appears in the night sky'
    elif len(deaths_) == 2:
        return '2 cannon shots were heard through the night, the faces of ' + str(deaths_[0]) + ' and ' + str(deaths_[1]) + ' appear in the night sky'
    else:
        dead_people = ', '.join(deaths_[:-1]) + ', and ' + (deaths_[-1])
        return str(len(deaths_)) + ' cannon shots were heard through the night, the faces of ' + str(dead_people) + ' appear in the night sky'

class HungerGamesSim:
    def main():
        intro()
        names = get_names()
        if len(names) == 0:
            print('President Snow has you excuted for making a game without any tributes')
            return
        tributes = create_tributes(names,20)
        alive_tributes = [tribute for tribute in tributes]
        day = 1
        update_targets(alive_tributes)
        show_scores(alive_tributes)
        print('Let the games begin!')
        while True:
            num_of_events = round(len(alive_tributes)/2)
            print(f'Day {day}')
            deaths = []
            if day == 1:
                num_of_events = round(num_of_events/3)
                bloodbath_deaths = bloodbath(alive_tributes)
                deaths = [death for death in bloodbath_deaths]
            for i in range(num_of_events):
                if len(alive_tributes) == 1:
                    break            
                elif len(alive_tributes) < 6:
                    event = random.randint(1,8)
                else:
                    event = random.randint(1,10)
                match event:
                    case 1:
                        deaths.append(combat_event(alive_tributes))
                    case 2:
                        deaths.append(combat_event(alive_tributes))
                    case 3:
                        deaths.append(combat_event(alive_tributes))
                    case 4:
                        deaths.append(combat_event(alive_tributes))
                    case 5:
                        flavor_text_event(alive_tributes)
                    case 6:
                        flavor_text_event(alive_tributes)
                    case 7:
                        flavor_text_event(alive_tributes)
                    case 8:
                        flavor_text_event(alive_tributes)
                    case 9:
                        flavor_text_event(alive_tributes)
                    case 10:
                        deaths.append(self_kill_event(alive_tributes))
                if len(alive_tributes) == 1:
                    break 
            if len(alive_tributes) == 1:
                break
            cannon_message = get_dead_tributes(deaths)
            print(f'End of day {day}, {cannon_message}, {len(alive_tributes)} tributes remain')
            print() 
            day += 1 
        print()
        print(f'The victor is {alive_tributes[0].name} with {alive_tributes[0].kills} kills')
        print()
        show_kill_counts(tributes)
        
HungerGamesSim.main()