import settings
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
    main()
