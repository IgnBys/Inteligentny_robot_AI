import math
import pygame
import sys
import package
import os
from keeper import Keeper
from board import Board
from collections import deque
from shelf import Shelf
from client import Client
import itertools
from package_generator import PackageGenerator
from queue import PriorityQueue
from charger import Charger


class Robot(Keeper):
    def __init__(self,id,posx,posy, board:Board,color=(204, 102, 0),inventory_size=1):
        super().__init__(id, inventory_size, posx, posy)
        self.board = board
        self.color = color
        self.robotImg = None
        self.inventory_taken = 0
        self.inventory = list()
        self.nearby_keeper = None
        self.direction = 0
        self.shelvesLog = list() #nie trzeba packagesLog bo do shelfsLog.add(shelf[0]), a szelf sam w sobie trzyma inventory
        self.generatorsLog = list()
        self.clientsLog = list()
        self.Img = pygame.image.load(os.path.join('src', 'robotWithDirection.png')).convert_alpha()
        self.ImgRight = pygame.image.load(os.path.join('src', 'robotWithDirectionRight.png')).convert_alpha()
        self.ImgLeft = pygame.image.load(os.path.join('src', 'robotWithDirectionLeft.png')).convert_alpha()
        self.ImgDown = pygame.image.load(os.path.join('src', 'robotWithDirectionDown.png')).convert_alpha()
        self.energy_level = 10
    #   0
    # 3     1
    #   2

    def fill_logs(self, log, item=None):
        if log == "shelvesLog" and (type(item) is Shelf):
            if item:
                self.shelvesLog.append(item)
        elif log == "generatorsLog" and (type(item) is PackageGenerator):
            if item:
                self.generatorsLog.append(item)
        elif log == "clientsLog" and (type(item) is Client):
            if item:
                self.clientsLog.append(item)

    def update_log(self):
        if (type(self.nearby_keeper) is Shelf) and self.shelvesLog:
            for index, item in enumerate(self.shelvesLog):
                if item.posx == self.nearby_keeper.posx and item.posy == self.nearby_keeper.posy:
                    self.shelvesLog[index] = self.nearby_keeper
        elif (type(self.nearby_keeper) is Client) and self.clientsLog:
            for index, item in enumerate(self.clientsLog):
                if item.posx == self.nearby_keeper.posx and item.posy == self.nearby_keeper.posy:
                    self.clientsLog[index] = self.nearby_keeper
        elif (type(self.nearby_keeper) is PackageGenerator) and self.generatorsLog:
            for index, item in enumerate(self.generatorsLog):
                if item.posx == self.nearby_keeper.posx and item.posy == self.nearby_keeper.posy:
                    self.generatorsLog[index] = self.nearby_keeper

    def rotate_left(self):
        self.direction = (self.direction - 1) % 4
       # print("direction", str(self.direction))

    def rotate_right(self):
        self.direction = (self.direction + 1) % 4
     #  print("direction", str(self.direction))
    def correct_illegal_movement(self):
        # if robot goes abroad
        if self.posx < 0:
            self.posx += 1

        elif self.posx >= self.board.width:
            self.posx -= 1

        elif self.posy < 0:
            self.posy += 1

        elif self.posy >= self.board.height:
            self.posy -= 1
        if (self.board.positions[self.posx,self.posy]!=self.id):
            self.rotate_right()
            self.rotate_right()
            self.forward()
            self.rotate_right()
            self.rotate_right()
    def forward(self):
        match self.direction:
            case 0:
                self.posy -= 1
            case 1:
                self.posx += 1
            case 2:
                self.posy += 1
            case 3:
                self.posx -= 1

    def turnByDirection(self, size_between):

        if self.direction == 0:
            turnImg = pygame.transform.scale(self.ImgDown, (size_between - 1, size_between - 1))
        elif self.direction == 1:
            turnImg = pygame.transform.scale(self.ImgRight, (size_between - 1, size_between - 1))
        elif self.direction == 2:
            turnImg = pygame.transform.scale(self.Img, (size_between - 1, size_between - 1))
        elif self.direction == 3:
            turnImg = pygame.transform.scale(self.ImgLeft, (size_between - 1, size_between - 1))
        return turnImg


    def move_test(self, letter, charger):
        self.energy_level-=1
        if letter == 'f':
            self.forward()
            # number_of_list.pop(0)
            letter = 'up'
        elif letter == 'r':
            self.rotate_right()
            letter = 'right'
        elif letter == 'l':
            self.rotate_left()
            letter = 'left'
        elif letter == 'c':
            self.start_charging(charger)
        elif letter == 't':#take
            for i in range (0,1):
                self.trade(self.nearby_keeper)
        elif letter == 'g':#give
            for i in range (0,len(self.inventory)):
                self.nearby_keeper.trade(self)
    #    self.correct_illegal_movement()
        #print(f"el:{self.energy_level}")
        return letter

    def start_charging(self, charger: Charger):
        if (self.posx == charger.posx and self.posy == charger.posy):
            #print("Charging.")
            charger.charge(self)

    def move(self):
        size_between = 1
        letter=None
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_a:
                            self.posx -= size_between
                            letter = 'a'
                        case pygame.K_d:
                            self.posx += size_between
                            letter = 'd'
                        case pygame.K_w:
                            self.posy -= size_between
                            letter = 'w'
                        case pygame.K_s:
                            self.posy += size_between
                            letter = 's'
                        case pygame.K_j: #robot oddaje paczke
                            if self.nearby_keeper is not None:
                                self.nearby_keeper.trade(self)
                                try:
                                    self.update_log()
                                except:
                                    print("cos nie tak z oddaniem")
                            letter = 'j'
                        case pygame.K_k: #robot bierze paczke
                            if self.nearby_keeper is not None:
                                self.trade(self.nearby_keeper)
                                try:
                                    self.update_log()
                                except:
                                    print("cos nie tak z odbieraniem paczki")
                            letter = 'k'
                        case pygame.K_UP:
                            self.forward()
                            letter='up'
                        case pygame.K_RIGHT:
                            letter = 'right'
                            self.rotate_right()
                        case pygame.K_LEFT:
                            self.rotate_left()
                            letter = 'left'

                        case pygame.K_q:
                            pygame.quit()
                            sys.exit()

        self.correct_illegal_movement()
        return letter
    def draw(self):
        point_x0 = self.posx*self.board.scale
        point_y0 = self.posy*self.board.scale
        size_between = self.board.scale
        self.robotImg = self.turnByDirection(size_between)
        self.board.window.blit(self.robotImg, (point_x0 + 1, point_y0 + 1))



