import pygame
import random
import settings


class Obstacle(pygame.sprite.Sprite):
    ICON_KEY = None   # subclass must set

    def __init__(self, position=None):
        super().__init__()
        assert self.ICON_KEY, "ICON_KEY must be set in subclass"
        icon_path = settings.ICONS[self.ICON_KEY]
        self.image = pygame.image.load(icon_path).convert_alpha()
        self.rect  = self.image.get_rect()
        if position:
            self.rect.topleft = position
            
    @classmethod
    def spawn(cls, all_sprites, target_group,
              position=None, max_attempts=20, inflate_px=10):
        """
        If `position` is provided, place exactly there.
        Otherwise, attempt up to `max_attempts` random non‑overlapping spots.
        """
        # Exact placement
        if position is not None:
            obj = cls(position=position)
            all_sprites.add(obj)
            target_group.add(obj)
            settings.OBSTACLES.add(obj)
            return obj

        # Random placement
        icon_path = settings.ICONS[cls.ICON_KEY]
        tmp_img   = pygame.image.load(icon_path).convert_alpha()
        w, h      = tmp_img.get_size()
        sw, sh    = settings.WINDOW_DIMENSIONS

        for _ in range(max_attempts):
            x = random.randint(0, sw - w)
            y = random.randint(0, sh - h)
            test = pygame.Rect(x, y, w, h).inflate(inflate_px, inflate_px)
            if any(test.colliderect(o.rect) for o in all_sprites):
                continue
            obj = cls(position=(x, y))
            all_sprites.add(obj)
            target_group.add(obj)
            settings.OBSTACLES.add(obj)
            return obj

        # Fallback: last‐ditch random
        x = random.randint(0, sw - w)
        y = random.randint(0, sh - h)
        obj = cls(position=(x, y))
        all_sprites.add(obj)
        target_group.add(obj)
        settings.OBSTACLES.add(obj)
        return obj
    
    def on_collision(self, character):
        """
        Default: do nothing. Subclasses should override.
        """
        pass
    
    def add_to_groups(self, *groups):
        for g in groups:
            g.add(self)
            
class Coin(Obstacle):
    ICON_KEY = 'coin'
    def __init__(self, position=None):
        super().__init__(position)
        self.group = settings.COINS
        
    def on_collision(self, character):
        settings.change_points(1)
        character.change_speed(1)
        # Respawn another coin
        Coin.spawn(settings.GAME_SPRITES, settings.COINS)

class Bomb(Obstacle):
    ICON_KEY = 'bomb'
    def __init__(self, position=None):
        super().__init__(position)
        self.group = settings.BOMBS
    
    def on_collision(self, character):
        settings.change_health(-1)
        Bomb.spawn(settings.GAME_SPRITES, settings.BOMBS)
        HealthPotion.spawn(settings.GAME_SPRITES, settings.POTIONS)

class HealthPotion(Obstacle):
    ICON_KEY = 'health_potion'
    def __init__(self, position=None):
        super().__init__(position)
        self.group = settings.POTIONS
    
    def on_collision(self, character):
        if settings.health < settings.max_health:
            settings.change_health(1)
        
class MaxHealthPotion(Obstacle):
    ICON_KEY = 'max_health_potion'
    def __init__(self, position=None):
        super().__init__(position)
        self.group = settings.POTIONS
    
    def on_collision(self, character):
        settings.change_max_health(1)
        settings.change_health(settings.max_health - settings.health)
        
class ReduceSpeedPotion(Obstacle):
    ICON_KEY = 'reduce_speed_potion'
    def __init__(self, position=None):
        super().__init__(position)
        self.group = settings.POTIONS
    
    def on_collision(self, character):
        character.change_speed(-20)

class Chest(Obstacle):
    ICON_KEY = 'chest'
    def __init__(self, position=None):
        super().__init__(position)
        self.group = settings.CHESTS
        
    def on_collision(self, character):
        MaxHealthPotion.spawn(settings.GAME_SPRITES, settings.POTIONS, position=(settings.WINDOW_WIDTH//2+80, settings.WINDOW_HEIGHT//2+80))
        ReduceSpeedPotion.spawn(settings.GAME_SPRITES, settings.POTIONS, position=(settings.WINDOW_WIDTH//2-80, settings.WINDOW_HEIGHT//2-80))

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
                