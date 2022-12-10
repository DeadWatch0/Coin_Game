import pygame
from pygame.locals import *


class Character(pygame.sprite.Sprite):

    def __init__(self, skin, window_demensions):
        super().__init__()

        self.image = pygame.image.load(skin).convert_alpha()

        self.rect = self.image.get_rect()

        self.max_latitude = window_demensions[0] - self.rect.width
        self.max_longitude = window_demensions[1] - self.rect.height

        self.rect.x = self.max_latitude/2
        self.rect.y = self.max_longitude/2

        self.speed = 5

    def moveLeft(self):
        if self.rect.x <= 0:
            self.rect.x = 0
        else:
            self.rect.x = self.rect.x - self.speed

    def moveRight(self):
        if self.rect.x >= self.max_latitude:
            self.rect.x = self.max_latitude
        else:
            self.rect.x = self.rect.x + self.speed

    def moveUp(self):
        if self.rect.y <= 0:
            self.rect.y = 0
        else:
            self.rect.y = self.rect.y - self.speed

    def moveDown(self):
        if self.rect.y >= self.max_longitude:
            self.rect.y = self.max_longitude
        else:
            self.rect.y = self.rect.y + self.speed

    def add_to_group(self, group1, group2):
        group1.add(self)
        group2.add(self)
