import sys
import random
import pygame
import settings
from settings import *
from pygame.locals import *


class Interface (pygame.sprite.Sprite):

    def __init__(self, icon_name, window_demensions, surface=None):
        super().__init__()

        if icon_name == None:
            self.image = surface
        else:
            self.image = pygame.image.load(icon_name).convert_alpha()

        self.rect = self.image.get_rect()
        self.max_latitude = window_demensions[0] - self.rect.width
        self.max_longitude = window_demensions[1] - self.rect.height

    def add_to_group(self, group1, group2):
        group1.add(self)
        group2.add(self)


class Button(Interface):

    def __init__(self, icon_name, window_demensions, actionName=None):
        super().__init__(icon_name, window_demensions)

        self.collision = False
        self.action_name = actionName

    def action(self, coliding, function, *argumens):
        if coliding:
            function(*argumens)

    def quiting(self, text, screen, background):

        screen.blit(background, (0, 0))
        screen.blit(text.image, text.rect)
        pygame.display.flip()

        pygame.time.delay(2000)
        pygame.quit()
        sys.exit()

    def scrollingRight(self, dictionary):

        objects = list(dictionary)
        index = objects.index(settings.chosen)
        if index == len(objects) - 1:
            settings.chosen = objects[0]
        else:
            settings.chosen = objects[index + 1]

    def scrollingLeft(self, dictionary):

        objects = list(dictionary)
        index = objects.index(chosen)
        if index == 0:
            chosen = objects[len(objects) - 1]
            return chosen
        else:
            chosen = objects[index - 1]


class Coin(pygame.sprite.Sprite):

    def __init__(self, window_demensions):
        super().__init__()

        self.image = pygame.image.load("src\coin.png").convert_alpha()

        self.rect = self.image.get_rect()

        self.max_latitude = window_demensions[0] - self.rect.width
        self.max_longitude = window_demensions[1] - self.rect.height

        self.rect.x = random.randint(0, self.max_latitude)
        self.rect.y = random.randint(0, self.max_longitude)


class Text(Interface):

    def __init__(self, text, size, color, window_demensions, icon_name=None):
        self.font = pygame.font.SysFont("Arial", size)
        self.image = self.font.render(text, 1, color)
        super().__init__(icon_name, window_demensions, self.image)