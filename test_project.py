from pytest import raises
from project import calc_prize, make_racers, get_place, get_inverse_place, format_cars, get_cur_car
from classes import Garage, Player

def test_format_cars():
    assert format_cars([{
        "name":"mustang",
        "price":5000,
        "horsepower":500
    }]) == "1 mustang\n| Price: £5000\n| Horsepower: 500hp\n"

    with raises(KeyError):
        format_cars([{
            "price":10,
            "horsepower":500
        }])


def test_cur_car():
    g = Garage()
    assert get_cur_car(g) == None
    g.new()
    assert g.cur_car == {
                "name":"Silvia S15",
                "horsepower":100,
                "price":0,
                "mod-stage":0,
            }
    g.add_car(
        {"name":"720S",
    "horsepower":710,
    "price":90000,
    "mod-stage":0   
    }
    )
    g.cur_car = 1
    assert g.cur_car == {"name":"720S",
    "horsepower":710,
    "price":90000,
    "mod-stage":0   
    }

def test_get_place():
    assert get_place(100, [50, 60, 70, 80]) == 1
    assert get_place(50, [100, 110, 160]) == 4
    assert get_place(100, [50, 70, 60, 110]) == 2

def test_calc_prize():
    assert calc_prize(25, 25, 100) == 1000
    assert calc_prize(50, 100, 2500) == 0

    with raises(ValueError):
        calc_prize(50, 25, 10)

def test_make_racers():
    assert len(make_racers(100)) == 5
    assert min(make_racers(100)) >= 90
    assert max(make_racers(100)) <= 110

def test_inverse_place():
    assert get_inverse_place(100, [50, 60, 70, 80]) == 5
    assert get_inverse_place(50, [100, 110, 160]) == 1
    assert get_inverse_place(100, [50, 70, 60, 110]) == 4