class State:
    def __init__(self, posx, posy, turn,actions=""):
            self.posx = posx
            self.posy = posy
            self.turn = turn
            self.parent = None
            self.actions=actions

def bfs(fringe, instate, goal, limitx, limity,robot):
        action = ("l", "r", "f")  # mozliwe ruchy: left right forward
        explored = []
        fringe.append(instate)
        while True:
            if not fringe:
                print("no way")  # nie znalazl drogi
                return [" "]
            elem = fringe.popleft()

            #print(elem.posx, elem.posy)
            if (elem.posx == goal[0] and elem.posy==goal[1]):
                return elem.actions #wynik to lista krokow np. lrfrllflflr
            for a in action:
                s = State(elem.posx,elem.posy,elem.turn,elem.actions)
                s.parent = elem
                isok = True
            #wykonanie akcji
                match a:
                    case "f":
                        match s.turn:
                            case 0:
                                s.posy -= 1
                                if (s.posy <0):
                                    isok = False
                            case 1:
                                s.posx += 1
                                if (s.posx > limitx):
                                    isok = False
                            case 2:
                                s.posy += 1
                                if (s.posy > limity):
                                    isok = False
                            case 3:
                                s.posx -= 1
                                if (s.posx < 0):
                                    isok = False
                        try:
                            if robot.board.positions[s.posx,s.posy]!=0:
                                isok=False
                        except:
                            pass
                        s.actions = s.actions + "f"
                    case "l":
                        s.turn = (s.turn - 1) % 4
                        s.actions = s.actions + "l"
                    case "r":
                        s.turn = (s.turn + 1) % 4
                        s.actions = s.actions + "r"
                for i in explored:
                    if (i.posx == s.posx and i.posy == s.posy and i.turn == s.turn):
                        isok=False
                        break
                if (isok == True):
                    fringe.append(s)
                    explored.append(s)



