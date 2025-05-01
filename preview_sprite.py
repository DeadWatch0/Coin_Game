import pygame
import settings

class PreviewSprite(pygame.sprite.Sprite):

    def __init__(self, center_pos):
        super().__init__()
        self.center_x, self.center_y = center_pos
        self._last_skin = None
        self.image = None
        self.rect  = pygame.Rect(0,0,0,0)
        self._reload_if_needed()

    def _reload_if_needed(self):
        skin = settings.selected_skin
        if skin != self._last_skin:
            path = settings.SKINS[skin]
            self.image = pygame.image.load(path).convert_alpha()
            self.rect  = self.image.get_rect(center=(self.center_x, self.center_y))
            self._last_skin = skin

    def update(self, *args):
        # Called once per frame by LOBBY_SPRITES.update()
        self._reload_if_needed()

    def upgrade(self, *args, **kwargs):
        # Future hook for animations or effects
        pass
    
    def add_to_groups(self, *groups):
        for g in groups:
            g.add(self)
