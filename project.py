import sys
import os
from time import sleep
from typing import List
from classes import  SaveJson, CarsJson, Garage, Player, Tuner
from random import randint
import pyfiglet
from alive_progress import alive_bar
from actions import ACTIONBUNDLE, create_loader, load_player



VERSION = 1.0
TESTING = False
carsDB = CarsJson("cars.json")
savesDB = SaveJson("saves.json")



def calc_prize(inverse_place, count, bet) -> int:
    place_dec = 2*(inverse_place/count) - 1
    if place_dec > 1:
        raise ValueError
    half_multi = count*0.4 if place_dec > 0 else (0 if place_dec == 0 else 1)
    return round(half_multi * place_dec * bet)

def make_racers(hp:int) -> List[int]:
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
    return temp.index(hp)+1




def format_cars(cars):
    text = ""
    for index, car in enumerate(cars):
        text += f"{index+1} {car['name']}\n| Price: £{car['price']}\n| Horsepower: {car['horsepower']}hp\n"
    return text



def get_cur_car(g:Garage):
    if g.cur_car != None:
        return g.cur_car


        


def main():
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
    actions = {
        "dealership":dealership,
    }
    actions.update(ACTIONBUNDLE.actions)

    def help():
        
        desc = {
            "display": "-s to display stats, -c to display cars"
        }
        print(pyfiglet.figlet_format("HELP", font="slant"))
        for action in actions:
            
            if action not in desc:
                print(action)
            else:
                print(action, "|", desc[action])
    
    print(pyfiglet.figlet_format("TEXT-TURBO", font="slant"))
    print(f"v{VERSION}")    
    GARAGE, PLAYER = load_player(savesDB)
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
            print("Not an command, use \"help\" to get a list of all commands")


if __name__ == "__main__":
    main()
    
