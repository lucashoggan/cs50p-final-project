import os, sys, pyfiglet
from classes import Action, ActionBundle, Player, Garage, Tuner, SaveJson
from random import randint
from alive_progress import alive_bar
from time import sleep


ACTIONBUNDLE = ActionBundle()


def calc_prize(inverse_place, count, bet) -> int:
    place_dec = 2*(inverse_place/count) - 1
    half_multi = count*0.4 if place_dec > 0 else (0 if place_dec == 0 else 1)
    return round(half_multi * place_dec * bet)

def make_racers(hp:int) -> [int]:
    bars = [hp*0.9, hp*1.1]
    count = round(hp/100 + 4)
    output = []
    for _ in range(count):
        while True:
            r_h = randint(round(bars[0]), round(bars[1]))
            if r_h != hp:
                output.append(r_h)
                break
    return output

def get_place(hp, racers:[int]):
    temp = racers.copy()
    temp.append(hp)
    temp.sort()
    temp.reverse()
    return temp.index(hp)+1

def get_inverse_place(hp, racers:list):
    temp = racers.copy()
    temp.append(hp)
    temp.sort()
    return temp.index(hp)+1
def format_cars(cars):
    text = ""
    for index, car in enumerate(cars):
        text += f"{index+1} {car['name']}\n| Price: £{car['price']}\n| Horsepower: {car['horsepower']}hp\n"
    return text

def make_racers(hp:int) -> [int]:
    bars = [hp*0.9, hp*1.1]
    count = round(hp/100 + 4)
    output = []
    for x in range(count):
        while True:
            r_h = randint(round(bars[0]), round(bars[1]))
            if r_h != hp:
                output.append(r_h)
                break
    return output

def valid_input(in_msg, clss, err_msg, f=None):
    while True:
        try:
            i = clss(input(in_msg))
            if f != None:
                if f(i):
                    return i
                else:
                    print(err_msg)
            else:
                return i
        except ValueError:
            print(err_msg)

def clear_screen_func(*o):
    os.system("cls" if os.name == "nt" else clear)

def exit_app_func(a, p, g):
    sys.exit("Thank you for playing!")

def display_cars(a, p, g:Garage):
    current = g.cur_car["name"]

    for index, car in enumerate(g.cars):
        print(f'{index + 1}|{car["name"]} - {car["horsepower"]} {"- SELECTED" if car["name"] == current else ""}')

def display_stats(a:str, p:Player, g:Garage):
    print(f"${p.money} | Car count - {len(g.cars)}")
    
def select_car_func(a, p:Player, g:Garage):
    while True:
        try:
            display_cars(a, p, g)
            pick = input("Pick (Press Enter to exit) >")
            if pick == "":
                break
            pick = int(pick)
            if 1 <= pick <= len(g.cars)+1:
                g.cur_car = pick-1
                print(f"{g.cars[pick-1]['name']} selected")
                break
        except ValueError:
            pass
        except EOFError:
            break

def display_func(a, p:Player, g:Garage):
    if "-c" in a:
        display_cars(a, p, g)
    if "-s" in a:
        display_stats(a, p, g)

def upgrade_func(a, p:Player, g:Garage):
    print(pyfiglet.figlet_format("Upgrade-stages", font="slant"))
    print(Tuner.get_stage_costs(g.cur_car["horsepower"], g.cur_car["mod-stage"]))
    while True:
        try:
            pick = int(input("Stage (Ctrl+D to exit)>"))
            if 0 < pick < 21:
                Tuner.upgrade_car(g.cur_car, pick, p)
                return {
                    "save":True
                }
            else:
                print("Invalid input")
        except EOFError:
            break
        except ValueError:
            print("Invalid input")

def create_loader(cap, length):
    with alive_bar(cap) as bar:
        for _ in range(cap):
            sleep(length/cap)
            bar()   

def get_cur_car(g:Garage):
    if g.cur_car != None:
        return g.cur_car

def race(a, p:Player, g):
    c_c = get_cur_car(g)
    bet = valid_input("Bet >", int, "Invalid bet", lambda a: 0<a<p.money)
    racers = make_racers(c_c["horsepower"])
    place = get_place(c_c["horsepower"], racers)
    inverse_place = get_inverse_place(c_c["horsepower"], racers)
    prize_money = calc_prize( inverse_place, len(racers)+1, bet)
    print(f"You won {prize_money}" if prize_money > 0 else f"You lost {-prize_money}", end="")
    print(" | You placed", "1st" if str(place)[-1] == "1" else ("2nd" if str(place)[-1] == "2" else ("3rd" if str(place)[-1] == "3" else f"{place}th")), f"out of {len(racers)+1} racers")

    p.money += prize_money
    return {
        "save":True
    }

def load_player(savesDB:SaveJson):
    if savesDB.existing_saves > 0:
        while True:
            d = input("Do you want to load a save (Y/N)?").lower()
            if d == "y":
                print(savesDB.format_saves(savesDB.saves), end="")
                while True:
                    try:
                        pick = input("SAVE (Ctrl+D to exit) >").strip()
                        if 0 < int(pick) < savesDB.existing_saves+1:
                            create_loader(100, 0.25)
                            break
                        else:
                            print("Invalid Save")
                    except ValueError:
                        print("Invalid Save")
                    except EOFError:
                        break
                save_json = savesDB.saves[pick]    
                savesDB.current_save = pick
                g = Garage()
                p = Player()
                g.load_from_save(save_json["garage"])
                p.load_from_save(save_json["player"])
                return g, p
                
            elif d == "n":
                g = Garage()
                g.new()
                p = Player()
                p.new()
                return g, p
    else:
        print("New Save")
        g = Garage()
        g.new()
        p = Player()
        p.new()
        savesDB.create_first_save(p, g)
        return g, p

ACTIONBUNDLE.add_multi([
    Action("clear", clear_screen_func),
    Action("quit", exit_app_func),
    Action("display", display_func),
    Action("select-car", select_car_func),
    Action("upgrade", upgrade_func),
    Action("race", race),
])