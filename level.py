from character import *
import settings
from settings import *
from game_elements import *
from lobby import *
from collisions import *
import pygame
from pygame.locals import *


def level():

    coins = [Obstacle(icon["coin"], window_demensions, 1)]

    while (True):
        settings.running = True
        if settings.start_pressed == False:
            settings.runnung = False

        for each in settings.all_sprites:
            each.kill()
        settings.screen.blit(settings.background, (0, 0))

        settings.exit.add_to_group(settings.button_group, settings.all_sprites)
        settings.character.add_to_group(
            settings.character_group, settings.all_sprites)
        settings.lobby_button.add_to_group(
            settings.button_group, settings.all_sprites)
        coins[0].add_to_group(
            settings.coin_group, settings.all_sprites)
        settings.bomb.add_to_group(settings.bomb_group, settings.all_sprites)
        settings.points_counter.add_to_group(
            settings.text_group, settings.all_sprites)

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
                        if button == settings.lobby_button:
                            if button.rect.collidepoint(event.pos) == True:
                                settings.start_pressed = False
                                return settings.start_pressed
                        else:
                            button.collision = button.rect.collidepoint(
                                event.pos)
                            button.action(button.collision, button.action_name,
                                          settings.exit_text, settings.screen, settings.background)

                key_pressed = pygame.key.get_pressed()
                if key_pressed[K_w]:
                    settings.character.moveUp()
                if key_pressed[K_s]:
                    settings.character.moveDown()
                if key_pressed[K_d]:
                    settings.character.moveRight()
                if key_pressed[K_a]:
                    settings.character.moveLeft()

                if settings.start_pressed == False:
                    break

            if settings.start_pressed == False:
                break

            if settings.bomb.rect.colliderect(settings.character.rect):
                bomb_collision()

            settings.screen.blit(settings.background, (0, 0))
            for each in settings.all_sprites:
                settings.screen.blit(each.image, each.rect)
            pygame.display.flip()
