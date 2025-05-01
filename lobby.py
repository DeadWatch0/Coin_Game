import sys, pygame
from character import Character
from pygame.locals import *
import settings
from game_elements import Button
from preview_sprite import PreviewSprite  
from pygame.font import SysFont

def lobby_screen():
    screen = settings.SCREEN
    w, h   = settings.WINDOW_DIMENSIONS
    clock  = settings.CLOCK

    # Fonts & title
    title_font = SysFont("Arial", 48)
    instr_font = SysFont("Arial", 28)
    title_surf = title_font.render("Choose your character", True, (255,255,255))
    title_rect = title_surf.get_rect(center=(w//2, 80))

    # Scroll helper
    def scroll(dir):
        keys = list(settings.SKINS.keys())
        idx  = keys.index(settings.selected_skin)
        settings.selected_skin = keys[(idx + dir) % len(keys)]

    # Buttons
    exit_btn  = Button('exit',       ( 60,  60), action=lambda: sys.exit())
    left_btn  = Button('buttonLeft', (w//2 -200, h//2), action=lambda: scroll(-1))
    right_btn = Button('buttonRight',(w//2 +200, h//2), action=lambda: scroll( 1))
    start_btn = Button('start',      (w//2,      h -100), action=lambda: settings.change_state(settings.STATE_PLAY))

    # Preview sprite
    preview = PreviewSprite((w//2, h//2 - 40))

    # Add to groups
    for btn in (exit_btn, left_btn, right_btn, start_btn):
        btn.add_to_groups(settings.LOBBY_SPRITES, settings.BUTTONS)
    preview.add_to_groups(settings.LOBBY_SPRITES)

    # Main lobby loop
    while True:
        # Update preview (and any future animated sprites)
        settings.LOBBY_SPRITES.update()

        # Draw background, title, sprites & buttons
        screen.blit(settings.BACKGROUND_IMG, (0,0))
        screen.blit(title_surf, title_rect)
        settings.LOBBY_SPRITES.draw(screen)
        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'QUIT'
            if event.type == MOUSEBUTTONDOWN:
                for btn in settings.BUTTONS:
                    btn.handle_event(event)

            # State switch
            if settings.GAME_STATE == settings.STATE_PLAY:
                # Clean up lobby sprites/buttons before leaving
                settings.LOBBY_SPRITES.empty()
                settings.BUTTONS.empty()
                settings.reset()
                return 'PLAY'

        clock.tick(30)
