import os
import random
from operator import attrgetter

import pygame
from moviepy.editor import VideoFileClip

pygame.init()
monitor_info = pygame.display.Info()
MONITOR_WIDTH = monitor_info.current_w
MONITOR_HEIGHT = monitor_info.current_h
os.environ["SDL_VIDEO_WINDOW_POS"] = "0,0"
screen = pygame.display.set_mode((1920, 1080), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.NOFRAME)


from lib.base import Base
from lib.session import Session
from lib.audio import AudioClip
from lib.surfaces import Image

from lib.save import Save

from lib.hud import Hud
from lib.loot import Loot
from lib.item import Item
from lib.coordinates import Coordinates


# VARIABLE ASSIGNMENT ------------------------------------------------------------------------------
# Assigning essential game variables
session = Session(screen)
show_hud = False
show_spellbook = False
levelling_up = False
levelup_frame = 0
movement_started = False

cutscene_played = [False for _cutscene in range(9)]

coordinates_set = False
portal_x = -10
portal_y = -10

zaal_life = 1782
zaal_animation = -1

font = pygame.font.SysFont("Arial Regular", 90, False, False)
dropfont = pygame.font.SysFont("Impact", 20, False, False)

screen_width, screen_height = session.screen.get_size()
# Creating an extra surface for put on top of the screen, for fading
fade_screen = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)


# Changes and reinitialises the screen with new settings
def reinitialise_screen(resolution=(screen_width, screen_height), mode="fullscreen"):
    global screen, screen_width, screen_height
    screen_width, screen_height = resolution
    flags = pygame.HWSURFACE | pygame.DOUBLEBUF
    if mode == "fullscreen":
        flags |= pygame.FULLSCREEN
    elif mode == "windowed":
        x, y = (MONITOR_WIDTH - screen_width)//2, (MONITOR_HEIGHT - screen_height)//2
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x},{y}"
    elif mode == "borderless":
        flags |= pygame.NOFRAME
        os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
    else:
        raise ValueError("Unknown mode for reinitialise_screen(): " + mode + "[coding syntax error].")
    screen = pygame.display.set_mode(resolution, flags)


# FUNCTION DEFINING --------------------------------------------------------------------------------

# Checking if the given arrow key has been held down the longest
def is_longest_held(direction_held_time):
    longest = max(session.keys.left_arrow.time_held, session.keys.right_arrow.time_held,
                  session.keys.up_arrow.time_held, session.keys.down_arrow.time_held,
                  session.keys.a.time_held, session.keys.d.time_held,
                  session.keys.w.time_held, session.keys.s.time_held)
    return direction_held_time == longest


# Corrects the player's coordinates if they are moving
def add_movement(self, character, axis, file_type):
    x_movement = (self.square_size[0] * character.movement_cooldown * character.movespeed) // (3 * session.fps)
    y_movement = (self.square_size[1] * character.movement_cooldown * character.movespeed) // (3 * session.fps)
    self_or_character = character if file_type == "image" else self
    sign = 1 if file_type == "image" else -1
    if axis == "x":
        if character.orientation == "left":
            return self_or_character.x + sign*x_movement
        if character.orientation == "right":
            return self_or_character.x - sign*x_movement
        return self_or_character.x
    if axis == "y":
        if character.orientation == "up":
            return self_or_character.y + sign*y_movement
        if character.orientation == "down":
            return self_or_character.y - sign*y_movement
        return self_or_character.y


# Defining a function to check if Vincent is in a valid place to interact with the given coordinates
def is_interactable(coordinates):
    return (vincent.position == coordinates
            or (vincent.position == coordinates.left and vincent.orientation == "right")
            or (vincent.position == coordinates.up and vincent.orientation == "down")
            or (vincent.position == coordinates.right and vincent.orientation == "left")
            or (vincent.position == coordinates.down and vincent.orientation == "up"))


# Defining functinos to show exp drops, damage values and healing values
def number_drop(number_type, character, value):
    """number_type = \"damage\", \"exp\", \"heal\""""
    global number_drops
    drop_x = character.x + character.width // 2
    drop_y = character.y + character.height // 2
    if number_type == "damage":
        colour = (255, 0, 0)
    elif number_type == "exp":
        colour = (255, 215, 0)
    elif number_type == "heal":
        colour = (43, 255, 0)
    else:
        raise ValueError(f"Invalid number_type '{number_type}'.")

    if value > 0:
        if number_type == "damage":
            value = str(-value)
        else:
            value = "+" + str(value)
    else:
        value = str(value)

    number_drops.append([drop_x, drop_y, colour, value, drop_y])


def display_number_drop(number_drop_item):
    session.screen.blit(dropfont.render(number_drop_item[3], True, number_drop_item[2]),
                        (number_drop_item[0], number_drop_item[1]))
    return number_drop_item[1] - 3


# Defining a function that displays the spellbook
def display_spellbook():
    if not cutscene_played[6]:
        spellbook_images["spellbook_default"].display(0, 0)
    else:
        spellbook_images["firebolt1"].display(0, 0)
    spellbook_images["firebolt_uncharged"].display(0, 0)
    session.screen.blit(font.render(str(vincent.level), True, (199, 189, 189)), (610, 20))
    session.screen.blit(font.render(str(vincent.skill_points), True, (199, 189, 189)), (1665, 20))
    session.screen.blit(font.render(str(firebolt.level), True, (142, 0, 0)), (834, 239))
    esc_exit.display(0, 0)


# Defining a function that displays dialogue boxes with the respective text
def display_dialogue(character, dialogue_number):
    dialogue[character + "box"].display(0, 0)
    dialogue[character + str(dialogue_number)].display(765, 895)
    return not (session.keys.space or session.keys.enter or session.keys.numpad_enter)


# CLASS DEFINING -----------------------------------------------------------------------------------
class Menu:
    def __init__(self, name, permanent, options, coordinates, actions, escape_action, settings=None):
        self.name = name
        self.background = Image("menus/" + self.name + "/background.png")
        self.permanent = [Image("menus/" + self.name + "/" + item + ".png") for item in permanent] # A list of all the different thing in the menu that are always shown
        self.sliders = []   # A list showing which settings in the menu are sliders        
        self.original_x = 0 # shows where the mouse was orignially pressed when moving a slider
        for option in options:
            if option[0][0:6] == "SLIDER":
                self.sliders.append([True, int(option[0][6:])])
            else:
                self.sliders.append([False])
        self.options = [[Image("menus/" + self.name + "/" + setting + ".png") for setting in option] for option in options] # A list of all the different options that the user can select in the menu
        self.settings = settings    # Shows which setting each option is currently on
        if self.settings is None:
            self.settings = [0 for option in range(len(options))]
        self.coordinates = coordinates  # The screen coordinates of each option in the permananent list above (for 1920x1080; this is adjusted for other resolutions)
        self.actions = actions  # The new value for current that each option leads to when its clicked
        self.escape_action = escape_action # The value for current if escape is pressed
        self.current_selection = 0  # The index of the option that the user has currently selected (is hovering over)
    
    # Displays the menu on the screen
    def display(self):
        self.background.display(0, 0)
        for item in self.permanent:
            item.display(0, 0)

        for option in range(len(self.options)):
            if self.sliders[option][0]:
                self.options[option][0].display((960 + 4*self.settings[option])*(screen_width/1920.0), self.sliders[option][1]*(screen_height/1080.0))

        if not self.sliders[self.current_selection][0]:
            self.options[self.current_selection][self.settings[self.current_selection]].display(0, 0)

        for index in range(len(self.options)):
            if len(self.options[index]) > 1:
                self.options[index][self.settings[index]].display(0, 0)
        
    # Changes the user's current selection in the menu
    def change_selection(self):
        for index in range(len(self.options)):
            if session.mouse.is_in(*self.coordinates[index]):
                self.current_selection = index
                return

        if (session.keys.up_arrow or session.keys.w) and self.current_selection > 0:
            self.current_selection -= 1
        if (session.keys.down_arrow or session.keys.s) and self.current_selection < len(self.options) - 1:
            self.current_selection += 1
    
    def change_settings(self):
        if session.mouse.left.is_pressed:
            global movement_started
            if not movement_started:
                self.original_x = session.mouse.x
                slider_selected = False
                for index in range(len(self.options)):
                    if session.mouse.is_in(*self.coordinates[index]):
                        self.current_selection = index
                        if self.sliders[self.current_selection][0]:
                            slider_selected = True
                if not slider_selected:
                    return
                movement_started = True
            else:
                if self.settings[self.current_selection] + session.mouse.x - self.original_x < 0:
                    self.settings[self.current_selection] = 0
                elif self.settings[self.current_selection] + session.mouse.x - self.original_x > 100:
                    self.settings[self.current_selection] = 100
                else:
                    self.settings[self.current_selection] = session.mouse.x - self.original_x

        elif self.sliders[self.current_selection][0]:
            if (session.keys.left_arrow or session.keys.left_arrow.is_pressed or session.keys.a or session.keys.a.is_pressed) and self.settings[self.current_selection] > 0:
                self.settings[self.current_selection] -= 1
            if (session.keys.right_arrow or session.keys.right_arrow.is_pressed or session.keys.d or session.keys.d.is_pressed) and self.settings[self.current_selection] < 100:
                self.settings[self.current_selection] += 1
        else:
            if (session.keys.left_arrow or session.keys.a) and self.settings[self.current_selection] > 0:
                self.settings[self.current_selection] -= 1
            if (session.keys.right_arrow or session.keys.d) and self.settings[self.current_selection] < len(self.options[self.current_selection]) - 1:
                self.settings[self.current_selection] += 1
    
    # Checks if the user has issued a continue command (by clicking or pressing enter/spacebar)
    def check_action(self):
        """returns True if current is changed"""
        global current
        if session.mouse.left or session.keys.space or session.keys.enter or session.keys.numpad_enter:
            current = self.actions[self.current_selection]
            return True
    
    def check_escape(self):
        global current
        if session.keys.escape:
            current = self.escape_action


