from character import *
import settings
from settings import *
from game_elements import *
from lobby import *
import pygame
from pygame.locals import *
from level import *


def obstacle_collision(obstacle, array, group):

    temp_icon = obstacle.icon
    temp_effect = obstacle.effect

    if (temp_effect == -1 and settings.points == 0):
        settings.exit.quiting(settings.exit_text1, settings.exit_text2,
                              settings.screen, settings.background)

    else:

        settings.character.speed += obstacle.effect
        settings.points += obstacle.effect

        settings.points_counter.kill()

        array.remove(obstacle)

        array.append(
            (Obstacle(temp_icon, settings.window_demensions, temp_effect)))
        array[-1].add_to_group(
            group, settings.all_sprites)

        settings.points_counter = Text(
            f"points: {settings.points}", 36, (110, 50, 60), settings.window_demensions)
        settings.points_counter.rect.x = settings.window_demensions[0] - \
            settings.points_counter.rect.width
        settings.points_counter.add_to_group(
            settings.text_group, settings.all_sprites)
        return array
