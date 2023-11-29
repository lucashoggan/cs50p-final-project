import json

class Car:
    def __init__(self, information):
        try:
            self._horsepower = information["horsepower"]
            self._name = information["name"]
            self._price = information["price"]
        except KeyError:
            raise ValueError("Invalid information")

    @property
    def horsepower(self):
        return self._horsepower
    
    @horsepower.setter
    def horsepower(self, hp:int):
        if hp > 0:
            self._horsepower = hp
        else:
            raise ValueError("Invalid horsepower")

    @property    
    def json(self):
        return {
            "horsepower":self._horsepower,
            "name":self._name,
        }
        
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
    
    def __str__(self) -> str:
        ## TODO impliment to show all existing saves
        pass

    @property
    def existing_saves(self) -> int:
        with open(self._filename, "r") as file:
            data = json.load(file)
        return len([key for key in data])
    
    @property
    def saves(self):
        with open(self._filename, "r") as file:
            return json.load(file)
    
    def new_save(self, player, garage) -> None:
        data = {
            "player":player.json,
            "garage":garage.json
        }
        with open(self._filename, "w") as file:
            saves: dict = self.saves
            saves.pop({str(self.existing_saves+1):data})
            json.dump(saves, file)
    
    def format_saves(self, saves):
        text = ""
        for x in saves:
            text+= f"\t{x}  |  Money:£{0} | Car Count: {1}"
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
        
    def add_car(self, name, horsepower, price) -> None:
        cur = self.cars
        cur.append({
            "name":name,
            "horsepower":horsepower,
            "price":price
        })
        self.cars = cur
    
class Garage:
    def __init__(self):
        self.cars = [ ]

    def new(self):
        self.cars.append(
            {
                "name":"Silvia S15",
                "horsepower":100,
                "price":0,
            }
        )
    
    def load_from_save(self, save):
        """
        Save Struct:
        [
            {
            "name":str,
            "horsepower":int,
            "price",
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

        




    