import traceback
from character import *
import settings
from settings import *
from game_elements import *
import pygame
from pygame.locals import *

pygame.init()

window_demensions = width, height = 1275, 690
screen = pygame.display.set_mode((width, height))

background = pygame.image.load(r"src\background.png").convert()

icon = {"exit": "src\exit.png", "buttonRight": r"src\buttonRight.png",
        "buttonLeft": r"src\buttonLeft.png"}
skin = {"cookie": "src\cookie.png", "tower": r"src\tower.png"}

pygame.display.set_caption("Coin Game")


def add_coin(group1, group2, name):
    group1.add(name)
    group2.add(name)


def main():
    points = 0

    all_sprites = pygame.sprite.Group()
    button_group = pygame.sprite.Group()
    character_group = pygame.sprite.Group()
    coin_group = pygame.sprite.Group()
    text_group = pygame.sprite.Group()
    settings.init()

    character = Character(skin[settings.chosen], window_demensions)
    character.add_to_group(character_group, all_sprites)

    exit_text = Text("GAME OVER!", 56, (255, 20, 20), window_demensions)
    exit_text.rect.x = exit_text.max_latitude/2
    exit_text.rect.y = exit_text.max_longitude/2

    start_text = Text("START", 34, (255, 255, 255), window_demensions)
    start_text.rect.x = start_text.max_latitude/2
    start_text.rect.y = character.rect.y + character.rect.width + 80
    start_text.add_to_group(text_group, all_sprites)

    points_counter = Text(f"points: {points}",
                          46, (110, 50, 60), window_demensions)
    points_counter.rect.x = points_counter.max_latitude

    rightScroll = Button(icon["buttonRight"],
                         window_demensions)
    rightScroll.action_name = rightScroll.scrollingRight
    rightScroll.rect.x = character.rect.x + 140
    rightScroll.rect.y = character.rect.y + 40
    rightScroll.add_to_group(button_group, all_sprites)

    leftScroll = Button(icon["buttonLeft"], window_demensions)
    leftScroll.action_name = leftScroll.scrollingLeft
    leftScroll.rect.x = character.rect.x - 20 - leftScroll.rect.width
    leftScroll.rect.y = character.rect.y + 40
    leftScroll.add_to_group(button_group, all_sprites)

    exit = Button(icon["exit"], window_demensions)
    exit.action_name = exit.quiting
    exit.add_to_group(button_group, all_sprites)

    coin1 = Coin(window_demensions)

    screen.blit(background, (0, 0))
    for each in all_sprites:
        screen.blit(each.image, each.rect)
    pygame.display.flip()

    while 1:
        global start_pressed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

            if event.type == MOUSEBUTTONDOWN:
                for button in button_group:
                    button.collision = button.rect.collidepoint(event.pos)
                    if button == exit:
                        button.action(
                            button.collision, button.action_name, exit_text, screen, background)
                    else:
                        button.action(button.collision,
                                      button.action_name, skin)
                        character.kill()
                        character = Character(
                            skin[settings.chosen], window_demensions)
                        character.add_to_group(character_group, all_sprites)
                        screen.blit(background, (0, 0))
                        for each in all_sprites:
                            screen.blit(each.image, each.rect)
                        pygame.display.flip()
                        if start_text.rect.collidepoint(event.pos):
                            settings.start_pressed = True
            if settings.start_pressed:
                start_text.kill()
                for button in button_group:
                    if button == exit:
                        pass
                    else:
                        button.kill()
                points_counter.add_to_group(text_group, all_sprites)
                add_coin(coin_group, all_sprites, coin1)
                screen.blit(background, (0, 0))
                for each in all_sprites:
                    screen.blit(each.image, each.rect)
                pygame.display.flip()
                while 1:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit(0)

                        if event.type == MOUSEBUTTONDOWN:
                            for button in button_group:
                                button.collision = button.rect.collidepoint(
                                    event.pos)
                                button.action(
                                    button.collision, button.action_name, exit_text, screen, background)

                        key_pressed = pygame.key.get_pressed()
                        if key_pressed[K_w]:
                            character.moveUp()
                        if key_pressed[K_s]:
                            character.moveDown()
                        if key_pressed[K_d]:
                            character.moveRight()
                        if key_pressed[K_a]:
                            character.moveLeft()

                    if coin1.rect.colliderect(character.rect):
                        coin1.kill()
                        points_counter.kill()

                        character.speed += 2
                        points += 1

                        coin1 = Coin(window_demensions)
                        add_coin(coin_group, all_sprites, coin1)

                        points_counter = Text(
                            f"points: {points}", 36, (110, 50, 60), window_demensions)
                        points_counter.rect.x = window_demensions[0] - \
                            points_counter.rect.width
                        points_counter.add_to_group(text_group, all_sprites)

                    screen.blit(background, (0, 0))
                    for each in all_sprites:
                        screen.blit(each.image, each.rect)
                    pygame.display.flip()


if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
