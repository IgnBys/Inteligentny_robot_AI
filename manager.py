from keeper import Keeper
from board import Board
from robot import Robot
from shelf import Shelf
from shelf import ShelfType
from client import Client
from charger import Charger
from package_generator import PackageGenerator

class Manager():

    def __init__(self, sis=20):
        self.shelf_inventory_size = sis

    def board_from_string(self, blueprint: str) -> Board:

        column_count = 0
        for i in blueprint:
            if (i == '\n'):
                break
            else:
                column_count += 1
        row_count = len(blueprint) / (column_count + 1)  # we take into account '\n' character
        board = Board(column_count, row_count)

        def calculate_position(pos: int):
            x = pos % column_count
            y = pos // column_count
            return (x, y)

        position = 0
        memory = []
        for i in blueprint:
            if i != '\n':
                if i != '0':
                    memory.append((i, position))
                position += 1
        robots = []
        generators = []
        clients = []
        shelves = []
        chargers=[]
        i_position_in_memory = 0
        sis = self.shelf_inventory_size
        for i in memory:
            x, y = calculate_position(i[1])
            match i[0]:
                case 'R':
                    robots.append(Robot(i_position_in_memory, x, y, board))

                case 'G':
                    generators.append(PackageGenerator(i_position_in_memory, x, y, board,ShelfType._member_names_))

                case 'C':
                    clients.append(Client(i_position_in_memory, x, y, board))
                case 'B':
                    chargers.append(Charger(i_position_in_memory,x, y,board))
                case _:
                    shelves.append(Shelf(i_position_in_memory, sis, x, y, board,ShelfType(int(i[0])).name))
                # TODO: add type
            i_position_in_memory += 1
        return (board, robots, generators, clients,chargers, shelves)

    def trade(self, giver: Keeper, taker: Keeper):
        try:
            wanted_package, wanted_package_position = giver.get_wanted_package(giver.get_inventory())
            if taker.inventory_taken + wanted_package.get_size() <= taker.inventory_size:
                giver.pop_package(wanted_package_position)
                taker.insert_package(wanted_package)
            else:
                print("taker has no room in inventory")
        except:
            # TODO
            print("taker has no wanted package")

    # TODO: find_nearby_keeper
    # def find_nearby_keeper(self):

    # def trade_with_id wywołuje metodę get_wanted_package_by_id w której szuka paczkę o niezbędnym id (wanted_id)
    # i sprawdza czy taker ma wolne miejsce dla umieszczenia paczki

    def trade_with_id(self, giver: Keeper, taker: Keeper, wanted_id):
        try:
            wanted_package, wanted_package_position = giver.get_wanted_package_by_id(giver.get_inventory(), wanted_id)
            if taker.inventory_taken + wanted_package.get_size() <= taker.inventory_size:
                giver.pop_package(wanted_package_position)
                taker.insert_package(wanted_package)
            else:
                print("taker has no room in inventory")
        except:
            # TODO
            print("taker has no wanted package")
