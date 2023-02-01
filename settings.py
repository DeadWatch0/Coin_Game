from character import *
from game_elements import *
import pygame
from pygame.locals import *


def init():

    global running
    running = True

    global chosen
    chosen = "cookie"

    global window_demensions
    window_demensions = width, height = 1275, 690

    global screen
    screen = pygame.display.set_mode((width, height))

    global start_pressed
    start_pressed = False

    global background
    background = pygame.image.load(r"src\background.png").convert()

    global icon
    icon = {"exit": "src\exit.png", "buttonRight": r"src\buttonRight.png",
            "buttonLeft": r"src\buttonLeft.png", "lobby": r"src\lobby.png", "bomb": r"src\bomb.png", "spikes": r"src\spikes.png"}

    global skin
    skin = {"cookie": "src\cookie.png", "tower": r"src\tower.png"}

    global points
    points = 0

    global all_sprites
    all_sprites = pygame.sprite.Group()

    global button_group
    button_group = pygame.sprite.Group()

    global character_group
    character_group = pygame.sprite.Group()

    global coin_group
    coin_group = pygame.sprite.Group()

    global text_group
    text_group = pygame.sprite.Group()

    global bomb_group
    bomb_group = pygame.sprite.Group()

    global spikes_group
    spikes_group = pygame.sprite.Group()

    global character
    character = Character(skin[settings.chosen], window_demensions)

    global exit_text
    exit_text = Text("GAME OVER!", 56, (255, 20, 20), window_demensions)

    global start_text
    start_text = Text("START", 34, (255, 255, 255), window_demensions)

    global points_counter
    points_counter = Text(f"points: {points}",
                          46, (110, 50, 60), window_demensions)

    global rightScroll
    rightScroll = Button(icon["buttonRight"],
                         window_demensions)

    global leftScroll
    leftScroll = Button(icon["buttonLeft"], window_demensions)

    global exit
    exit = Button(icon["exit"], window_demensions)

    global coin1
    coin1 = Coin(window_demensions)

    global lobby_button
    lobby_button = Button(icon["lobby"], window_demensions)

    global bomb
    bomb = []

    global spikes
    spikes = []

    global bombs_number
    bombs_number = 5

    global spikes_number
    spikes_number = 5
