import time

import pygame


class Key:
    """Class for representing a key on the keyboard."""

    all = {}

    def __init__(self, keycode):
        self.keycode = keycode
        self.just_pressed = False
        self.is_pressed = False
        self._pressed_time = None
        self.all[self.keycode] = self

    def __bool__(self):
        return self.just_pressed

    def down(self):
        self.just_pressed = True
        self.is_pressed = True
        self._pressed_time = time.time()

    def up(self):
        self.is_pressed = False
        self._pressed_time = None

    @property
    def time_held(self):
        """Return how long the key has been held for."""
        if self._pressed_time is None:
            return 0
        return time.time() - self._pressed_time


class Keys:
    def __init__(self):
        pygame.key.set_repeat(500, 50)

        self.keys_pressed = 0
        self.receiving_text_input = False
        self.text_input = ""
        self.maximum_characters = 0

        self.backspace = Key(8)
        self.enter = Key(13)
        self.escape = Key(27)
        self.space = Key(32)
        self.tab = Key(9)
        self.numpad_enter = Key(1073741912)

        self.right_arrow = Key(1073741903)
        self.left_arrow = Key(1073741904)
        self.down_arrow = Key(1073741905)
        self.up_arrow = Key(1073741906)

        self.w = Key(119)
        self.a = Key(97)
        self.s = Key(115)
        self.d = Key(100)

        self.e = Key(101)
        self.r = Key(114)

        self.one = Key(49)
        self.numpad_one = Key(1073742050)

    def __getitem__(self, keycode):
        try:
            return Key.all[keycode]
        except KeyError:
            print(f"Generating Key({keycode}) instance.")
            return Key(keycode)

    @staticmethod
    def reset():
        for key in Key.all.values():
            key.just_pressed = False

    def start_text_input(self, maximum_characters, *, default_text=""):
        """Start receiving text input. Be sure to call stop_text_input() after you're done."""
        self.receiving_text_input = True
        self.text_input = default_text
        self.maximum_characters = maximum_characters
        pygame.key.start_text_input()

    def process_text_input(self, text_input_event):
        """Process the receiving of text input whilst it's actively being received.

        This will be after calling start_text_input() and before calling stop_text_input().
        """
        new_text = self.text_input + text_input_event.text
        if len(new_text) <= self.maximum_characters:
            self.text_input = new_text

    def process_text_input_special_keys(self):
        """Process special keys like backspace in the context of text input."""
        if not self.receiving_text_input:
            return
        if self.backspace and self.text_input:
            self.text_input = self.text_input[:-1]
        # Could have code for arrow keys with a cursor and the delete key here. Not a big priority though.

    def stop_text_input(self):
        pygame.key.stop_text_input()
        self.receiving_text_input = False
        return self.text_input

    def process_key_down(self, key_down_event):
        """Process a pygame.KEYDOWN event."""
        self[key_down_event.key].down()

    def process_key_up(self, key_up_event):
        """Process a pygame.KEYUP event."""
        self[key_up_event.key].up()
