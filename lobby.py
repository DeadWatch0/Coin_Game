import sys, pygame
from pygame.locals import *
import settings
from game_elements import Button
from pygame.font import SysFont


def lobby_screen():
    screen = settings.SCREEN
    w, h = settings.WINDOW_DIMENSIONS
    title_font = SysFont("Arial", 48)
    instr_font = SysFont("Arial", 28)
    title_surf = title_font.render("Choose your character", True, (255,255,255))
    title_rect = title_surf.get_rect(center=(w//2, 80))

    def scroll(dir):
        keys = list(settings.SKINS.keys())
        idx = keys.index(settings.selected_skin)
        settings.selected_skin = keys[(idx + dir) % len(keys)]

    exit_btn = Button('exit', (60, 60), action=lambda: sys.exit())
    left_btn = Button('buttonLeft', (w//2 - 200, h//2), action=lambda: scroll(-1))
    right_btn = Button('buttonRight', (w//2 + 200, h//2), action=lambda: scroll(1))
    start_btn = Button('start', (w//2, h - 100), action=None)

    # Only lobby buttons go here
    for btn in [exit_btn, left_btn, right_btn, start_btn]:
        btn.add_to_groups(settings.ALL_SPRITES, settings.BUTTONS)

    clock = settings.CLOCK
    while True:
        # Draw lobby
        screen.blit(settings.BACKGROUND_IMG, (0,0))
        screen.blit(title_surf, title_rect)
        skin_path = settings.SKINS[settings.selected_skin]
        char_img = pygame.image.load(skin_path).convert_alpha()
        char_rect = char_img.get_rect(center=(w//2, h//2))
        screen.blit(char_img, char_rect)
        for btn in settings.BUTTONS:
            screen.blit(btn.image, btn.rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            for btn in settings.BUTTONS:
                btn.handle_event(event)
            if event.type == MOUSEBUTTONDOWN and start_btn.rect.collidepoint(event.pos):
                # Clear only lobby buttons
                settings.BUTTONS.empty()
                return True
        clock.tick(30)
