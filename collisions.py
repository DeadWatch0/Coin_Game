import pygame
import settings
from hud import handle_game_over
from settings import add_points, lose_health


def check_collisions(character):
    # Coin collisions
    hits = pygame.sprite.spritecollide(character, settings.COINS, True)
    for _ in hits:
        add_points(1)
        from game_elements import Obstacle
        Obstacle('coin', 1).add_to_groups(settings.ALL_SPRITES, settings.COINS)
    # Bomb collisions
    hits = pygame.sprite.spritecollide(character, settings.BOMBS, True)
    for _ in hits:
        lose_health()
        from game_elements import Obstacle
        Obstacle('bomb', -1).add_to_groups(settings.ALL_SPRITES, settings.BOMBS)
        if settings.health <= 0:
            handle_game_over()
            return 'game_over'
    return 'continue'
