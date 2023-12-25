import time

import pygame

from lib.game import Game
from lib.base import Base
from lib.system import System
from lib.keys import Keys
from lib.mouse import Mouse
from lib.audio import AudioController
from lib.surfaces import Image
from lib.window import Window


class Session:
    """Class representing the entire game session and meta related variables."""

    def __init__(self):
        pygame.init()

        self.system = System(pygame.display.Info())
        self.window = Window(self.system, "Otherworld Blight (Alpha 2.0)", Image("game_icon.png"))
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
    def screen(self):
        return self.window.screen

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
