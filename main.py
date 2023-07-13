from keeper import Keeper
from package import Package
from manager import Manager
from board import Board
from shelf import Shelf
from shelf import ShelfType
from robot import Robot, State,bfs, a_star, AStarState
from package_generator import PackageGenerator
from shelf_manager import ShelfManager
from client import Client
import ID3
from collections import deque
import random
import math
from queue import PriorityQueue
import numpy as np
import itertools

import pygame

def resolve_goal(goal_name:str):
    match goal_name:
        case "client":
            return (client.posx,client.posy)
        case "charger":
            return (charger.posx, charger.posy)
        case "generator":
            return (generator.posx,generator.posy)
def tree_states(board:Board, generator:PackageGenerator,client:Client):
    tree_values = []
    #Max(oczek.)||Ilość zam.||Sum(prior.)||Ilość pacz. w gen.||Odl. od gen. ||Odl. od kli.||Odległość od ład.||Poziom energii||
    maxlen = board.width + board.height
    carry_limit = 4 # ile moze uniesc robocik
    max_energy = 100 # ile energy ma robot
    TREE_INTERVALS = [(maxlen*2/3,maxlen*6),(carry_limit, carry_limit*2),(4, 10),(6, 20),(maxlen/5, maxlen*4/5),(maxlen/5, maxlen*4/5), (maxlen/5, maxlen*4/5), (max_energy/3, max_energy*5/6)]
    max_oczek = 0 # czas oczekiwania klienta
    tree_values.append(max_oczek)
    ilosc_zam = len(client.wanted_ids) #ilosc zamowien w danej chwili
    tree_values.append(ilosc_zam)
    prior_sum = len(client.wanted_ids)*2 #suma priorytetow
    tree_values.append(prior_sum)

    gen_packages_count = len(generator.inventory) #ilosc paczek w generatorze
    tree_values.append(gen_packages_count)

    instate = AStarState(robot.posx, robot.posy, robot.direction)  # initial state
    limitx = board.width
    limity = board.height

    goal = (generator.posx, generator.posy)
    list_AStar = a_star(instate, goal, limitx, limity, board)
    list_AStar = list(list_AStar)
    gen_distance = len(list_AStar)
    tree_values.append(gen_distance)

    goal = (client.posx, client.posy)
    list_AStar = a_star(instate, goal, limitx, limity, board)
    list_AStar = list(list_AStar)
    client_distance = len(list_AStar)
    tree_values.append(client_distance)

    #goal = (charger.posx, charger.posy) //comment bc charger doesnt exist yet
    list_AStar = a_star(instate, goal, limitx, limity, board)
    list_AStar = list(list_AStar)
    charger_distance = len(list_AStar)
    charger_distance = 0
    tree_values.append(charger_distance)

    enegry_level = robot.energy_level
    tree_values.append(enegry_level)
    levels = []
    for i, elem in enumerate(tree_values):
        if(elem<TREE_INTERVALS[i][0]):
            levels.append("low")
        elif (elem > TREE_INTERVALS[i][1]):
            levels.append("high")
        else:
            levels.append("mid")
    return levels


def setup():
    global tree
    global board, robots, generators, clients, shelves, clock, manager,chargers
    global manager,robot, generator, client,charger
    tree = ID3.make_variable_tree()
    manager = Manager(20)
    f=open("chosen_board.txt","r")
    #f = open("src/default_board.txt", "r")
    #f2= open("src/biases.txt")
    (board, robots, generators, clients,chargers, shelves) = manager.board_from_string(f.read())
    #board.load_biases(f2.read())
    board.update_positions(robots, generators, clients, shelves,chargers)
    f.close()
    #f2.close()
    robot = robots[0]
    generator = generators[0]
    client = clients[0]
    charger = chargers[0]
    robot.fill_logs("clientsLog", client)
    clock = pygame.time.Clock()
    # for j in range (0,len(generators)):
    #    # generators[j].types_list=[ShelfType(j+1).name]
    #     for i in range(0, 10):
    #         generators[j].generate_package()
    #     robot.fill_logs("generatorsLog", generators[j])
    size_between = board.scale
    for i in shelves:
        robot.fill_logs("shelvesLog", i)


