import traceback
from character import *
import settings
from settings import *
from game_elements import *
from lobby import *
from level import *
import pygame
from pygame.locals import *


def main():

    while (True):
        if lobby():
            level()


if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
