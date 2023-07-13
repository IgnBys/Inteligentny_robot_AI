import pygame
import math
import random
import tkinter as tk
import numpy as np
from tkinter import messagebox
import os

class Board():
    def __init__(self,width,height, scale=40, background_color=(255, 255, 255)): #width in squares times scale equals actual pixels
        self.width=int(width)
        self.height=int(height)
        self.scale=scale
        self.window = pygame.display.set_mode((width*scale,height*scale ))
        self.background_color = background_color
        self.positions = np.zeros((int(width),int(height)), dtype=int)
        self.biases = np.zeros((int(width), int(height)), dtype=float)
        self.itemsTable = {}
        self.Img = pygame.image.load(os.path.join('src', 'bg.png')).convert_alpha()
        pass

    def draw_window(self):
        self.window.fill(self.background_color)
        self.window.blit(self.Img, (0,0))
        self.draw_grid()
        self.window.blit(self.draw_biases(),(0,0))


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

            pygame.draw.line(self.window, (150, 150, 150), (x, 0), (x,self.height*self.scale))
            pygame.draw.line(self.window, (130, 130, 130), (0, y), (self.width*self.scale, y))
    def update_positions(self, robots,generators,clients, chargers,shelves):
        self.positions = np.zeros(((self.width+1, self.height+1)), dtype=int)
        for i in robots:
            self.positions[i.posx, i.posy] = i.id
            self.itemsTable[i.id] = "robot"
        for i in generators:
            self.positions[i.posx, i.posy] = i.id
            self.itemsTable[i.id] = "generator"
        for i in clients:
            self.positions[i.posx, i.posy] = i.id
            self.itemsTable[i.id] = "client"
        for i in chargers:
            self.positions[i.posx, i.posy] = i.id
            self.itemsTable[i.id] = "charger"
        for i in shelves:
            self.positions[i.posx, i.posy] = i.id
            self.itemsTable[i.id] = "shelf"
        # for key, value in self.itemsTable.items():
        #     print(key, ": ", value)
    def update_biases(self,x,y,bias_value):
        self.biases[x,y]+=bias_value
    def reset_biases(self):
        self.biases=zeros((self.width,self.height),dtype=int)
    def load_biases(self,blueprint: str):
        blueprint=blueprint.split("\n")
        for i,row in enumerate(blueprint):
            row=row.split(",")
            for j,row_member in enumerate(row):
                self.biases[j][i]=float(row_member)

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
    def draw_biases(self):
        surface=pygame.Surface((self.width*self.scale,self.height*self.scale), pygame.SRCALPHA)
        for i in range (0,self.width):
            for j in range(0,self.height):
                if self.biases[i][j]!=0:
                    color = pygame.Color(0, 0, 0)
                    color.hsva = (22, 92, 47,np.clip(10*self.biases[i][j],0,90))
                    pygame.draw.rect(surface, color, (i * self.scale + 1, j * self.scale + 1,
                                                                     self.scale - 1, self.scale - 1))
        return surface.convert_alpha()