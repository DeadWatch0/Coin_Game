import sys
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN, K_w, K_s, K_a, K_d
import settings
from game_elements import Coin, Bomb, HealthPotion, Chest, Button
from character import Character
from collisions import check_collisions
from game_over import show_game_over
from hud import HUD
from objective import ObjectiveManager


def level_loop():
    # 1) Start a fresh session
    settings.reset()

    screen = settings.SCREEN
    clock  = settings.CLOCK
    w, h   = settings.WINDOW_DIMENSIONS

    hud = HUD()
    
    # 2) Create & add the player
    player = Character()
    settings.GAME_SPRITES.add(player)

    # 3) Spawn initial coins and bombs into GAME_SPRITES & their groups
    for _ in range(5):
        Coin.spawn(settings.GAME_SPRITES, settings.COINS)
    for _ in range(3):
        Bomb.spawn(settings.GAME_SPRITES, settings.BOMBS)

    # 4) In-game “back to lobby” button
    lobby_btn = Button('lobby',
        (settings.WINDOW_WIDTH-40, 20), action=lambda: settings.change_state(settings.STATE_LOBBY))
    exit_btn  = Button('exit',(settings.WINDOW_WIDTH-40,  60), action=lambda: settings.change_state(settings.STATE_QUIT))
    
    settings.GAME_SPRITES.add(lobby_btn, exit_btn)
    settings.BUTTONS.add(lobby_btn, exit_btn)

    # 5) Main game loop
    while True:
        dt = clock.tick(60) / 1000.0  # seconds
        
        # --- Event handling ---
        for ev in pygame.event.get():
            if ev.type == QUIT:
                ObjectiveManager.reset()
                return settings.STATE_QUIT
            if ev.type == MOUSEBUTTONDOWN:
                for btn in settings.BUTTONS:
                    btn.handle_event(ev)
                    if settings.GAME_STATE == settings.STATE_QUIT:
                    # clean up if you like
                        return settings.STATE_QUIT
        
                if settings.GAME_STATE == settings.STATE_LOBBY:
                # cleanup & return immediately
                    ObjectiveManager.reset()
                    settings.GAME_SPRITES.empty()
                    settings.BUTTONS.empty()
                    return settings.STATE_LOBBY

        # Update player physics
        player.update(dt)
        
        for spr in settings.OBSTACLES:
            if hasattr(spr, 'activate_frame'):
                spr.activate_frame()

        # --- Collisions & potential game over ---
        result = check_collisions(player)
        if result == 'game_over':
            show_game_over(settings.SCREEN)
            ObjectiveManager.reset()
            settings.change_state(settings.STATE_LOBBY)
            return settings.STATE_LOBBY
        
        # Update objectives
        ObjectiveManager.update_all()

        # --- Drawing ---
        screen.blit(settings.BACKGROUND_IMG, (0, 0))
        settings.GAME_SPRITES.draw(screen)
        hud.draw(screen)
        # Draw current objective
        ObjectiveManager.draw_current(screen, hud.font, position=(10, 100))
        pygame.display.flip()