def gameloop():
    # for event in pygame.event.get():
    # if event.type == pygame.QUIT:
    # flag = False
    for i in shelves:
        if i.posx == robot.posx and i.posy == robot.posy:
            robot.nearby_keeper = i
            break
    for i in generators:
        if i.posx == robot.posx and i.posy == robot.posy:
            robot.nearby_keeper = i
            break
    for i in clients:
        if i.posx == robot.posx and i.posy == robot.posy:
            robot.nearby_keeper = i
            break
    # pygame.time.delay(50)
    clock.tick(5)
    last_pressed = None
    while last_pressed == None:
        last_pressed = robot.move()
    print(last_pressed)

    board.draw_window()
    for i in shelves:
        i.draw()
    for i in generators:
        i.draw()
    for i in clients:
        i.draw()
    robot.draw()

    pygame.display.update()
    robot.nearby_keeper = None

def gameloop2():
    def generate_goals():
        goals_list=[]
        constraint_x=board.width
        constraint_y=board.height
        i = 0
        j = 0
        while True:
            goal=(i,j)
            goals_list.append(goal)
            goal=(i,constraint_y)
            goals_list.append(goal)
            goal=(constraint_x,constraint_y)
            constraint_y-=1
            goals_list.append(goal)
            goal=(constraint_x,j)
            constraint_x-=1
            goals_list.append(goal)
            i=i+1
            j=j+1
            if i>constraint_x:
                break
        return goals_list

    def generate_goals2():
        goals_list = []
        constraint_x = board.width
        constraint_y = board.height
        for i in range (0,100):
            goal=(random.randint(0,constraint_x-1),random.randint(0,constraint_y-1))
            goals_list.append(goal)
        return goals_list

    goals=generate_goals2()
    while True:
        # for event in pygame.event.get():
        # if event.type == pygame.QUIT:
        # flag = False

        for i in robot.shelvesLog:
            if i.posx == robot.posx and i.posy == robot.posy:
                robot.nearby_keeper = i
                #print("Nearby_shelf: " + str(i.posx) + " " + str(i.posy) + " " + str(type(i)))
                break
        for i in robot.generatorsLog:
            if i.posx == robot.posx and i.posy == robot.posy:
                robot.nearby_keeper = i
                #print("Nearby_generator: " + str(i.posx) + " " + str(i.posy) + " " + str(type(i)))
                break
        for i in robot.clientsLog:
            if i.posx == robot.posx and i.posy == robot.posy:
                robot.nearby_keeper = i
                #print("Nearby_client: " + str(i.posx) + " " + str(i.posy) + " " + str(type(i)))
                break
        # pygame.time.delay(50)
        clock.tick(10)
        last_pressed = None
        try:
            if not list_bfs:
                fringe = deque()  # wierzcholki do odwiedzenia
                instate = State(robot.posx, robot.posy, robot.direction)  # initial state
                goal = goals.pop(0)
                print("Goal: ",goal[0],goal[1])
                limitx = board.width
                limity = board.height
                list_bfs = bfs(fringe, instate, goal, limitx, limity,robot)
                list_bfs=list(list_bfs)
                print(list_bfs)

        except UnboundLocalError:
            list_bfs = ['f']

        # for i in range(10):
        #     input(list_bfs[i])
        # robot.move1(list_bfs)
        # print(list_bfs)
        # while allI == None:
        #     match list_bfs[allI]:
        #         case 'f':
        #             robot.forward()
        #         case 'l':
        #             robot.rotate_left()
        #         case 'r':
        #             robot.rotate_right()
        while last_pressed == None:
            #print("In while_main:", list_bfs)
            last_pressed=list_bfs.pop(0)
            robot.move_test(last_pressed, charger)
        #last_pressed == robot.move()
        try:
            board.draw_window()
            for i in shelves:
                i.draw()
            for i in generators:
                i.draw()
            for i in clients:
                i.draw(2)
            pygame.draw.rect(board.window, (170, 227, 123), (goal[0]*board.scale + 1, goal[1]*board.scale + 1,
                                                        board.scale - 1, board.scale - 1))
            robot.draw()
        except:
            print("X")


        pygame.display.update()
        board.update_positions(robots,generators,clients,shelves)
        robot.nearby_keeper = None


