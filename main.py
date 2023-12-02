import math
import sys
import os
from time import sleep
from typing import List
from classes import Car, SaveJson, CarsJson, Garage, Player
from random import randint
import pyfiglet
from alive_progress import alive_bar


VERSION = 0.1
TESTING = False
carsDB = CarsJson("cars.json")
savesDB = SaveJson("saves.json")

def print_if_testing(*objects, end="\n"):
    if TESTING: print(*objects, end=end)

def calc_prize(inverse_place, count, bet) -> int:
    place_dec = 2*(inverse_place/count) - 1
    half_multi = count*0.4 if place_dec > 0 else (0 if place_dec == 0 else 1)
    print_if_testing(half_multi, place_dec, bet, inverse_place)
    return round(half_multi * place_dec * bet)

def make_racers(hp:int) -> List[int]:
    bars = [hp*.75, hp*1.1]
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
                        pick = input("SAVE>").strip()
                        if 0 < int(pick) < savesDB.existing_saves+1:
                            create_loader(100, 0.25)
                            break
                        else:
                            print("Invalid Save")
                    except ValueError:
                        print("Invalid Save")
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
            pick = int(input("Pick >"))
            if 1 <= pick <= len(g.cars)+1:
                g.cur_car = pick-1
                print(f"{g.cars[pick-1]['name']} selected")
                break

        except ValueError:
            pass

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
    try:
        pick = int(input("Pick >").strip())
        if not (1 <= pick <= len(cars)):
            raise ValueError
        car_price = cars[pick-1]['price']
        if p.money >= car_price:
            g.add_car(cars[pick-1])
            p.money -= car_price
            print(f"{cars[pick-1]['name']} bought")
            
            
            

    except ValueError:
        print("Invalid Value")

def get_cur_car_hp(g:Garage):
    if g.cur_car != None:
        return g.cur_car

def get_int_in(*objects):
    output = []
    for object in objects:
        while True:
            try:
                i = int(input(object[0]))
                if len(object) == 2:
                    if object[1](i) == True:
                        output.append(i)
                        break
                else:
                    output.append(i)
                    break
            except ValueError:
                pass
    return output

def race(a, p:Player, g):
    c_c = get_cur_car_hp(g)
    bet = get_int_in(("Bet> ", lambda a: 0<a<p.money))[0]
    racers = make_racers(c_c["horsepower"])
    place = get_place(c_c["horsepower"], racers)
    inverse_place = get_inverse_place(c_c["horsepower"], racers)
    prize_money = calc_prize( inverse_place, len(racers)+1, bet)
    print(f"You won {prize_money}" if prize_money > 0 else f"You lost {-prize_money}", end="")
    print(" | You placed", "1st" if place == 1 else ("2nd" if place == 2 else f"{place}rd"), f"out of {len(racers)+1} racers")

    p.money += prize_money

def display_stats(a:str, p:Player, g:Garage):
    print(f"${p.money} | Car count - {len(g.cars)}")

def main():
    print(pyfiglet.figlet_format("TEXT-TURBO", font="slant"))
    print(f"v{VERSION}")    
    GARAGE, PLAYER = load_player()
    actions = {
        "display-stats":display_stats, 
        "quit":exit_app,
        "display-cars":display_cars,
        "clear":clear_screen,
        "save":save,
        "dealership":dealership,
        "select-car":select_car,
        "race":race
    }
    while True:
        action = input(">").strip()
        for name in actions:
            if action.startswith(name):
                actions[name](action.split(name)[0].strip(), PLAYER, GARAGE)


if __name__ == "__main__":
    main()
    """
    while True:
        hp = int(input("Hp>"))
        bet = int(input("Bet>"))
        racers = make_racers(hp)
        place = get_place(hp, racers)
        inverse_place = get_inverse_place(hp, racers)
        print(calc_prize(place, inverse_place, len(racers), bet), place, len(racers), inverse_place)
"""
