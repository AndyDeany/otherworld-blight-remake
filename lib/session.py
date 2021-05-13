from lib.keys import Keys
from lib.mouse import Mouse
from lib.audio import AudioController


class Session:
    """Class representing the entire game session and meta related variables."""

    def __init__(self):
        self.mouse = Mouse()
        self.keys = Keys()
        self.audio = AudioController()

