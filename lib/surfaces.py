import pygame


class Surface:

    default_screen = None

    @classmethod
    def initialise(cls, session):
        cls.default_screen = session.screen

    def __init__(self, default_coords: tuple):
        self.default_x, self.default_y = default_coords
        self.surface = None

    def display(self, x=None, y=None, *, area=None, special_flags=0, screen=None):
        x = x if x is not None else self.default_x
        y = y if y is not None else self.default_y
        screen = screen or self.default_screen
        screen.blit(self.surface, (x, y), area=area, special_flags=special_flags)

    def blit(self, source, dest, area=None, special_flags=0):
        """Blit another surface over this one."""
        self.surface.blit(source.surface, dest, area=area, special_flags=special_flags)

    @property
    def width(self):
        """Get the width of the pygame.Surface represented by this object."""
        return self.surface.get_width()

    @property
    def height(self):
        """Get the height of the pygame.Surface represented by this object."""
        return self.surface.get_height()

    def set_alpha(self, alpha):
        """Set the alpha of the pygame.Surface represented by this object."""
        self.surface.set_alpha(alpha)


class Image(Surface):
    def __init__(self, path_or_surface, default_coords=(None, None), *, convert_alpha=True):
        super().__init__(default_coords)
        if isinstance(path_or_surface, pygame.Surface):
            self.surface = path_or_surface
        else:
            self.surface = pygame.image.load("../images/" + path_or_surface)
            if convert_alpha:
                self.surface = self.surface.convert_alpha()
            else:
                self.surface = self.surface.convert()


class Text(Surface):
    """Class for representing a generated text image."""

    def __init__(self, text, font, color, default_coords: tuple = (None, None), *,
                 antialias=True, with_outline=False, outline_color=(0, 0, 0)):
        super().__init__(default_coords)
        self.surface = font.render(text, antialias, color)
        self.is_outlined = with_outline
        if self.is_outlined:
            outline_text = font.render(text, antialias, outline_color)
            width, height = self.surface.get_size()
            outlined_image = pygame.Surface((width + 2, height + 2)).convert_alpha()
            pygame.draw.rect(outlined_image, (0, 0, 0, 0), [0, 0, width + 2, height + 2])
            outlined_image.blit(outline_text, (0, 0))
            outlined_image.blit(outline_text, (0, 1))
            outlined_image.blit(outline_text, (0, 2))
            outlined_image.blit(outline_text, (1, 2))
            outlined_image.blit(outline_text, (2, 2))
            outlined_image.blit(outline_text, (2, 1))
            outlined_image.blit(outline_text, (2, 0))
            outlined_image.blit(outline_text, (1, 0))
            outlined_image.blit(self.surface, (1, 1))
            self.surface = outlined_image
            if self.default_x is not None:
                self.default_x -= 1
            if self.default_y is not None:
                self.default_y -= 1

    def display(self, x=None, y=None, *, area=None, special_flags=0, screen=None):
        if self.is_outlined:
            if x is not None:
                x -= 1
            if y is not None:
                y -= 1
        super().display(x, y, area=area, screen=screen)
