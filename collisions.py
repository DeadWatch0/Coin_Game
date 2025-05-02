import pygame
import settings
from settings import add_points, lose_health
from game_elements import Obstacle

# --- Spatial Hash Implementation ---
class SpatialHash:
    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.cells = {}

    def _key(self, x, y):
        return (x // self.cell_size, y // self.cell_size)

    def clear(self):
        """Empty out all buckets (call once per frame)."""
        self.cells.clear()

    def insert(self, sprite):
        """
        Hash each sprite by its top-left corner into one cell.
        For many small sprites, this is sufficient and O(1).
        """
        x0, y0 = self._key(sprite.rect.left,  sprite.rect.top)
        x1, y1 = self._key(sprite.rect.right, sprite.rect.bottom)
        for ix in range(x0, x1 + 1):
            for iy in range(y0, y1 + 1):
                self.cells.setdefault((ix, iy), []).append(sprite)

    def query(self, rect):
        """
        Return all sprites whose top-left corner lies under any
        of the four corners of the query rect.
        """
        corners = [
            (rect.left,   rect.top),
            (rect.right,  rect.top),
            (rect.left,   rect.bottom),
            (rect.right,  rect.bottom),
        ]
        found = set()
        for x, y in corners:
            key = self._key(x, y)
            for spr in self.cells.get(key, ()):
                found.add(spr)
        return found

# Create a global grid; pick cell_size ~ sprite size (e.g. 64 or 128)
_grid = SpatialHash(cell_size=128)

def check_collisions(character):
    # 1) Rebuild spatial hash of all game sprites
    _grid.clear()
    for spr in settings.GAME_SPRITES:
        _grid.insert(spr)

    # 2) Coin collisions
    # Query nearby sprites before precise check
    coin_candidates = _grid.query(character.rect)
    for spr in coin_candidates:
        if spr in settings.COINS and character.rect.colliderect(spr.rect):
            # Remove and respawn
            settings.GAME_SPRITES.remove(spr)
            settings.COINS.remove(spr)
            add_points(1)
            Obstacle.spawn('coin', 1,
                           settings.GAME_SPRITES, settings.COINS)

    # 3) Bomb collisions
    bomb_candidates = _grid.query(character.rect)
    for spr in bomb_candidates:
        if spr in settings.BOMBS and character.rect.colliderect(spr.rect):
            settings.GAME_SPRITES.remove(spr)
            settings.BOMBS.remove(spr)
            lose_health()
            Obstacle.spawn('bomb', -1,
                           settings.GAME_SPRITES, settings.BOMBS)

    # 4) Check for game over
    if settings.health <= 0:
        return 'game_over'
    return 'continue'
