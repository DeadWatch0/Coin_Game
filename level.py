from character import *
import settings
from settings import *
from game_elements import *
from lobby import *
import pygame
from pygame.locals import *


def level():
    settings.start_text.kill()
    for button in settings.button_group:
        if button == settings.exit:
            pass
        else:
            button.kill()
            settings.points_counter.add_to_group(
                settings.text_group, settings.all_sprites)
            settings.coin1.add_to_group(
                settings.coin_group, settings.all_sprites)
            settings.lobby_button.add_to_group(
                settings.button_group, settings.all_sprites)
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
                    if button == settings.lobby_button:
                        if button.rect.collidepoint(event.pos) == True:
                            settings.start_pressed = False
                            break
                    else:
                        button.collision = button.rect.collidepoint(event.pos)
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

        if settings.coin1.rect.colliderect(settings.character.rect):
            settings.coin1.kill()
            settings.points_counter.kill()

            settings.character.speed += 2
            settings.points += 1

            settings.coin1 = Coin(settings.window_demensions)
            settings.coin1.add_to_group(
                settings.coin_group, settings.all_sprites)

            settings.points_counter = Text(
                f"points: {settings.points}", 36, (110, 50, 60), settings.window_demensions)
            settings.points_counter.rect.x = settings.window_demensions[0] - \
                settings.points_counter.rect.width
            settings.points_counter.add_to_group(
                settings.text_group, settings.all_sprites)

        settings.screen.blit(settings.background, (0, 0))
        for each in settings.all_sprites:
            settings.screen.blit(each.image, each.rect)
        pygame.display.flip()
        return settings.start_pressed
    return settings.start_pressed