import pygame
from pygame.font import SysFont
import settings

class HUD:
    def __init__(self):
        self.font = SysFont('Arial', 24)
        # Cached values & surfaces
        self._last_points = None
        self._surf_points   = None
        self._last_high     = None
        self._surf_high     = None
        self._last_health   = None
        self._surf_health   = None

    def draw(self, screen):
        # Points
        if settings.points != self._last_points:
            text = f"Score: {settings.points}"
            self._surf_points = self.font.render(text, True, (255,255,255))
            self._last_points = settings.points

        # Session high
        if settings.session_high != self._last_high:
            text = f"High: {settings.session_high}"
            self._surf_high = self.font.render(text, True, (255,255, 0))
            self._last_high = settings.session_high

        # Health
        if settings.health != self._last_health:
            text = f"Health: {settings.health}"
            self._surf_health = self.font.render(text, True, (255, 0, 0))
            self._last_health = settings.health

        # Blit all
        screen.blit(self._surf_points, (10,10))
        screen.blit(self._surf_high,   (10,40))
        screen.blit(self._surf_health, (10,70))
