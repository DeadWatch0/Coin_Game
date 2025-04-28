import pygame
import settings

class Character(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        skin_path = settings.SKINS[settings.selected_skin]
        self.image = pygame.image.load(skin_path).convert_alpha()
        self.rect = self.image.get_rect()
        w, h = settings.WINDOW_DIMENSIONS
        self.rect.center = (w//2, h//2)
        self.speed = 5
        self.max_x = w - self.rect.width
        self.max_y = h - self.rect.height

    def move(self, dx, dy):
        self.rect.x = max(0, min(self.max_x, self.rect.x + dx * self.speed))
        self.rect.y = max(0, min(self.max_y, self.rect.y + dy * self.speed))

    def add_to_groups(self, *groups):
        for g in groups:
            g.add(self)