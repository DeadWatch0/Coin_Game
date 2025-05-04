import pygame
import persistence

def init():
    pygame.init()
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
        'health_potion': 'src/health_potion.png',
        'buttonRight': 'src/buttonRight.png',
        'buttonLeft': 'src/buttonLeft.png',
        'start': 'src/start.png',
        'lobby': 'src/lobby.png'
    }
    SKINS = {
        'cookie': 'src/cookie.png',
        'tower': 'src/tower.png'
    }
    BACKGROUND_IMG = pygame.image.load('src/background.png').convert()

    # Game state
    global points, session_high, health, max_health, high_score, selected_skin, _persisted, objective
    points = session_high = 0
    max_health = 3
    health = max_health
    selected_skin = 'cookie'
    objective = False

    # Load persisted data (e.g. high score)
    _persisted = persistence.load()
    high_score = _persisted.get('high_score', 0)

    # Sprite groups
    global LOBBY_SPRITES, GAME_SPRITES, BUTTONS, COINS, BOMBS, HEALTH_POTIONS
    LOBBY_SPRITES = pygame.sprite.Group()
    GAME_SPRITES = pygame.sprite.Group()
    HEALTH_POTIONS = pygame.sprite.Group()
    BUTTONS = pygame.sprite.Group()
    COINS = pygame.sprite.Group()
    BOMBS = pygame.sprite.Group()
    
    global GAME_STATE, STATE_LOBBY, STATE_PLAY, STATE_QUIT
    STATE_LOBBY = 'LOBBY'
    STATE_PLAY  = 'PLAY'
    STATE_QUIT  = 'QUIT'
    GAME_STATE = STATE_LOBBY


def change_points(delta):
    global points, session_high
    points += delta
    session_high = max(session_high, points)


def change_health(delta):
    global health
    health += delta
    if health < 0:
        health = 0


def save_high_score():
    global high_score, _persisted
    if session_high > high_score:
        high_score = session_high
        _persisted['high_score'] = high_score
        persistence.save(_persisted)
            


def change_state(state):
    global GAME_STATE 
    GAME_STATE = state


def reset():
    global points, session_high, health
    points = 0
    session_high = 0
    health = max_health
    GAME_SPRITES.empty()
    LOBBY_SPRITES.empty()
    COINS.empty()
    BOMBS.empty()
    HEALTH_POTIONS.empty() 
