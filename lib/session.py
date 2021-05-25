import time

import pygame

from lib.game import Game
from lib.base import Base
from lib.keys import Keys
from lib.mouse import Mouse
from lib.audio import AudioController
from lib.surfaces import Image


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

        self.game = Game(self)

        Base.initialise(self)

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, icon: Image):
        self._icon = icon
        pygame.display.set_icon(icon.surface)

    @property
    def caption(self):
        return self._caption

    @caption.setter
    def caption(self, caption: str):
        self._caption = caption
        pygame.display.set_caption(caption)

    def event_handling(self):
        """Run the code for the main event loop to deal with user inputs/actions."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse.process_button_down(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse.process_button_up(event)
            elif event.type == pygame.KEYDOWN:
                self.keys.process_key_down(event)
            elif event.type == pygame.KEYUP:
                self.keys.process_key_up(event)

    def loop(self):
        """Run the main program loop."""
        self.uptime = time.time() - self.start_time
        self.mouse.reset_buttons()
        self.mouse.update_coordinates()
        self.keys.reset()
        self.event_handling()
