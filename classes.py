import json
from typing import List, Dict


        
class SaveJson:
    """
    DataBase Strut
        id(str): {
        "player":{},
        "garage": {},
        }
    """
    def __init__(self, filename:str="saves.json") -> None:
        self._filename = filename
        self._cursave = None

    @property
    def current_save(self):
        return self._cursave
    
    @current_save.setter
    def current_save(self, id:str):
        self._cursave = id

    def player_garage_to_json(player, garage) -> dict:
        return {
            "player":player.json,
            "garage":garage.json
        }

    def update_cur_save(self, player, garage):
        self.update_save(self._cursave, player, garage)

    def update_save(self, id, player, garage):
        if id in self.saves:
            cur_saves = self.saves
            cur_saves[id] = SaveJson.player_garage_to_json(player, garage)
            self.saves = cur_saves

    def create_first_save(self, player, garage):
        with open(self._filename, "w") as file:
            json.dump({"1":{
                "player":player.json,
                "garage":garage.json
            }}, file)
            self.current_save = "1"

    @property
    def existing_saves(self) -> int:
        with open(self._filename, "r") as file:
            data = json.load(file)
        return len([key for key in data])
    
    @property
    def saves(self):
        with open(self._filename, "r") as file:
            return json.load(file)
    
    @saves.setter
    def saves(self, data):
        with open(self._filename, "w") as file:
            json.dump(data, file)

    
    def new_save(self, player, garage) -> None:
        data = SaveJson.player_garage_to_json(player, garage)
        with open(self._filename, "w") as file:
            saves: dict = self.saves
            saves.update({str(self.existing_saves+1):data})
            json.dump(saves, file)
    
    def format_saves(self, saves):
        text = ""
        for x in saves:
            text+= f"\t{x}  |  Money:£{saves[x]['player']['money']} | Car Count: {len(saves[x]['garage'])}"
        text+="\n"
        return text

    def setup(self):
        no_of_saves = self.existing_saves
        if no_of_saves == 0:
            return False
        else:
            return True

class CarsJson:
    """database structure:
            list[
                name:str,
                horespower:int,
                price: int

            ]

    """

    def __init__(self, filename:str="cars.json"):
        self._filename = filename
    
    @property
    def cars(self):
        with open(self._filename, "r") as file:
            return json.load(file)
        
    @cars.setter
    def cars(self, c:list):
        with open(self._filename, "w") as file:
            json.dump(c)
        
    def add_car(self, name, horsepower, price, mod_stage) -> None:
        cur = self.cars
        cur.append({
            "name":name,
            "horsepower":horsepower,
            "price":price,
            "mod-stage":mod_stage
        })
        self.cars = cur
    
class Garage:
    def __init__(self):
        self.cars:list = [ ]
        self._curcar = 0

    def add_car(self, car):
        self.cars.append(car)

    def new(self):
        self.cars.append(
            {
                "name":"Silvia S15",
                "horsepower":100,
                "price":0,
                "mod-stage":0,
            }
        )
        
    @property
    def cur_car(self) -> dict:
        return self.cars[self._curcar]
    
    @cur_car.setter
    def cur_car(self, id) -> None:
        if 0 <= id <= len(self.cars):
            self._curcar = id
        else:
            raise ValueError

    @property
    def json(self) -> list:
        return self.cars
    
    def load_from_save(self, save):
        """
        Save Struct:
        [
            {
            "name":str,
            "horsepower":int,
            "price":int,
            "mod-stage":int
            }, 
            ...
        ]
        """
        self.cars = save

class Player:
    def __init__(self):
        self.money = 0
    
    def new(self):
        self.money = 1000
    
    def load_from_save(self, save):
        self.money = save["money"]

    @property
    def json(self) -> dict:
        return {
            "money":self.money
        }

class Mod:
    def __init__(self, name:str=None, func=None):
        self._name = name
        self._func = func

    def setup(self, name:str, func):
        self._name = name
        self._func = func
    
    def export(self):
        return {self._name:self._func}

    

class ModBundle:
    def __init__(self):
        self._mods = {}
    def add(self, mod:Mod):
        self._mods.update(mod.export())
    
    @property
    def mods(self):
        return self._mods
    
class Tuner:
    def __init__(self):
        pass


    def get_stage_costs(cur_hp:int, cur_stage:int):
        if cur_stage < 20:
            costs = [(stage, (stage**1.25)*100 + 100) for stage in range(cur_stage+1, 21)]
            hps = [cur_hp + stage*200 + stage**3 for stage in range(cur_stage+1, 21)]
            return "\n".join([f"{stage} ${cost} {hp}hp" for [stage,cost],hp in zip(costs, hps)])
        else:
            return "Fully Upgraded"
    def upgrade_car(car:dict, stage:int, person:Player):
        cur_stage = car["mod-stage"]
        cur_hp = car["horsepower"]
        relative_stage = stage - cur_stage
        costs = [(stage, (stage**1.25)*100 + 100) for stage in range(cur_stage+1, 21)]
        hps = [cur_hp + stage*200 + stage**3 for stage in range(cur_stage+1, 21)]
        if costs[relative_stage-1][1] <= person.money:
            person.money -= costs[relative_stage-1][1]
            car["mod-stage"] = stage
            car["horsepower"] = hps[relative_stage-1]
            print(f"Upgraded {car['name']} to stage {stage}")
        else:
            print("Not enough money in acount")


        
        return None



    