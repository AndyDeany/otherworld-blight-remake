"""Module containing the Save class for managing saves of the game."""
import json

from lib.coordinates import Coordinates


class Save:
    """Class representing a save of the game."""

    CURRENT = "current"
    ROOM_NUMBER = "room_number"
    CUTSCENE_PLAYED = "cutscene_played"
    PLAYER = "player"
    SETTINGS = "settings"

    PLAYER_ATTRIBUTES = ("form", "position", "orientation", "room", "exp", "level",
                         "skill_points", "max_life", "current_life")

    def __init__(self, number):
        """Create a Save instance with the given number as it's name."""
        self.number = number
        self.file_name = f"../saves/save{self.number}.json"

        with open(self.file_name, "r") as save_file:
            self.data = json.load(save_file)
        if self.is_empty:
            return

        self.current = self.data[self.CURRENT]
        self.room_number = self.data[self.ROOM_NUMBER]
        self.cutscene_played = list(self.data[self.CUTSCENE_PLAYED])
        self.player = self.data[self.PLAYER]
        self.settings = self.data[self.SETTINGS]

    @property
    def is_empty(self):
        """Return whether the save is empty (contains no save data)."""
        return not bool(self.data)

    def save(self, current, room_number, cutscene_played, player, settings):
        """Save the given data to the save file, overwriting any existing data there."""
        player = {
            attribute: getattr(player, attribute)
            for attribute in self.PLAYER_ATTRIBUTES
        }
        data = {
            self.CURRENT: current,
            self.ROOM_NUMBER: room_number,
            self.CUTSCENE_PLAYED: cutscene_played,
            self.PLAYER: player,
            self.SETTINGS: settings,
        }
        with open(self.file_name, "w") as save_file:
            json.dump(data, save_file, cls=OtherworldBlightEncoder, indent=4)
        self.current = current
        self.room_number = room_number
        self.cutscene_played = cutscene_played
        self.player = player
        self.settings = settings

    def delete(self):
        """Delete the contents of this save permanently."""
        with open(self.file_name, "w") as save_file:
            json.dump({}, save_file)

    def set_player_attributes(self, player):
        for attribute in self.PLAYER_ATTRIBUTES:
            setattr(player, attribute, self.player[attribute])
        player.position = Coordinates(*player.position)


class OtherworldBlightEncoder(json.JSONEncoder):
    """Subclass of json.JSONEncoder for serializing objects of non builtin classes."""

    def default(self, o):
        if isinstance(o, Coordinates):
            return (o.x, o.y)
        return super().default(o)
