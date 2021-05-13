class Game:
    """Class representing the actual game - everything to do with gameplay functionality."""

    def __init__(self, session):
        """Create a Game instance."""
        self.session = session
        self.player = None
