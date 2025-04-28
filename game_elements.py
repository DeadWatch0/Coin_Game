import pygame
import random
import settings

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, icon_key, value, position=None):
        """
        Initialize obstacle with given icon_key and effect. Optionally pass a position tuple (x,y).
        """
        super().__init__()
        icon_path = settings.ICONS[icon_key]
        self.image = pygame.image.load(icon_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.effect = value
        if position:
            self.rect.topleft = position

    @classmethod
    def spawn(cls, icon_key, value, all_sprites, target_group, avoid_groups, max_attempts=20, inflate_px=10):
        """
        Spawn a new Obstacle of given type at a random location
        that does not overlap any sprite in avoid_groups.
        """
        icon_path = settings.ICONS[icon_key]
        temp_image = pygame.image.load(icon_path).convert_alpha()
        w, h = temp_image.get_size()
        screen_w, screen_h = settings.WINDOW_DIMENSIONS

        for _ in range(max_attempts):
            x = random.randint(0, screen_w - w)
            y = random.randint(0, screen_h - h)
            obj = cls(icon_key, value, position=(x, y))
            obj.image = temp_image
            obj.rect = temp_image.get_rect(topleft=(x, y))
            test_rect = obj.rect.inflate(inflate_px, inflate_px)
            collision = False
            for group in avoid_groups:
                if any(test_rect.colliderect(other.rect) for other in group):
                    collision = True
                    break
            if not collision:
                obj.add_to_groups(all_sprites, target_group)
                return obj
        # fallback spawn at random without overlap check
        x = random.randint(0, screen_w - w)
        y = random.randint(0, screen_h - h)
        obj = cls(icon_key, value, position=(x, y))
        obj.image = temp_image
        obj.rect = temp_image.get_rect(topleft=(x, y))
        obj.add_to_groups(all_sprites, target_group)
        return obj
    
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