class AStarState:
    def __init__(self, posx, posy, turn, action="", actions="", g_score=0, h_score=0, f_score=0):
            self.posx = posx
            self.posy = posy
            self.turn = turn
            self.parent = None
            self.action = action # ruch tego wezla; jest potrzebny dla recursion path
            self.g_score = g_score
            self.h_score = h_score
            self.f_score = f_score

def a_star(instate, goal, limitx, limity, board):
    count=itertools.count(start=0, step=1)
    fringe = PriorityQueue()
    def path(node):
        if node.parent is None:
            return node.action
        else:
            return (path(node.parent) + node.action)

    def heuristic(f_cell, g_cell):
        x1, y1 = f_cell
        x2, y2 = g_cell
        res = abs(x1 - x2) + abs(y1 - y2)
        return res

    action = ("l", "r", "f")  # mozliwe ruchy: left right forward
    explored = []
    costs = {
        "l": 1,
        "r": 1,
        "f": 1,
        "shelf": 6,
        "generator": 2,
        "client": 2
    }
    instate.f_score = heuristic((instate.posx, instate.posy), (goal[0], goal[1]))
    fringe.put((instate.f_score,next(count),instate))
    open_list = deque()

    while True:
        if not fringe:
            print("no way")
            return [" "]
        elem = fringe.get()[2]
        #open_list.append(elem)


        if (elem.posx == goal[0] and elem.posy == goal[1]):
           # print("\ng_score ==", str(elem.g_score))
           # print("h_score ==", str(elem.h_score))
           # print("f_score ==", str(elem.f_score))
            return path(elem)  # wynik to lista krokow np. lrfrllflflr

        for a in action:
            s = AStarState(elem.posx, elem.posy, elem.turn, elem.action)
            s.parent = elem
            isok = True
            in_explored = False
            match a:
                case "f":
                    match s.turn:
                        case 0:
                            s.posy -= 1
                            if (s.posy < 0):
                                isok = False
                        case 1:
                            s.posx += 1
                            if (s.posx > limitx):
                                isok = False
                        case 2:
                            s.posy += 1
                            if (s.posy > limity):
                                isok = False
                        case 3:
                            s.posx -= 1
                            if (s.posx < 0):
                                isok = False

                    s.action = "f"
                case "l":
                    s.turn = (s.turn - 1) % 4
                    s.action = "l"
                case "r":
                    s.turn = (s.turn + 1) % 4
                    s.action = "r"
            if isok:
                block = costs[a]
                if a == 'f':
                    try:
                        id = board.positions[s.posx, s.posy]
                    except:
                        id = 0

                    if id != 0:
                        place = board.itemsTable[id]
                        match place:
                            case "generator":
                                block = costs[place]
                            case "client":
                                block = costs[place]
                            case "shelf":
                                block = costs[place]
                        #print("\tplace: ", str(place), "; cost = ", str(block))

                    try:
                        bias=board.biases[s.posx][s.posy]
                    except IndexError:
                        bias=0 #its out of bounds
                else:
                    bias=0
                temp_g_score = elem.g_score + block+bias
                temp_h_score = heuristic((s.posx, s.posy), (goal[0], goal[1]))
                temp_f_score = temp_g_score + temp_h_score

                for i in explored:
                    if (i.posx == s.posx and i.posy == s.posy and i.turn == s.turn):
                        in_explored = True
                        break

                for i in open_list:
                    if (i.posx == s.posx and i.posy == s.posy and i.turn == s.turn):
                        if temp_f_score < i.f_score:
                           # print("if p < priority:")

                            open_list.remove(i)

                            s.g_score = temp_g_score
                            s.h_score = temp_h_score
                            s.f_score = temp_f_score

                        #    print("\n\ts.g_score ==", str(s.g_score))
                         #   print("\ts.h_score ==", str(s.h_score))
                          #  print("\ts.f_score ==", str(s.f_score))

                            fringe.put((s.f_score,next(count),s))
                            open_list.append(s)
                            explored.append(s)

                            isok = False
                            break

                if isok and not in_explored:
                    s.g_score = temp_g_score
                    s.h_score = temp_h_score
                    s.f_score = temp_f_score

                   # print("\n\ts.g_score ==", str(s.g_score))
                   # print("\ts.h_score ==", str(s.h_score))
                   # print("\ts.f_score ==", str(s.f_score))

                    fringe.put((s.f_score,next(count),s))
                    open_list.append(s)
                    explored.append(s)
