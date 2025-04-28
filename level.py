import pygame
import settings
from game_elements import Obstacle
from character import Character
from collisions import check_collisions
from hud import draw_hud

def level_loop():
    # 1) Lobby
    settings.reset()
    
    from lobby import lobby_screen
    if not lobby_screen():
        return 'quit'

    # 2) clear
    settings.ALL_SPRITES.empty()
    settings.COINS.empty()
    settings.BOMBS.empty()

    # 3) Spawn initial elements
    for _ in range(5):
        Obstacle.spawn('coin',  1, settings.ALL_SPRITES, settings.COINS)
    for _ in range(3):
        Obstacle.spawn('bomb', -1, settings.ALL_SPRITES, settings.BOMBS)

    # 4) Player
    player = Character()
    player.add_to_groups(settings.ALL_SPRITES)

    # 5) Game loop
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return 'quit'

        keys = pygame.key.get_pressed()
        dx = keys[pygame.K_d] - keys[pygame.K_a]
        dy = keys[pygame.K_s] - keys[pygame.K_w]
        player.move(dx, dy)

        if check_collisions(player) == 'game_over':
            return 'game_over'

        settings.SCREEN.blit(settings.BACKGROUND_IMG, (0,0))
        settings.ALL_SPRITES.draw(settings.SCREEN)
        draw_hud()
        pygame.display.flip()
        settings.CLOCK.tick(60)