def gameloop3():
    def generate_goals():
        goals_list=[]
        constraint_x=board.width
        constraint_y=board.height
        i = 0
        j = 0
        while True:
            goal=(i,j)
            goals_list.append(goal)
            goal=(i,constraint_y)
            goals_list.append(goal)
            goal=(constraint_x,constraint_y)
            constraint_y-=1
            goals_list.append(goal)
            goal=(constraint_x,j)
            constraint_x-=1
            goals_list.append(goal)
            i=i+1
            j=j+1
            if i>constraint_x:
                break
        return goals_list

    def generate_goals2():
        goals_list = []
        constraint_x = board.width
        constraint_y = board.height
        for i in range (0,100):
            goal=(random.randint(0,constraint_x-1),random.randint(0,constraint_y-1))
            goals_list.append(goal)
        return goals_list

    goals=generate_goals2()
  #  board.update_biases(6,4,10)
   # goals=[(5,4),(10,0),(5,4),(10,0),(5,4),(10,0),(5,4),(10,0),(5,4),(10,0),(5,4),(10,0),(5,4),(10,0),(5,4),(10,0),(5,4),(10,0),(5,4),(10,0),(5,4),(10,0),(5,4),(10,0)]
    goal=goals.pop()

    turnSwitch=0
    counter=itertools.count(start=0,step=1)
    def go_to_charger():
        list_AStar = a_star(instate, goal, limitx, limity, board)
        list_AStar = list(list_AStar)
        charger_distance = len(list_AStar)
        temp = math.ceil((100 - robot.energy_level + charger_distance) / charger.charging_speed)
        for i in range(temp):
            list_AStar.append('c')
    while True:
        # for event in pygame.event.get():
        # if event.type == pygame.QUIT:
        # flag = False

        for i in shelves:
            if i.posx == robot.posx and i.posy == robot.posy:
                robot.nearby_keeper = i
                #print("Nearby_shelf: " + str(i.posx) + " " + str(i.posy) + " " + str(type(i)))
                break
        for i in generators:
            if i.posx == robot.posx and i.posy == robot.posy:
                robot.nearby_keeper = i
                #print("Nearby_generator: " + str(i.posx) + " " + str(i.posy) + " " + str(type(i)))
                break
        for i in clients:
            if i.posx == robot.posx and i.posy == robot.posy:
                robot.nearby_keeper = i
                #print("Nearby_client: " + str(i.posx) + " " + str(i.posy) + " " + str(type(i)))
                break
        # pygame.time.delay(50)
        clock.tick(30)
        last_pressed = None
        tree = ID3.make_variable_tree()
        try:
            if not list_AStar:
                #fringe = PriorityQueue()  # wierzcholki do odwiedzenia
                instate = AStarState(robot.posx, robot.posy, robot.direction)  # initial state
                levels = []
                levels = tree_states(board, generator, client)
                goal = resolve_goal(ID3.answer(levels,tree))
                print("Goal: ",goal[0],goal[1])
                limitx = board.width
                limity = board.height

                if (goal[0] == charger.posx and goal[1] == charger.posy):
                    list_AStar = a_star(instate, goal, limitx, limity, board)
                    list_AStar = list(list_AStar)
                    charger_distance = len(list_AStar)
                    temp = math.ceil((100 - robot.energy_level + charger_distance)/charger.charging_speed)
                    for i in range (temp):
                        list_AStar.append('c')
                if (goal[0] == generator.posx and goal[1] == generator.posy):
                    list_AStar = a_star(instate, goal, limitx, limity, board)
                    list_AStar = list(list_AStar)
                    list_AStar.append('t')
                    typ = generator.inventory[0].type
                    for i in shelves:
                        try:
                            if(i.type==typ):
                                goal=(i.posx,i.posy)
                        except:
                            print ("cannot assign shelf")
                            pass
                    count = 0
                    for i in range (len(list_AStar)):
                        if(list_AStar[i] == 'l'):
                            count = count -1
                        if (list_AStar[i] == 'r'):
                            count = count + 1
                    rdir = (robot.direction + count) %4
