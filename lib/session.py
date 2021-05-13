import time

import pygame

from lib.base import Base
from lib.keys import Keys
from lib.mouse import Mouse
from lib.audio import AudioController
from lib.surfaces import Surface, Image


class Session:
    """Class representing the entire game session and meta related variables."""

    def __init__(self, screen):
        self.screen = screen
        self.caption = "Otherworld Blight (Alpha 2.0)"
        self.icon = Image("game_icon.png")
        self.fps = 30
        self.clock = pygame.time.Clock()
        self.start_time = time.time()
        self.uptime = 0
        self.is_running = True

        self.mouse = Mouse()
        self.keys = Keys()
        self.audio = AudioController()

        Base.initialise(self)
        Surface.initialise(self)

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, icon: Image):
        self._icon = icon
        pygame.display.set_icon(icon.image)

    @property
    def caption(self):
        return self._caption

    @caption.setter
    def caption(self, caption: str):
        self._caption = caption
        pygame.display.set_caption(caption)
