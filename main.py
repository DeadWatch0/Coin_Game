import settings
import pygame
from lobby import lobby_screen
from level import level_loop
from fsm import StateMachine

def main():
    settings.init()
    sm = StateMachine(settings.STATE_LOBBY)
    sm.add(settings.STATE_LOBBY, lobby_screen)
    sm.add(settings.STATE_PLAY,  level_loop)
    sm.add(settings.STATE_QUIT,  lambda: None)

    while True:
        next_state = sm.run()
        if next_state == settings.STATE_QUIT:
            break
        sm.transition(next_state)

if __name__ == '__main__':
    try:
        main()
    except Exception:
        import traceback
        traceback.print_exc()
        # optional in‑game error screen
        try:
            settings.SCREEN.fill((0,0,0))
            font = pygame.font.SysFont(None, 48)
            msg  = font.render("Unexpected error occurred", True, (255,0,0))
            settings.SCREEN.blit(msg, (50, settings.WINDOW_HEIGHT//2))
            pygame.display.flip()
            pygame.time.wait(2000)
        except:
            pass
    finally:
        pygame.quit()
