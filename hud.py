import pygame
from pygame.font import SysFont
import settings

class HUD:
    def __init__(self):
        self.font = SysFont('Arial', 24)
        self._last = {'points': None, 'high': None, 'health': None}
        self._surf = {}

    def draw(self, screen):
        # Points
        if settings.points != self._last['points']:
            self._surf['points'] = self.font.render(
                f"Score: {settings.points}", True, (255,255,255)
            )
            self._last['points'] = settings.points
        # High score
        if settings.session_high != self._last['high']:
            self._surf['high'] = self.font.render(
                f"High:  {settings.session_high}", True, (255,255, 0)
            )
            self._last['high'] = settings.session_high
        # Health
        if settings.health != self._last['health']:
            self._surf['health'] = self.font.render(
                f"Health:{settings.health}", True, (255,  0,  0)
            )
            self._last['health'] = settings.health

        screen.blit(self._surf['points'], (10,10))
        screen.blit(self._surf['high'],   (10,40))
        screen.blit(self._surf['health'], (10,70))