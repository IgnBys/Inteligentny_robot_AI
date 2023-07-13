from keeper import Keeper
from shelf import Shelf
import pygame

#storage - list of all shelves
class ShelfManager():

    def __init__(self, board):
        self.storage = []
        self.board = board

#TODO: change 25 and 50 to values that correspond to the board parameters
    def create_shelves(self):
        x = 0
        y = 0
        id = 0
        distance_between=self.board.scale  #between lines in pixels
        self.storage=[]

        for i in range(5):

            for j in range(5):
                if (i < 2 and j < 3):
                    if (j < 3):
                        type = "plants"
                elif (i < 2 and j > 2):
                    type = "food"
                elif (i > 1 and j < 3):
                    if (i < 4):
                        type = "clothes"
                    else: type = "sport"
                elif (i > 1 and j > 2):
                    if (i < 4):
                        type = "garden_house"
                    else: type = "electronics"



                size = distance_between
                if (j % 3 == 0):
                    size = 2*distance_between
                shelf =Shelf(id, size, x, y, self.board, type)
                self.storage.append(shelf)
                id += 1

                x = x+size+2*distance_between
            y = y + 4*distance_between
            x=0
    def draw_shelves(self):
        height = 25
        for i in range(len(self.storage)):
            shelf = self.storage[i]
            shelf.draw(self.board.window)
            shelf.filling(self.board.window)
        #progress bar
        #pygame.draw.rect(surface, (255, 0, 0), (400, 475, 70, 25))
        #pygame.draw.rect(surface, (0, 0, 0), (400, 475, 100, 25), 4)