import pygame
import settings
from hud import handle_game_over
from settings import add_points, lose_health
from game_elements import Obstacle


def check_collisions(character):
    hits = pygame.sprite.spritecollide(character, settings.COINS, True)
    for _ in hits:
        add_points(1)
        Obstacle.spawn('coin', 1, settings.ALL_SPRITES, settings.COINS, [settings.COINS, settings.BOMBS])

    hits = pygame.sprite.spritecollide(character, settings.BOMBS, True)
    for _ in hits:
        lose_health()
        Obstacle.spawn('bomb', -1, settings.ALL_SPRITES, settings.BOMBS, [settings.COINS, settings.BOMBS])
        if settings.health <= 0:
            handle_game_over()
            return 'game_over'
    return 'continue'