import os
import pygame

class Charger():
    def __init__(self,id,posx,posy,board):
        self.board = board
        self.Img = pygame.transform.scale( pygame.image.load(os.path.join('src', 'charger.png')).convert_alpha(), (self.board.scale - 1, self.board.scale - 1))
        self.id=id
        self.posx = posx
        self.posy = posy
        self.charging_speed = 20

    def draw(self):
        point_x0 = self.posx * self.board.scale
        point_y0 = self.posy * self.board.scale
        self.board.window.blit(self.Img, (point_x0 + 1, point_y0 + 1))

    def charge(self, robot):
        robot.energy_level += self.charging_speed
