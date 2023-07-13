import os
import sys
from enum import Enum
import pygame


class ShelfType(Enum):
    PLANTS = 1
    FOOD = 2
    CLOTHES = 3
    ELECTRONICS = 4
    GARDEN_HOUSE = 5
    SPORT = 6
    NOT_ASSIGNED = 7

class Board():
    def __init__(self,width,height, scale=40, background_color=(255,255,255)): #width in squares times scale equals actual pixels
        self.width=int(width)
        self.height=int(height)
        self.scale=scale
        self.window = pygame.display.set_mode((width*scale,height*scale ))
        self.background_color = background_color
        self.Img = pygame.image.load(os.path.join(parent_dir, 'src', 'bg.png')).convert_alpha()
        pass

    def draw_window(self):
        self.window.fill(self.background_color)
        self.window.blit(self.Img, (0,0))
        self.draw_grid()

    def draw_grid(self):
        global size_between
        size_between = self.scale
        x = 0
        y = 0
        if(self.width>self.height):
            bigger=self.width
        else:
            bigger=self.height
        for i in range(bigger):
            x = x + size_between
            y = y + size_between
            pygame.draw.line(self.window, (150, 150, 150), (x, 0), (x, self.height * self.scale))
            pygame.draw.line(self.window, (130, 130, 130), (0, y), (self.width * self.scale, y))

class Robot:
    def __init__(self,id,posx,posy, board:Board,color=(204, 102, 0)):
        self.id = id
        self.posx = posx
        self.posy = posy
        self.board = board
        self.color = color
        self.img = pygame.image.load(os.path.join(parent_dir, 'src', 'robotWithDirection.png')).convert_alpha()
        self.robotImg = None

    def draw(self):
        point_x0 = self.posx*self.board.scale
        point_y0 = self.posy*self.board.scale
        size_between = self.board.scale
        self.robotImg = pygame.transform.scale(self.img, (size_between - 1, size_between - 1))
        self.board.window.blit(self.robotImg, (point_x0 + 1, point_y0 + 1))

class PackageGenerator:
    def __init__(self,id,posx,posy,board,types_list=["SPORT"]):
        self.id=id
        self.posx=posx
        self.posy=posy
        self.board=board
        self.color=(255, 163, 140)
        self.types_list=types_list
    def draw(self):
        point_x0 = self.posx*self.board.scale
        point_y0 = self.posy*self.board.scale
        color=self.color
        size_between=self.board.scale
        pygame.draw.rect(self.board.window, color, (point_x0 + 1, point_y0 + 1,
                                               size_between - 1, size_between - 1))

class Shelf:
    def __init__(self, id, inventory_size, posx, posy, board, type, color=(255, 255, 0)):

        self.posx = posx
        self.posy = posy
        self.size = inventory_size
        self.id = id
        self.board = board
        self.type = type
        self.color = color
        if (self.type == "PLANTS"):
            shelf = pygame.image.load(os.path.join(parent_dir, 'src', 'plants_green_shelf.png ')).convert()
        # for food
        elif (self.type == "FOOD"):
            shelf = pygame.image.load(os.path.join(parent_dir, 'src', 'food_blue_shelf.png')).convert()
            # for clothes
        elif (self.type == "CLOTHES"):
            shelf = pygame.image.load(os.path.join(parent_dir, 'src', 'clothes_shelf_yellow.png')).convert()
            # for electronics
        elif (self.type == "ELECTRONICS"):
            shelf = pygame.image.load(os.path.join(parent_dir, 'src', 'electronics_shelf_grey.png')).convert()
            # for garden and house
        elif (self.type == "GARDEN_HOUSE"):
            shelf = pygame.image.load(os.path.join(parent_dir, 'src', 'garden_house_shelf_brown.png')).convert()
        # for sport
        elif (self.type == "SPORT"):
            shelf = pygame.image.load(os.path.join(parent_dir, 'src', 'sport_shelf_red.png')).convert()
        else:
            shelf = pygame.image.load(os.path.join(parent_dir, 'src', 'something_shelf_lilac.png')).convert()

        size_between = self.board.scale
        if (self.size // size_between == 2):
            self.shelfImg = pygame.transform.scale(shelf, (2 * size_between - 2, size_between - 1))
        else:
            self.shelfImg = pygame.transform.scale(shelf, (size_between - 1, size_between - 1))

    def set_xy(self):
        return self.posx * self.board.scale, self.posy * self.board.scale

    def draw(self):
        surface = self.board.window
        point_x0, point_y0 = self.set_xy()
        surface.blit(self.shelfImg, (point_x0 + 1, point_y0 + 1))


class Client:
    def __init__(self, id, posx, posy, board, color=(21, 214, 195)):
        self.id = id
        self.posx = posx
        self.posy = posy
        self.color = color
        self.board = board

    def draw(self):
        point_x0 = self.posx * self.board.scale
        point_y0 = self.posy * self.board.scale
        size_between = self.board.scale
        pygame.draw.rect(self.board.window, self.color, (point_x0 + 1, point_y0 + 1,
                                                         size_between - 1, size_between - 1))


class Charger:
    def __init__(self,id,posx,posy,board):
        self.board = board
        self.Img = pygame.transform.scale( pygame.image.load(os.path.join(parent_dir, 'src', 'charger.png')).convert_alpha(), (self.board.scale - 1, self.board.scale - 1))
        self.id=id
        self.posx = posx
        self.posy = posy

    def draw(self):
        point_x0 = self.posx * self.board.scale
        point_y0 = self.posy * self.board.scale
        self.board.window.blit(self.Img, (point_x0 + 1, point_y0 + 1))

def board_from_string(blueprint: str) -> Board:
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
    chargers = []
    i_position_in_memory = 0
    sis = 20
    for i in memory:
        x, y = calculate_position(i[1])
        match i[0]:
            case 'R':
                robots.append(Robot(i_position_in_memory, x, y, board))

            case 'G':
                generators.append(PackageGenerator(i_position_in_memory, x, y, board, ShelfType._member_names_))

            case 'C':
                clients.append(Client(i_position_in_memory, x, y, board))
            case 'B':
                chargers.append(Charger(i_position_in_memory, x, y, board))
            case _:
                shelves.append(Shelf(i_position_in_memory, sis, x, y, board, ShelfType(int(i[0])).name))
            # TODO: add type
        i_position_in_memory += 1
    return (board, robots, generators, clients, chargers, shelves)

if __name__ == "__main__":
    global board, robots, generators, clients, chargers, shelves, clock
    global parent_dir
    clock = pygame.time.Clock()
    parent_dir = os.path.dirname(os.getcwd())
    dir = os.getcwd() + "/boards"

    for filename in os.scandir(dir):
        if filename.is_file():
            go = True
            f = open(filename.path, "r")
            print(filename.name)
            board_string =f.read()
            (board, robots, generators, clients, chargers, shelves) = board_from_string(board_string)
            while go:
                clock.tick(20)
                board.draw_window()
                for i in shelves:
                    i.draw()
                for i in generators:
                    i.draw()
                for i in clients:
                    i.draw()
                for i in chargers:
                    i.draw()
                for i in robots:
                    i.draw()
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        raise SystemExit
                    if event.type == pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_RIGHT: #for the next testBoard
                                f.close()
                                go = False
                            case pygame.K_UP:
                                g=open("..\chosen_board.txt","w")
                                g.write(board_string)
                                f.close()
                                g.close()
                                raise SystemExit