#
                    next_state = AStarState(generator.posx, generator.posy, rdir)
                    newlist=a_star(next_state, goal, limitx, limity, board)
                    newlist=list(newlist)
                    list_AStar += newlist
                    list_AStar.append('g')

                if (goal[0] == client.posx and goal[1] == client.posy):
                    found_package=False
                    for i in range (0,len(client.wanted_ids)):
                        print(f"client.wanted_ids[0]: {client.wanted_ids[i]}")
                        for iter,s in enumerate(shelves):
                            print(f"shelf number {iter}:")
                            for item in s.inventory:
                                print(f"{item.id}",end="")
                                if(item.id == client.wanted_ids[i]):
                                    goal=(s.posx,s.posy)
                                    found_package=True
                                    print(s.posx, s.posy)
                                    break
                        if found_package==True:
                            break
                    if found_package==True: #go to the shelf and take the package
                        list_AStar = a_star(instate, goal, limitx, limity, board)
                        list_AStar = list(list_AStar)
                        list_AStar.append("t")
                        print(list_AStar)

                        # dostarczenie do klienta
                        count = 0
                        for i in range(len(list_AStar)):
                            if (list_AStar[i] == 'l'):
                                count = count - 1
                            if (list_AStar[i] == 'r'):
                                count = count + 1
                        rdir = (robot.direction + count) % 4
                        next_state = AStarState(goal[0], goal[1], rdir)
                        goal = (client.posx, client.posy)

                        clilist = a_star(next_state, goal, limitx, limity, board)
                        clilist = list(clilist)
                        print(clilist)
                        list_AStar = list_AStar + clilist
                        list_AStar.append('g')
                    else:
                        list_AStar = a_star(instate, (random.randint(0,limitx), random.randint(0,limity)), limitx, limity, board)
                        list_AStar = list(list_AStar)
                print("Full path by recursion: ")
                print(list_AStar)


        except UnboundLocalError:
            list_AStar = ['f']
        while last_pressed == None:
            #print("In while_main:", list_bfs)
            try:
                last_pressed = list_AStar.pop(0)
            except:
                list_AStar = [""]
            robot.move_test(last_pressed, charger)
        #last_pressed == robot.move()
        board.draw_window()
        for i in shelves:
            i.draw()
        for i in generators:
            if (0<=turnSwitch<=6):
                i.generate_package()
                turnSwitch+=1
            i.draw()
        for i in clients:
            if(turnSwitch>6 and turnSwitch<=7):
                i.generateClients()
                turnSwitch+=1

            i.draw()
        for i in chargers:
            i.draw()
        pygame.draw.rect(board.window, (170, 227, 123), (goal[0]*board.scale + 1, goal[1]*board.scale + 1,
                                                    board.scale - 1, board.scale - 1))
        robot.draw()
        robot.energy_level-=5

        pygame.display.update()
        board.update_positions(robots,generators,clients,chargers,shelves)
        robot.nearby_keeper = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
        if (turnSwitch>=8):
            turnSwitch=-300
        if(turnSwitch<0):
            turnSwitch+=1

if __name__ == "__main__":
    setup()
    gameloop3()


