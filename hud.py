import pygame
from pygame.font import SysFont
import settings

def draw_hud():
    font = SysFont('Arial', 24)
    SCREEN = settings.SCREEN
    # Score
    score_surf = font.render(f"Score: {settings.points}", True, (255,255,255))
    SCREEN.blit(score_surf, (10, 10))
    # Session high
    high_surf = font.render(f"High: {settings.session_high}", True, (255,255,0))
    SCREEN.blit(high_surf, (10, 40))
    # Health
    health_surf = font.render(f"Health: {settings.health}", True, (255,0,0))
    SCREEN.blit(health_surf, (10, 70))


def handle_game_over():
    import pygame
    from pygame.font import SysFont
    import settings
    from settings import save_high_score

    save_high_score()
    SCREEN = settings.SCREEN
    w, h = settings.WINDOW_DIMENSIONS
    font1 = SysFont('Arial', 56)
    font2 = SysFont('Arial', 36)
    SCREEN.fill((0,0,0))
    go = font1.render("GAME OVER", True, (255,0,0))
    final = font2.render(f"Final: {settings.points}", True, (255,255,255))
    high = font2.render(f"Best: {settings.high_score}", True, (255,255,0))
    SCREEN.blit(go, (w//2 - go.get_width()//2, h//2 - 80))
    SCREEN.blit(final, (w//2 - final.get_width()//2, h//2))
    SCREEN.blit(high, (w//2 - high.get_width()//2, h//2 + 40))
    pygame.display.flip()
    pygame.time.wait(2000)
