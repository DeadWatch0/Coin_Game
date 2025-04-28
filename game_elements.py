import pygame
import random
import settings

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, icon_key, value):
        super().__init__()
        icon_path = settings.ICONS[icon_key]
        self.image = pygame.image.load(icon_path).convert_alpha()
        self.rect = self.image.get_rect()
        w, h = settings.WINDOW_DIMENSIONS
        self.rect.x = random.randint(0, w - self.rect.width)
        self.rect.y = random.randint(0, h - self.rect.height)
        self.effect = value

    def add_to_groups(self, *groups):
        for g in groups:
            g.add(self)

class Button(pygame.sprite.Sprite):
    def __init__(self, icon_key, pos, action=None):
        super().__init__()
        icon_path = settings.ICONS[icon_key]
        self.image = pygame.image.load(icon_path).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.action = action

    def add_to_groups(self, *groups):
        for g in groups:
            g.add(self)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if self.action:
                self.action()
