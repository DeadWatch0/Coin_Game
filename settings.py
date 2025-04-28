import pygame

def init():
    # Window
    global WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_DIMENSIONS, SCREEN, CLOCK
    WINDOW_WIDTH, WINDOW_HEIGHT = 1275, 690
    WINDOW_DIMENSIONS = (WINDOW_WIDTH, WINDOW_HEIGHT)
    SCREEN = pygame.display.set_mode(WINDOW_DIMENSIONS)
    CLOCK = pygame.time.Clock()

    # Assets
    global ICONS, SKINS, BACKGROUND_IMG
    ICONS = {
        'exit': 'src/exit.png',
        'coin': 'src/coin.png',
        'bomb': 'src/bomb.png',
        'buttonRight': 'src/buttonRight.png',
        'buttonLeft': 'src/buttonLeft.png',
        'start': 'src/start.png'
    }
    SKINS = {
        'cookie': 'src/cookie.png',
        'tower': 'src/tower.png'
    }
    BACKGROUND_IMG = pygame.image.load('src/background.png').convert()

    # Game state
    global points, session_high, health, max_health, high_score, selected_skin
    points = 0
    session_high = 0
    max_health = 3
    health = max_health
    selected_skin = 'cookie'

    # Load persistent high score
    global high_score
    try:
        with open('high_score.txt', 'r') as f:
            high_score = int(f.read())
    except:
        high_score = 0

    # Sprite groups
    global ALL_SPRITES, BUTTONS, COINS, BOMBS
    ALL_SPRITES = pygame.sprite.Group()
    BUTTONS = pygame.sprite.Group()
    COINS = pygame.sprite.Group()
    BOMBS = pygame.sprite.Group()


def add_points(delta):
    global points, session_high
    points += delta
    session_high = max(session_high, points)


def lose_health():
    global health
    health -= 1


def save_high_score():
    global high_score, session_high
    if session_high > high_score:
        high_score = session_high
        with open('high_score.txt', 'w') as f:
            f.write(str(high_score))


def reset():
    global points, session_high, health
    points = 0
    session_high = 0
    health = max_health
