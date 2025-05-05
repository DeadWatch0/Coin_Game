import pygame
import persistence
from objective import ObjectiveManager

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
        'exit':           'src/exit.png',
        'coin':           'src/coin.png',
        'bomb':           'src/bomb.png',
        'health_potion':  'src/health_potion.png',
        'buttonRight':    'src/buttonRight.png',
        'buttonLeft':     'src/buttonLeft.png',
        'start':          'src/start.png',
        'lobby':          'src/lobby.png',
        'chest':          'src/chest.png',
    }
    SKINS = {
        'cookie': 'src/cookie.png',
        'tower':  'src/tower.png',
    }
    BACKGROUND_IMG = pygame.image.load('src/background.png').convert()

    # Game state
    global points, session_high, health, max_health
    global selected_skin, high_score, _persisted
    points = session_high = 0
    max_health = 3
    health = max_health
    selected_skin = 'cookie'

    _persisted = persistence.load()
    high_score = _persisted.get('high_score', 0)

    # Sprite groups
    global LOBBY_SPRITES, GAME_SPRITES, BUTTONS
    global COINS, BOMBS, HEALTH_POTIONS, CHESTS, OBSTACLES
    LOBBY_SPRITES     = pygame.sprite.Group()
    GAME_SPRITES      = pygame.sprite.Group()
    BUTTONS           = pygame.sprite.Group()
    COINS             = pygame.sprite.Group()
    BOMBS             = pygame.sprite.Group()
    HEALTH_POTIONS    = pygame.sprite.Group()
    CHESTS            = pygame.sprite.Group()
    OBSTACLES         = pygame.sprite.Group()

    # FSM states
    global STATE_LOBBY, STATE_PLAY, STATE_QUIT, GAME_STATE
    STATE_LOBBY = 'LOBBY'
    STATE_PLAY  = 'PLAY'
    STATE_QUIT  = 'QUIT'
    GAME_STATE  = STATE_LOBBY

    # Objectives
    from objective import ObjectiveManager, make_collect_objective

    # Example: collect 50 coins → spawn a chest + +1 max health
    def reward_collect_50():
        from game_elements import Chest
        sw, sh = WINDOW_DIMENSIONS
        Chest.spawn(GAME_SPRITES, CHESTS, position=(sw//2, sh//2))

    ObjectiveManager.register(
        make_collect_objective(5, reward_fn=reward_collect_50)
    )

def change_points(delta):
    global points, session_high
    points += delta
    session_high = max(session_high, points)

def change_health(delta):
    global health
    health = max(0, health + delta)
    
def change_max_health(delta):
    global max_health
    max_health = max(0, health + delta)

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
    points = session_high = 0
    health = max_health = 3
    GAME_SPRITES.empty()
    LOBBY_SPRITES.empty()
    COINS.empty()
    BOMBS.empty()
    HEALTH_POTIONS.empty()
    CHESTS.empty()
    OBSTACLES.empty()