class Character(Base):    # maybe add an "id" attribute. One to identify each object for coding purposes. Incase the names change/need to be different or whatever
    def __init__(self, name, frames, position, orientation, movespeed, room, exp, max_life, current_life):
        self.name = name    # Character's name
        self.x = 0  # Character's screen x coordinate
        self.y = 0  # Character's screen y coordinate
        self.frames = {frame: {direction: Image(self.name.lower().replace(" ", "/") + "/" + direction + str(frame) + ".png") for direction in ["left","up","right","down"]} for frame in range(frames)} #frames # The number of frames in the character's movement animation. The attribute "frames" becomes a dictionary of all the images during initialisation.
        self.position = position    # Character's grid position
        self.orientation = orientation  # The direction in which the character is facing
        self.movespeed = movespeed  # Character's movement speed. Should divide 3*session.fps (currently 90). Definitely should NOT be 90 or even near it. Also the 3*session.fps value may need changing.
        self.movement_cooldown = 0
        self.current_ability = ""   # The ability the character is currently using
        self.ability_frame = 0  # The frame of the ability animation the character is currently playing
        self.image = self.select_image()  # Character's image file        
        self.width = self.image.width      # Width of character's image in pixels
        self.height = self.image.height    # Height of character's image in pixels
        self.room = room  # Character's room
        self.exp = exp      # Friendly character's current experience/enemy character's experience given
        self.level = 1
        self.skill_points = 0
        self.max_life = max_life            # Life (health) points
        self.current_life = current_life
        self.alive = True
        self.death_frame = 0
        self.dead = False
    
    # Changes the x and y grid coordinates of the character
    def move(self, room, direction):
        """returns True if desired position is valid"""
        if not self.movement_cooldown and current[:8] != "cutscene" and self.alive:
            if (direction == "left"
                and (not (self.position.x - 1, self.position.y) in room.blocked)
                and (self.position.x > 0 or self.position.x-1 in
                     (exit_.coordinates.x for exit_ in room.exits
                      if exit_.coordinates.y == self.position.y))):
                self.orientation = "left"
                self.position = self.position.left
                self.movement_cooldown = (3*session.fps)//self.movespeed
                return True
            elif (direction == "right"
                  and (not (self.position.x + 1, self.position.y) in room.blocked)
                  and (self.position.x < room.max_coord.x or self.position.x+1 in [exit.coordinates.x for exit in room.exits if exit.coordinates.y == self.position.y])):
                self.orientation = "right"
                self.position = self.position.right
                self.movement_cooldown = (3*session.fps)//self.movespeed
                return True
            elif (direction == "up" and (not (self.position.x, self.position.y - 1) in room.blocked)
                  and (self.position.y > 0 or self.position.y-1 in [exit.coordinates.y for exit in room.exits if exit.coordinates.x == self.position.x])):
                self.orientation = "up"
                self.position = self.position.up
                self.movement_cooldown = (3*session.fps)//self.movespeed
                return True
            elif (direction == "down" and (not (self.position.x, self.position.y + 1) in room.blocked)
                  and (self.position.y < room.max_coord.y or self.position.y+1 in [exit.coordinates.y for exit in room.exits if exit.coordinates.x == self.position.x])):
                self.orientation = "down"
                self.position = self.position.down
                self.movement_cooldown = (3*session.fps)//self.movespeed
                return True
            else:
                self.orientation = direction
                return False

    def check_death(self):
        if self.current_life <= 0:
            self.alive = False
    
    def die(self, kill=False):
        if not self.alive and not self.dead:
            self.image = death_images[self.name][self.death_frame]
            if not isinstance(self.image, Image):
                self.image = self.image[self.orientation]
                
            self.death_frame += 1
            if self.death_frame == len(death_images[self.name]):
                self.dead = True
                self.death_frame = 0
                self.displayed = False  # for abilities
                if kill:
                    vincent.gain_exp(self)
    
    # Returns an image for the character based on their current state
    def select_image(self): # Add current action to this somehow? Characters will certainly look different when standing still/walking/using moves
        if self.current_ability:
            selected_image = ability_images[self.current_ability][self.name][self.orientation][self.ability_frame]
            self.ability_frame += 1
            if self.ability_frame == len(ability_images[self.current_ability][self.name][self.orientation]):
                abilities[self.current_ability].cast(self)
                self.current_ability = ""
                self.ability_frame = 0
            return selected_image
        else:
            return self.frames[(self.movement_cooldown * (len(self.frames)-1) * self.movespeed + (3*session.fps) - 1 +
                                int((session.keys.left_arrow.is_pressed or session.keys.right_arrow.is_pressed or
                                     session.keys.up_arrow.is_pressed or session.keys.down_arrow.is_pressed or
                                     session.keys.a.is_pressed or session.keys.d.is_pressed or
                                     session.keys.w.is_pressed or session.keys.s.is_pressed)
                                and not(self.movement_cooldown == (3*session.fps)//self.movespeed)))//(3*session.fps)][self.orientation]
    
    # Changes the character's image to reflect the character's current disposition
    def change_image(self):
        if self.alive:
            self.image = self.select_image()
                                
    def gain_exp(self, opponent):
        self.exp += opponent.exp
        number_drop("exp", self, opponent.exp)
        # Add exp drop code here? Perhaps call another function here to do it?


class Player(Character):
    def __init__(self, name, frames, position, orientation, movespeed, room, exp, max_life, current_life):
        self.form = "human"
        super().__init__(name, frames, position, orientation, movespeed, room, exp, max_life, current_life)
        self._slime_frames = {frame: {direction: Image(f"vincent/slime/{direction}{frame}.png")
                                      for direction in ("left", "up", "right", "down")}
                              for frame in range(6)}

    @property
    def name(self):
        return "Vincent Human" if self.form == "human" else "Vincent Slime"

    @name.setter
    def name(self, value):
        pass

    def transform(self):
        """Transform between a human and a slime."""
        if self.form == "human":
            self.form = "slime"
            self._human_frames = self.frames
            self.frames = self._slime_frames
            self.movespeed = 20
        elif self.form == "slime":
            self.form = "human"
            self.frames = self._human_frames
            self.movespeed = 15
        self.image = self.select_image()
        self.width = self.image.width
        self.height = self.image.height

    # Changing the direction in which the player is facing. This is useful for directing the player's abilities
    def change_orientation(self):
        if not self.movement_cooldown:
            if session.keys.left_arrow or session.keys.a:
                self.orientation = "left"
            if session.keys.right_arrow or session.keys.d:
                self.orientation = "right"
            if session.keys.up_arrow or session.keys.w:
                self.orientation = "up"
            if session.keys.down_arrow or session.keys.s:
                self.orientation = "down"
    
    # Changing the player's x and y grid coordinates according to user input
    def change_position(self, room):
        if self.movement_cooldown:  # decrementing self.movement cooldown if it is not equal to 0
            self.movement_cooldown -= 1
        elif ((session.keys.left_arrow.time_held > 1/session.fps or session.keys.a.time_held > 1/session.fps) or ((session.keys.left_arrow.time_held or session.keys.a.time_held) and self.orientation == "left")) and (is_longest_held(session.keys.left_arrow.time_held) or is_longest_held(session.keys.a.time_held)):
            self.move(room, "left")
        elif ((session.keys.right_arrow.time_held > 1/session.fps or session.keys.d.time_held > 1/session.fps) or ((session.keys.right_arrow.time_held or session.keys.d.time_held) and self.orientation == "right")) and (is_longest_held(session.keys.right_arrow.time_held) or is_longest_held(session.keys.d.time_held)):
            self.move(room, "right")
        elif ((session.keys.up_arrow.time_held > 1/session.fps or session.keys.w.time_held > 1/session.fps) or ((session.keys.up_arrow.time_held or session.keys.w.time_held) and self.orientation == "up")) and (is_longest_held(session.keys.up_arrow.time_held) or is_longest_held(session.keys.w.time_held)):
            self.move(room, "up")
        elif ((session.keys.down_arrow.time_held > 1/session.fps or session.keys.s.time_held > 1/session.fps) or ((session.keys.down_arrow.time_held or session.keys.s.time_held) and self.orientation == "down")) and (is_longest_held(session.keys.down_arrow.time_held) or is_longest_held(session.keys.s.time_held)):
            self.move(room, "down")
    
    def check_exit(self, room):
        if not self.movement_cooldown:
            for exit_ in room.exits:
                if self.position == exit_.coordinates:
                    self.join(exit_.room, exit_.position)
    
    def join(self, room, position):
        global current_room
        session.audio.sound.stop()
        current_room = rooms[room]
        self.room = room
        if room == 0:
            session.audio.sound.play(AudioClip("portal.ogg", 0.1), loop=True)
        self.position = position

        
class Npc(Character):
    def __init__(self, name, frames, position, orientation, movespeed, room, damage, exp, max_life, current_life):
        super(Npc, self).__init__(name, frames, position, orientation, movespeed, room, exp, max_life, current_life)
        self.moves = []  # A list of pending moves to be made by the npc
        self.damage = damage
        self.damage_cooldown = 0
        npcs.append(self)
        
    # Changing the npc's orientation based on its current pending moves
    def change_orientation(self):
        if len(self.moves) != 0 and not self.movement_cooldown:
            self.orientation = self.moves[0]
    
    # Moving the npc based on its current pending moves
    def change_position(self, room):
        if self.movement_cooldown: # decrementing self.movement cooldown if it is not equal to 0
            self.movement_cooldown -= 1
        elif len(self.moves) != 0:
            self.move(room, self.moves[0])
            if self.movement_cooldown == (3*session.fps)//self.movespeed: # Deleting the current move after the movement command has been issued
                del self.moves[0]
    
    def check_collision(self, player):
        if self.position == player.position and self.damage_cooldown == 0 and self.alive:
            damage_dealt = int(self.damage*(0.9 + 0.2*random.random()))
            player.current_life -= damage_dealt
            number_drop("damage", player, damage_dealt)
            self.damage_cooldown = session.fps
        elif self.damage_cooldown > 0:
            self.damage_cooldown -= 1
    
            
    
    # Finding the route from the npc's current position to the desired position using the A* search algorithm
    def find_route(self, room, goal):
        # (maybe somehow make this only run when the player moves? recalculating every frame seems inefficient...)
        if not self.alive or abs(self.position.x - goal[0]) + abs(self.position.y - goal[1]) > 15 or (frame % session.fps != 0 and abs(self.position.x - goal[0]) + abs(self.position.y - goal[1]) > 4):
            return
        elif (self.position == goal
              or goal[0] < 0 or goal[0] > room.max_coord.x or goal[1] < 0 or goal[1] > room.max_coord.y): # Ensuring that the algorithm isn't run to try to get to a place the npc cannot access.
            self.moves = []
        else:
            class Square(Coordinates):
                def __init__(self, coordinates, parent=None):  # If no parent value (starting square)
                    super().__init__(*coordinates)
                    self.parent = parent            # Parent square; the square which the cell is adjacent to that it came from
                    self.min_distance = abs(coordinates.x - goal[0]) + abs(coordinates.y - goal[1])   # Direct route to goal from square, as if there were no walls
                    if self.parent is None:   # Setting the square's current distance to 0 if it is the starting square
                        self.current_distance = 0
                    else:
                        self.current_distance = self.parent.current_distance + 1    # Distance from starting square to current square
                    self.total_distance = self.current_distance + self.min_distance

            goal_reached = False # Showing that the goal has not been reached (yet)
            processed = []  # A list of already processed squares; i.e. all directions from them have been explored
            pending = [Square(self.position)]    # A list of squares that have not been fully explored from. The starting square has no parent because it has not travelled from anywhere to get there

            while (len(pending) != 0
                   and len(pending) < (room.max_coord.x + 1)*(room.max_coord.y + 1)): # Making sure the algorithm doesn't carry on forever if it cannot find a route
                square = min(pending, key=attrgetter("total_distance"))

                processed.append(square)
                pending.remove(square)

                adjacents = []   # A list of squares adjacent to the current square
                if not square.x == 0:
                    adjacents.append(Square(square.left, square))
                if not square.y == 0:
                    adjacents.append(Square(square.up, square))
                if not square.x == room.max_coord.x:
                    adjacents.append(Square(square.right, square))
                if not square.y == room.max_coord.y:
                    adjacents.append(Square(square.down, square))

                for adjacent in adjacents:
                    if adjacent == goal:
                        goal = adjacent
                        goal_reached = True
                        break
                    elif (adjacent in room.blocked
                          or adjacent in [cell for cell in processed]):
                        pass    # Cell blocked, already processed or already queued to be processed
                    else:
                        pending.append(adjacent)
                if goal_reached:
                    break

            else:   # Unable to find a route to the goal - create a route to the next closest square
                closest_square = processed[0]   # Default VALID value
                for square in processed:
                    if square.distance_to(goal) < closest_square.distance_to(goal):
                        closest_square = square
                goal = closest_square

            # Compiling the route list
            route = []
            while True:
                if goal == self.position:
                    break
                elif goal.x == goal.parent.x - 1:
                    route.append("left")
                elif goal.x == goal.parent.x + 1:
                    route.append("right")
                elif goal.y == goal.parent.y - 1:
                    route.append("up")
                elif goal.y == goal.parent.y + 1:
                    route.append("down")
                goal = goal.parent

            route.reverse()   # Putting the commands in the correct order (they were placed in the list backwards)
            self.moves = route


# The class for abilities           
class Ability(Character):
    def __init__(self, name, frames, position, orientation, movespeed, room, damage, max_cooldown,
                 max_range, exp=0, max_life=1, current_life=1, icon_image=None, icon_cooldown_image=None):    # TODO: don't give images default values.
        super().__init__(name, frames, position, orientation, movespeed, exp, room, max_life, current_life)
        self.unlocked = False
        self.displayed = False
        self.damage = damage
        self.max_cooldown = max_cooldown
        self.cooldown = 0
        self.max_range = max_range
        self.moves = []  # A list of pending moves to be made by the ability
        abilities[self.name.lower()] = self
        self.icon_image = icon_image
        self.icon_cooldown_image = icon_cooldown_image
        
    def use(self, player):
        global zaal_animation
        if self.name != "Inferno":
            if self.cooldown == 0 and self.unlocked:
                self.room = player.room
                player.current_ability = self.name.lower()            
                self.cooldown = session.fps*self.max_cooldown
        elif self.dead and zaal_animation == -1 and player.position in [(x, y) for y in range(4, 15) for x in range(10, 13)]+[(x, y) for y in range(2, 4) for x in range(10)]+[(x, y) for y in range(2) for x in range(10, 13)]+[(x, y) for y in range(2, 4) for x in range(13, 20)]:
            zaal_animation = 18
            session.audio.sound.play(AudioClip("zaalattack.ogg", 0.2))
    
    def cast(self, player):
        global zaal_animation
        if self.name != "Inferno":            
            self.alive = True
            self.dead = False        
            self.displayed = True   
            if player.orientation == "left":
                self.position = player.position.left
            elif player.orientation == "up":
                self.position = player.position.up
            elif player.orientation == "right":
                self.position = player.position.right
            elif player.orientation == "down":
                self.position = player.position.down
            self.moves = [player.orientation for distance in range(self.max_range)]
        elif zaal_animation == 0:
            self.alive = True
            self.dead = False        
            self.displayed = True 
            self.room = player.room
            self.cooldown = session.fps*self.max_cooldown
            zaal_animation = -1
            if player.position in [(x, y) for y in range(4, 15) for x in range(10, 13)]:
                self.position = Coordinates(player.position.x, 5)
                self.moves = ["down" for distance in range(self.max_range)]
            elif player.position in [(x, y) for y in range(2, 4) for x in range(10)]:
                self.position = Coordinates(9, player.position.y)
                self.moves = ["left" for distance in range(self.max_range)]
            elif player.position in [(x, y) for y in range(2) for x in range(10, 13)]:
                self.position = Coordinates(player.position.x, 1)
                self.moves = ["up" for distance in range(self.max_range)]
            elif player.position in [(x, y) for y in range(2, 4) for x in range(13, 20)]:
                self.position = Coordinates(13, player.position.y)
                self.moves = ["right" for distance in range(self.max_range)]
            else:
                self.position = Coordinates(-10, -10)
                self.alive = False
                self.dead = True
                self.display = False
                self.cooldown = 0   
    
    def exist(self, room):
        if self.cooldown > 0:
            self.cooldown -= 1
        self.die()
        self.change_position(room)
        self.change_image()
        self.check_display()
        self.check_collision()
    
    def change_position(self, room):
        if self.movement_cooldown: # decrementing self.movement cooldown if it is not equal to 0
            self.movement_cooldown -= 1
        elif len(self.moves) != 0:
            if not self.move(room, self.moves[0]):
                self.alive = False
            if self.movement_cooldown == (3*session.fps)//self.movespeed: # Deleting the current move after the movement command has been issued
                del self.moves[0]
        
    def check_display(self):
        if len(self.moves) == 0 and self.movement_cooldown == 0:
            self.alive = False
    
    def check_collision(self):
        if self.name != "Inferno":
            for npc in npcs:
                if npc.position == self.position and self.alive:
                    damage_dealt = int(self.damage*(0.9 + 0.2*random.random()))
                    npc.current_life -= damage_dealt
                    number_drop("damage", npc, damage_dealt)
                    self.alive = False
        else:
            if self.position == vincent.position and self.alive:
                damage_dealt = int(self.damage*(0.9 + 0.2*random.random()))
                vincent.current_life -= damage_dealt
                number_drop("damage", vincent, damage_dealt)
                self.alive = False
                

# The class for extra things that are shown as well as the canvas and characters in rooms                   
class Extra(object):
    def __init__(self, image_name, placement, x, y, scroll_speed=0, scroll_axis=None, rotations=1, rotation_interval=0.0, start_x=None, end_x=None, start_y=None, end_y=None):
        # Default values are for when the extra should always be shown.
        self.image_name = image_name
        if image_name[0:9] in ["TESSELATE", "NEGATIVES"]:   # TESSELATE indicates that the image should be tesselated until the end of the screen. NEGATIVES indicates that the image should be shown if the player is NOT in the specified bounds
            self.image = extra_images[image_name[9:]]
        else:
            self.image = extra_images[image_name]
        self.width = self.image.width
        self.height = self.image.height
        self.placement = placement  # Whether the extra is shown below or above the characters
        self.x = x*(screen_width/1920.0)  # The image's x displacement from the canvas in pixels
        self.y = y*(screen_height/1080.0)  # The image's y displacement from the canvas in pixels
        self.original_x = self.x
        self.original_y = self.y
        self.scroll_speed = scroll_speed    # The scroll speed of the image in pixels per second in the positive direction of the axis
        self.scroll_axis = scroll_axis      # The axis in which the image scrolls
        self.rotations = rotations  # The number of images the extra switches between over time
        if rotations > 1:
            if image_name[0:9] in ["TESSELATE", "NEGATIVES"]:
                self.images = [extra_images[image_name[9:len(image_name)-len(str(rotations-1))] + str(n)] for n in range(rotations)] # Making a list of all the image files for extras that rotate through images
            else:
                self.images = [extra_images[image_name[0:len(image_name)-len(str(rotations-1))] + "".join(["0" for zero in range(len(str(rotations-1)) - len(str(n)))]) + str(n)] for n in range(rotations)] # Making a list of all the image files for extras that rotate through images

        self.rotation_interval = rotation_interval    # How often the images rotate (in seconds) (must be at least 1/session.fps)
        self.image_number = 0
        self.rotation_direction = "up"
        self.start_x = start_x  # The first grid x coordinate of the player's character where the image must be shown
        self.end_x = end_x      # The last grid x coordinate of the player's character where the image must be shown
        self.start_y = start_y  # The first grid y coordinate of the player's character where the image must be shown
        self.end_y = end_y      # The last grid y coordinate of the player's character where the image must be shown

    def display(self, room, player):
        # Checking if the player is within the coordinates at which the extra should be displayed
        in_x = (self.start_x is None and self.end_x is None) or self.start_x <= player.position.x <= self.end_x
        in_y = (self.start_y is None and self.end_y is None) or self.start_y <= player.position.y <= self.end_y
        show_extra = in_x and in_y

        if self.scroll_speed != 0:   # Changing the position of images that should scroll
            if self.scroll_axis == "x":
                self.x += float(self.scroll_speed)/session.fps
                if abs(self.x - self.original_x) >= self.width:
                    self.x = self.original_x
            elif self.scroll_axis == "y":
                if abs(self.y - self.original_y) >= self.height:
                    self.y = self.original_y
            else:
                raise ValueError(f"Invalid scroll axis '{self.scroll_axis}'.")

        if self.rotations > 1:  # Changing the image at the correct time for images that rotate
            if frame % int(self.rotation_interval*session.fps) == 0:
                if self.rotation_direction == "up":
                    self.image_number += 1
                    if self.image_number == self.rotations:
                        self.image_number -= 2
                        self.rotation_direction = "down"
                else:   # When rotation direction = "down"
                    self.image_number -= 1
                    if self.image_number == -1:
                        self.image_number = 1
                        self.rotation_direction = "up"
                self.image = self.images[self.image_number]

        if (show_extra and not self.image_name[0:9] == "NEGATIVES") or (not show_extra and self.image_name[0:9] == "NEGATIVES"):
            if self.image_name[0:9] == "TESSELATE":
                for horizontal in range(-1,(room.width//self.width) + 1):
                    for vertical in range(-1,(room.height//self.height) + 1):
                        self.image.display(room.x + self.x + horizontal*self.width, room.y + self.y + vertical*self.height)
            else:
                self.image.display(room.x + self.x, room.y + self.y)

            if self.scroll_speed != 0:   # Showing an extra copy of the image file for smooth scrolling
                if self.scroll_speed > 0:
                    if self.scroll_axis == "x":
                        self.image.display(room.x + self.x - room.width, room.y + self.y)
                    elif self.scroll_axis == "y":
                        self.image.display(room.x + self.x, room.y + self.y - room.height)
                else:   # When the scroll speed is negative
                    if self.scroll_axis == "x":
                        self.image.display(room.x + self.x + room.width, room.y + self.y)
                    elif self.scroll_axis == "y":
                        self.image.display(room.x + self.x, room.y + self.y + room.height)
            
            
class Exit(object):
    def __init__(self, coordinates, direction, room, position):
        self.coordinates = coordinates  # The grid coordinates of the exit square
        self.direction = direction      # The direction the player must be facing to walk through the exit
        self.room = room                # The room the exit leads to
        self.position = position        # The player's character's position in the new room    

            
class Room(object):
    def __init__(self, name, canvas, extras, square_size, grey_left, grey_up, grey_right, grey_down, blocked, exits):
        self.name = name    # The room name
        self.number = int(self.name[-1])    # The room number
        self.canvas = canvas    # Image file of the room. Will usually be a big canvas
        self.extras = extras    # A list of extra things that will be shown on top of characters in the room
        self.x = 0  # Canvas's screen x coordinate
        self.y = 0  # Canvas's screen y coordinate
        self.width = canvas.width
        self.height = canvas.height
        self.square_size = square_size      # this NEEDS to be a multiple/division of the screen size, so that zoom room is maintained across all resolutions
        # The amounts of inaccessible terrain at each side of the canvas
        self.grey_left = grey_left
        self.grey_up = grey_up
        self.grey_right = grey_right
        self.grey_down = grey_down
        self.max_coord = Coordinates(((self.width - (grey_left + grey_right))//self.square_size[0]) - 1, ((self.height - (grey_up + grey_down))//self.square_size[1]) - 1)
        self.blocked = blocked  # A list of squares which are blocked by terrain, such that the player cannot walk on them. Don't add squares higher than the max coordinate >_> (waste of space)
        self.exits = exits # A list of tuples, showing squares which cause the player to exit the current room, and which area's they lead to.

    def add_blocked(self, square):
        """Add a grid coordinate to the list of blocked squares for this room"""
        if square in self.blocked:
            raise ValueError(f"Square '{square}' is already blocked.")
        if not (0 <= square.x <= self.max_coord.x and 0 <= square.y <= self.max_coord.y):
            raise ValueError(f"Square '{square}' not in coordinate range of current room ({self.name})")
        self.blocked.append(square)

    def remove_blocked(self, square):
        """Remove a grid coordinate from the list of blocked squares for this room"""
        if square not in self.blocked:
            raise ValueError(f"Square '{square}' is not currently blocked.")
        if not (0 <= square.x <= self.max_coord.x and 0 <= square.y <= self.max_coord.y):
            raise ValueError(f"Square '{square}' not in coordinate range of current room ({self.name})")
        self.blocked.remove(square)

    def display_room(self, player):
        """Display everything that will be on screen for the room"""
        self.calculate_player_position(player)  # Calculating the player's and canvas's x and y coordinates on the screen
        self.canvas.display(self.x, self.y)   # Blitting the canvas first, so everything else goes on top of it

        for extra in self.extras:   # Showing the extras that go below the characters
            if extra.placement == "below":
                extra.display(self, player)

        for npc in npcs:    # Displaying all the npcs. This may require an order for bosses. Maybe the npcs list should be sorted by a "(display_)priority" attribute?
            if npc.room == self.number and not npc.dead:   # Only displaying npcs that are in the current room
                self.display_npc(npc)
        player.image.display(player.x, player.y)  # Displaying the player last, so they are always on top
        for name, ability in abilities.items():
            if ability.room == self.number and ability.displayed:
                self.display_npc(ability)

        for extra in self.extras: # Showing the extras that go on top of the characters
            if extra.placement == "above":
                extra.display(self, player)

    # Calculating the player's and canvas's position on the screen correctly (such that when the player is near the edge THEY move, not the canvas)
    def calculate_player_position(self, player):
        # Player's and canvas's x coordinates
        player.x = (screen_width - player.width)//2
        if self.grey_left + (self.square_size[0]*player.position.x) + ((self.square_size[0] - player.width)//2) < player.x:
            player.x = self.grey_left + (self.square_size[0]*player.position.x) + ((self.square_size[0] - player.width)//2)
            player.x = add_movement(self, player, "x", "image")
            self.x = 0
            # If the player is transistioning between a place where the player model would move and a place where the canvas would move
            if (player.x > (screen_width - player.width)//2
                and (not self.grey_left + (self.square_size[0]*player.position.x) + ((self.square_size[0] - player.width)//2) < player.x
                     or self.width > screen_width + self.square_size[0])):
                self.x -= player.x - (screen_width - player.width)//2
                player.x = (screen_width - player.width)//2
        elif screen_width - self.grey_right - (self.square_size[0]*(1 + self.max_coord.x - player.position.x)) + ((self.square_size[0] - player.width)//2) > player.x:
            player.x = screen_width - self.grey_right - (self.square_size[0]*(1 + self.max_coord.x - player.position.x)) + ((self.square_size[0] - player.width)//2)
            player.x = add_movement(self, player, "x", "image")
            self.x = -(self.width - screen_width)
            # If the player is transistioning between a place where the player model would move and a place where the canvas would move
            if (player.x < (screen_width - player.width)//2
                and (not screen_width - self.grey_right - (self.square_size[0]*(1 + self.max_coord.x - player.position.x)) + ((self.square_size[0] - player.width)//2) > player.x
                     or self.width > screen_width + self.square_size[0])):
                self.x += (screen_width - player.width)//2 - player.x
                player.x = (screen_width - player.width)//2
        else:
            self.x = -(self.grey_left + (self.square_size[0]*player.position.x) - ((screen_width - player.width)//2) + (self.square_size[0] - player.width)//2)
            self.x = add_movement(self, player, "x", "canvas")
            if self.x > 0:
                player.x -= self.x
                self.x = 0
            elif self.x < -(self.width - screen_width):
                player.x += -(self.width - screen_width) - self.x
                self.x = -(self.width - screen_width)

        # Player's and canvas's y coordinates
        player.y = (screen_height - player.height)//2
        if self.grey_up + self.square_size[1]*(player.position.y - 1) + (2*self.square_size[1] - player.height) < player.y:
            player.y = self.grey_up + self.square_size[1]*(player.position.y - 1) + (2*self.square_size[1] - player.height)
            player.y = add_movement(self, player, "y", "image")
            self.y = 0
            # If the player is transistioning between a place where the player model would move and a place where the canvas would move
            if (player.y > (screen_height - player.height)//2
                and (not self.grey_up + self.square_size[1]*(player.position.y - 1) + (2*self.square_size[1] - player.height) < player.y
                     or self.height > screen_height + self.square_size[1])):
                self.y -= player.y - (screen_height - player.height)//2
                player.y = (screen_height - player.height)//2
        elif screen_height - self.grey_down - (self.square_size[1]*(self.max_coord.y - player.position.y + 2)) + (2*self.square_size[1] - player.height) > player.y:
            player.y = screen_height - self.grey_down - (self.square_size[1]*(self.max_coord.y - player.position.y + 2)) + (2*self.square_size[1] - player.height)
            player.y = add_movement(self, player, "y", "image")
            self.y = -(self.height - screen_height)
            # If the player is transistioning between a place where the player model would move and a place where the canvas would move
            if (player.y < (screen_height - player.height)//2
                and (not screen_height - self.grey_down - (self.square_size[1]*(self.max_coord.y - player.position.y + 2)) + (2*self.square_size[1] - player.height) > player.y
                     or self.height > screen_height + self.square_size[1])):
                self.y += (screen_height - player.height)//2 - player.y
                player.y = (screen_height - player.height)//2
        else:
            self.y = -(self.grey_up + (self.square_size[1]*(player.position.y - 1)) - ((screen_height - player.height)//2) + (2*self.square_size[1] - player.height))
            self.y = add_movement(self, player, "y", "canvas")
            if self.y > 0:
                player.y -= self.y
                self.y = 0
            elif self.y < -(self.height - screen_height):
                player.y += -(self.height - screen_height) - self.y
                self.y = -(self.height - screen_height)

    # Displaying NPCs on the canvas (and screen if their coordinates are on the screen)
    def display_npc(self, npc):
        npc.x = self.grey_left + self.square_size[0]*npc.position.x + (self.square_size[0] - npc.width)//2 + self.x
        npc.y = self.grey_up + self.square_size[1]*(npc.position.y - 1) + (2*self.square_size[1] - npc.height) + self.y
        npc.x = add_movement(self, npc, "x", "image")
        npc.y = add_movement(self, npc, "y", "image")
        npc.image.display(npc.x, npc.y)
        

# IMAGE IMPORTING ----------------------------------------------------------------------------------
extra_images = {
    "sharedroom/lava_back_glow0": Image("sharedroom/lava_back_glow0.png"),
    "sharedroom/lava_back_glow1": Image("sharedroom/lava_back_glow1.png"),
    "sharedroom/lava_back_glow2": Image("sharedroom/lava_back_glow2.png"),
    "sharedroom/lava_back_glow3": Image("sharedroom/lava_back_glow3.png"),
    "sharedroom/lava_back_glow4": Image("sharedroom/lava_back_glow4.png"),
    "sharedroom/black_patches0": Image("sharedroom/black_patches0.png"),
    "sharedroom/black_patches1": Image("sharedroom/black_patches1.png"),
    # Room 0
    "room0/black_patches0": Image("room0/black_patches0.png"),
    "room0/black_patches1": Image("room0/black_patches1.png"),
    "room0/back": Image("room0/back.png"),
    "room0/front": Image("room0/front.png"),
    "room0/portal0": Image("room0/portal0.png"),
    "room0/portal1": Image("room0/portal1.png"),
    "room0/portal2": Image("room0/portal2.png"),
    "room0/portal3": Image("room0/portal3.png"),
    "room0/portal4": Image("room0/portal4.png"),
    "room0/portal5": Image("room0/portal5.png"),
    "room0/portal6": Image("room0/portal6.png"),
    "room0/portal7": Image("room0/portal7.png"),
    "room0/portal8": Image("room0/portal8.png"),
    "room0/portal9": Image("room0/portal9.png"),
    # Room 1
    "room1/barrier": Image("room1/barrier.png"),
    "room1/bottom": Image("room1/bottom.png"),
    "room1/bottom80": Image("room1/bottom80.png"),
    "room1/sides": Image("room1/sides.png"),
    "room1/star0": Image("room1/star0.png"),
    "room1/star1": Image("room1/star1.png"),
    "room1/star2": Image("room1/star2.png"),
    "room1/star3": Image("room1/star3.png"),
    "room1/star4": Image("room1/star4.png"),
    "room1/star5": Image("room1/star5.png"),
    "room1/star6": Image("room1/star6.png"),
    "room1/star7": Image("room1/star7.png"),
    "room1/star8": Image("room1/star8.png"),
    "room1/flux00": Image("room1/flux00.png"),
    "room1/flux01": Image("room1/flux01.png"),
    "room1/flux02": Image("room1/flux02.png"),
    "room1/flux03": Image("room1/flux03.png"),
    "room1/flux04": Image("room1/flux04.png"),
    "room1/flux05": Image("room1/flux05.png"),
    "room1/flux06": Image("room1/flux06.png"),
    "room1/flux07": Image("room1/flux07.png"),
    "room1/flux08": Image("room1/flux08.png"),
    "room1/flux09": Image("room1/flux09.png"),
    "room1/flux10": Image("room1/flux10.png"),
    "room1/flux11": Image("room1/flux11.png"),
    "room1/flux12": Image("room1/flux12.png"),
    # Room 2
    "room2/back": Image("room2/back.png"),
    "room2/barriers": Image("room2/barriers.png"),
    "room2/left_bottom_front1": Image("room2/left_bottom_front1.png"),
    "room2/left_bottom_front180": Image("room2/left_bottom_front180.png"),
    "room2/left_bottom_front2": Image("room2/left_bottom_front2.png"),
    "room2/left_bottom_front280": Image("room2/left_bottom_front280.png"),
    "room2/left_front1": Image("room2/left_front1.png"),
    "room2/left_front180": Image("room2/left_front180.png"),
    "room2/left_front2": Image("room2/left_front2.png"),
    "room2/left_front280": Image("room2/left_front280.png"),
    "room2/middle_front1": Image("room2/middle_front1.png"),
    "room2/middle_front180": Image("room2/middle_front180.png"),
    "room2/middle_front2": Image("room2/middle_front2.png"),
    "room2/middle_front280": Image("room2/middle_front280.png"),
    "room2/right_bottom_front": Image("room2/right_bottom_front.png"),
    "room2/right_bottom_front80": Image("room2/right_bottom_front80.png"),
    "room2/right_front": Image("room2/right_front.png"),
    "room2/right_front80": Image("room2/right_front80.png"),
    "room2/small_front1": Image("room2/small_front1.png"),
    "room2/small_front2": Image("room2/small_front2.png"),
    "room2/ruin": Image("room2/ruin.png"),
    "room2/farleft_sidewall": Image("room2/farleft_sidewall.png"),
    "room2/left_sidewall": Image("room2/left_sidewall.png"),
    "room2/middle_sidewall1": Image("room2/middle_sidewall1.png"),
    "room2/middle_sidewall2": Image("room2/middle_sidewall2.png"),
    "room2/right_sidewall": Image("room2/right_sidewall.png"),
    "room2/bottom_wall": Image("room2/bottom_wall.png"),
    "room2/bottom_wall80": Image("room2/bottom_wall80.png"),
    "room2/portal_burn": Image("room2/portal_burn.png"),
    "room2/portal_symbol": Image("room2/portal_symbol.png"),
    "room2/portal_symbol_slime": Image("room2/portal_symbol_slime.png"),
    "room2/book0": Image("room2/book0.png"),
    "room2/book1": Image("room2/book1.png"),
    "room2/book2": Image("room2/book2.png"),
    "room2/light00": Image("room2/light00.png"),
    "room2/light01": Image("room2/light01.png"),
    "room2/light02": Image("room2/light02.png"),
    "room2/light03": Image("room2/light03.png"),
    "room2/light04": Image("room2/light04.png"),
    "room2/light05": Image("room2/light05.png"),
    "room2/light06": Image("room2/light06.png"),
    "room2/light07": Image("room2/light07.png"),
    "room2/light08": Image("room2/light08.png"),
    "room2/light09": Image("room2/light09.png"),
    "room2/light10": Image("room2/light10.png"),
    "room2/light11": Image("room2/light11.png"),
    "room2/light12": Image("room2/light12.png"),
    "room2/light13": Image("room2/light13.png"),
    "room2/light14": Image("room2/light14.png"),
    "room2/light15": Image("room2/light15.png"),
    "room2/drop0": Image("room2/drop0.png"),
    "room2/drop1": Image("room2/drop1.png"),
    "room2/drop2": Image("room2/drop2.png"),
    "room2/drop3": Image("room2/drop3.png"),
    "room2/drop4": Image("room2/drop4.png"),
    "room2/drop5": Image("room2/drop5.png"),
    "room2/drop6": Image("room2/drop6.png"),
    # Room 3
    "room3/platform": Image("room3/platform.png")
}

# Loading dialogue images
dialogue = {
    "mysteriousbox": Image("dialogue/mysteriousbox.png"),
    "vincentbox": Image("dialogue/vincentbox.png"),
    "zaalbox": Image("dialogue/zaalbox.png"),
    "mysterious0": Image("dialogue/mysterious0.png"),
    "mysterious1": Image("dialogue/mysterious1.png"),
    "mysterious2": Image("dialogue/mysterious2.png"),
    "mysterious3": Image("dialogue/mysterious3.png"),
    "vincent0": Image("dialogue/vincent0.png"),
    "vincent1": Image("dialogue/vincent1.png"),
    "vincent2": Image("dialogue/vincent2.png"),
    "vincent3": Image("dialogue/vincent3.png"),
    "vincent4": Image("dialogue/vincent4.png"),
    "vincent5": Image("dialogue/vincent5.png"),
    "vincent6": Image("dialogue/vincent6.png"),
    "vincent7": Image("dialogue/vincent7.png"),
    "vincent8": Image("dialogue/vincent8.png"),
    "zaal0": Image("dialogue/zaal0.png"),
    "zaal1": Image("dialogue/zaal1.png"),
    "zaal2": Image("dialogue/zaal2.png"),
    "zaal3": Image("dialogue/zaal3.png"),
    "zaal4": Image("dialogue/zaal4.png"),
}

# Loading ability images
ability_images = {
    "firebolt": {
        "Vincent Slime": {
            "left": [Image("vincent/slime/firebolt/left" + str(n) + ".png") for n in range(12)],
            "up": [Image("vincent/slime/firebolt/up" + str(n) + ".png") for n in range(12)],
            "right": [Image("vincent/slime/firebolt/right" + str(n) + ".png") for n in range(12)],
            "down": [Image("vincent/slime/firebolt/down" + str(n) + ".png") for n in range(12)]
        }
    }
}

# Loading death images
death_images = {
    "Vincent Slime": [Image("vincent/slime/death" + str(n) + ".png") for n in range(12)],
    "Enemy Slime": [Image("enemy/slime/death" + str(n) + ".png") for n in range(10)],
    "Firebolt": [{direction: Image("firebolt/death/" + direction + str(n) + ".png") for direction in ["left", "up", "right", "down"]} for n in range(8)],
    "Inferno": [{direction: Image("inferno/death/" + direction + str(n) + ".png") for direction in ["left", "up", "right", "down"]} for n in range(11)],
}

# Loading tutorial images
tutorial = [Image("tutorial/tutorial" + str(n) + ".png") for n in range(13)]

# Loading spellbook images
spellbook_images = {
    "spellbook_default": Image("spellbook/spellbook_default.png"),
    "firebolt_uncharged": Image("spellbook/firebolt_uncharged.png"),
    "firebolt1": Image("spellbook/firebolt1.png")
    }

# Loading level up images
levelup_images = [Image("levelup/" + str(n) + ".png") for n in range(15)]

# Loading zaal images
zaal_images = {
    "health_back": Image("zaal/health_back.png"),
    "health": Image("zaal/health.png"),
    "health_icon": Image("zaal/health_icon.png"),
    "death": [Image("zaal/death" + str(n) + ".png") for n in range(12)],
    "zaal": [Image("zaal/zaal" + str(n) + ".png") for n in range(2)],
    "attack": [Image("zaal/attack" + str(n) + ".png") for n in range(19)]
}

credits_images = [Image("credits/credits" + str(n) + ".png", convert_alpha=False) for n in range(8)]

esc_exit = Image("esc_exit.png")
controls_page = Image("controls.png")
controls_page.blit(esc_exit, (0, 0))


# VIDEO IMPORTING ----------------------------------------------------------------------------------
introduction = VideoFileClip("../Video Files/introduction.mpg").subclip(0, 3)


# PROGRAM DISPLAY ----------------------------------------------------------------------------------
current = "main menu"
npcs = []   # A list of all currently loaded npcs. All Npc objects are appended to this list when they are initialised.
abilities = {}  # A dictionary of all currently loaded abilities
loot = Loot()
spells = [] # The characters unlocked spells
inventory = [] # The characters inventory
hud = Hud()
slime_chunk = Item("Slime Chunk", Image("hud/slime_chunk.png"), Image("loot/slime_chunk.png"))
number_drops = []   # The list of current number drops
menus = {"main menu": Menu("main", ["title"],
                           [["play"], ["options"], ["controls"], ["exit"]],
                           [(620, 605, 1300, 648), (620, 663, 1300, 706), (620, 717, 1300, 760), (620, 774, 1300, 817)],
                           ["saves menu", "options menu", "controls", "exit"], "sure quit?"),
         "options menu": Menu("options", ["headings", "apply reset", "sliders"],
                              [["SLIDER278"], ["SLIDER335"], ["SLIDER392"], ["SLIDER449"], ["windowed", "borderless", "fullscreen"],
                               ["800x600", "1024x768", "1152x864", "1280x720", "1280x768", "1280x1024", "1366x768", "1600x900", "1600x1024", "1680x1050", "1920x1080"],
                               ["SLIDER669"], ["subs_on", "subs_off"], ["damage_on", "damage_off"], ["apply", "reset"]],
                              [(123, 123, 123, 123), (123, 123, 123, 123), (123, 123, 123, 123), (123, 123, 123, 123), (123, 123, 123, 123), (123, 123, 123, 123), (123, 123, 123, 123), (123, 123, 123, 123), (123, 123, 123, 123), (123, 123, 123, 123)],
                              ["options menu", "options menu", "options menu", "options menu", "options menu", "options menu", "options menu", "options menu", "options menu", "options menu"],
                              "main menu", [50, 100, 100, 100, 1, 10, 100, 0, 0, 0]),
         "saves menu": Menu("saves", [],
                            [["slot0"], ["slot1"], ["slot2"], ["slot3"]],
                            [(525, 255, 1413, 386), (525, 433, 1413, 564), (525, 611, 1413, 742), (525, 789, 1413, 920)],
                            ["save0", "save1", "save2", "save3"], "main menu")}

# Extras that need to be displayed during cutscenes
portal = Extra("room0/portal0", "below", 790, 660, 0, 0, 10, 0.1)
star = Extra("room1/star0", "below", 0, 0, 0, 0, 9, 0.1)
flux = Extra("room1/flux00", "above", 0, 0, 0, 0, 13, 0.1)
book_item = Extra("room2/book0", "below", 3280, 1815, 0, 0, 3, 0.3)
book_light = Extra("room2/light00", "below", 3290, 1605, 0, 0, 16, 0.1)
placed_portal = Extra("room2/portal_symbol", "below", -1000, -1000)
drop = Extra("room2/drop0", "below", -1000, -1000, 0, 0, 7, 0.1)
slime_portal = Extra("room2/portal_symbol_slime", "below", -1000, -1000)
portal_burn = Extra("room2/portal_burn", "below", -1000, -1000)

rooms = [
    Room("Room 0", Image("room0/lava_back.png"),
         [Extra("sharedroom/lava_back_glow0", "below", 0, 1166, 0, 0, 5, 0.2),
          Extra("room0/black_patches0", "below", 0, 1166, 10, "x", 2, 1),
          Extra("room0/back", "below", 0, 0),
          portal,
          Extra("room0/front", "above", 0, 62)],
         (70, 70), 420, 420, 450, 330, [(7, 5)],
         [Exit(Coordinates(6, -1), "up", 1, Coordinates(11, 14)),
          Exit(Coordinates(7, -1), "up", 1, Coordinates(12, 14)),
          Exit(Coordinates(8, -1), "up", 1, Coordinates(13, 14))]),
    Room("Room 1", Image("room1/back.png"),
         [Extra("room1/barrier", "below", 55, 1054),
          Extra("room1/bottom", "above", 0, 1051, start_y=0, end_y=11),
          Extra("room1/bottom", "above", 0, 1051, start_x=11, end_x=13, start_y=12, end_y=15),
          Extra("room1/bottom80", "above", 0, 1051, start_x=0, end_x=10, start_y=12, end_y=14),
          Extra("room1/bottom80", "above", 0, 1051, start_x=14, end_x=24, start_y=12, end_y=14),
          Extra("room1/sides", "above", 0, 0)],
         (70, 70), 70, 280, 100, 50, [],
         [Exit(Coordinates(11, 15), "down", 0, Coordinates(6, 0)),
          Exit(Coordinates(12, 15), "down", 0, Coordinates(7, 0)),
          Exit(Coordinates(13, 15), "down", 0, Coordinates(8, 0)),
          Exit(Coordinates(11, -1), "up", 2, Coordinates(45, 32)),
          Exit(Coordinates(12, -1), "up", 2, Coordinates(46, 32)),
          Exit(Coordinates(13, -1), "up", 2, Coordinates(47, 32))]),
    Room("Room 2", Image("room2/lava_back.png"),
         [Extra("TESSELATEsharedroom/lava_back_glow0", "below", 0, 276, 0, 0, 5, 0.2),
          Extra("TESSELATEsharedroom/black_patches0", "below", 0, 276, 10, "x", 2, 1),
          Extra("room2/back", "below", 0, 0),
          Extra("room2/barriers", "below", 58, 764),
          Extra("room2/left_bottom_front1", "above", 44, 2166, start_y=0, end_y=24),
          Extra("room2/left_bottom_front1", "above", 44, 2166, start_x=11, end_x=107, start_y=25, end_y=30),
          Extra("room2/left_bottom_front1", "below", 44, 2166, start_y=31, end_y=32),
          Extra("room2/left_bottom_front1", "above", 44, 2166, start_x=0, end_x=10, start_y=25, end_y=30),
          Extra("room2/left_bottom_front2", "above", 1001, 2294, start_y=0, end_y=27),
          Extra("room2/left_bottom_front2", "above", 1001, 2294, start_x=0, end_x=13, start_y=28, end_y=29),
          Extra("room2/left_bottom_front2", "above", 1001, 2294, start_x=25, end_x=107, start_y=28, end_y=29),
          Extra("room2/left_bottom_front2", "below", 1001, 2294, start_y=30, end_y=32),
          Extra("room2/left_bottom_front280", "above", 1001, 2294, start_x=14, end_x=24, start_y=28, end_y=29),
          Extra("NEGATIVESroom2/left_front1", "above", 1185, 268, start_x=17, end_x=20, start_y=2, end_y=4),
          Extra("room2/left_front180", "above", 1185, 268, start_x=17, end_x=20, start_y=2, end_y=4),
          Extra("room2/left_front2", "above", 36, 1027, start_y=0, end_y=8),
          Extra("room2/left_front2", "above", 36, 1027, start_x=5, end_x=7, start_y=9, end_y=13),
          Extra("room2/left_front2", "above", 36, 1027, start_x=14, end_x=107, start_y=9, end_y=13),
          Extra("room2/left_front2", "below", 36, 1027, start_y=14, end_y=32),
          Extra("room2/left_front280", "above", 36, 1027, start_x=0, end_x=4, start_y=9, end_y=13),
          Extra("room2/left_front280", "above", 36, 1027, start_x=8, end_x=13, start_y=9, end_y=13),
          Extra("NEGATIVESroom2/middle_front1", "above", 2451, 696, start_x=34, end_x=44, start_y=4, end_y=8),
          Extra("room2/middle_front180", "above", 2451, 696, start_x=34, end_x=44, start_y=4, end_y=8),
          Extra("NEGATIVESroom2/middle_front2", "above", 3414, 789, start_x=48, end_x=54, start_y=7, end_y=8),
          Extra("room2/middle_front280", "above", 3414, 789, start_x=48, end_x=54, start_y=7, end_y=8),
          Extra("room2/right_bottom_front", "above", 6016, 1317, start_y=0, end_y=12),
          Extra("room2/right_bottom_front", "above", 6016, 1317, start_x=0, end_x=90, start_y=13, end_y=18),
          Extra("room2/right_bottom_front", "above", 6016, 1317, start_x=91, end_x=96, start_y=13, end_y=14),
          Extra("room2/right_bottom_front", "above", 6016, 1317, start_x=97, end_x=100, start_y=13, end_y=18),
          Extra("room2/right_bottom_front", "below", 6016, 1317, start_y=19, end_y=32),
          Extra("room2/right_bottom_front80", "above", 6016, 1317, start_x=91, end_x=96, start_y=15, end_y=18),
          Extra("room2/right_bottom_front80", "above", 6016, 1317, start_x=101, end_x=107, start_y=13, end_y=18),
          Extra("room2/right_front", "above", 6020, 363, start_x=0, end_x=86, start_y=0, end_y=9),
          Extra("room2/right_front", "above", 6020, 363, start_x=87, end_x=90, start_y=0, end_y=2),
          Extra("room2/right_front", "above", 6020, 363, start_x=91, end_x=107, start_y=0, end_y=9),
          Extra("room2/right_front", "below", 6020, 363, start_y=10, end_y=32),
          Extra("room2/right_front80", "above", 6020, 363, start_x=87, end_x=90, start_y=3, end_y=9),
          Extra("room2/small_front1", "above", 2134, 1062),
          Extra("room2/small_front2", "below", 7278, 1822),
          Extra("room2/ruin", "below", 212, 1327),
          Extra("room2/farleft_sidewall", "above", 0, 65),
          Extra("room2/left_sidewall", "above", 1175, 673),
          Extra("room2/middle_sidewall1", "above", 2450, 1217),
          Extra("room2/middle_sidewall2", "above", 3954, 1218),
          Extra("room2/right_sidewall", "above", 7620, 20),
          Extra("room2/bottom_wall", "above", 0, 2183, start_y=0, end_y=27),
          Extra("room2/bottom_wall", "above", 0, 2183, start_x=45, end_x=47, start_y=28, end_y=32),
          Extra("room2/bottom_wall80", "above", 0, 2183, start_x=0, end_x=44, start_y=28, end_y=32),
          Extra("room2/bottom_wall80", "above", 0, 2183, start_x=48, end_x=107, start_y=28, end_y=32)],
         (70, 70), 70, 420, 50, 20,
         [(22, 0), (85, 0)]
         + [(x, 1) for x in range(22, 86)]
         + [(22, 2), (23, 2)]
         + [(x, 5) for x in range(16, 21)]
         + [(x, 6) for x in range(21, 31)]
         + [(x, 6) for x in range(60, 86)]
         + [(87+s, 5+s) for s in range(5)]
         + [(86, 5), (30, 7), (30, 8), (60, 7), (60, 8)]
         + [(x, 9) for x in range(31, 45)]
         + [(x, 9) for x in range(48, 60)]
         + [(16, y) for y in range(6, 13)]
         + [(44, y) for y in range(10, 15)]
         + [(48, y) for y in range(10, 15)]
         + [(90, y) for y in range(10, 19)]
         + [(x, 13) for x in range(5)]
         + [(x, 13) for x in range(8, 16)]
         + [(4, 14), (3, 15), (3, 16), (3, 17), (2, 17)]
         + [(15, y) for y in range(14, 19)]
         + [(x, 18) for x in range(16, 22)]
         + [(x, 19) for x in range(22, 35)]
         + [(x, 19) for x in range(91, 104)]
         + [(105, 19), (106, 19), (107, 19), (103, 20),
            (105, 20), (105, 21), (105, 22), (104, 22),
            (100, 20), (100, 21), (99, 21), (98, 21),
            (97, 22), (97, 23), (97, 24)]
         + [(96, y) for y in range(25, 33)]
         + [(x, 30) for x in range(12)]
         + [(x, 30) for x in range(13, 28)]
         + [(14, 31), (13, 32), (25, 31), (25, 32)]
         + [(35, y) for y in range(16, 33)]
         + [(57, y) for y in range(16, 33)]
         + [(x, 15) for x in range(36, 45)]
         + [(x, 15) for x in range(48, 57)],
         [Exit(Coordinates(45, 33), "down", 1, Coordinates(11, 0)),
          Exit(Coordinates(46, 33), "down", 1, Coordinates(12, 0)),
          Exit(Coordinates(47, 33), "down", 1, Coordinates(13, 0))]),
    Room("Room 3", Image("room3/background.png"),
         [Extra("TESSELATEsharedroom/lava_back_glow0", "below", 0, 0, 0, 0, 5, 0.2),
          Extra("TESSELATEsharedroom/black_patches0", "below", 0, 0, 10, "x", 2, 1),
          Extra("room3/platform", "below", 0, 0)],
         (70, 70), 280, 140, 200, 210,
         [(x, 0) for x in range(6)]
         + [(20, y) for y in range(6, 10)]
         + [(x, 10) for x in range(16, 20)],
         [])
    ]


current_room = rooms[0]
vincent = Player("Vincent Human", 4, Coordinates(7, 7), "down", 15, 0, 0, 1000, 1000)
mean_slime = Npc("Enemy Slime", 6, Coordinates(0, 4), "right", 15, -1, 50, 80, 500, 500)
firebolt = Ability("Firebolt", 6, Coordinates(0, 0), "right", 45, 2, 100, 2, 10, icon_image=Image("hud/firebolt.png"), icon_cooldown_image=Image("hud/firebolt_cooldown.png"))
inferno = Ability("Inferno", 12, Coordinates(0, 0), "down", 90, 3, 200, 2, 10)
inferno.unlocked = True
inferno.dead = True

# Initialising screen/window related variables
frame = 1   # Storing the current frame as a variable

# Program window while loop
while session.is_running:
    session.loop()

    if frame == 1:
        introduction.preview()

    # elif introduction.get_busy():   # Checking to see that the introduction video hasn't stopped playing for whatever reason
    #     if session.keys.escape or session.keys.space or session.keys.enter or session.keys.numpad_enter:
    #         introduction.stop()
            
    else:
        if current[-4:] == "menu":
            menus[current].display()
            menus[current].change_selection()
            menus[current].change_settings()
            if not menus[current].check_action():
                menus[current].check_escape()
            # Changing the volume levels according to what the option menu says
            session.audio.master_volume = menus["options menu"].settings[0]
            session.audio.sound_volume = menus["options menu"].settings[1]
            session.audio.music_volume = menus["options menu"].settings[2]
            session.audio.voice_volume = menus["options menu"].settings[3]
                
        elif current == "controls":
            menus["main menu"].background.display(0, 0)
            controls_page.display(0, 0)
            
            if session.keys.escape or session.keys.backspace:
                current = "main menu"
                
        elif current[0:4] == "save":
            save = Save(current[4])
            if not save.is_empty:
                current_room = rooms[save.room_number]
                save.set_player_attributes(vincent)
                cutscene_played = save.cutscene_played
                menus["options menu"].settings = save.settings
            current = "in game"
        
        elif current[0:8] == "cutscene":
            cutscene_time = session.uptime - cutscene_start_time
            if cutscene_time < 1:                
                vincent.change_image()
            if current[8] == "0":
                if cutscene_time < 3:
                    session.screen.fill((0, 0, 0))
                elif cutscene_time < 5:
                    if not session.audio.sound.is_playing:
                        session.audio.sound.play(AudioClip("thunder.ogg"))
                        session.audio.sound.play(AudioClip("portal.ogg", 0.1), loop=True)
                    session.screen.fill((0, 0, 0))
                    portal.display(current_room, vincent)
                    fade_screen.fill((255, 255, 255, 255*(1-0.5*(cutscene_time-3))))
                    session.screen.blit(fade_screen, (0, 0))
                elif cutscene_time < 10:
                    portal.display(current_room, vincent)
                    if not display_dialogue("vincent", 0):
                        cutscene_start_time = session.uptime - 10
                elif cutscene_time < 12:
                    if len(session.audio.sound.currently_playing) < 2:
                        session.audio.sound.play(AudioClip("thunder.ogg"))
                    current_room.display_room(vincent)
                    fade_screen.fill((255, 255, 255, 255*(1-0.5*(cutscene_time-10))))
                    session.screen.blit(fade_screen, (0, 0))
                elif cutscene_time < 17:
                    current_room.display_room(vincent)
                    if not display_dialogue("vincent", 1):
                        cutscene_start_time = session.uptime - 17
                elif cutscene_time < 10017:
                    current_room.display_room(vincent)
                    tutorial[0].display(0, 0)
                    if session.keys.space or session.keys.enter or session.keys.numpad_enter:
                        cutscene_start_time = session.uptime - 10017
                else:
                    cutscene_played[0] = True
                    current = "in game"
            
            elif current[8] == "1":
                current_room.display_room(vincent)
                if cutscene_time < 10:
                    if not display_dialogue("vincent", 1):
                        cutscene_start_time = session.uptime - 10
                elif cutscene_time < 20:
                    if not display_dialogue("mysterious", 0):
                        cutscene_start_time = session.uptime - 20
                elif cutscene_time < 30:
                    if not display_dialogue("mysterious", 1):
                        cutscene_start_time = session.uptime - 30
                elif cutscene_time < 40:
                    if not display_dialogue("vincent", 2):
                        cutscene_start_time = session.uptime - 40
                elif cutscene_time < 50:
                    if not display_dialogue("vincent", 3):
                        cutscene_start_time = session.uptime - 50
                elif cutscene_time < 60:
                    if not display_dialogue("mysterious", 2):
                        cutscene_start_time = session.uptime - 60
                elif cutscene_time < 62.4:
                    if not coordinates_set:                        
                        star.x += 70*(vincent.position.x - 12)
                        flux.x += 70*(vincent.position.x - 12)
                        coordinates_set = True
                    star.display(current_room, vincent)
                    vincent.image.display(vincent.x, vincent.y)
                    current_room.extras[5].display(current_room, vincent)
                    if cutscene_time > 61 and not session.audio.sound.is_playing:
                        session.audio.sound.play(AudioClip("transform.ogg"))
                elif cutscene_time < 63.7:                
                    star.display(current_room, vincent)
                    vincent.image.display(vincent.x, vincent.y)
                    flux.display(current_room, vincent)                    
                    current_room.extras[5].display(current_room, vincent)
                    fade_screen.fill((151, 0, 0, int(255*((1/1.3)*(cutscene_time-62.4)))))
                    session.screen.blit(fade_screen, (0, 0))
                elif cutscene_time < 64:
                    session.screen.fill((151, 0, 0))
                    if vincent.form == "human":
                        vincent.transform()
                elif cutscene_time < 66:
                    vincent.image.display(vincent.x, vincent.y)                    
                    current_room.extras[5].display(current_room, vincent)
                    fade_screen.fill((151, 0, 0, int(255*(1-0.5*(cutscene_time-64)))))
                    session.screen.blit(fade_screen, (0, 0))
                elif cutscene_time < 76:
                    if not display_dialogue("mysterious", 0):
                        cutscene_start_time = session.uptime - 76
                elif cutscene_time < 86:
                    if not display_dialogue("vincent", 4):
                        cutscene_start_time = session.uptime - 86
                elif cutscene_time < 96:
                    if not display_dialogue("mysterious", 3):
                        cutscene_start_time = session.uptime - 96
                elif cutscene_time < 106:
                    if not display_dialogue("vincent", 5):
                        cutscene_start_time = session.uptime - 106
                elif cutscene_time < 116:
                    if not display_dialogue("mysterious", 0):
                        cutscene_start_time = session.uptime - 116
                else:
                    session.audio.music.play(AudioClip("main.ogg", 0.5))
                    coordinates_set = False
                    cutscene_played[1] = True
                    current = "in game"
                
            elif current[8] == "2":
                current_room.display_room(vincent)
                if cutscene_time < 2:
                    if not session.audio.sound.is_playing:
                        session.audio.sound.play(AudioClip("thunder.ogg"))
                        current_room.extras.append(book_item)
                        current_room.extras.append(book_light)
                    fade_screen.fill((255, 255, 255, 255*(1-0.5*(cutscene_time))))
                    session.screen.blit(fade_screen, (0, 0))
                elif cutscene_time < 10002:
                    tutorial[1].display(0, 0)
                    if session.keys.space or session.keys.enter or session.keys.numpad_enter:
                        cutscene_start_time = session.uptime - 10002
                else:
                    cutscene_played[2] = True
                    current = "in game"
            
            elif current[8] == "3":
                current_room.display_room(vincent)
                if cutscene_time < 10000:
                    display_spellbook()
                    tutorial[2].display(0, 0)
                    if session.keys.space or session.keys.enter or session.keys.numpad_enter:
                        cutscene_start_time = session.uptime - 10000
                elif cutscene_time < 20000:
                    hud.display(spells, inventory, vincent)
                    firebolt.icon_image.display(760, 1029)
                    display_spellbook()
                    if session.keys.escape or session.keys.backspace:
                        cutscene_start_time = session.uptime - 20000
                elif cutscene_time < 30000:
                    tutorial[3].display(0, 0)
                    if session.keys.space or session.keys.enter or session.keys.numpad_enter:
                        cutscene_start_time = session.uptime - 30000
                elif cutscene_time < 40000:
                    tutorial[4].display(0, 0)
                    if session.keys.space or session.keys.enter or session.keys.numpad_enter:
                        cutscene_start_time = session.uptime - 40000
                elif cutscene_time < 50000:
                    tutorial[5].display(0, 0)
                    if session.keys.space or session.keys.enter or session.keys.numpad_enter:
                        cutscene_start_time = session.uptime - 50000
                elif cutscene_time < 60000:
                    tutorial[6].display(0, 0)
                    if session.keys.space or session.keys.enter or session.keys.numpad_enter:
                        cutscene_start_time = session.uptime - 60000
                elif cutscene_time < 70000:
                    tutorial[7].display(0, 0)
                    if session.keys.space or session.keys.enter or session.keys.numpad_enter:
                        cutscene_start_time = session.uptime - 70000
                elif cutscene_time < 80000:
                    hud.display(spells, inventory, vincent)
                    firebolt.icon_image.display(760, 1029)
                    tutorial[8].display(0, 0)
                    if session.keys.space or session.keys.enter or session.keys.numpad_enter:
                        cutscene_start_time = session.uptime - 80000
                else:
                    hud.display(spells, inventory, vincent)
                    firebolt.icon_image.display(760, 1029)
                    show_hud = True
                    firebolt.unlocked = True
                    spells.append(firebolt)
                    cutscene_played[3] = True
                    current = "in game"
            
            elif current[8] == "4":
                current_room.display_room(vincent)
                if cutscene_time < 25:
                    if not display_dialogue("vincent", 6):
                        cutscene_start_time = session.uptime - 25
                elif cutscene_time < 10025:
                    tutorial[9].display(0, 0)
                    if session.keys.space or session.keys.enter or session.keys.numpad_enter:
                        cutscene_start_time = session.uptime - 10025
                else:
                    vincent.exp += 35
                    number_drop("exp", vincent, 35)
                    mean_slime.room = 2
                    mean_slime.moves = ["right" for n in range(100)] + ["down" for n in range(10)]
                    cutscene_played[4] = True
                    current_room.extras.append(placed_portal)
                    current = "in game"
            
            elif current[8] == "5":
                current_room.display_room(vincent)
                if cutscene_time < 10000:
                    tutorial[10].display(0, 0)
                    if session.keys.space or session.keys.enter or session.keys.numpad_enter:
                        cutscene_start_time = session.uptime - 10000
                else:
                    cutscene_played[5] = True
                    current = "in game"
            
            elif current[8] == "7":
                current_room.display_room(vincent)
                firebolt.exist(current_room)
                if cutscene_time < 2:
                    if not session.audio.sound.is_playing:
                        session.audio.sound.play(AudioClip("thunder.ogg"))
                        session.audio.sound.play(AudioClip("portal.ogg", 0.1), loop=True)
                        current_room.extras.remove(slime_portal)
                        current_room.extras.remove(placed_portal)
                        current_room.extras.append(portal_burn)
                        current_room.extras.append(portal)
                        portal.x = placed_portal.x - 87
                        portal_burn.x = placed_portal.x - 111
                        portal.y = placed_portal.y - 84
                        portal_burn.y = placed_portal.y - 119
                        current_room.exits.append(Exit(Coordinates(portal_x, portal_y), "left", 3, Coordinates(5, 5)))
                        current_room.exits.append(Exit(Coordinates(portal_x, portal_y), "up", 3, Coordinates(5, 5)))
                        current_room.exits.append(Exit(Coordinates(portal_x, portal_y), "right", 3, Coordinates(5, 5)))
                        current_room.exits.append(Exit(Coordinates(portal_x, portal_y), "down", 3, Coordinates(5, 5)))
                    fade_screen.fill((255, 255, 255, 255*(1-0.5*cutscene_time)))
                    session.screen.blit(fade_screen, (0, 0))
                else:
                    cutscene_played[7] = True
                    current = "in game"
            
            elif current[8] == "8":
                current_room.display_room(vincent)                
                zaal_images["zaal"][(frame%6)//3].display(current_room.x + 840, current_room.y + 71)
                if cutscene_time < 2:
                    if not session.audio.sound.is_playing:
                        session.audio.sound.play(AudioClip("thunder.ogg"))
                    fade_screen.fill((255, 255, 255, int(255*(1-0.5*cutscene_time))))
                    session.screen.blit(fade_screen, (0, 0))
                elif cutscene_time < 10:                    
                    if not display_dialogue("vincent", 1):
                        cutscene_start_time = session.uptime - 10
                elif cutscene_time < 25:
                    if not display_dialogue("zaal", 0):
                        cutscene_start_time = session.uptime - 25
                elif cutscene_time < 40:
                    if not display_dialogue("vincent", 7):
                        cutscene_start_time = session.uptime - 40
                elif cutscene_time < 50:
                    if not display_dialogue("zaal", 1):
                        cutscene_start_time = session.uptime - 50
                elif cutscene_time < 65:
                    if not display_dialogue("zaal", 2):
                        cutscene_start_time = session.uptime - 65
                elif cutscene_time < 75:
                    if not display_dialogue("vincent", 8):
                        cutscene_start_time = session.uptime - 75
                elif cutscene_time < 100:
                    if not display_dialogue("zaal", 3):
                        cutscene_start_time = session.uptime - 100
                elif cutscene_time < 125:
                    if not display_dialogue("zaal", 4):
                        cutscene_start_time = session.uptime - 125
                else:
                    session.audio.music.play(AudioClip("boss.ogg", 0.5))
                    firebolt.room = 3
                    cutscene_played[8] = True
                    current = "in game"
                    
            elif current[8] == "9":
                current_room.display_room(vincent)
                if cutscene_time < 2:
                    if not session.audio.sound.is_playing:
                        session.audio.sound.play(AudioClip("thunder.ogg"))
                    fade_screen.fill((255, 255, 255, 255*(1-0.5*(cutscene_time))))
                    session.screen.blit(fade_screen, (0, 0))
                else:
                    current = "credits"
            
        elif current == "credits":
            cutscene_time = session.uptime - cutscene_start_time
            if cutscene_time < 12.0/session.fps:
                current_room.display_room(vincent)
                zaal_images["death"][int(cutscene_time*session.fps)].display(current_room.x + 840, current_room.y + 71)
            elif cutscene_time < 5:
                current_room.display_room(vincent)
                fade_screen.fill((0, 0, 0, 51*cutscene_time))
                session.screen.blit(fade_screen, (0, 0))
            else:
                credits_images[7].display(0, 0)
                if cutscene_time < 7:
                    credits_images[0].set_alpha(127.5*(cutscene_time-5))
                    credits_images[0].display(0, 0)
                elif cutscene_time < 10:
                    credits_images[0].display(0, 0)
                elif cutscene_time < 12:
                    credits_images[0].set_alpha(255*(1-0.5*(cutscene_time-10)))
                    credits_images[0].display(0, 0)
                    
                elif cutscene_time < 14:
                    credits_images[1].set_alpha(127.5*(cutscene_time-12))
                    credits_images[1].display(0, 0)
                elif cutscene_time < 17:
                    credits_images[1].display(0, 0)
                elif cutscene_time < 19:
                    credits_images[1].set_alpha(255*(1-0.5*(cutscene_time-17)))
                    credits_images[1].display(0, 0)
                    
                elif cutscene_time < 21:
                    credits_images[2].set_alpha(127.5*(cutscene_time-19))
                    credits_images[2].display(0, 0)
                elif cutscene_time < 24:
                    credits_images[2].display(0, 0)
                elif cutscene_time < 26:
                    credits_images[2].set_alpha(255*(1-0.5*(cutscene_time-24)))
                    credits_images[2].display(0, 0)
                    
                elif cutscene_time < 28:
                    credits_images[3].set_alpha(127.5*(cutscene_time-26))
                    credits_images[3].display(0, 0)
                elif cutscene_time < 31:
                    credits_images[3].display(0, 0)
                elif cutscene_time < 33:
                    credits_images[3].set_alpha(255*(1-0.5*(cutscene_time-31)))
                    credits_images[3].display(0, 0)
                    
                elif cutscene_time < 35:
                    credits_images[4].set_alpha(127.5*(cutscene_time-33))
                    credits_images[4].display(0, 0)
                elif cutscene_time < 38:
                    credits_images[4].display(0, 0)
                elif cutscene_time < 40:
                    credits_images[4].set_alpha(255*(1-0.5*(cutscene_time-38)))
                    credits_images[4].display(0, 0)
                    
                elif cutscene_time < 42:
                    credits_images[5].set_alpha(127.5*(cutscene_time-40))
                    credits_images[5].display(0, 0)
                elif cutscene_time < 45:
                    credits_images[5].display(0, 0)
                elif cutscene_time < 47:
                    credits_images[5].set_alpha(255*(1-0.5*(cutscene_time-45)))
                    credits_images[5].display(0, 0)
                    
                elif cutscene_time < 49:
                    credits_images[6].set_alpha(127.5*(cutscene_time-47))
                    credits_images[6].display(0, 0)
                else:
                    credits_images[6].display(0, 0)
                    if session.keys.space or session.keys.enter or session.keys.numpad_enter:
                        session.audio.stop()
                        current = "main menu"   #(maybe), prolly go to credits isnt it
        
        elif current == "dead":
            cutscene_time = session.uptime - cutscene_start_time
            if cutscene_time < 5:
                current_room.display_room(vincent)
                fade_screen.fill((0, 0, 0, 51*cutscene_time))
                session.screen.blit(fade_screen, (0, 0))
            else:
                current = "saves menu"             
                    
        elif current == "in game":
            if not cutscene_played[0]:
                cutscene_start_time = session.uptime
                current = "cutscene0"
            elif not cutscene_played[1] and vincent.room == 1 and vincent.position.y < 7 and vincent.movement_cooldown == 0:
                cutscene_start_time = session.uptime
                current = "cutscene1"
            elif not cutscene_played[2] and vincent.room == 2 and vincent.position.y < 26 and vincent.movement_cooldown == 0:
                cutscene_start_time = session.uptime
                current = "cutscene2"
            elif not cutscene_played[8] and vincent.room == 3:
                cutscene_start_time = session.uptime
                current = "cutscene8"
            else:
                vincent.check_death()
                vincent.die()
                firebolt.exist(current_room)
                if not loot.is_displaying:
                    vincent.change_orientation()
                    vincent.change_position(current_room)
                    vincent.check_exit(current_room)

                    if mean_slime.room == current_room.number:
                        mean_slime.check_death()
                        mean_slime.die(kill=True)
                        if vincent.alive:
                            mean_slime.find_route(current_room, vincent.position)
                        else:
                            mean_slime.find_route(current_room, (vincent.position.x-10, vincent.position.y))
                        mean_slime.change_orientation()
                        mean_slime.change_position(current_room)
                        mean_slime.change_image()
                        mean_slime.check_collision(vincent)

                if vincent.dead:
                    current = "dead"

                vincent.change_image()

                current_room.display_room(vincent)

                if current_room.number == 3 and not cutscene_played[8]:
                    session.screen.fill((0, 0, 0))

                if current_room.number == 3 and cutscene_played[8] and vincent.alive:
                    inferno.exist(current_room)
                    inferno.use(vincent)
                    inferno.cast(vincent)
                    if zaal_animation > 0:
                        zaal_animation -= 1
                        zaal_images["attack"][18-zaal_animation].display(current_room.x + 840, current_room.y + 71)
                    else:
                        zaal_images["zaal"][(frame % 6)//3].display(current_room.x + 840, current_room.y + 71)
                    zaal_images["health_back"].display(69*(screen_width/1920.0), 80*(screen_height/1080.0))
                    zaal_images["health"].display(69*(screen_width/1920.0), 80*(screen_height/1080.0), area=(0, 0,zaal_life, 52))
                    zaal_images["health_icon"].display(1786, 0)

                    if firebolt.position in [(10, 2), (11, 2), (12, 2), (10, 3), (11, 3), (12, 3)] and firebolt.alive:
                        damage_dealt = int(firebolt.damage*(0.9 + 0.2*random.random()))
                        zaal_life -= damage_dealt
                        number_drop("damage", firebolt, damage_dealt)
                        firebolt.alive = False

                    if zaal_life <= 0:
                        cutscene_start_time = session.uptime
                        session.audio.stop()
                        current_room.extras.append(portal)
                        portal.x = 900
                        portal.y = 600
                        current = "cutscene9"

                if loot.is_displaying:
                    if not loot.display(inventory):
                        loot.is_displaying = False
                elif session.keys.escape and not show_spellbook:    # Opening the in game options menu upon escape being pressed
                    current = "in game options menu"

                if show_hud:
                    hud.display(spells, inventory, vincent)

                # Showing number drops
                for index in range(len(number_drops)):
                    number_drops[index][1] = display_number_drop(number_drops[index])

                for item in number_drops:
                    if item[1] < item[4]-90:
                        number_drops.remove(item)

                if show_spellbook:
                    display_spellbook()
                    if session.mouse.is_in(748, 499, 825, 576):
                        tutorial[12].display(0, 0)
                        if session.mouse.left and cutscene_played[5] and not cutscene_played[6] and vincent.skill_points > 0:
                            vincent.skill_points -= 1
                            cutscene_played[6] = True
                    elif session.mouse.is_in(579, 428, 656, 505):
                        tutorial[11].display(0, 0)
                    if session.keys.escape or session.keys.backspace:
                        show_spellbook = False

                if vincent.exp >= 100 and not levelling_up:
                    vincent.exp -= 100
                    vincent.level += 1
                    vincent.skill_points += 1
                    levelling_up = True

                if levelling_up:
                    if levelup_frame < 22:
                        levelup_images[levelup_frame//2].display(0, 0)
                    elif levelup_frame < 52:
                        levelup_images[11].display(0, 0)
                    elif levelup_frame < 58:
                        levelup_images[(levelup_frame-28)//2].display(0, 0)
                    else:
                        levelup_frame = 0
                        levelling_up = False
                    levelup_frame += 1

                if not cutscene_played[5] and vincent.level == 2 and not levelling_up:
                    cutscene_start_time = session.uptime
                    current = "cutscene5"

                if mean_slime.dead and not drop in rooms[2].extras and slime_chunk not in inventory and not slime_portal in rooms[2].extras:
                    current_room.extras.append(drop)
                    drop.x = current_room.grey_left + current_room.square_size[0]*mean_slime.position.x - 180
                    drop.y = current_room.grey_up + current_room.square_size[1]*mean_slime.position.y - 130
                    loot.items[0] = slime_chunk

                if not loot and drop in current_room.extras:
                    current_room.extras.remove(drop)
                    mean_slime.position = Coordinates(-10,-10)

                if session.keys.tab and not show_spellbook:
                    show_spellbook = True

                if session.keys.e:
                    if not cutscene_played[3]:
                        if is_interactable(Coordinates(46, 20)):
                            current_room.extras.remove(book_item)
                            current_room.extras.remove(book_light)
                            cutscene_start_time = session.uptime
                            current = "cutscene3"
                    elif not cutscene_played[4]:
                        if is_interactable(Coordinates(104, 25)):
                            cutscene_start_time = session.uptime
                            current = "cutscene4"
                    elif drop in current_room.extras:
                        if is_interactable(mean_slime.position):
                            loot.is_displaying = True
                    elif slime_chunk in inventory and is_interactable(Coordinates(portal_x, portal_y)):
                        current_room.extras.append(slime_portal)
                        inventory.remove(slime_chunk)
                        slime_portal.x = placed_portal.x
                        slime_portal.y = placed_portal.y

                if slime_portal in rooms[2].extras and firebolt.position == Coordinates(portal_x, portal_y) and firebolt.alive and not cutscene_played[7]:
                    firebolt.alive = False
                    cutscene_start_time = session.uptime
                    current = "cutscene7"

                if session.keys.one or session.keys.numpad_one:
                    firebolt.use(vincent)

                if session.keys.r and cutscene_played[4] and slime_portal not in rooms[2].extras:  # Creating a portal
                    if vincent.orientation == "left" and not (vincent.position.x-1, vincent.position.y) in (current_room.blocked + [(104, 25)]) and not vincent.position.x-1 < 0:
                        portal_x = vincent.position.x-1
                        portal_y = vincent.position.y
                        placed_portal.x = current_room.grey_left + current_room.square_size[0]*portal_x - 27
                        placed_portal.y = current_room.grey_up + current_room.square_size[1]*portal_y - 28
                    elif vincent.orientation == "up" and not (vincent.position.x, vincent.position.y-1) in (current_room.blocked + [(104, 25)]) and not vincent.position.y-1 < 0:
                        portal_y = vincent.position.y-1
                        portal_x = vincent.position.x
                        placed_portal.x = current_room.grey_left + current_room.square_size[0]*portal_x - 27
                        placed_portal.y = current_room.grey_up + current_room.square_size[1]*portal_y - 28
                    elif vincent.orientation == "right" and not (vincent.position.x+1, vincent.position.y) in (current_room.blocked + [(104, 25)]) and not vincent.position.x+1 > current_room.max_coord.x:
                        portal_x = vincent.position.x+1
                        portal_y = vincent.position.y
                        placed_portal.x = current_room.grey_left + current_room.square_size[0]*portal_x - 27
                        placed_portal.y = current_room.grey_up + current_room.square_size[1]*portal_y - 28
                    elif vincent.orientation == "down" and not (vincent.position.x, vincent.position.y+1) in (current_room.blocked + [(104, 25)]) and not vincent.position.y+1 > current_room.max_coord.y:
                        portal_y = vincent.position.y+1
                        portal_x = vincent.position.x
                        placed_portal.x = current_room.grey_left + current_room.square_size[0]*portal_x - 27
                        placed_portal.y = current_room.grey_up + current_room.square_size[1]*portal_y - 28
            
        elif current == "exit":
            session.is_running = False

    frame += 1  # Incrementing the current frame
    pygame.display.flip()   # Updating the screen at the end of blitting
    session.clock.tick(session.fps)          # Setting session.fps limit

# Closing and saving the program
try:
    save.save(current, current_room.number, cutscene_played, vincent, menus["options menu"].settings)
except NameError:
    pass

pygame.quit()
