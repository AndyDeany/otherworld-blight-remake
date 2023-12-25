from lib.hud import Hud
from lib.number_dropper import NumberDropper


class Game:
    """Class representing the actual game - everything to do with gameplay functionality."""

    def __init__(self, session):
        """Create a Game instance."""
        self.session = session
        self.player = None
        self.hud = Hud()
        self.number_dropper = NumberDropper()

    def loop(self):
        """Run the game loop logic."""
        self.number_dropper.logic()
