import pygame
import random
import settings


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, icon_key, position=None):
        super().__init__()
        icon_path = settings.ICONS[icon_key]
        self.image = pygame.image.load(icon_path).convert_alpha()
        self.rect  = self.image.get_rect()
        if position:
            self.rect.topleft = position

    @classmethod
    def spawn(cls, icon_key, all_sprites, target_group,
              max_attempts=20, inflate_px=10):
        import random
        import settings

        icon_path = settings.ICONS[icon_key]
        tmp_img = pygame.image.load(icon_path).convert_alpha()
        w, h = tmp_img.get_size()
        sw, sh = settings.WINDOW_DIMENSIONS

        for _ in range(max_attempts):
            x = random.randint(0, sw - w)
            y = random.randint(0, sh - h)
            test_rect = pygame.Rect(x, y, w, h).inflate(inflate_px, inflate_px)

            # Avoid any existing sprite, including the player
            if any(test_rect.colliderect(other.rect) for other in all_sprites):
                continue

            # Good position
            obj = cls(icon_key, position=(x, y))
            obj.image = tmp_img
            obj.rect  = tmp_img.get_rect(topleft=(x, y))
            all_sprites.add(obj)
            target_group.add(obj)
            return obj

        # Fallback
        x = random.randint(0, sw - w)
        y = random.randint(0, sh - h)
        obj = cls(icon_key, position=(x, y))
        obj.image = tmp_img
        obj.rect  = tmp_img.get_rect(topleft=(x, y))
        all_sprites.add(obj)
        target_group.add(obj)
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
