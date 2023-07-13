import pygame
import random
from package import Package
from keeper import Keeper
from client import Client
import numpy as np
class PackageGenerator(Keeper):
    id_counter=0

    def __init__(self,id,posx,posy,board,types_list=["SPORT"]):
        inventory_size=10000
        super().__init__(id, inventory_size, posx, posy)
        self.board=board
        self.color=(255, 163, 140)
        self.types_list=types_list
        self.wait_counter=0
    def draw(self):
        point_x0 = self.posx*self.board.scale
        point_y0 = self.posy*self.board.scale
        color=self.color

        size_between=self.board.scale
        pygame.draw.rect(self.board.window, color, (point_x0 + 1, point_y0 + 1,
                                               size_between - 1, size_between - 1))
#TODO:

    def generate_package(self,size=None,type=None,max_size=1):
        print("package generated!")
        n = abs(round(np.random.normal(20, 1.5)))
        self.wait_counter += n
        if not size:
            size = random.randint(1, max_size)
        if not type:
            type=random.choice(self.types_list)
        self.insert_package(Package(self.id_counter,size,type))
        Client.possible_ids.append(self.id_counter)
        PackageGenerator.id_counter+=1
