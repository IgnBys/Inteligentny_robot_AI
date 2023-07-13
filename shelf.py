from keeper import Keeper
import pygame
import sys
import os
from enum import Enum


class ShelfType(Enum):
    PLANTS = 1
    FOOD = 2
    CLOTHES = 3
    ELECTRONICS = 4
    GARDEN_HOUSE = 5
    SPORT = 6
    NOT_ASSIGNED = 7



class Shelf(Keeper):

    def __init__(self, id, inventory_size, posx, posy, board, type, color=(255, 255, 0)):
        super().__init__(id, inventory_size, posx, posy)
        self.posx = posx
        self.posy = posy
        self.size = inventory_size
        self.inventory = list()
        self.id = id
        self.state = 0
        self.board = board
        self.type = type
        # TODO: powiązać color z type
        self.color = color
        # TODO: zrobić żeby to było dynamiczne
        self.filled_color = (color[0] - 30, color[1] - 30, color[2] - 30)

        # TODO: zrobić żeby to było dynamiczne
        # self.filled_color=(color[0]-30,color[1]-30,color[2]-30)

        size_between = self.board.scale

        # shelfs sprite
        emptyShelf = pygame.image.load(os.path.join('src', 'any_empty_shelf.png')).convert()

        if (self.type == "PLANTS"):
            shelf = pygame.image.load(os.path.join('src', 'plants_green_shelf.png ')).convert()
        # for food
        elif (self.type == "FOOD"):
            shelf = pygame.image.load(os.path.join('src', 'food_blue_shelf.png')).convert()
            # for clothes
        elif (self.type == "CLOTHES"):
            shelf = pygame.image.load(os.path.join('src', 'clothes_shelf_yellow.png')).convert()
            # for electronics
        elif (self.type == "ELECTRONICS"):
            shelf = pygame.image.load(os.path.join('src', 'electronics_shelf_grey.png')).convert()
            # for garden and house
        elif (self.type == "GARDEN_HOUSE"):
            shelf = pygame.image.load(os.path.join('src', 'garden_house_shelf_brown.png')).convert()
        # for sport
        elif (self.type == "SPORT"):
            shelf = pygame.image.load(os.path.join('src', 'sport_shelf_red.png')).convert()
        else:
            shelf = pygame.image.load(os.path.join('src', 'something_shelf_lilac.png')).convert()

        if (self.size // size_between == 2):
            self.emptyShelfImg = pygame.transform.scale(emptyShelf, (2 * size_between - 2, size_between - 1))
            self.shelfImg = pygame.transform.scale(shelf, (2 * size_between - 2, size_between - 1))
        else:
            self.emptyShelfImg = pygame.transform.scale(emptyShelf, (size_between - 1, size_between - 1))
            self.shelfImg = pygame.transform.scale(shelf, (size_between - 1, size_between - 1))

    def get_id(self):
        return self.id

    def get_posx(self):
        return posx.id

    def get_posy(self):
        return posy.id

    def filling(self):
        surface = self.board.window
        if (self.inventory_taken / self.size > 0.7):
            color = (255, 0, 0)
        elif (self.inventory_taken / self.size < 0.3):
            color = (0, 255, 0)
        else:
            color = (255, 140, 0)
        hue = (self.inventory_taken / self.size) * 100
        hue = 100 - hue
        saturation = 87
        value = 95
        alpha = 100
        color = pygame.Color(0, 0, 0)
        color.hsva = (hue, saturation, value, alpha)
        point_x0, point_y0 = self.set_xy()

        if (self.inventory_taken > 0):
            pygame.draw.rect(surface, color,
                             (point_x0 + 1, point_y0 + 1, (self.inventory_taken / self.size) * self.board.scale, 8))
        pygame.draw.rect(surface, (0, 0, 0), (point_x0 + 1, point_y0 + 1, self.board.scale, 8), 2)

    def set_xy(self):
        return self.posx * self.board.scale, self.posy * self.board.scale

    def get_wanted_package(self,inventory):
        candidates=[]
        for package in inventory:
            if package.type==self.type:
                candidates.append(package)
        return candidates


    def draw(self):
        surface = self.board.window
        point_x0, point_y0 = self.set_xy()
        if (self.inventory_taken == 0):
            surface.blit(self.emptyShelfImg, (point_x0 + 1, point_y0 + 1))
        else:
            surface.blit(self.shelfImg, (point_x0 + 1, point_y0 + 1))
        self.filling()
        # else:
        #   disp_color=self.color
        # pygame.draw.rect(self.board.window, disp_color, pygame.Rect(self.posx, self.posy, self.inventory_size,self.board.size//self.board.rows))
    #  pygame.display.flip()

    # def insert_package(self, package):
    #     #fill rectangle
    #     border_radius=2
    #     if(len(self.inventory) >0):
    #         x = get_posx
    #         y = get_posx
    #         pygame.draw.rect(self.board.window, color, pygame.Rect(x, y, width, height,),border_radius)
