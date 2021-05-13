class Coordinates:
    """Class for representing a set of (x, y) coordinates in a room."""

    def __init__(self, x, y):
        """Create a Coordinate instance."""
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (self.x, self.y) == other

    def __getitem__(self, item):
        return (self.x, self.y)[item]

    def __repr__(self):
        return f"{type(self).__name__}({self.x}, {self.y})"

    @property
    def up(self):
        """Get the coordinates above this one."""
        return Coordinates(self.x, self.y - 1)

    @property
    def right(self):
        """Get the coordinates to the right of this one."""
        return Coordinates(self.x + 1, self.y)

    @property
    def down(self):
        """Get the coordinates below this one."""
        return Coordinates(self.x, self.y + 1)

    @property
    def left(self):
        """Get the coordinates to the left of this one."""
        return Coordinates(self.x - 1, self.y)
