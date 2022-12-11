from character import *
import settings
from settings import *
from game_elements import *
import pygame
from pygame.locals import *

pygame.init()
settings.init()
pygame.display.set_caption("Coin Game")


settings.exit_text.rect.x = settings.exit_text.max_latitude/2
settings.exit_text.rect.y = settings.exit_text.max_longitude/2

settings.start_text.rect.x = settings.start_text.max_latitude/2
settings.start_text.rect.y = settings.character.rect.y + \
    settings.character.rect.width + 80


settings.points_counter.rect.x = settings.points_counter.max_latitude

settings.rightScroll.action_name = settings.rightScroll.scrollingRight
settings.rightScroll.rect.x = settings.character.rect.x + 140
settings.rightScroll.rect.y = settings.character.rect.y + 40


settings.leftScroll.action_name = settings.leftScroll.scrollingLeft
settings.leftScroll.rect.x = settings.character.rect.x - \
    20 - settings.leftScroll.rect.width
settings.leftScroll.rect.y = settings.character.rect.y + 40


settings.exit.action_name = settings.exit.quiting

settings.lobby_button.rect.x = 0 + settings.exit.rect.width


def lobby():
    for each in settings.all_sprites:
        each.kill()
    settings.screen.blit(settings.background, (0, 0))

    settings.character.rect.x = settings.character.max_latitude/2
    settings.character.rect.y = settings.character.max_longitude/2
    settings.character.add_to_group(
        settings.character_group, settings.all_sprites)
    settings.start_text.add_to_group(settings.text_group, settings.all_sprites)
    settings.rightScroll.add_to_group(
        settings.button_group, settings.all_sprites)
    settings.leftScroll.add_to_group(
        settings.button_group, settings.all_sprites)
    settings.exit.add_to_group(settings.button_group, settings.all_sprites)

    settings.screen.blit(settings.background, (0, 0))
    for each in settings.all_sprites:
        settings.screen.blit(each.image, each.rect)
    pygame.display.flip()

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

            if event.type == MOUSEBUTTONDOWN:

                for button in settings.button_group:
                    button.collision = button.rect.collidepoint(event.pos)
                    if button == settings.exit:
                        button.action(
                            button.collision, button.action_name, settings.exit_text, settings.screen, settings.background)
                    else:
                        button.action(button.collision,
                                      button.action_name, settings.skin)
                        settings.character.kill()
                        settings.character = Character(
                            settings.skin[settings.chosen], settings.window_demensions)
                        settings.character.add_to_group(
                            settings.character_group, settings.all_sprites)
                        settings.screen.blit(settings.background, (0, 0))
                        for each in settings.all_sprites:
                            settings.screen.blit(each.image, each.rect)
                        pygame.display.flip()
                if settings.start_text.rect.collidepoint(event.pos):
                    settings.start_pressed = True
                    return settings.start_pressed
