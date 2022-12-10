import pygame
from pygame.locals import *

SURFACE_COLOR = (9, 35, 18)


class Character(pygame.sprite.Sprite):

    def __init__(self,  posX, posY):
        super().__init__()

        self.image = pygame.image.load("src\cookie.png").convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.x = posX
        self.rect.y = posY

    def moveLeft(self):
        if self.rect.x <= 0:
            self.rect.x = 0
        else:
            self.rect.x = self.rect.x - 20

    def moveRight(self):
        if self.rect.x >= 550:
            self.rect.x = self.rect.x = 550
        else:
            self.rect.x = self.rect.x + 20

    def moveUp(self):
        if self.rect.y <= 0:
            self.rect.y = 0
        else:
            self.rect.y = self.rect.y - 20

    def moveDown(self):
        if self.rect.y >= 2050:
            self.rect.y = 2050
        else:
            self.rect.y = self.rect.y + 20


class Button(pygame.sprite.Sprite):

    def __init__(self, posX, posY, action_name):
        super().__init__()

        self.image = pygame.image.load("src\cookie.png").convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.x = posX
        self.rect.y = posY
        self.collision = False
        self.actioning = action_name

    def action(self, coliding, function):
        if coliding:
            function()


class Coin(pygame.sprite.Sprite):

    def __init__(self, posX, posY):
        super().__init__()

        self.image = pygame.image.load("src\coin.png").convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.x = posX
        self.rect.y = posY


pygame.init()

screen = pygame.display.set_mode((1080, 600))


def add_characer(group1, group2, name):
    group1.add(name)
    group2.add(name)


def add_coin(group1, group2, name):
    group1.add(name)
    group2.add(name)


def add_button(group1, group2, name):
    group1.add(name)
    group2.add(name)


all_sprites = pygame.sprite.Group()
button_group = pygame.sprite.Group()
character_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()

character = Character(100, 300)
add_characer(character_group, all_sprites,  character)

LeftButton = Button(350, 250, character.moveLeft)
add_button(button_group, all_sprites, LeftButton)

RightButton = Button(750, 250, character.moveRight)
add_button(button_group, all_sprites, RightButton)

UpButton = Button(550, 150, character.moveUp)
add_button(button_group, all_sprites, UpButton)

DownButton = Button(550, 450, character.moveDown)
add_button(button_group, all_sprites, DownButton)

coin1 = Coin(0, 0)
add_coin(coin_group, all_sprites, coin1)

while True:

    screen.fill((20, 50, 60))
    for each in all_sprites:
        screen.blit(each.image, each.rect)
    pygame.display.flip()

    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()

        if event.type == MOUSEBUTTONDOWN:
            for button in button_group:
                button.collision = button.rect.collidepoint(event.pos)
        elif event.type == MOUSEBUTTONUP:
            for button in button_group:
                button.collision = False

        for button in button_group:
            button.action(button.collision, button.actioning)

    if coin1.rect.colliderect(character.rect):
        character.moveDown()
