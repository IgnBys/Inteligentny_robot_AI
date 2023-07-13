from keeper import Keeper
import pygame
import random
import numpy as np
import itertools

class Client(Keeper):
    possible_ids=[]

    def __init__(self, id, posx, posy, board, color=(21, 214, 195), priority=0):
        inventory_size = 1000
        super().__init__(id, inventory_size, posx, posy)
        self.color = color
        self.board = board
        self.wanted_ids = []
        self.priority = priority
        self.wait_counter=0

    def draw(self):
        point_x0 = self.posx * self.board.scale
        point_y0 = self.posy * self.board.scale
        size_between = self.board.scale
        filling=len(self.wanted_ids)
        if filling>0 and filling<3:
            self.color = (114, 219, 242)
        elif filling>2: #maksymalnie chyba = 7
            self.color = (22, 68, 195)
        pygame.draw.rect(self.board.window, self.color, (point_x0 + 1, point_y0 + 1,
                                                         size_between - 1, size_between - 1))


    def get_wanted_package(self, inventory):
        candidates = []
        for i in inventory:
            if i.id in(self.wanted_ids):
                candidates.append(i)
        return candidates

    def generate_ticket(self,timeout):
        try:
            choice=random.randint(0, len(Client.possible_ids)-1)
            self.wanted_ids.append(Client.possible_ids.pop(choice))
            self.wait_counter += timeout
            print("new ticket!")
        except ValueError:
            pass

    def ticket_cleanup(self):
        for i in self.inventory:
            if i.id in self.wanted_ids:
                self.wanted_ids.pop(self.wanted_ids.index(i.id))

    def generateClients(self):
        #count = itertools.count(start=0, step=1)
        n = abs(round(np.random.normal(5, 1.5)))
        self.generate_ticket(n)

        # c = []
        # if n!=0:
        #     for i in range(n):
        #         id = next(count)
        #         if id == main.id:
        #             id = next(count)
        #         pr = random.randint(0,1)
        #         c.append(Client(id, main.posx, main.posy, main.board, priority=pr))
        #         c[i].generate_ticket()
        # return c


