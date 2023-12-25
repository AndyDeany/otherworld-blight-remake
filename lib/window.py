import os

import pygame

from lib.surfaces import Image


class Window:
    """Class representing the application window."""

    MODE_WINDOWED = "windowed"
    MODE_BORDERLESS = "borderless"
    MODE_FULLSCREEN = "fullscreen"

    screen: pygame.Surface

    def __init__(self, system, caption, icon):
        self.system = system
        self.caption = caption
        self.icon = icon
        self.initialise_screen()

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

    def initialise_screen(self, *, mode=MODE_BORDERLESS, resolution=None):
        if resolution is None:
            resolution = self.screen.get_size()

        flags = pygame.HWSURFACE | pygame.DOUBLEBUF
        if mode == self.MODE_WINDOWED:
            x = (self.system.MONITOR_WIDTH - resolution[0]) // 2
            y = (self.system.MONITOR_HEIGHT - resolution[1]) // 2
            os.environ["SDL_VIDEO_WINDOW_POS"] = f"{x},{y}"
        elif mode == self.MODE_BORDERLESS:
            flags |= pygame.NOFRAME
            os.environ["SDL_VIDEO_WINDOW_POS"] = "0,0"
        elif mode == self.MODE_FULLSCREEN:
            flags |= pygame.FULLSCREEN
        else:
            raise ValueError("Unknown mode for reinitialise_screen(): " + mode + "[coding syntax error].")

        self.screen = pygame.display.set_mode(resolution, flags)