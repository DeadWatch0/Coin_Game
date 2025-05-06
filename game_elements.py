import pygame
import random
import settings
import math


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
              position=None, max_attempts=20, inflate_px=10, **kwargs):
        """
        Universal spawn: extra kwargs passed to __init__.
        If position is None, attempts random placement.
        """
        sw, sh = settings.WINDOW_DIMENSIONS
        # helper to actually construct and add
        def make_obj(pos):
            obj = cls(position=pos, **kwargs)
            all_sprites.add(obj)
            target_group.add(obj)
            settings.OBSTACLES.add(obj)
            return obj

        if position is not None:
            return make_obj(position)

        # random placement
        icon_path = settings.ICONS[cls.ICON_KEY]
        tmp_img   = pygame.image.load(icon_path).convert_alpha()
        w, h      = tmp_img.get_size()

        for _ in range(max_attempts):
            x = random.randint(0, sw - w)
            y = random.randint(0, sh - h)
            test = pygame.Rect(x, y, w, h).inflate(inflate_px, inflate_px)
            if any(test.colliderect(o.rect) for o in all_sprites):
                continue
            return make_obj((x, y))

        # fallback
        x = random.randint(0, sw - w)
        y = random.randint(0, sh - h)
        return make_obj((x, y))
    
    def on_collision(self, character):
        """
        Default: do nothing. Subclasses should override.
        """
        pass
    
    def add_to_groups(self, *groups):
        for g in groups:
            g.add(self)
            
class RewardMixin:
    def __init__(self, *args, **kwargs):
        # Call next in MRO (Obstacle.__init__)
        super().__init__(*args, **kwargs)
        # Number of frames before this reward becomes “active”
        self._frames_to_activate = 1

    def activate_frame(self):
        """Call once per frame in update loop to count down."""
        if self._frames_to_activate > 0:
            self._frames_to_activate -= 1

    @property
    def active(self):
        """True once the grace period has passed."""
        return self._frames_to_activate <= 0
            
class Coin(Obstacle):
    ICON_KEY = 'coin'
    TARGET_GROUP = lambda: settings.COINS
    
    def __init__(self, position=None):
        super().__init__(position)
        
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
        HealthPotion.spawn(settings.GAME_SPRITES, settings.HEALTH_POTIONS)

class HealthPotion(RewardMixin, Obstacle):
    ICON_KEY = 'health_potion'
    TARGET_GROUP = lambda: settings.HEALTH_POTIONS
    
    def __init__(self, position=None):
        super().__init__(position)
    
    def on_collision(self, character):
        if settings.health < settings.max_health:
            settings.change_health(1)
        
class MaxHealthPotion(RewardMixin, Obstacle):
    ICON_KEY = 'max_health_potion'
    TARGET_GROUP = lambda: settings.MAX_HEALTH_POTIONS
    
    def __init__(self, position=None):
        super().__init__(position)
    
    def on_collision(self, character):
        settings.change_max_health(1)
        settings.change_health(settings.max_health - settings.health)
        
class ReduceSpeedPotion(RewardMixin, Obstacle):
    ICON_KEY = 'reduce_speed_potion'
    TARGET_GROUP = lambda: settings.REDUCE_SPEED_POTIONS
    
    def __init__(self, position=None):
        super().__init__(position)
    
    def on_collision(self, character):
        character.change_speed(-20)

class Chest(Obstacle):
    ICON_KEY = 'chest'
    TARGET_GROUP = lambda: settings.CHESTS
    
    def __init__(self, position=None, reward_classes=(), **kwargs):
        super().__init__(position, **kwargs)
        self.reward_classes = reward_classes

    def on_collision(self, character):
        import math
        cx, cy  = self.rect.center
        n       = len(self.reward_classes)
        radius  = 80

        for i, RewardCls in enumerate(self.reward_classes):
            angle = (2 * math.pi * i) / n
            pos   = (round(cx + math.cos(angle)*radius),
                     round(cy + math.sin(angle)*radius))
            # kwargs pass-through works here:
            RewardCls.spawn(settings.GAME_SPRITES,
                            RewardCls.TARGET_GROUP(),
                            position=pos)



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
                