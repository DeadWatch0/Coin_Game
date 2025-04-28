import traceback
import pygame
import settings
from level import level_loop


def main():
    pygame.init()
    settings.init()
    while True:
        result = level_loop()
        if result == 'quit': break

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
