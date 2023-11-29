from time import sleep
from classes import Car, SaveJson, CarsJson, Garage, Player
import pyfiglet
from alive_progress import alive_bar


VERSION = 0.1
carsDB = CarsJson("cars.json")
savesDB = SaveJson("saves.json")

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
        g = Garage()
        g.new()
        p = Player()
        p.new()
        return g, p

def display_stats(a:str, p:Player, g:Garage):
    print(p.money)

def main():
    print(pyfiglet.figlet_format("TEXT-TURBO", font="slant"))
    print(f"version: {VERSION}")    
    GARAGE, PLAYER = load_player()
    actions = {"display":display_stats}
    while True:
        action = input(">").strip()
        for name in actions:
            if action.startswith(name):
                actions[name](action.split(name)[0].strip(), PLAYER, GARAGE)

if __name__ == "__main__":
    main()