import traceback
import pygame
import settings
from level import level_loop
from lobby import lobby_screen


def main():
    pygame.init()
    settings.init()
    while True:
            
        if settings.GAME_STATE == settings.STATE_LOBBY:
            lobby_screen()
            
        if settings.GAME_STATE == settings.STATE_PLAY:
            level_loop()
            
        if settings.GAME_STATE == settings.STATE_QUIT:
            break
        
if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
