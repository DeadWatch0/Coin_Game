import pygame

class Objective:
    def __init__(self, description, check_fn, on_complete_fn=None):
        self.description     = description
        self.check_fn        = check_fn
        self.on_complete_fn  = on_complete_fn or (lambda: None)
        self.completed       = False

    def update(self):
        if not self.completed and self.check_fn():
            self.completed = True
            self.on_complete_fn()

    def render(self, font):
        color = (170,255,170) if self.completed else (255,255,255)
        text  = "Objective Completed!" if self.completed else self.description
        return font.render(text, True, color)

def make_collect_objective(target_count, reward_fn=None):
    def check_fn():
        import settings
        return settings.points >= target_count
    desc = f"Collect {target_count} coins"
    return Objective(desc, check_fn, reward_fn)

def make_survive_objective(seconds, reward_fn=None):
    start = pygame.time.get_ticks()
    def check_fn():
        return (pygame.time.get_ticks() - start) >= seconds * 1000
    desc = f"Survive {seconds} seconds"
    return Objective(desc, check_fn, reward_fn)

class ObjectiveManager:
    """
    Holds objectives and exposes update/draw calls.
    """
    _objectives = []
    _current    = 0

    @classmethod
    def register(cls, objective):
        cls._objectives.append(objective)
    
    @classmethod
    def reset(cls):
        """Clear completion state and rewind to the first objective."""
        cls._current = 0
        for obj in cls._objectives:
            obj.completed = False

    @classmethod
    def update_all(cls):
        if cls._current < len(cls._objectives):
            cls._objectives[cls._current].update()

    @classmethod
    def draw_current(cls, screen, font, position):
        if cls._current < len(cls._objectives):
            surf = cls._objectives[cls._current].render(font)
            screen.blit(surf, position)
