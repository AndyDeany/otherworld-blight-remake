import pygame


class MouseButton:
    """Class for representing a button on the mouse."""

    all = {}

    def __init__(self, button: int):
        self.button = button
        self.just_pressed = False
        self.is_pressed = False
        self.just_released = False
        self.all[self.button] = self

    def __bool__(self):
        return self.just_released

    def down(self):
        """Process the pressing down of the mouse button."""
        self.just_pressed = True
        self.is_pressed = True

    def up(self):
        """Process the release of the mouse button."""
        self.is_pressed = False
        self.just_released = True


class Mouse:
    """Class for representing the user's mouse."""

    def __init__(self):
        self.x = 0
        self.y = 0

        self.left = MouseButton(1)
        self.middle = MouseButton(2)
        self.right = MouseButton(3)

    def __getitem__(self, button):
        try:
            return MouseButton.all[button]
        except KeyError:
            print(f"Generating MouseButton({button}) instance.")
            return MouseButton(button)

    @staticmethod
    def reset_buttons():
        for button in MouseButton.all.values():
            button.just_pressed = False
            button.just_released = False

    def update_coordinates(self):
        """Update the stored x and y coordinates of the mouse."""
        self.x, self.y = pygame.mouse.get_pos()

    def process_button_down(self, mouse_button_down_event):
        """Process a pygame.MOUSEBUTTONDOWN event."""
        self[mouse_button_down_event.button].down()

    def process_button_up(self, mouse_button_up_event):
        """Process a pygame.MOUSEBUTTONUP event."""
        self[mouse_button_up_event.button].up()

    def is_in(self, start_x, start_y, end_x, end_y):
        """Return whether or not the mouse curosr is within the given boundaries."""
        return start_x < self.x < end_x and start_y < self.y < end_y
