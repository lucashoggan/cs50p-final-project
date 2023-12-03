import sys
import os
from time import sleep
from typing import List
from classes import  SaveJson, CarsJson, Garage, Player, Tuner
from random import randint
import pyfiglet
from alive_progress import alive_bar



VERSION = 0.1
TESTING = False
carsDB = CarsJson("cars.json")
savesDB = SaveJson("saves.json")

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

def print_if_testing(*objects, end="\n"):
    if TESTING: print(*objects, end=end)

def calc_prize(inverse_place, count, bet) -> int:
    place_dec = 2*(inverse_place/count) - 1
    half_multi = count*0.4 if place_dec > 0 else (0 if place_dec == 0 else 1)
    print_if_testing(half_multi, place_dec, bet, inverse_place)
    return round(half_multi * place_dec * bet)

def make_racers(hp:int) -> List[int]:
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

def get_place(hp, racers:List[int]):
    temp = racers.copy()
    temp.append(hp)
    temp.sort()
    temp.reverse()
    return temp.index(hp)+1

def get_inverse_place(hp, racers:list):
    temp = racers.copy()
    temp.append(hp)
    temp.sort()
    print_if_testing(temp)
    return temp.index(hp)+1


def create_loader(cap, length):
    with alive_bar(cap) as bar:
        for _ in range(cap):
            sleep(length/cap)
            bar()   

def load_player():
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

def exit_app(a, p, g):
    if "-ds" not in a:
        savesDB.update_cur_save(p, g)
    sys.exit("Thank you for playing!")

def display_cars(a, p:Player, g:Garage):
    current = g.cur_car["name"]
    for index, car in enumerate(g.cars):
        print(f'{index + 1}|{car["name"]} - {car["horsepower"]} {"- SELECTED" if car["name"] == current else ""}')

def select_car(a, p:Player, g:Garage):
    while True:
        try:
            display_cars(a, p, g)
            pick = int(input("Pick (Ctrl+D to exit) >"))
            if 1 <= pick <= len(g.cars)+1:
                g.cur_car = pick-1
                print(f"{g.cars[pick-1]['name']} selected")
                break

        except ValueError:
            pass
        except EOFError:
            break

def clear_screen(*o):
    os.system('cls' if os.name == 'nt' else 'clear')

def save(a, p, g):
    print("Progress Saved!")
    print(savesDB.current_save)
    savesDB.update_cur_save(p, g)

def format_cars(cars):
    text = ""
    for index, car in enumerate(cars):
        text += f"{index+1} {car['name']}\n| Price: £{car['price']}\n| Horsepower: {car['horsepower']}hp\n"
    return text

def dealership(a, p, g:Garage):
    cars = carsDB.cars
    print(format_cars(cars), end="")
    while True:
        try:
            pick = int(input("Pick (Ctrl+D to exit)>").strip())
            if not (1 <= pick <= len(cars)):
                raise ValueError
            car_price = cars[pick-1]['price']
            if p.money >= car_price:
                g.add_car(cars[pick-1])
                p.money -= car_price
                print(f"{cars[pick-1]['name']} bought")
                break
            else:
                print("Not enough funds")
                break
        except ValueError:
            print("Invalid Value")
        except EOFError:
            break

    return {
        "save":True
    }

def get_cur_car_hp(g:Garage):
    if g.cur_car != None:
        return g.cur_car



def race(a, p:Player, g):
    c_c = get_cur_car_hp(g)
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

def upgrade(a, p:Player, g:Garage):
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
        
    

def display(a, p:Player, g:Garage):
    if "-c" in a:
        display_cars(a, p, g)
    if "-s" in a:
        display_stats(a, p, g)

def display_stats(a:str, p:Player, g:Garage):
    print(f"${p.money} | Car count - {len(g.cars)}")


actions = {
        "quit":exit_app,
        "display":display,
        "clear":clear_screen,
        "save":save,
        "dealership":dealership,
        "select-car":select_car,
        "race":race,
        "upgrade":upgrade
}

def help():
    global actions
    desc = {
        "display": "-s to display stats, -c to display cars"
    }
    print(pyfiglet.figlet_format("HELP", font="slant"))
    for action in actions:
        
        if action not in desc:
            print(action)
        else:
            print(action, "|", desc[action])

    

def main():
    global actions
    print(pyfiglet.figlet_format("TEXT-TURBO", font="slant"))
    print(f"v{VERSION}")    
    GARAGE, PLAYER = load_player()
    while True:
        action = input(">").strip()
        found = False
        for name in actions:
            if action.split(" ")[0] == name:
                found = True
                result = actions[name]("".join(action.split(name)).strip(), PLAYER, GARAGE)
                if result != None:
                    try:
                        if result["save"] == True:
                            savesDB.update_cur_save(PLAYER, GARAGE)
                    except KeyError:
                        pass
        if action.startswith("help"):
            help()
        elif not found:
            print("Not an comand, use \"help\" to get a list of all commands")


if __name__ == "__main__":
    main()
    
