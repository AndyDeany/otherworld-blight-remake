from lib.base import Base
from lib.keys import Keys
from lib.mouse import Mouse
from lib.audio import AudioController
from lib.surfaces import Surface


class Session:
    """Class representing the entire game session and meta related variables."""

    def __init__(self, screen):
        self.screen = screen
        self.mouse = Mouse()
        self.keys = Keys()
        self.audio = AudioController()

        Base.initialise(self)
        Surface.initialise(self)
