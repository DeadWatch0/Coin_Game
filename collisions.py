from character import *
import settings
from settings import *
from game_elements import *
from lobby import *
import pygame
from pygame.locals import *
from level import *


def coin_collision(obstacle):

    settings.points += obstacle.effect
    obstacle.kill()
    settings.points_counter.kill()

    obstacle = (Obstacle(icon["coin"], settings.window_demensions, 1))
    obstacle.add_to_group(
        settings.coin_group, settings.all_sprites)

    settings.points_counter = Text(
        f"points: {settings.points}", 36, (110, 50, 60), settings.window_demensions)
    settings.points_counter.rect.x = settings.window_demensions[0] - \
        settings.points_counter.rect.width
    settings.points_counter.add_to_group(
        settings.text_group, settings.all_sprites)


def bomb_collision(touched_bomb):

    if settings.points == 0:
        settings.exit.quiting(settings.exit_text,
                              settings.screen, settings.background)

    else:
        touched_bomb.bombing()
        touched_bomb.kill
        settings.points_counter.kill()
        settings.bomb.append(
            Bombs(settings.icon["bomb"], settings.window_demensions, 1))
        settings.bomb[-1].add_to_group(settings.bomb_group,
                                       settings.all_sprites)

        settings.points_counter = Text(
            f"points: {settings.points}", 36, (110, 50, 60), settings.window_demensions)
        settings.points_counter.rect.x = settings.window_demensions[0] - \
            settings.points_counter.rect.width
        settings.points_counter.add_to_group(
            settings.text_group, settings.all_sprites)
