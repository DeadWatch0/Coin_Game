import pygame
from pygame.font import SysFont
import settings
from settings import save_high_score

def show_game_over(screen):
    save_high_score()

    w, h = settings.WINDOW_DIMENSIONS
    screen.fill((0,0,0))

    font_big = SysFont('Arial', 56)
    font_sm  = SysFont('Arial', 36)

    lines = [
        ("GAME OVER", font_big,    (255,  0,  0)),
        (f"Final: {settings.points}", font_sm,    (255,255,255)),
        (f"Best:  {settings.high_score}", font_sm,  (255,255, 0)),
    ]

    y = h//2 - 80
    for text, font, color in lines:
        surf = font.render(text, True, color)
        screen.blit(surf, (w//2 - surf.get_width()//2, y))
        y += surf.get_height() + 10

    pygame.display.flip()
    pygame.time.wait(2000)
