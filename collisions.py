import pygame
import settings
from settings import add_points, lose_health
from game_elements import Obstacle

def check_collisions(character):
    # Collect coins
    coin_hits = pygame.sprite.spritecollide(
        character, settings.COINS, True
    )
    for _ in coin_hits:
        add_points(1)
        # Respawn a new coin in view
        Obstacle.spawn('coin',  1,
                       settings.GAME_SPRITES, settings.COINS)

    # Hit bombs
    bomb_hits = pygame.sprite.spritecollide(
        character, settings.BOMBS, True
    )
    for _ in bomb_hits:
        lose_health()
        # Respawn a new bomb in view
        Obstacle.spawn('bomb', -1,
                       settings.GAME_SPRITES, settings.BOMBS)

    # Signal game over when health runs out
    if settings.health <= 0:
        return 'game_over'

    return 'continue'
