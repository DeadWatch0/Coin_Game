import pygame
import settings
from game_elements import Obstacle
from character import Character
from collisions import check_collisions
from hud import draw_hud


def level_loop():
    # First show lobby
    from lobby import lobby_screen
    if not lobby_screen():
        return 'quit'

    # Then reset and clear any sprites
    settings.reset()
    settings.ALL_SPRITES.empty()
    settings.COINS.empty()
    settings.BOMBS.empty()

    # Spawn game elements
    for _ in range(5):
        Obstacle.spawn('coin', 1, settings.ALL_SPRITES, settings.COINS, [settings.COINS, settings.BOMBS])

    for _ in range(3):
        Obstacle.spawn('bomb', -1, settings.ALL_SPRITES, settings.BOMBS, [settings.COINS, settings.BOMBS])
        
    # Add character
    char = Character()
    char.add_to_groups(settings.ALL_SPRITES)

    # Main game loop
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return 'quit'
        keys = pygame.key.get_pressed()
        dx = keys[pygame.K_d] - keys[pygame.K_a]
        dy = keys[pygame.K_s] - keys[pygame.K_w]
        char.move(dx, dy)
        status = check_collisions(char)
        if status == 'game_over':
            return 'game_over'
        settings.SCREEN.blit(settings.BACKGROUND_IMG, (0,0))
        settings.ALL_SPRITES.draw(settings.SCREEN)
        draw_hud()
        pygame.display.flip()
        settings.CLOCK.tick(60)
