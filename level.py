import sys
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN, K_w, K_s, K_a, K_d
import settings
from game_elements import Obstacle, Button
from character import Character
from collisions import check_collisions
from hud import draw_hud, handle_game_over

def level_loop():
    # 1) Start a fresh session
    settings.reset()

    screen = settings.SCREEN
    clock  = settings.CLOCK
    w, h   = settings.WINDOW_DIMENSIONS

    # 2) Create & add the player
    player = Character()
    settings.GAME_SPRITES.add(player)

    # 3) Spawn initial coins and bombs into GAME_SPRITES & their groups
    for _ in range(5):
        Obstacle.spawn('coin',  1, settings.GAME_SPRITES, settings.COINS)
    for _ in range(3):
        Obstacle.spawn('bomb', -1, settings.GAME_SPRITES, settings.BOMBS)

    # 4) In-game “back to lobby” button
    lobby_btn = Button('lobby',
        (settings.WINDOW_WIDTH-40, 20), action=lambda: settings.change_state(settings.STATE_LOBBY))
    exit_btn  = Button('exit',(settings.WINDOW_WIDTH-40,  60), action=lambda: sys.exit())
    settings.GAME_SPRITES.add(lobby_btn, exit_btn)
    settings.BUTTONS.add(lobby_btn, exit_btn)

    # 5) Main game loop
    while True:
        # --- Event handling ---
        for ev in pygame.event.get():
            if ev.type == QUIT:
                return 'QUIT'
            if ev.type == MOUSEBUTTONDOWN:
                for btn in settings.BUTTONS:
                    btn.handle_event(ev)
        
        if settings.GAME_STATE == settings.STATE_LOBBY:
            # cleanup & return immediately
            settings.GAME_SPRITES.empty()
            settings.BUTTONS.empty()
            return 'LOBBY'

        # --- Player movement ---
        keys = pygame.key.get_pressed()
        dx = keys[K_d] - keys[K_a]
        dy = keys[K_s] - keys[K_w]
        if dx or dy:
            player.move(dx, dy)

        # --- Collisions & potential game over ---
        result = check_collisions(player)
        if result == 'game_over':
            handle_game_over()
            return 'LOBBY'

        # --- Drawing ---
        screen.blit(settings.BACKGROUND_IMG, (0, 0))
        settings.GAME_SPRITES.draw(screen)
        draw_hud()
        pygame.display.flip()

        # --- Tick ---
        clock.tick(60)
