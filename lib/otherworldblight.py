import ctypes

from lib.keys import Keys
from lib.mouse import Mouse

import moviepy
from moviepy.editor import VideoFileClip


# Defining the error logging function
def log(error, error_message):
    try:
        error_log = open("../log.txt", "a")
        try:
            error_log.write(str(datetime.datetime.utcnow())[0:19] + " - " + error_message + ": " + str(error) + "\n")
        except:
            error_log.write(str(datetime.datetime.utcnow())[0:19] + " - " + error_message + ": Details Unknown\n")
        error_log.close()
    except Exception as error:  # Likely never happens as no reliance on file_directory anymore - remove.
        ctypes.windll.user32.MessageBoxW(0, "An error has occurred:\n\n    " + error_message + ".\n\n\nThis error occurred very early during game initialisation and could not be logged.", "Error", 1)
        raise

    global ongoing              # Also temporary
    ongoing = False             # Also temporary
    if False and pygame.display.get_surface() is not None and error_message != "Failed to display error message":
        error_time = 3*fps
    # add some error sound to play here
    else:   # Creating a window to inform the user that error has occurred
        ctypes.windll.user32.MessageBoxW(0, "An error has occurred:\n\n    " + error_message + ".\n\n\nPlease check log.txt for details.", "Error", 1)
        raise
    
        
### Defining the load function for loading other files
def load(file_name):
    global error
    try:
        file_type = ""
        length = len(file_name)
        for index in range(length):
            if file_name[length-index-1] == ".":
                file_type = file_name[length-index:length]
        if file_type == "":
            error = "null file type [coding syntax error]"
            log(error, "Missing file extension")
    except Exception as error:
        log(error, "Failed to determine file type of \"" + file_name + "\"")
        
    try:        
        if file_type == "png":
            return pygame.image.load("../images/" + file_name).convert_alpha()
        elif file_type == "ogg":
            pygame.mixer.music.load("../Sound Files/" + file_name)
        elif file_type == "mpg":
            return VideoFileClip("../Video Files/" + file_name).subclip(0, 3)
        else:
            raise Exception("Invalid file type")
    except Exception as error:
        log(error, "Failed to load file: \"" + file_name + "\"")
        


        

### ---------- IMPORTING MODULES - START ---------- ###
import os
os.environ["SDL_VIDEODRIVER"] = "windib"
import pygame
pygame.init()

import datetime, time
import random
from operator import attrgetter

### ---------- IMPORTING MODULES - END ---------- ###


### ---------- VARIABLE ASSIGNMENT - START ---------- ###

## Assigning essential game variables
try:
    fps = 30
    error_time = 0
    display_loot_menu = False
    current_loot_slot = 0
    show_hud = False
    show_spellbook = False
    levelling_up = False
    levelup_frame = 0
    music_playing = False
    sound_playing = False
    master_volume = 1
    sfx_volume = 1
    music_volume = 1
    voice_volume = 1
    volumes = {"sfx":sfx_volume,
               "music":music_volume,
               "voice":voice_volume}
    cutscene_playing = False
    movement_started = False
    #display_options = False
    #display_sure = False
    
    cutscene0_played = False
    cutscene1_played = False
    cutscene2_played = False
    cutscene3_played = False
    cutscene4_played = False
    cutscene5_played = False
    cutscene6_played = False
    cutscene7_played = False
    cutscene8_played = False

    coordinates_set = False
    portal_x = -10
    portal_y = -10
    
    zaal_life = 1782
    zaal_animation = -1
    
    font = pygame.font.SysFont("Arial Regular", 90, False, False)
    dropfont = pygame.font.SysFont("Impact", 20, False, False)
    
except Exception as error:
    log(error, "Unable to initialise essential game variables")

# Setting the screen resolution and creating the screen
try:
    os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
    screen = pygame.display.set_mode((1920,1080), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.NOFRAME)
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    MONITOR_WIDTH = screen_width
    MONITOR_HEIGHT = screen_height
    
    fade_screen = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)    # An extra surface for put on top of the screen, for fading
    
    # Changes and reinitialises the screen with new settings
    def reinitialise_screen(resolution=(screen_width,screen_height), mode="fullscreen"):
        global error
        try:
            global screen, screen_width, screen_height
            screen_width = resolution[0]
            screen_height = resolution[1]
            if mode == "fullscreen":
                screen = pygame.display.set_mode(resolution, pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.FULLSCREEN)
            elif mode == "windowed":
                os.environ['SDL_VIDEO_WINDOW_POS'] = str((MONITOR_WIDTH - screen_width)/2) + "," + str((MONITOR_HEIGHT - screen_height)/2)
                screen = pygame.display.set_mode(resolution, pygame.HWSURFACE|pygame.DOUBLEBUF)
            elif mode == "borderless":
                os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
                screen = pygame.display.set_mode(resolution, pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.NOFRAME)
            else:
                error = "Unknown mode for reinitialise_screen(): " + mode + "[coding syntax error]."
                raise
        except:
            log(error, "Failed to reinitialise screen in " + mode + " mode at " + str(screen_width) + "x" + str(screen_height) + " resolution")
            
    pygame.display.set_caption("Spietz (Alpha 1.0)")
    pygame.display.set_icon(load("game_icon.png")) # Setting the icon for the game window    
except Exception as error:
    log(error, "Failed to initialise the game window")

# Keyboard inputs
try:
    accepting_text = False
    input_text = ""
    keys = Keys()
    mouse = Mouse()
except Exception as error:
    log(error, "Failed to initialise keyboard input variabes")

### ---------- VARIABLE ASSIGNMENT - END ---------- ###


### ---------- FUNCTION DEFINING - START ---------- ###

# Defining a function to check if the mouse is in a certain area
def mousein(start_x, end_x, start_y, end_y):
    """Takes in coordinates as if it was a 1920x1080 screen"""
    global error
    try:
        if mouse.x > start_x * (screen_width / 1920.0) and mouse.x < end_x * (
                screen_width / 1920.0) and mouse.y > start_y * (screen_height / 1080.0) and mouse.y < end_y * (
                screen_height / 1080.0):
            return True
        else:
            return False
    except Exception as error:
        log("Unable to determine whether mouse coordinates meet the requirements: " + str(start_x) + " < x < " + str(
            end_x) + ", " + str(start_y) + " < " + str(end_y))


# Checking if the given arrow key has been held down the longest
def is_longest_held(direction_held_time):
    global error
    try:
        longest = max(keys.left_arrow.time_held, keys.right_arrow.time_held, keys.up_arrow.time_held, keys.down_arrow.time_held, keys.a.time_held,
                      keys.d.time_held, keys.w.time_held, keys.s.time_held)
        if direction_held_time == longest:
            return True
        else:
            return False
    except Exception as error:
        log("Unable to determine direction command which has been issued the longest")


# Corrects the player's coordinates if they are moving
def add_movement(self, character, axis, file_type):
    global error
    try:
        if file_type == "image":
            if axis == "x":
                if character.orientation == "left":
                    return character.x + (self.square_size[0] * character.movement_cooldown * character.movespeed) / (
                                3 * fps)
                elif character.orientation == "right":
                    return character.x - (self.square_size[0] * character.movement_cooldown * character.movespeed) / (
                                3 * fps)
                else:
                    return character.x
            elif axis == "y":
                if character.orientation == "up":
                    return character.y + (self.square_size[1] * character.movement_cooldown * character.movespeed) / (
                                3 * fps)
                elif character.orientation == "down":
                    return character.y - (self.square_size[1] * character.movement_cooldown * character.movespeed) / (
                                3 * fps)
                else:
                    return character.y
        elif file_type == "canvas":
            if axis == "x":
                if character.orientation == "left":
                    return self.x - (self.square_size[0] * character.movement_cooldown * character.movespeed) / (
                                3 * fps)
                elif character.orientation == "right":
                    return self.x + (self.square_size[0] * character.movement_cooldown * character.movespeed) / (
                                3 * fps)
                else:
                    return self.x
            elif axis == "y":
                if character.orientation == "up":
                    return self.y - (self.square_size[1] * character.movement_cooldown * character.movespeed) / (
                                3 * fps)
                elif character.orientation == "down":
                    return self.y + (self.square_size[1] * character.movement_cooldown * character.movespeed) / (
                                3 * fps)
                else:
                    return self.y
    except Exception as error:
        log("Unable to add movement smoothing to character's (" + character.name + ") movement")


# Defining a function that transforms Vincent
def transform():
    global error
    try:
        global form, vincent_slime, vincent_human
        if form == "human":
            vincent_slime.position = vincent_human.position
            vincent_slime.orientation = vincent_human.orientation
            vincent_slime.room = vincent_human.room
            vincent_slime.exp = vincent_human.exp
            vincent_slime.level = vincent_human.level
            vincent_slime.skill_points = vincent_human.skill_points
            vincent_slime.current_life = vincent_human.current_life
            form = "slime"
        else:  # when form = "slime"
            vincent_human.position = vincent_slime.position
            vincent_human.orientation = vincent_slime.orientation
            vincent_human.room = vincent_slime.room
            vincent_human.exp = vincent_slime.exp
            vincent_human.level = vincent_slime.level
            vincent_human.skill_points = vincent_slime.skill_points
            vincent_human.current_life = vincent_slime.current_life
            form = "human"
    except Exception as error:
        log(error, "Failed to transform Vincent")


# Defining a function to check if Vincent is in a valid place to interact with the given coordinates
def is_interactable(coordinates):
    if (vincent[form].position == coordinates
            or (vincent[form].position == (coordinates[0] - 1, coordinates[1]) and vincent[form].orientation == "right")
            or (vincent[form].position == (coordinates[0], coordinates[1] - 1) and vincent[form].orientation == "down")
            or (vincent[form].position == (coordinates[0] + 1, coordinates[1]) and vincent[form].orientation == "left")
            or (vincent[form].position == (coordinates[0], coordinates[1] + 1) and vincent[form].orientation == "up")):
        return True
    else:
        return False


# Defining functinos to show exp drops, damage values and healing values
def number_drop(number_type, character, value):
    """number_type = \"damage\", \"exp\", \"heal\""""
    global error
    try:
        global number_drops
        drop_x = character.x + character.width / 2
        drop_y = character.y + character.height / 2
        if number_type == "damage":
            colour = (255, 0, 0)
        elif number_type == "exp":
            colour = (255, 215, 0)
        elif number_type == "heal":
            colour = (43, 255, 0)
        else:
            error = "Invalid value for number_type: " + str(number_type)
            raise

        if value > 0:
            if number_type == "damage":
                value = str(-value)
            else:
                value = "+" + str(value)
        else:
            value = str(value)

        number_drops.append([drop_x, drop_y, colour, value, drop_y])
    except Exception as error:
        log(error, "Failed to start number drop display")


def display_number_drop(number_drop_item):
    global error
    try:
        global number_drops
        screen.blit(dropfont.render(number_drop_item[3], True, number_drop_item[2]),
                    (number_drop_item[0], number_drop_item[1]))
        return number_drop_item[1] - 3
    except Exception as error:
        log(error, "Failed to display number drop")


# Defining a function to display current loot on the floor
def display_loot():
    """returns False when the loot menu is closed"""
    global error
    try:
        global loot, current_loot_slot

        if keys.escape or keys.backspace:
            return False

        screen.blit(loot_images["loot" + str(current_loot_slot)], (0, 0))

        for index in range(len(loot)):
            if loot[index] != "":
                screen.blit(loot_images[loot[index]], (781, 225 + 89 * index))

        screen.blit(loot_images["controls"], (0, 0))

        if (keys.up_arrow or keys.w) and current_loot_slot > 0:
            current_loot_slot -= 1
        if (keys.down_arrow or keys.s) and current_loot_slot < 5:
            current_loot_slot += 1

        if keys.enter and loot[current_loot_slot] != "":
            inventory.append(loot[current_loot_slot])
            loot[current_loot_slot] = ""
        if keys.e:
            for item in loot:
                if item != "":
                    inventory.append(item)
            loot = ["" for nothing in range(6)]

        return True
    except Exception as error:
        log(error, "Failed to display loot")


# Defining a function that displays the spellbook
def display_spellbook():
    global error
    try:
        if not cutscene6_played:
            screen.blit(spellbook_images["spellbook_default"], (0, 0))
        else:
            screen.blit(spellbook_images["firebolt1"], (0, 0))
        screen.blit(spellbook_images["firebolt_uncharged"], (0, 0))
        screen.blit(font.render(str(vincent[form].level), True, (199, 189, 189)), (610, 20))
        screen.blit(font.render(str(vincent[form].skill_points), True, (199, 189, 189)), (1665, 20))
        screen.blit(font.render(str(firebolt.level), True, (142, 0, 0)), (834, 239))
        screen.blit(esc_exit, (0, 0))
    except Exception as error:
        log(error, "Failed to display spellbook")


# Defining a function that displays the Heads-up Display (HUD)
def display_hud():
    global error
    try:
        screen.blit(hud_images["expback"], (0, 0))
        screen.blit(hud_images["expbar"], (728, 951), (0, 0, (vincent[form].exp / 100.0) * 467, 130))
        screen.blit(hud_images["hud"], (0, 0))
        screen.blit(hud_images["health_orb"],
                    (1025, 994 + (1 - (vincent[form].current_life / float(vincent[form].max_life))) * 87), (
                    0, (1 - (vincent[form].current_life / float(vincent[form].max_life))) * 87, 123,
                    (vincent[form].current_life / float(vincent[form].max_life)) * 87))

        for index in range(len(spells)):
            if abilities[spells[index]].cooldown > 0:
                screen.blit(hud_images[spells[index] + "_cooldown"], (760 + 51 * index, 1029))
            else:
                screen.blit(hud_images[spells[index]], (760 + 51 * index, 1029))

        for index in range(len(inventory)):
            screen.blit(hud_images[inventory[index]], (964 + 51 * index, 1029))
    except Exception as error:
        log(error, "Failed to display heads up display")


# Defining a function that displays dialogue boxes with the respective text
def display_dialogue(character, dialogue_number):
    global error
    try:
        screen.blit(dialogue[character + "box"], (0, 0))
        screen.blit(dialogue[character + str(dialogue_number)], (765, 895))
        if keys.space or keys.enter or keys.numpad_enter:
            return False
        return True
    except Exception as error:
        log(error, "Failed to display dialogue (" + character + str(dialogue_number) + ") correctly")


# Defining a function to start the playing of music
def play_music(name, music_type, multiplier=1, loops=-1):
    """sound_type = \"sfx\", \"music\", \"voice\""""
    global error
    try:
        global music_playing
        pygame.mixer.music.stop()
        music_playing = True
        load(name + ".ogg")
        pygame.mixer.music.set_volume(multiplier * master_volume * volumes[music_type])
        pygame.mixer.music.play(loops)
    except Exception as error:
        log(error, "Failed to play music track: " + name + ".ogg")


# Defining a function to start the playing of sound effects
def play_sound(name, sound_type, multiplier=1, loops=0):
    """sound_type = \"sfx\", \"music\", \"voice\""""
    global error
    try:
        global sound_playing
        sound_playing = True
        sound = pygame.mixer.Sound("../Sound Files/" + name + ".ogg")
        sounds.append(sound)
        sound.set_volume(multiplier * master_volume * volumes[sound_type])
        sound.play(loops)
    except Exception as error:
        log(error, "Failed to play music track: " + name + ".ogg")


# Defining a function to load a save file
def load_game(savefile):
    try:
        save = open("../Save Files/" + savefile + ".txt", "r")
        current = save.readline()[:-1]
        if current == "No save data":
            save.close()
            return
        current_room = rooms[int(save.readline()[:-1])]
        form = save.readline()[:-1]
        cutscene0_played = bool(save.readline()[:-1])
        cutscene1_played = bool(save.readline()[:-1])
        cutscene2_played = bool(save.readline()[:-1])
        cutscene3_played = bool(save.readline()[:-1])
        cutscene4_played = bool(save.readline()[:-1])
        cutscene5_played = bool(save.readline()[:-1])
        cutscene6_played = bool(save.readline()[:-1])
        cutscene7_played = bool(save.readline()[:-1])
        cutscene8_played = bool(save.readline()[:-1])
        vincent[form].position = (int(save.readline()[:-1]), int(save.readline()[:-1]))
        vincent[form].orientation = save.readline()[:-1]
        vincent[form].room = int(save.readline()[:-1])
        vincent[form].exp = int(save.readline()[:-1])
        vincent[form].level = int(save.readline()[:-1])
        vincent[form].skill_points = int(save.readline()[:-1])
        vincent[form].max_life = int(save.readline()[:-1])
        vincent[form].current_life = int(save.readline()[:-1])
        for setting_value in menus["options menu"].settings:  # Reading in the saved options settings
            setting_value = int(save.readline()[:-1])
        globals().update(locals())  # Making all variables loaded global
    except Exception as error:
        log(error, "Failed to load " + savefile + " correctly")
        raise


# Defining a function to save a save file
def save_game(savefile):
    try:
        save = open("../Save Files/" + savefile + ".txt", "w")
        save.write(current + "\n")
        save.write(current_room.name[-1] + "\n")
        save.write(form + "\n")
        save.write(str(cutscene0_played) + "\n")
        save.write(str(cutscene1_played) + "\n")
        save.write(str(cutscene2_played) + "\n")
        save.write(str(cutscene3_played) + "\n")
        save.write(str(cutscene4_played) + "\n")
        save.write(str(cutscene5_played) + "\n")
        save.write(str(cutscene6_played) + "\n")
        save.write(str(cutscene7_played) + "\n")
        save.write(str(cutscene8_played) + "\n")
        save.write(str(vincent[form].position[0]) + "\n")
        save.write(str(vincent[form].position[1]) + "\n")
        save.write(str(vincent[form].orientation) + "\n")
        save.write(str(vincent[form].room) + "\n")
        save.write(str(vincent[form].exp) + "\n")
        save.write(str(vincent[form].level) + "\n")
        save.write(str(vincent[form].skill_points) + "\n")
        save.write(str(vincent[form].max_life) + "\n")
        save.write(str(vincent[form].current_life) + "\n")
        for setting_value in menus["options menu"].settings:  # Saving the players option settings
            save.write(str(setting_value) + "\n")
        save.close()
    except Exception as error:
        log(error, "Failed to save game to " + savefile + ".txt")


# Defining a function to delete save files
def deletesave(savefile):
    line_number = 0
    save = open("../Save Files/" + savefile + ".txt", "r")
    while True:
        if save.readline() == "\n":
            number_of_lines = line_number
            break
        else:
            line_number += 1
    save.close()

    save = open("../Save Files/save" + savefile + ".txt", "w")
    save.write("No save data\n")
    for line in range(number_of_lines - 1):
        save.write("\n")
    save.close()


### ---------- FUNCTION DEFINING - END ---------- ###


### ---------- CLASS DEFINING - START ---------- ###

class Menu:
    def __init__(self, name, permanent, options, coordinates, actions, escape_action, settings=None):
        self.name = name
        self.background = load("menus/" + self.name + "/background.png")
        self.permanent = [load("menus/" + self.name + "/" + item + ".png") for item in permanent] # A list of all the different thing in the menu that are always shown
        self.sliders = []   # A list showing which settings in the menu are sliders        
        self.original_x = 0 # shows where the mouse was orignially pressed when moving a slider
        for option in options:
            if option[0][0:6] == "SLIDER":
                self.sliders.append([True, int(option[0][6:])])
            else:
                self.sliders.append([False])
        self.options = [[load("menus/" + self.name + "/" + setting + ".png") for setting in option] for option in options] # A list of all the different options that the user can select in the menu
        self.settings = settings    # Shows which setting each option is currently on
        if self.settings is None:
            self.settings = [0 for option in range(len(options))]
        self.coordinates = coordinates  # The screen coordinates of each option in the permananent list above (for 1920x1080; this is adjusted for other resolutions)
        self.actions = actions  # The new value for current that each option leads to when its clicked
        self.escape_action = escape_action # The value for current if escape is pressed
        self.current_selection = 0  # The index of the option that the user has currently selected (is hovering over)
    
    # Displays the menu on the screen
    def display(self):
        global error
        try:
            screen.blit(self.background, (0,0))
            for item in self.permanent:
                screen.blit(item, (0,0))
            
            for option in range(len(self.options)):
                if self.sliders[option][0]:
                    screen.blit(self.options[option][0], ((960 + 4*self.settings[option])*(screen_width/1920.0), self.sliders[option][1]*(screen_height/1080.0)))
                
            if not self.sliders[self.current_selection][0]:    
                screen.blit(self.options[self.current_selection][self.settings[self.current_selection]], (0,0))
            
            for index in range(len(self.options)):
                if len(self.options[index]) > 1:
                    screen.blit(self.options[index][self.settings[index]], (0,0))
            
        except Exception as error:
            log(error, "Failed to display " + self.name + " menu")
        
    # Changes the user's current selection in the menu
    def change_selection(self):
        global error
        global movement_started
        try:
            for index in range(len(self.options)):
                if mousein(self.coordinates[index][0], self.coordinates[index][1], self.coordinates[index][2], self.coordinates[index][3]):
                    self.current_selection = index
                    return
            
            if (keys.up_arrow or keys.w) and self.current_selection > 0:
                self.current_selection -= 1
            if (keys.down_arrow or keys.s) and self.current_selection < len(self.options) - 1:
                self.current_selection += 1
        except Exception as error:
            log(error, "Failed to change menu selection in " + self.name + " menu")
    
    def change_settings(self):
        global error
        try:
            if mouse.left.is_pressed:
                global movement_started
                if not movement_started:
                    self.original_x = mouse.x
                    slider_selected = False
                    for index in range(len(self.options)):
                        if mousein(self.coordinates[index][0], self.coordinates[index][1], self.coordinates[index][2], self.coordinates[index][3]):
                            self.current_selection = index
                            if self.sliders[self.current_selection][0]:
                                slider_selected = True
                    if not slider_selected:
                        return
                    movement_started = True
                else:
                    if self.settings[self.current_selection] + mouse.x - self.original_x < 0:
                        self.settings[self.current_selection] = 0
                    elif self.settings[self.current_selection] + mouse.x - self.original_x > 100:
                        self.settings[self.current_selection] = 100
                    else:
                        self.settings[self.current_selection] = mouse.x - self.original_x
                            
            elif self.sliders[self.current_selection][0]:
                if (keys.left_arrow or keys.left_arrow.is_pressed or keys.a or keys.a.is_pressed) and self.settings[self.current_selection] > 0:
                    self.settings[self.current_selection] -= 1
                if (keys.right_arrow or keys.right_arrow.is_pressed or keys.d or keys.d.is_pressed) and self.settings[self.current_selection] < 100:
                    self.settings[self.current_selection] += 1
            else:
                if (keys.left_arrow or keys.a) and self.settings[self.current_selection] > 0:
                    self.settings[self.current_selection] -= 1
                if (keys.right_arrow or keys.d) and self.settings[self.current_selection] < len(self.options[self.current_selection]) - 1:
                    self.settings[self.current_selection] += 1
        except Exception as error:
            log(error, "Failed to change option setting in " + self.name + " menu")
    
    # Checks if the user has issued a continue command (by clicking or pressing enter/spacebar)
    def check_action(self):
        """returns True if current is changed"""
        global error
        global current
        try:
            if mouse.left or keys.space or keys.enter or keys.numpad_enter:
                current = self.actions[self.current_selection]
                return True
        except Exception as error:
            log(error, "Failed to check for user menu action in " + self.name + "menu")
    
    def check_escape(self):
        global error
        global current
        try:
            if keys.escape:
                current = self.escape_action
        except Exception as error:
            log(error, "Failed to check escape")
    
    

class Character(object):    # maybe add an "id" attribute. One to identify each object for coding purposes. Incase the names change/need to be different or whatever
    def __init__(self, name, frames, position, orientation, movespeed, room, exp, max_life, current_life):
        self.name = name    # Character's name
        self.x = 0  # Character's screen x coordinate
        self.y = 0  # Character's screen y coordinate
        self.frames = {str(frame): {direction: load(self.name.lower().replace(" ", "/") + "/" + direction + str(frame) + ".png") for direction in ["left","up","right","down"]} for frame in range(frames)} #frames # The number of frames in the character's movement animation. The attribute "frames" becomes a dictionary of all the images during initialisation.
        self.position = position    # Character's grid position
        self.orientation = orientation  # The direction in which the character is facing
        self.movespeed = movespeed  # Character's movement speed. Should divide 3*fps (currently 90). Definitely should NOT be 90 or even near it. Also the 3*fps value may need changing.
        self.movement_cooldown = 0
        self.current_ability = ""   # The ability the character is currently using
        self.ability_frame = 0  # The frame of the ability animation the character is currently playing
        self.image = self.select_image()  # Character's image file        
        self.width = self.image.get_width()      # Width of character's image in pixels
        self.height = self.image.get_height()    # Height of character's image in pixels
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
        global error
        try:
            if not self.movement_cooldown and not cutscene_playing and self.alive:
                if (direction == "left" and (not (self.position[0] - 1, self.position[1]) in room.blocked)
                    and (self.position[0] > 0 or self.position[0]-1 in [exit.coordinates[0] for exit in room.exits if exit.coordinates[1] == self.position[1]])):
                    self.orientation = "left"
                    self.position = (self.position[0] - 1, self.position[1])
                    self.movement_cooldown = (3*fps)/self.movespeed
                    return True
                elif (direction == "right" and (not (self.position[0] + 1, self.position[1]) in room.blocked)
                      and (self.position[0] < room.max_coord[0] or self.position[0]+1 in [exit.coordinates[0] for exit in room.exits if exit.coordinates[1] == self.position[1]])):
                    self.orientation = "right"
                    self.position = (self.position[0] + 1, self.position[1])
                    self.movement_cooldown = (3*fps)/self.movespeed
                    return True
                elif (direction == "up" and (not (self.position[0], self.position[1] - 1) in room.blocked)
                      and (self.position[1] > 0 or self.position[1]-1 in [exit.coordinates[1] for exit in room.exits if exit.coordinates[0] == self.position[0]])):
                    self.orientation = "up"
                    self.position = (self.position[0], self.position[1] - 1)
                    self.movement_cooldown = (3*fps)/self.movespeed
                    return True
                elif (direction == "down" and (not (self.position[0], self.position[1] + 1) in room.blocked)
                      and (self.position[1] < room.max_coord[1] or self.position[1]+1 in [exit.coordinates[1] for exit in room.exits if exit.coordinates[0] == self.position[0]])):
                    self.orientation = "down"
                    self.position = (self.position[0], self.position[1] + 1)
                    self.movement_cooldown = (3*fps)/self.movespeed
                    return True
                else:
                    self.orientation = direction
                    return False
                    
        except Exception as error:
            log(error, "Failed to change character's (" + self.name + ") coordinates")

    def check_death(self):
        if self.current_life <= 0:
            self.alive = False
    
    def die(self, kill=False, directional=False):
        if not self.alive and not self.dead:
            if not directional:
                self.image = death_images[self.name][self.death_frame]
            else:
                self.image = death_images[self.name][self.death_frame][self.orientation]
                
            self.death_frame += 1
            if self.death_frame == len(death_images[self.name]):
                self.dead = True
                self.death_frame = 0
                try:
                    self.displayed = False  # for abilities
                except:
                    pass
                if kill:
                    vincent[form].gain_exp(self)
    
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
            return self.frames[str(int((self.movement_cooldown*(len(self.frames)-1)*self.movespeed + (3*fps) - 1 + int((keys.left_arrow.is_pressed or keys.right_arrow.is_pressed or keys.up_arrow.is_pressed or keys.down_arrow.is_pressed or keys.a.is_pressed or keys.d.is_pressed or keys.w.is_pressed or keys.s.is_pressed) and not(self.movement_cooldown == (3*fps)/self.movespeed)))/(3*fps)))][self.orientation]
    
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
        super(Player, self).__init__(name, frames, position, orientation, movespeed, room, exp, max_life, current_life)

    # Changing the direction in which the player is facing. This is useful for directing the player's abilities
    def change_orientation(self):
        global error
        try:
            if not self.movement_cooldown:
                if keys.left_arrow or keys.a:
                    self.orientation = "left"
                if keys.right_arrow or keys.d:
                    self.orientation = "right"
                if keys.up_arrow or keys.w:
                    self.orientation = "up"
                if keys.down_arrow or keys.s:
                    self.orientation = "down"
        except Exception as error:
            log(error, "Failed to change player's (" + self.name + ") orientation") 
    
    # Changing the player's x and y grid coordinates according to user input
    def change_position(self, room):
        global error
        try:            
            if self.movement_cooldown: # decrementing self.movement cooldown if it is not equal to 0
                self.movement_cooldown -= 1
            elif ((keys.left_arrow.time_held > 1 or keys.a.time_held > 1) or ((keys.left_arrow.time_held or keys.a.time_held) and self.orientation == "left")) and (is_longest_held(keys.left_arrow.time_held) or is_longest_held(keys.a.time_held)):
                self.move(room, "left")
            elif ((keys.right_arrow.time_held > 1 or keys.d.time_held > 1) or ((keys.right_arrow.time_held or keys.d.time_held) and self.orientation == "right")) and (is_longest_held(keys.right_arrow.time_held) or is_longest_held(keys.d.time_held)):
                self.move(room, "right")
            elif ((keys.up_arrow.time_held > 1 or keys.w.time_held > 1) or ((keys.up_arrow.time_held or keys.w.time_held) and self.orientation == "up")) and (is_longest_held(keys.up_arrow.time_held) or is_longest_held(keys.w.time_held)):
                self.move(room, "up")
            elif ((keys.down_arrow.time_held > 1 or keys.s.time_held > 1) or ((keys.down_arrow.time_held or keys.s.time_held) and self.orientation == "down")) and (is_longest_held(keys.down_arrow.time_held) or is_longest_held(keys.s.time_held)):
                self.move(room, "down")
        except Exception as error:
            log(error, "Failed to change player's (" + self.name + ") position")
    
    def check_exit(self, room):
        if not self.movement_cooldown:
            for exit in room.exits:
                if self.position == exit.coordinates:
                    self.join(exit.room, exit.position)
    
    def join(self, room, position):
        global current_room, sound_playing
        for sound in sounds:
            sound.stop()
        sound_playing = False
        current_room = rooms[room]
        self.room = room
        if room == 0:
            play_sound("portal", "sfx", 0.1, -1)
            sound_playing = True
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
        global error
        try:
            if len(self.moves) != 0 and not self.movement_cooldown:
                self.orientation = self.moves[0]            
        except Exception as error:
            log(error, "Failed to change NPC's (" + self.name + ") orientation")
    
    # Moving the npc based on its current pending moves
    def change_position(self, room):
        global error
        try:
            if self.movement_cooldown: # decrementing self.movement cooldown if it is not equal to 0
                self.movement_cooldown -= 1
            elif len(self.moves) != 0:
                self.move(room, self.moves[0])
                if self.movement_cooldown == (3*fps)/self.movespeed: # Deleting the current move after the movement command has been issued
                    del self.moves[0]
        except Exception as error:
            log(error, "Failed to change NPC's (" + self.name + ") position")
    
    def check_collision(self, player):
        if self.position == player.position and self.damage_cooldown == 0 and self.alive:
            damage_dealt = int(self.damage*(0.9 + 0.2*random.random()))
            player.current_life -= damage_dealt
            number_drop("damage", player, damage_dealt)
            self.damage_cooldown = fps
        elif self.damage_cooldown > 0:
            self.damage_cooldown -= 1
    
            
    
    # Finding the route from the npc's current position to the desired position using the A* search algorithm
    def find_route(self, room, goal):
        global error
        
        try:    # (maybe somehow make this only run when the player moves? recalculating every frame seems inefficient...)
            if not self.alive or abs(self.position[0] - goal[0]) + abs(self.position[1] - goal[1]) > 15 or (frame % fps != 0 and abs(self.position[0] - goal[0]) + abs(self.position[1] - goal[1]) > 4):  
                return
            elif (self.position == goal
                  or goal[0] < 0 or goal[0] > room.max_coord[0] or goal[1] < 0 or goal[1] > room.max_coord[1]): # Ensuring that the algorithm isn't run to try to get to a place the npc cannot access.
                self.moves = []
            else:
                class Square(object):
                    def __init__(self, coordinates, parent=""):  # If no parent value (starting square)
                        self.coordinates = coordinates  # Coordinates of the square
                        self.parent = parent            # Parent square; the square which the cell is adjacent to that it came from
                        self.min_distance = abs(coordinates[0] - goal[0]) + abs(coordinates[1] - goal[1])   # Direct route to goal from square, as if there were no walls
                        if self.parent == "":   # Setting the square's current distance to 0 if it is the starting square
                            self.current_distance = 0
                        else:
                            self.current_distance = self.parent.current_distance + 1    # Distance from starting square to current square
                        self.total_distance = self.current_distance + self.min_distance
                
                goal_reached = False # Showing that the goal has not been reached (yet)
                processed = []  # A list of already processed squares; i.e. all directions from them have been explored
                pending = [Square(self.position)]    # A list of squares that have not been fully explored from. The starting square has no parent because it has not travelled from anywhere to get there
                
                while (len(pending) != 0
                       and len(pending) < (room.max_coord[0] + 1)*(room.max_coord[1] + 1)): # Making sure the algorithm doesn't carry on forever if it cannot find a route
                    square = min(pending, key=attrgetter("total_distance"))
                    
                    processed.append(square)
                    pending.remove(square)
                    
                    adjacents = []   # A list of squares adjacent to the current square
                    if not square.coordinates[0] == 0:
                        adjacents.append(Square((square.coordinates[0]-1,square.coordinates[1]), square))
                    if not square.coordinates[1] == 0:
                        adjacents.append(Square((square.coordinates[0],square.coordinates[1]-1), square))
                    if not square.coordinates[0] == room.max_coord[0]:
                        adjacents.append(Square((square.coordinates[0]+1,square.coordinates[1]), square))
                    if not square.coordinates[1] == room.max_coord[1]:
                        adjacents.append(Square((square.coordinates[0],square.coordinates[1]+1), square))
                    
                    for adjacent in adjacents:
                        if adjacent.coordinates == goal:
                            goal = adjacent
                            goal_reached = True # Showing that the goal has been reached
                            break
                        elif (adjacent.coordinates in room.blocked
                              or adjacent.coordinates in [cell.coordinates for cell in processed]):
                            pass    # Cell blocked, already processed or already queued to be processed
                        else:
                            pending.append(adjacent)                    
                    if goal_reached:    # If the goal has been found, the "else" statement will be skipped by breaking
                        break
                    
                else:   # If the algorithm is unable to find a route to the goal, it will create a route to the closest square to the goal
                    closest_square = processed[0]   # Default VALID value
                    for square in processed:
                        if (abs(square.coordinates[0] - goal.coordinates[0]) + abs(square.coordinates[1] - goal.coordinates[1]) <
                            abs(closest_square.coordinates[0] - goal.coordinates[0]) + abs(closest_square.coordinates[1] - goal.coordinates[1])):
                            closest_square = square
                    goal = closest_square
                
                # Compiling the route list
                route = []                
                while True:
                    if goal.coordinates == self.position:
                        break
                    elif goal.coordinates[0] == goal.parent.coordinates[0] - 1:
                        route.append("left")
                    elif goal.coordinates[0] == goal.parent.coordinates[0] + 1:
                        route.append("right")
                    elif goal.coordinates[1] == goal.parent.coordinates[1] - 1:
                        route.append("up")
                    elif goal.coordinates[1] == goal.parent.coordinates[1] + 1:
                        route.append("down")
                    goal = goal.parent
                
                route.reverse()   # Putting the commands in the correct order (they were placed in the list backwards)
                self.moves = route
        except Exception as error:
            error_logged = False    # Showing that the error has not yet been logged
            try:    # If "goal" is not yet an object; i.e it has not yet been found
                error_logged = True # Showing that the error has been logged
                log(error, "Unable to calculate NPC's (" + self.name + ") route from " + str(self.position) + " to " + str(goal))                
            except: # If "goal" has become an object; i.e. the goal has been found
                if not error_logged:
                    log(error, "Unable to calculate NPC's (" + self.name + ") route from " + str(self.position) + " to " + str(goal.coordinates))

# The class for abilities           
class Ability(Character):
    def __init__(self, name, frames, position, orientation, movespeed, room, damage, max_cooldown, max_range, exp=0, max_life=1, current_life=1):
        super(Ability, self).__init__(name, frames, position, orientation, movespeed, exp, room, max_life, current_life)
        self.unlocked = False
        self.displayed = False
        self.damage = damage
        self.max_cooldown = max_cooldown
        self.cooldown = 0
        self.max_range = max_range
        self.moves = []  # A list of pending moves to be made by the ability
        abilities[self.name.lower()] = self
        
    def use(self, player):
        global zaal_animation
        if self.name != "Inferno":
            if self.cooldown == 0 and self.unlocked:
                self.room = player.room
                player.current_ability = self.name.lower()            
                self.cooldown = fps*self.max_cooldown
        elif self.dead and zaal_animation == -1 and player.position in [(x,y) for y in range(4,15) for x in range(10,13)]+[(x,y) for y in range(2,4) for x in range(10)]+[(x,y) for y in range(2) for x in range(10,13)]+[(x,y) for y in range(2,4) for x in range(13,20)]:
            zaal_animation = 18
            global sound_playing
            play_sound("zaalattack", "sfx", 0.2)
        
    
    def cast(self, player):
        global zaal_animation
        if self.name != "Inferno":            
            self.alive = True
            self.dead = False        
            self.displayed = True   
            if player.orientation == "left":
                self.position = (player.position[0] - 1, player.position[1])
            elif player.orientation == "up":
                self.position = (player.position[0], player.position[1] - 1)
            elif player.orientation == "right":
                self.position = (player.position[0] + 1, player.position[1])
            elif player.orientation == "down":
                self.position = (player.position[0], player.position[1] + 1)
            self.moves = [player.orientation for distance in range(self.max_range)]
        elif zaal_animation == 0:
            sound_playing = False
            self.alive = True
            self.dead = False        
            self.displayed = True 
            self.room = player.room
            self.cooldown = fps*self.max_cooldown
            zaal_animation = -1
            if player.position in [(x,y) for y in range(4,15) for x in range(10,13)]:
                self.position = (player.position[0], 5)
                self.moves = ["down" for distance in range(self.max_range)]
            elif player.position in [(x,y) for y in range(2,4) for x in range(10)]:
                self.position = (9, player.position[1])
                self.moves = ["left" for distance in range(self.max_range)]
            elif player.position in [(x,y) for y in range(2) for x in range(10,13)]:
                self.position = (player.position[0], 1)
                self.moves = ["up" for distance in range(self.max_range)]
            elif player.position in [(x,y) for y in range(2,4) for x in range(13,20)]:
                self.position = (13, player.position[1])                    
                self.moves = ["right" for distance in range(self.max_range)]
            else:
                self.position = (-10,-10)
                self.alive = False
                self.dead = True
                self.display = False
                self.cooldown = 0
        
    
    def exist(self, room):
        if self.cooldown > 0:
            self.cooldown -= 1
        self.die(directional=True)
        self.change_position(room)
        self.change_image()
        self.check_display()
        self.check_collision()
    
        
    def change_position(self, room):
        global error
        try:
            if self.movement_cooldown: # decrementing self.movement cooldown if it is not equal to 0
                self.movement_cooldown -= 1
            elif len(self.moves) != 0:                
                if not self.move(room, self.moves[0]):
                    self.alive = False
                if self.movement_cooldown == (3*fps)/self.movespeed: # Deleting the current move after the movement command has been issued
                    del self.moves[0]
        except Exception as error:
            log(error, "Failed to change ability's (" + self.name + ") position")
        
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
            if self.position == vincent[form].position and self.alive:
                damage_dealt = int(self.damage*(0.9 + 0.2*random.random()))
                vincent[form].current_life -= damage_dealt
                number_drop("damage", vincent[form], damage_dealt)
                self.alive = False
                

# The class for extra things that are shown as well as the canvas and characters in rooms                   
class Extra(object):
        def __init__(self, image_name, placement, x, y, scroll_speed=0, scroll_axis=0, rotations=1, rotation_interval=0, start_x="all", end_x="all", start_y="all", end_y="all"): # Default values are for when the extra should always be shown.
            self.image_name = image_name
            if image_name[0:9] in ["TESSELATE", "NEGATIVES"]:   # TESSELATE indicates that the image should be tesselated until the end of the screen. NEGATIVES indicates that the image should be shown if the player is NOT in the specified bounds
                self.image = extra_images[image_name[9:]]
            else:
                self.image = extra_images[image_name]
            self.width = self.image.get_width()
            self.height = self.image.get_height()
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
                
            self.rotation_interval = rotation_interval    # How often the images rotate (in seconds) (must be at least 1/fps)
            self.image_number = 0
            self.rotation_direction = "up"
            self.start_x = start_x  # The first grid x coordinate of the player's character where the image must be shown
            self.end_x = end_x      # The last grid x coordinate of the player's character where the image must be shown
            self.start_y = start_y  # The first grid y coordinate of the player's character where the image must be shown
            self.end_y = end_y      # The last grid y coordinate of the player's character where the image must be shown
                        
        def display(self, room, player):
            global error
            try:
                # Checking if the player is within the coordinates at which the extra should be displayed
                if self.start_x == "all" and self.end_x == "all" and self.start_y == "all" and self.end_y == "all":
                    show_extra = True
                elif self.start_x == "all" and self.end_x == "all" and player.position[1] >= self.start_y and player.position[1] <= self.end_y:
                    show_extra = True
                elif self.start_y == "all" and self.end_y == "all" and player.position[0] >= self.start_x and player.position[0] <= self.end_x:
                    show_extra = True
                elif (player.position[0] >= self.start_x and player.position[0] <= self.end_x
                        and player.position[1] >= self.start_y and player.position[1] <= self.end_y):   
                        show_extra = True
                else:
                    show_extra = False                
                
                if self.scroll_speed != 0:   # Changing the position of images that should scroll
                    if self.scroll_axis == "x":
                        self.x += float(self.scroll_speed)/fps
                        if abs(self.x - self.original_x) >= self.width:
                            self.x = self.original_x
                    elif self.scroll_axis == "y":
                        if abs(self.y - self.original_y) >= self.height:
                            self.y = self.original_y
                    else:
                        error = "Invalid scroll axis: " + str(self.scroll_axis) + " [coding syntax error]"
                        raise
                
                if self.rotations > 1:  # Changing the image at the correct time for images that rotate
                    if frame % int(self.rotation_interval*fps) == 0:
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
                        for horizontal in range(-1,(room.width/self.width) + 1):
                            for vertical in range(-1,(room.height/self.height) + 1):
                                screen.blit(self.image, (room.x + self.x + horizontal*self.width, room.y + self.y + vertical*self.height))
                    else:
                        screen.blit(self.image, (room.x + self.x, room.y + self.y))
                    
                    if self.scroll_speed != 0:   # Showing an extra copy of the image file for smooth scrolling
                        if self.scroll_speed > 0:
                            if self.scroll_axis == "x":
                                screen.blit(self.image, (room.x + self.x - room.width, room.y + self.y))
                            elif self.scroll_axis == "y":
                                screen.blit(self.image, (room.x + self.x, room.y + self.y - room.height))
                        else:   # When the scroll speed is negative
                            if self.scroll_axis == "x":
                                screen.blit(self.image, (room.x + self.x + room.width, room.y + self.y))
                            elif self.scroll_axis == "y":
                                screen.blit(self.image, (room.x + self.x, room.y + self.y + room.height))
            except Exception as error:
                log(error, "Failed to display extra in " + current_room.name)
            
            
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
        self.width = canvas.get_width()
        self.height = canvas.get_height()
        self.square_size = square_size      # this NEEDS to be a multiple/division of the screen size, so that zoom room is maintained across all resolutions
        ## The amounts of inaccessible terrain at each side of the canvas
        self.grey_left = grey_left
        self.grey_up = grey_up
        self.grey_right = grey_right
        self.grey_down = grey_down
        self.max_coord = (((self.width - (grey_left + grey_right))/self.square_size[0]) - 1, ((self.height - (grey_up + grey_down))/self.square_size[1]) - 1)        
        self.blocked = blocked  # A list of squares which are blocked by terrain, such that the player cannot walk on them. Don't add squares higher than the max coordinate >_> (waste of space)
        self.exits = exits # A list of tuples, showing squares which cause the player to exit the current room, and which area's they lead to.
    
       
    # Adding a square to the blocked list  
    def add_blocked(self, square):
        """Add a grid coordinate to the list of blocked squares for this room"""
        global error
        try:
            if square in self.blocked:
                error = "square already blocked"
                raise
            elif square[0] < 0 or square[1] < 0 or square[0] > self.max_coord[0] or square[1] > self.max_coord[1]:
                error = "square not in coordinate range of current room (" + self.name + ")"
                raise
            else:
                self.blocked.append(square)        
        except Exception as error:
            log(error, "Failed to add square to blocked squares list: " + str(square))
    
    # Removing a square from the blocked list
    def remove_blocked(self, square):
        """Remove a grid coordinate from the list of blocked squares for this room"""
        global error
        try:
            if not square in self.blocked:
                error = "square not currently blocked"
                raise
            elif square[0] < 0 or square[1] < 0 or square[0] > self.max_coord[0] or square[1] > self.max_coord[1]:
                error = "square not in coordinate range of current room (" + self.name + ")"
                raise
            else:
                self.blocked.remove(square)            
        except:
            log(error, "Failed to remove square from the blocked squares list: " + str(square))
            
    # Displaying everything in the room
    def display_room(self, player):
        """Displays everything that will be on screen for the room"""
        global error
        try:
            self.calculate_player_position(player)  # Calculating the player's and canvas's x and y coordinates on the screen
            screen.blit(self.canvas, (self.x,self.y))   # Blitting the canvas first, so everything else goes on top of it
            
            for extra in self.extras:   # Showing the extras that go below the characters
                if extra.placement == "below":
                    extra.display(self, player)
                
            for npc in npcs:    # Displaying all the npcs. This may require an order for bosses. Maybe the npcs list should be sorted by a "(display_)priority" attribute?
                if npc.room == self.number and not npc.dead:   # Only displaying npcs that are in the current room
                    self.display_npc(npc)
            screen.blit(player.image, (player.x,player.y))  # Displaying the player last, so they are always on top
            for name, ability in abilities.iteritems():
                if ability.room == self.number and ability.displayed:
                    self.display_npc(ability)
            
            for extra in self.extras: # Showing the extras that go on top of the characters
                if extra.placement == "above":
                    extra.display(self, player)
            
        except Exception as error:
            log(error, "Failed to display room (" + self.name + ") correctly")                 
    
    # Calculating the player's and canvas's position on the screen correctly (such that when the player is near the edge THEY move, not the canvas)
    def calculate_player_position(self, player):
        global error
        try:
            # Player's and canvas's x coordinates
            player.x = (screen_width - player.width)/2
            if self.grey_left + (self.square_size[0]*player.position[0]) + ((self.square_size[0] - player.width)/2) < player.x:
                player.x = self.grey_left + (self.square_size[0]*player.position[0]) + ((self.square_size[0] - player.width)/2)
                player.x = add_movement(self, player, "x", "image")
                self.x = 0
                # If the player is transistioning between a place where the player model would move and a place where the canvas would move
                if (player.x > (screen_width - player.width)/2
                    and (not self.grey_left + (self.square_size[0]*player.position[0]) + ((self.square_size[0] - player.width)/2) < player.x
                         or self.width > screen_width + self.square_size[0])):
                    self.x -= player.x - (screen_width - player.width)/2
                    player.x = (screen_width - player.width)/2
            elif screen_width - self.grey_right - (self.square_size[0]*(1 + self.max_coord[0] - player.position[0])) + ((self.square_size[0] - player.width)/2) > player.x:
                player.x = screen_width - self.grey_right - (self.square_size[0]*(1 + self.max_coord[0] - player.position[0])) + ((self.square_size[0] - player.width)/2)
                player.x = add_movement(self, player, "x", "image")
                self.x = -(self.width - screen_width)
                # If the player is transistioning between a place where the player model would move and a place where the canvas would move
                if (player.x < (screen_width - player.width)/2
                    and (not screen_width - self.grey_right - (self.square_size[0]*(1 + self.max_coord[0] - player.position[0])) + ((self.square_size[0] - player.width)/2) > player.x
                         or self.width > screen_width + self.square_size[0])):
                    self.x += (screen_width - player.width)/2 - player.x
                    player.x = (screen_width - player.width)/2
            else:
                self.x = -(self.grey_left + (self.square_size[0]*player.position[0]) - ((screen_width - player.width)/2) + (self.square_size[0] - player.width)/2)
                self.x = add_movement(self, player, "x", "canvas")
                if self.x > 0:
                    player.x -= self.x
                    self.x = 0
                elif self.x < -(self.width - screen_width):
                    player.x += -(self.width - screen_width) - self.x
                    self.x = -(self.width - screen_width)
            
            # Player's and canvas's y coordinates
            player.y = (screen_height - player.height)/2
            if self.grey_up + self.square_size[1]*(player.position[1] - 1) + (2*self.square_size[1] - player.height) < player.y:
                player.y = self.grey_up + self.square_size[1]*(player.position[1] - 1) + (2*self.square_size[1] - player.height)
                player.y = add_movement(self, player, "y", "image")
                self.y = 0
                # If the player is transistioning between a place where the player model would move and a place where the canvas would move
                if (player.y > (screen_height - player.height)/2
                    and (not self.grey_up + self.square_size[1]*(player.position[1] - 1) + (2*self.square_size[1] - player.height) < player.y
                         or self.height > screen_height + self.square_size[1])):                    
                    self.y -= player.y - (screen_height - player.height)/2
                    player.y = (screen_height - player.height)/2
            elif screen_height - self.grey_down - (self.square_size[1]*(self.max_coord[1] - player.position[1] + 2)) + (2*self.square_size[1] - player.height) > player.y:
                player.y = screen_height - self.grey_down - (self.square_size[1]*(self.max_coord[1] - player.position[1] + 2)) + (2*self.square_size[1] - player.height)
                player.y = add_movement(self, player, "y", "image")
                self.y = -(self.height - screen_height)
                # If the player is transistioning between a place where the player model would move and a place where the canvas would move
                if (player.y < (screen_height - player.height)/2
                    and (not screen_height - self.grey_down - (self.square_size[1]*(self.max_coord[1] - player.position[1] + 2)) + (2*self.square_size[1] - player.height) > player.y
                         or self.height > screen_height + self.square_size[1])):
                    self.y += (screen_height - player.height)/2 - player.y
                    player.y = (screen_height - player.height)/2
            else:
                self.y = -(self.grey_up + (self.square_size[1]*(player.position[1] - 1)) - ((screen_height - player.height)/2) + (2*self.square_size[1] - player.height))
                self.y = add_movement(self, player, "y", "canvas")
                if self.y > 0:
                    player.y -= self.y
                    self.y = 0
                elif self.y < -(self.height - screen_height):
                    player.y += -(self.height - screen_height) - self.y
                    self.y = -(self.height - screen_height)
                    
        except Exception as error:
            log(error, "Failed to calculate player's  and canvas's positions")
    
    # Displaying NPCs on the canvas (and screen if their coordinates are on the screen)
    def display_npc(self, npc):
        global error
        try:
            npc.x = self.grey_left + self.square_size[0]*npc.position[0] + (self.square_size[0] - npc.width)/2 + self.x
            npc.y = self.grey_up + self.square_size[1]*(npc.position[1] - 1) + (2*self.square_size[1] - npc.height) + self.y
            npc.x = add_movement(self, npc, "x", "image")
            npc.y = add_movement(self, npc, "y", "image")
            screen.blit(npc.image, (npc.x,npc.y))
        except Exception as error:
            log(error, "Failed to display npc's (" + npc.name + ") position")  

### ---------- CLASS DEFINING - END ---------- ###
        

### ---------- IMAGE IMPORTING - START ---------- ###

try:    # loading images for extras into a dictionary so they only have to be loaded once, even though they will be used in multiple different places
    extra_images = {
        "sharedroom/lava_back_glow0":load("sharedroom/lava_back_glow0.png"),
        "sharedroom/lava_back_glow1":load("sharedroom/lava_back_glow1.png"),
        "sharedroom/lava_back_glow2":load("sharedroom/lava_back_glow2.png"),
        "sharedroom/lava_back_glow3":load("sharedroom/lava_back_glow3.png"),
        "sharedroom/lava_back_glow4":load("sharedroom/lava_back_glow4.png"),
        "sharedroom/black_patches0":load("sharedroom/black_patches0.png"),
        "sharedroom/black_patches1":load("sharedroom/black_patches1.png"),
        # Room 0
        "room0/black_patches0":load("room0/black_patches0.png"),
        "room0/black_patches1":load("room0/black_patches1.png"),
        "room0/back":load("room0/back.png"),
        "room0/front":load("room0/front.png"),
        "room0/portal0":load("room0/portal0.png"),
        "room0/portal1":load("room0/portal1.png"),
        "room0/portal2":load("room0/portal2.png"),
        "room0/portal3":load("room0/portal3.png"),
        "room0/portal4":load("room0/portal4.png"),
        "room0/portal5":load("room0/portal5.png"),
        "room0/portal6":load("room0/portal6.png"),
        "room0/portal7":load("room0/portal7.png"),
        "room0/portal8":load("room0/portal8.png"),
        "room0/portal9":load("room0/portal9.png"),
        # Room 1
        "room1/barrier":load("room1/barrier.png"),
        "room1/bottom":load("room1/bottom.png"),
        "room1/bottom80":load("room1/bottom80.png"),
        "room1/sides":load("room1/sides.png"),
        "room1/star0":load("room1/star0.png"),
        "room1/star1":load("room1/star1.png"),
        "room1/star2":load("room1/star2.png"),
        "room1/star3":load("room1/star3.png"),
        "room1/star4":load("room1/star4.png"),
        "room1/star5":load("room1/star5.png"),
        "room1/star6":load("room1/star6.png"),
        "room1/star7":load("room1/star7.png"),
        "room1/star8":load("room1/star8.png"),
        "room1/flux00":load("room1/flux00.png"),
        "room1/flux01":load("room1/flux01.png"),
        "room1/flux02":load("room1/flux02.png"),
        "room1/flux03":load("room1/flux03.png"),
        "room1/flux04":load("room1/flux04.png"),
        "room1/flux05":load("room1/flux05.png"),
        "room1/flux06":load("room1/flux06.png"),
        "room1/flux07":load("room1/flux07.png"),
        "room1/flux08":load("room1/flux08.png"),
        "room1/flux09":load("room1/flux09.png"),
        "room1/flux10":load("room1/flux10.png"),
        "room1/flux11":load("room1/flux11.png"),
        "room1/flux12":load("room1/flux12.png"),
        # Room 2
        "room2/back":load("room2/back.png"),
        "room2/barriers":load("room2/barriers.png"),
        "room2/left_bottom_front1":load("room2/left_bottom_front1.png"),
        "room2/left_bottom_front180":load("room2/left_bottom_front180.png"),
        "room2/left_bottom_front2":load("room2/left_bottom_front2.png"),
        "room2/left_bottom_front280":load("room2/left_bottom_front280.png"),
        "room2/left_front1":load("room2/left_front1.png"),
        "room2/left_front180":load("room2/left_front180.png"),
        "room2/left_front2":load("room2/left_front2.png"),
        "room2/left_front280":load("room2/left_front280.png"),
        "room2/middle_front1":load("room2/middle_front1.png"),
        "room2/middle_front180":load("room2/middle_front180.png"),
        "room2/middle_front2":load("room2/middle_front2.png"),
        "room2/middle_front280":load("room2/middle_front280.png"),
        "room2/right_bottom_front":load("room2/right_bottom_front.png"),
        "room2/right_bottom_front80":load("room2/right_bottom_front80.png"),
        "room2/right_front":load("room2/right_front.png"),
        "room2/right_front80":load("room2/right_front80.png"),
        "room2/small_front1":load("room2/small_front1.png"),
        "room2/small_front2":load("room2/small_front2.png"),
        "room2/ruin":load("room2/ruin.png"),
        "room2/farleft_sidewall":load("room2/farleft_sidewall.png"),
        "room2/left_sidewall":load("room2/left_sidewall.png"),
        "room2/middle_sidewall1":load("room2/middle_sidewall1.png"),
        "room2/middle_sidewall2":load("room2/middle_sidewall2.png"),
        "room2/right_sidewall":load("room2/right_sidewall.png"),
        "room2/bottom_wall":load("room2/bottom_wall.png"),
        "room2/bottom_wall80":load("room2/bottom_wall80.png"),
        "room2/portal_burn":load("room2/portal_burn.png"),
        "room2/portal_symbol":load("room2/portal_symbol.png"),
        "room2/portal_symbol_slime":load("room2/portal_symbol_slime.png"),
        "room2/book0":load("room2/book0.png"),
        "room2/book1":load("room2/book1.png"),
        "room2/book2":load("room2/book2.png"),
        "room2/light00":load("room2/light00.png"),
        "room2/light01":load("room2/light01.png"),
        "room2/light02":load("room2/light02.png"),
        "room2/light03":load("room2/light03.png"),
        "room2/light04":load("room2/light04.png"),
        "room2/light05":load("room2/light05.png"),
        "room2/light06":load("room2/light06.png"),
        "room2/light07":load("room2/light07.png"),
        "room2/light08":load("room2/light08.png"),
        "room2/light09":load("room2/light09.png"),
        "room2/light10":load("room2/light10.png"),
        "room2/light11":load("room2/light11.png"),
        "room2/light12":load("room2/light12.png"),
        "room2/light13":load("room2/light13.png"),
        "room2/light14":load("room2/light14.png"),
        "room2/light15":load("room2/light15.png"),
        "room2/drop0":load("room2/drop0.png"),
        "room2/drop1":load("room2/drop1.png"),
        "room2/drop2":load("room2/drop2.png"),
        "room2/drop3":load("room2/drop3.png"),
        "room2/drop4":load("room2/drop4.png"),
        "room2/drop5":load("room2/drop5.png"),
        "room2/drop6":load("room2/drop6.png"),
        # Room 3
        "room3/platform":load("room3/platform.png")
    }

    # Loading dialogue images
    dialogue = {
        "mysteriousbox":load("dialogue/mysteriousbox.png"),
        "vincentbox":load("dialogue/vincentbox.png"),
        "zaalbox":load("dialogue/zaalbox.png"),
        "mysterious0":load("dialogue/mysterious0.png"),
        "mysterious1":load("dialogue/mysterious1.png"),
        "mysterious2":load("dialogue/mysterious2.png"),
        "mysterious3":load("dialogue/mysterious3.png"),
        "vincent0":load("dialogue/vincent0.png"),
        "vincent1":load("dialogue/vincent1.png"),
        "vincent2":load("dialogue/vincent2.png"),
        "vincent3":load("dialogue/vincent3.png"),
        "vincent4":load("dialogue/vincent4.png"),
        "vincent5":load("dialogue/vincent5.png"),
        "vincent6":load("dialogue/vincent6.png"),
        "vincent7":load("dialogue/vincent7.png"),
        "vincent8":load("dialogue/vincent8.png"),
        "zaal0":load("dialogue/zaal0.png"),
        "zaal1":load("dialogue/zaal1.png"),
        "zaal2":load("dialogue/zaal2.png"),
        "zaal3":load("dialogue/zaal3.png"),
        "zaal4":load("dialogue/zaal4.png"),
    }

    # Loading ability images
    ability_images = {
        "firebolt":
            {"Vincent Slime":
                {
                    "left":[load("vincent/slime/firebolt/left" + str(n) + ".png") for n in range(12)],
                        "up":[load("vincent/slime/firebolt/up" + str(n) + ".png") for n in range(12)],
                            "right":[load("vincent/slime/firebolt/right" + str(n) + ".png") for n in range(12)],
                                "down":[load("vincent/slime/firebolt/down" + str(n) + ".png") for n in range(12)]
                }
            }
    }

    # Loading death images
    death_images = {
        "Vincent Slime":[load("vincent/slime/death" + str(n) + ".png") for n in range(12)],
            "Enemy Slime":[load("enemy/slime/death" + str(n) + ".png") for n in range(10)],
                "Firebolt":[{direction:load("firebolt/death/" + direction + str(n) + ".png") for direction in ["left", "up", "right", "down"]} for n in range(8)],
                    "Inferno":[{direction:load("inferno/death/" + direction + str(n) + ".png") for direction in ["left", "up", "right", "down"]} for n in range(11)],
    }

    # Loading loot images:
    loot_images = {
        "controls":load("loot/controls.png"),
        "loot0":load("loot/loot0.png"),
        "loot1":load("loot/loot1.png"),
        "loot2":load("loot/loot2.png"),
        "loot3":load("loot/loot3.png"),
        "loot4":load("loot/loot4.png"),
        "loot5":load("loot/loot5.png"),
        "slime_chunk":load("loot/slime_chunk.png")
    }


    # Loading tutorial images
    tutorial = [load("tutorial/tutorial" + str(n) + ".png") for n in range(13)]

    # Loading spellbook images
    spellbook_images = {
        "spellbook_default":load("spellbook/spellbook_default.png"),
        "firebolt_uncharged":load("spellbook/firebolt_uncharged.png"),
        "firebolt1":load("spellbook/firebolt1.png")
        }

    # Loading hud images
    hud_images = {
        "hud":load("hud/hud.png"),
        "health_orb":load("hud/health_orb.png"),
        "expbar":load("hud/expbar.png"),
        "expback":load("hud/expback.png"),
        "firebolt":load("hud/firebolt.png"),
        "firebolt_cooldown":load("hud/firebolt_cooldown.png"),
        "slime_chunk":load("hud/slime_chunk.png")
    }

    # Loading level up images
    levelup_images = [load("levelup/" + str(n) + ".png") for n in range(15)]

    # Loading zaal images
    zaal_images = {
        "health_back":load("zaal/health_back.png"),
        "health":load("zaal/health.png"),
        "health_icon":load("zaal/health_icon.png"),
        "death":[load("zaal/death" + str(n) + ".png") for n in range(12)],
            "zaal":[load("zaal/zaal" + str(n) + ".png") for n in range(2)],
                "attack":[load("zaal/attack" + str(n) + ".png") for n in range(19)]


    }
    
    credits_images = [load("credits/credits" + str(n) + ".png").convert() for n in range(8)]
    
    esc_exit = load("esc_exit.png")
    controls_page = load("controls.png")
except Exception as error:
    log(error, "Failed to load image files")

### ---------- IMAGE IMPORTING - END ---------- ###


### ---------- VIDEO IMPORTING - START ---------- ###

try:
    introduction = load("introduction.mpg")
except Exception as error:
    log(error, "Failed to load video files")

### ---------- VIDEO IMPORTING - END ---------- ###


### ---------- PROGRAM DISPLAY - START ---------- ###

try:    # Initialising game objects.
    current = "main menu"
    npcs = [] # A list of all currently loaded npcs. All Npc objects are appended to this list when they are initialised.
    abilities = {}  # A dictionary of all currently loaded abilities
    sounds = [] # A list of sounds that are currently playing
    loot = ["" for nothing in range(6)]   # A list of loot that is currently available in the loot pile
    spells = [] # The characters unlocked spells
    inventory = [] # The characters inventory
    number_drops = []   # The list of current number drops
    menus = {"main menu":Menu("main", ["title"],
                              [["play"], ["options"], ["controls"], ["exit"]],
                              [(620,1300,605,648), (620,1300,663,706), (620,1300,717,760), (620,1300,774,817)],
                              ["saves menu", "options menu", "controls", "exit"], "sure quit?"),
             "options menu":Menu("options", ["headings", "apply reset", "sliders"],
                                 [["SLIDER278"], ["SLIDER335"], ["SLIDER392"], ["SLIDER449"], ["windowed", "borderless", "fullscreen"],
                                    ["800x600", "1024x768", "1152x864", "1280x720", "1280x768", "1280x1024", "1366x768", "1600x900", "1600x1024", "1680x1050", "1920x1080"],
                                    ["SLIDER669"], ["subs_on", "subs_off"], ["damage_on", "damage_off"], ["apply", "reset"]],
                                 [(123,123,123,123), (123,123,123,123), (123,123,123,123), (123,123,123,123), (123,123,123,123), (123,123,123,123), (123,123,123,123), (123,123,123,123), (123,123,123,123), (123,123,123,123)],
                                 ["options menu", "options menu", "options menu", "options menu", "options menu", "options menu", "options menu", "options menu", "options menu", "options menu"],
                                 "main menu", [50, 100, 100, 100, 1, 10, 100, 0, 0, 0]),
             "saves menu":Menu("saves", [],
                                [["slot0"], ["slot1"], ["slot2"], ["slot3"]],
                                [(525,1413,255,386), (525,1413,433,564), (525,1413,611,742), (525,1413,789,920)],
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
        Room("Room 0", load("room0/lava_back.png"),
             [Extra("sharedroom/lava_back_glow0", "below", 0, 1166, 0, 0, 5, 0.2),
              Extra("room0/black_patches0", "below", 0, 1166, 10, "x", 2, 1),
              Extra("room0/back", "below", 0, 0),
              portal,
              Extra("room0/front", "above", 0, 62)],
             (70,70), 420, 420, 450, 330, [(7,5)],
             [Exit((6,-1), "up", 1, (11,14)),
              Exit((7,-1), "up", 1, (12,14)),
              Exit((8,-1), "up", 1, (13,14))]),
        Room("Room 1", load("room1/back.png"),
             [Extra("room1/barrier", "below", 55, 1054),
              Extra("room1/bottom", "above", 0, 1051, start_y=0, end_y=11),
              Extra("room1/bottom", "above", 0, 1051, start_x=11, end_x=13, start_y=12, end_y=15),
              Extra("room1/bottom80", "above", 0, 1051, start_x=0, end_x=10, start_y=12, end_y=14),
              Extra("room1/bottom80", "above", 0, 1051, start_x=14, end_x=24, start_y=12, end_y=14),
              Extra("room1/sides", "above", 0, 0)],
             (70,70), 70, 280, 100, 50, [],
             [Exit((11,15), "down", 0, (6,0)),
               Exit((12,15), "down", 0, (7,0)),
               Exit((13,15), "down", 0, (8,0)),
               Exit((11,-1), "up", 2, (45,32)),
               Exit((12,-1), "up", 2, (46,32)),
               Exit((13,-1), "up", 2, (47,32))]),
        Room("Room 2", load("room2/lava_back.png"),
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
             (70,70), 70, 420, 50, 20,
             [(22,0), (85,0)]
             + [(x,1) for x in range(22,86)]
             + [(22,2), (23,2)]
             + [(x,5) for x in range(16,21)]
             + [(x,6) for x in range(21,31)]
             + [(x,6) for x in range(60,86)]
             + [(87+s,5+s) for s in range(5)]
             + [(86,5), (30,7), (30,8), (60,7), (60,8)]
             + [(x,9) for x in range(31,45)]
             + [(x,9) for x in range(48,60)]
             + [(16,y) for y in range(6,13)]
             + [(44,y) for y in range(10,15)]
             + [(48,y) for y in range(10,15)]
             + [(90,y) for y in range(10,19)]
             + [(x,13) for x in range(5)]
             + [(x,13) for x in range(8,16)]
             + [(4,14), (3,15), (3,16), (3,17), (2,17)]
             + [(15,y) for y in range(14,19)]
             + [(x,18) for x in range(16,22)]
             + [(x,19) for x in range(22,35)]
             + [(x,19) for x in range(91,104)]
             + [(105,19), (106,19), (107,19), (103,20),
                (105,20), (105,21), (105,22), (104,22),
                (100,20), (100,21), (99,21), (98,21),
                (97,22), (97,23), (97,24)]
             + [(96,y) for y in range(25,33)]
             + [(x,30) for x in range(12)]
             + [(x,30) for x in range(13,28)]
             + [(14,31), (13,32), (25,31), (25,32)]
             + [(35,y) for y in range(16,33)]
             + [(57,y) for y in range(16,33)]             
             + [(x,15) for x in range(36,45)]
             + [(x,15) for x in range(48,57)],
             [Exit((45,33), "down", 1, (11,0)),
              Exit((46,33), "down", 1, (12,0)),
              Exit((47,33), "down", 1, (13,0))]),
        Room("Room 3", load("room3/background.png"),
             [Extra("TESSELATEsharedroom/lava_back_glow0", "below", 0, 0, 0, 0, 5, 0.2),
              Extra("TESSELATEsharedroom/black_patches0", "below", 0, 0, 10, "x", 2, 1),
              Extra("room3/platform", "below", 0, 0)],
             (70,70), 280, 140, 200, 210,
             [(x,0) for x in range(6)]
             + [(20,y) for y in range(6,10)]
             + [(x,10) for x in range(16,20)],
             [])
        ]            
              
              
    current_room = rooms[0]
    vincent_human = Player("Vincent Human", 4, (7,7), "down", 15, 0, 0, 1000, 1000)
    vincent_slime = Player("Vincent Slime", 6, (7,7), "down", 20, 0, 0, 1000, 1000)
    vincent = {"human": vincent_human, "slime": vincent_slime}
    form = "human"
    mean_slime = Npc("Enemy Slime", 6, (0,4), "right", 15, -1, 50, 80, 500, 500)
    firebolt = Ability("Firebolt", 6, (0,0), "right", 45, 2, 100, 2, 10)
    inferno = Ability("Inferno", 12, (0,0), "down", 90, 3, 200, 2, 10)
    inferno.unlocked = True
    inferno.dead = True
except Exception as error:
    log(error, "Failed to initialise game objects")
    raise

# Initialising screen/window related variables
ongoing = True
clock = pygame.time.Clock()
start_time = time.time()
frame = 1   # Storing the current frame as a variable

## Program window while loop
while ongoing:
    try:
        current_time = time.time() - start_time     # Storing the current amount of time that the program has been running
    except Exception as error:
        log(error, "Failed to update game run duration")

    mouse.reset_buttons()
    mouse.update_coordinates()
    keys.reset()

    ## Receiving user inputs
    try:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ongoing = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse.process_button_down(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse.process_button_up(event)
            elif event.type == pygame.KEYDOWN:
                keys.process_key_down(event)
                if accepting_text:
                    key_pressed = event.key # Assigning the last pressed key to a variable for accepting text
                    # input_text += add_character()
            elif event.type == pygame.KEYUP:
                keys.process_key_up(event)
                
    except Exception as error:
        log(error, "Failed to receive/process user inputs")
    ## Handling user inputs/Displaying the game
    if frame == 1:
        try:
            introduction.preview()
        except Exception as error:
            log(error, "Failed to start introduction")

    # elif introduction.get_busy():   # Checking to see that the introduction video hasn't stopped playing for whatever reason
    #     try:
    #         if keys.escape or keys.space or keys.enter or keys.numpad_enter:
    #             introduction.stop()
    #     except Exception as error:
    #         log(error, "Failed to display introduction")
            
    else:
        if current[-4:] == "menu":
            try:
                menus[current].display()
                menus[current].change_selection()
                menus[current].change_settings()
                if not menus[current].check_action():
                    menus[current].check_escape()
                # Changing the volume levels according to what the option menu says
                master_volume = 0.01*menus["options menu"].settings[0]
                sfx_volume = 0.01*menus["options menu"].settings[1]
                music_volume = 0.01*menus["options menu"].settings[2]
                voice_volume = 0.01*menus["options menu"].settings[3]
            except Exception as error:
                log(error, "An error occurred in the " + current)
                
        elif current == "controls":
            screen.blit(menus["main menu"].background, (0,0))
            screen.blit(controls_page, (0,0))
            screen.blit(esc_exit, (0,0))
            
            if keys.escape or keys.backspace:
                current = "main menu"
                
        elif current[0:4] == "save":
            save_number = current[4]
            load_game(current)
            current = "in game"
        
        elif current[0:8] == "cutscene":
            cutscene_time = current_time - cutscene_start_time
            if cutscene_time < 1:                
                vincent[form].change_image()
            if current[8] == "0":
                if cutscene_time < 3:
                    screen.fill((0,0,0))
                elif cutscene_time < 5:
                    if not sound_playing:
                        play_sound("thunder", "sfx")
                        play_sound("portal", "sfx", 0.1, -1)
                    screen.fill((0,0,0))
                    portal.display(current_room, vincent[form])
                    fade_screen.fill((255,255,255,255*(1-0.5*(cutscene_time-3))))
                    screen.blit(fade_screen, (0,0))
                elif cutscene_time < 10:
                    sound_playing = False 
                    portal.display(current_room, vincent[form])
                    if not display_dialogue("vincent", 0):
                        cutscene_start_time = current_time - 10
                elif cutscene_time < 12:
                    if not sound_playing:
                        play_sound("thunder", "sfx")
                    current_room.display_room(vincent[form])
                    fade_screen.fill((255,255,255,255*(1-0.5*(cutscene_time-10))))
                    screen.blit(fade_screen, (0,0))
                elif cutscene_time < 17:
                    sound_playing = False
                    current_room.display_room(vincent[form])
                    if not display_dialogue("vincent", 1):
                        cutscene_start_time = current_time - 17
                elif cutscene_time < 10017:
                    current_room.display_room(vincent[form])
                    screen.blit(tutorial[0], (0,0))
                    if keys.space or keys.enter or keys.numpad_enter:
                        cutscene_start_time = current_time - 10017
                else:
                    cutscene0_played = True
                    cutscene_playing = False
                    current = "in game"
            
            elif current[8] == "1":
                current_room.display_room(vincent[form])
                if cutscene_time < 10:
                    if not display_dialogue("vincent", 1):
                        cutscene_start_time = current_time - 10
                elif cutscene_time < 20:
                    if not display_dialogue("mysterious", 0):
                        cutscene_start_time = current_time - 20
                elif cutscene_time < 30:
                    if not display_dialogue("mysterious", 1):
                        cutscene_start_time = current_time - 30
                elif cutscene_time < 40:
                    if not display_dialogue("vincent", 2):
                        cutscene_start_time = current_time - 40
                elif cutscene_time < 50:
                    if not display_dialogue("vincent", 3):
                        cutscene_start_time = current_time - 50
                elif cutscene_time < 60:
                    if not display_dialogue("mysterious", 2):
                        cutscene_start_time = current_time - 60
                elif cutscene_time < 62.4:
                    if not coordinates_set:                        
                        star.x += 70*(vincent[form].position[0] - 12)
                        flux.x += 70*(vincent[form].position[0] - 12)
                        coordinates_set = True
                    star.display(current_room, vincent[form])
                    screen.blit(vincent[form].image, (vincent[form].x,vincent[form].y))
                    current_room.extras[5].display(current_room, vincent[form])
                    if cutscene_time > 61 and not sound_playing:
                        play_sound("transform", "sfx")
                elif cutscene_time < 63.7:                
                    star.display(current_room, vincent[form])
                    screen.blit(vincent[form].image, (vincent[form].x,vincent[form].y))
                    flux.display(current_room, vincent[form])                    
                    current_room.extras[5].display(current_room, vincent[form])
                    fade_screen.fill((151,0,0,255*((1/1.3)*(cutscene_time-62.4))))
                    screen.blit(fade_screen, (0,0))
                elif cutscene_time < 64:
                    screen.fill((151,0,0))
                    if form == "human":
                        transform()
                elif cutscene_time < 66:
                    screen.blit(vincent[form].image, (vincent[form].x,vincent[form].y))                    
                    current_room.extras[5].display(current_room, vincent[form])
                    fade_screen.fill((151,0,0,255*(1-0.5*(cutscene_time-64))))
                    screen.blit(fade_screen, (0,0))
                elif cutscene_time < 76:
                    sound_playing = False
                    if not display_dialogue("mysterious", 0):
                        cutscene_start_time = current_time - 76
                elif cutscene_time < 86:
                    if not display_dialogue("vincent", 4):
                        cutscene_start_time = current_time - 86
                elif cutscene_time < 96:
                    if not display_dialogue("mysterious", 3):
                        cutscene_start_time = current_time - 96
                elif cutscene_time < 106:
                    if not display_dialogue("vincent", 5):
                        cutscene_start_time = current_time - 106
                elif cutscene_time < 116:
                    if not display_dialogue("mysterious", 0):
                        cutscene_start_time = current_time - 116
                else:
                    play_music("main", "music", 0.5)
                    coordinates_set = False
                    cutscene1_played = True
                    cutscene_playing = False
                    current = "in game"
                
            elif current[8] == "2":
                current_room.display_room(vincent[form])
                if cutscene_time < 2:
                    if not sound_playing:
                        play_sound("thunder", "sfx")
                        current_room.extras.append(book_item)
                        current_room.extras.append(book_light)
                    fade_screen.fill((255,255,255,255*(1-0.5*(cutscene_time))))
                    screen.blit(fade_screen, (0,0))
                elif cutscene_time < 10002:
                    sound_playing = False
                    screen.blit(tutorial[1], (0,0))
                    if keys.space or keys.enter or keys.numpad_enter:
                        cutscene_start_time = current_time - 10002
                else:
                    cutscene2_played = True
                    cutscene_playing = False
                    current = "in game"
            
            elif current[8] == "3":
                current_room.display_room(vincent[form])
                if cutscene_time < 10000:
                    display_spellbook()
                    screen.blit(tutorial[2], (0,0))
                    if keys.space or keys.enter or keys.numpad_enter:
                        cutscene_start_time = current_time - 10000
                elif cutscene_time < 20000:
                    display_hud()
                    screen.blit(hud_images["firebolt"], (760, 1029))
                    display_spellbook()
                    if keys.escape or keys.backspace:
                        cutscene_start_time = current_time - 20000
                elif cutscene_time < 30000:
                    screen.blit(tutorial[3], (0,0))
                    if keys.space or keys.enter or keys.numpad_enter:
                        cutscene_start_time = current_time - 30000
                elif cutscene_time < 40000:
                    screen.blit(tutorial[4], (0,0))
                    if keys.space or keys.enter or keys.numpad_enter:
                        cutscene_start_time = current_time - 40000
                elif cutscene_time < 50000:
                    screen.blit(tutorial[5], (0,0))
                    if keys.space or keys.enter or keys.numpad_enter:
                        cutscene_start_time = current_time - 50000
                elif cutscene_time < 60000:
                    screen.blit(tutorial[6], (0,0))
                    if keys.space or keys.enter or keys.numpad_enter:
                        cutscene_start_time = current_time - 60000
                elif cutscene_time < 70000:
                    screen.blit(tutorial[7], (0,0))
                    if keys.space or keys.enter or keys.numpad_enter:
                        cutscene_start_time = current_time - 70000
                elif cutscene_time < 80000:
                    display_hud()                    
                    screen.blit(hud_images["firebolt"], (760, 1029))
                    screen.blit(tutorial[8], (0,0))
                    if keys.space or keys.enter or keys.numpad_enter:
                        cutscene_start_time = current_time - 80000
                else:
                    display_hud()
                    screen.blit(hud_images["firebolt"], (760, 1029))
                    show_hud = True
                    firebolt.unlocked = True
                    spells.append("firebolt")
                    cutscene3_played = True
                    cutscene_playing = False
                    current = "in game"
            
            elif current[8] == "4":
                current_room.display_room(vincent[form])
                if cutscene_time < 25:
                    if not display_dialogue("vincent", 6):
                        cutscene_start_time = current_time - 25
                elif cutscene_time < 10025:
                    screen.blit(tutorial[9], (0,0))
                    if keys.space or keys.enter or keys.numpad_enter:
                        cutscene_start_time = current_time - 10025
                else:
                    vincent[form].exp += 35
                    number_drop("exp", vincent[form], 35)
                    mean_slime.room = 2
                    mean_slime.moves = ["right" for n in range(100)] + ["down" for n in range(10)]
                    cutscene4_played = True
                    current_room.extras.append(placed_portal)
                    cutscene_playing = False
                    current = "in game"
            
            elif current[8] == "5":
                current_room.display_room(vincent[form])
                if cutscene_time < 10000:
                    screen.blit(tutorial[10], (0,0))
                    if keys.space or keys.enter or keys.numpad_enter:
                        cutscene_start_time = current_time - 10000
                else:
                    cutscene5_played = True
                    cutscene_playing = False
                    current = "in game"
            
            elif current[8] == "7":
                current_room.display_room(vincent[form])
                firebolt.exist(current_room)
                if cutscene_time < 2:
                    if not sound_playing:
                        play_sound("thunder", "sfx")
                        play_sound("portal", "sfx", 0.1, -1)
                        current_room.extras.remove(slime_portal)
                        current_room.extras.remove(placed_portal)
                        current_room.extras.append(portal_burn)
                        current_room.extras.append(portal)
                        portal.x = placed_portal.x - 87
                        portal_burn.x = placed_portal.x - 111
                        portal.y = placed_portal.y - 84
                        portal_burn.y = placed_portal.y - 119
                        current_room.exits.append(Exit((portal_x,portal_y), "left", 3, (5,5)))
                        current_room.exits.append(Exit((portal_x,portal_y), "up", 3, (5,5)))
                        current_room.exits.append(Exit((portal_x,portal_y), "right", 3, (5,5)))
                        current_room.exits.append(Exit((portal_x,portal_y), "down", 3, (5,5)))
                    fade_screen.fill((255,255,255,255*(1-0.5*(cutscene_time))))
                    screen.blit(fade_screen, (0,0))
                else:
                    sound_playing = False
                    cutscene7_played = True
                    cutscene_playing = False
                    current = "in game"
            
            elif current[8] == "8":
                current_room.display_room(vincent[form])                
                screen.blit(zaal_images["zaal"][(frame%6)/3], (current_room.x + 840, current_room.y + 71))
                if cutscene_time < 2:
                    if not sound_playing:
                        play_sound("thunder", "sfx")                            
                    fade_screen.fill((255,255,255,255*(1-0.5*(cutscene_time))))
                    screen.blit(fade_screen, (0,0))
                elif cutscene_time < 10:                    
                    if not display_dialogue("vincent", 1):
                        cutscene_start_time = current_time - 10
                elif cutscene_time < 25:
                    if not display_dialogue("zaal", 0):
                        cutscene_start_time = current_time - 25
                elif cutscene_time < 40:
                    if not display_dialogue("vincent", 7):
                        cutscene_start_time = current_time - 40
                elif cutscene_time < 50:
                    if not display_dialogue("zaal", 1):
                        cutscene_start_time = current_time - 50
                elif cutscene_time < 65:
                    if not display_dialogue("zaal", 2):
                        cutscene_start_time = current_time - 65
                elif cutscene_time < 75:
                    if not display_dialogue("vincent", 8):
                        cutscene_start_time = current_time - 75
                elif cutscene_time < 100:
                    if not display_dialogue("zaal", 3):
                        cutscene_start_time = current_time - 100
                elif cutscene_time < 125:
                    if not display_dialogue("zaal", 4):
                        cutscene_start_time = current_time - 125
                else:
                    play_music("boss", "music", 0.5)
                    firebolt.room = 3
                    cutscene8_played = True
                    cutscene_playing = False
                    current = "in game"
                    
            elif current[8] == "9":
                current_room.display_room(vincent[form])
                if cutscene_time < 2:
                    if not sound_playing:
                        play_sound("thunder", "sfx")                            
                    fade_screen.fill((255,255,255,255*(1-0.5*(cutscene_time))))
                    screen.blit(fade_screen, (0,0))
                else:
                    current = "credits"
            
        elif current == "credits":
            cutscene_time = current_time - cutscene_start_time
            if cutscene_time < 12.0/fps:
                current_room.display_room(vincent[form])
                screen.blit(zaal_images["death"][int(cutscene_time*fps)], (current_room.x + 840, current_room.y + 71))
            elif cutscene_time < 5:
                current_room.display_room(vincent[form])
                fade_screen.fill((0,0,0,51*cutscene_time))
                screen.blit(fade_screen, (0,0))
            else:
                screen.blit(credits_images[7], (0,0))
                if cutscene_time < 7:
                    credits_images[0].set_alpha(127.5*(cutscene_time-5))
                    screen.blit(credits_images[0], (0,0))
                elif cutscene_time < 10:
                    screen.blit(credits_images[0], (0,0))
                elif cutscene_time < 12:
                    credits_images[0].set_alpha(255*(1-0.5*(cutscene_time-10)))
                    screen.blit(credits_images[0], (0,0))
                    
                elif cutscene_time < 14:
                    credits_images[1].set_alpha(127.5*(cutscene_time-12))
                    screen.blit(credits_images[1], (0,0))
                elif cutscene_time < 17:
                    screen.blit(credits_images[1], (0,0))
                elif cutscene_time < 19:
                    credits_images[1].set_alpha(255*(1-0.5*(cutscene_time-17)))
                    screen.blit(credits_images[1], (0,0))
                    
                elif cutscene_time < 21:
                    credits_images[2].set_alpha(127.5*(cutscene_time-19))
                    screen.blit(credits_images[2], (0,0))
                elif cutscene_time < 24:
                    screen.blit(credits_images[2], (0,0))
                elif cutscene_time < 26:
                    credits_images[2].set_alpha(255*(1-0.5*(cutscene_time-24)))
                    screen.blit(credits_images[2], (0,0))
                    
                elif cutscene_time < 28:
                    credits_images[3].set_alpha(127.5*(cutscene_time-26))
                    screen.blit(credits_images[3], (0,0))
                elif cutscene_time < 31:
                    screen.blit(credits_images[3], (0,0))
                elif cutscene_time < 33:
                    credits_images[3].set_alpha(255*(1-0.5*(cutscene_time-31)))
                    screen.blit(credits_images[3], (0,0))
                    
                elif cutscene_time < 35:
                    credits_images[4].set_alpha(127.5*(cutscene_time-33))
                    screen.blit(credits_images[4], (0,0))
                elif cutscene_time < 38:
                    screen.blit(credits_images[4], (0,0))
                elif cutscene_time < 40:
                    credits_images[4].set_alpha(255*(1-0.5*(cutscene_time-38)))
                    screen.blit(credits_images[4], (0,0))
                    
                elif cutscene_time < 42:
                    credits_images[5].set_alpha(127.5*(cutscene_time-40))
                    screen.blit(credits_images[5], (0,0))
                elif cutscene_time < 45:
                    screen.blit(credits_images[5], (0,0))
                elif cutscene_time < 47:
                    credits_images[5].set_alpha(255*(1-0.5*(cutscene_time-45)))
                    screen.blit(credits_images[5], (0,0))
                    
                elif cutscene_time < 49:
                    credits_images[6].set_alpha(127.5*(cutscene_time-47))
                    screen.blit(credits_images[6], (0,0))
                else:
                    screen.blit(credits_images[6], (0,0))
                    if keys.space or keys.enter or keys.numpad_enter:                        
                        cutscene_playing = False
                        current = "main menu" #(maybe), prolly go to credits isnt it
        
        elif current == "dead":
            cutscene_time = current_time - cutscene_start_time
            if cutscene_time < 5:
                current_room.display_room(vincent[form])
                fade_screen.fill((0,0,0,51*cutscene_time))
                screen.blit(fade_screen, (0,0))
            else:
                current = "saves menu"             
                    
        elif current == "in game":
            try:
                if not cutscene0_played:
                    cutscene_playing = True
                    cutscene_start_time = current_time
                    current = "cutscene0"
                elif not cutscene1_played and vincent[form].room == 1 and vincent[form].position[1] < 7 and vincent[form].movement_cooldown == 0:
                    cutscene_playing = True
                    cutscene_start_time = current_time
                    current = "cutscene1"
                elif not cutscene2_played and vincent[form].room == 2 and vincent[form].position[1] < 26 and vincent[form].movement_cooldown == 0:
                    cutscene_playing = True
                    cutscene_start_time = current_time
                    current = "cutscene2"
                elif not cutscene8_played and vincent[form].room == 3:
                    cutscene_playing = True
                    cutscene_start_time = current_time
                    current = "cutscene8"
                else:                    
                    vincent[form].check_death()
                    vincent[form].die()                    
                    firebolt.exist(current_room)
                    if not display_loot_menu:
                        vincent[form].change_orientation()
                        vincent[form].change_position(current_room)
                        vincent[form].check_exit(current_room)
                        
                        if mean_slime.room == current_room.number:
                            mean_slime.check_death()
                            mean_slime.die(kill=True)
                            if vincent[form].alive:
                                mean_slime.find_route(current_room, vincent[form].position)
                            else:
                                mean_slime.find_route(current_room, (vincent[form].position[0]-10, vincent[form].position[1]))                            
                            mean_slime.change_orientation()
                            mean_slime.change_position(current_room)
                            mean_slime.change_image()
                            mean_slime.check_collision(vincent[form])
                        
                    if vincent[form].dead:
                        current = "dead"
                            
                    vincent[form].change_image()                   
                    
                    current_room.display_room(vincent[form])
                    
                    if current_room.number == 3 and not cutscene8_played:
                        screen.fill((0,0,0))
                    
                    if current_room.number == 3 and cutscene8_played and vincent[form].alive:                        
                        inferno.exist(current_room)
                        inferno.use(vincent[form])
                        inferno.cast(vincent[form])
                        if zaal_animation > 0:
                            zaal_animation -= 1
                            screen.blit(zaal_images["attack"][18-zaal_animation], (current_room.x + 840, current_room.y + 71))
                        else:
                            screen.blit(zaal_images["zaal"][(frame%6)/3], (current_room.x + 840, current_room.y + 71))
                        screen.blit(zaal_images["health_back"], (69*(screen_width/1920.0), 80*(screen_height/1080.0)))
                        screen.blit(zaal_images["health"], (69*(screen_width/1920.0), 80*(screen_height/1080.0)), (0,0,zaal_life,52))
                        screen.blit(zaal_images["health_icon"], (1786,0))
                        
                        
                        if firebolt.position in [(10,2), (11,2), (12,2), (10,3), (11,3), (12,3)] and firebolt.alive:
                            damage_dealt = int(firebolt.damage*(0.9 + 0.2*random.random()))
                            zaal_life -= damage_dealt                       
                            number_drop("damage", firebolt, damage_dealt)
                            firebolt.alive = False                
                            
                        if zaal_life <= 0:
                            cutscene_playing = True
                            cutscene_start_time = current_time
                            pygame.mixer.music.stop()
                            current_room.extras.append(portal)
                            portal.x = 900
                            portal.y = 600
                            current = "cutscene9"
                    
                    if display_loot_menu:
                        if not display_loot():
                            display_loot_menu = False
                    elif keys.escape and not show_spellbook:    # Opening the in game options menu upon escape being pressed
                        current = "in game options menu"  
                            
                    if show_hud:
                        display_hud()
                    
                    # Showing number drops
                    for index in range(len(number_drops)):
                        number_drops[index][1] = display_number_drop(number_drops[index])
                    
                    for item in number_drops:
                        if item[1] < item[4]-90:
                            number_drops.remove(item)
                    
                    if show_spellbook:
                        display_spellbook()
                        if mousein(748,825,499,576):
                            screen.blit(tutorial[12], (0,0))
                            if mouse.left and cutscene5_played and not cutscene6_played and vincent[form].skill_points > 0:
                                vincent[form].skill_points -= 1
                                cutscene6_played = True
                        elif mousein(579,656,428,505):
                            screen.blit(tutorial[11], (0,0))
                        if keys.escape or keys.backspace:
                            show_spellbook = False
                    
                    if vincent[form].exp >= 100 and not levelling_up:
                        vincent[form].exp -= 100
                        vincent[form].level += 1
                        vincent[form].skill_points += 1
                        levelling_up = True
                    
                    if levelling_up:                        
                        if levelup_frame < 22:
                            screen.blit(levelup_images[levelup_frame/2], (0,0))
                        elif levelup_frame < 52:                        
                            screen.blit(levelup_images[11], (0,0))
                        elif levelup_frame < 58:
                            screen.blit(levelup_images[(levelup_frame-28)/2], (0,0))
                        else:
                            levelup_frame = 0
                            levelling_up = False
                        levelup_frame += 1
                    
                    if not cutscene5_played and vincent[form].level == 2 and not levelling_up:
                        cutscene_playing = True
                        cutscene_start_time = current_time
                        current = "cutscene5"
                        
                    if mean_slime.dead and not drop in rooms[2].extras and not "slime_chunk" in inventory and not slime_portal in rooms[2].extras:
                        current_room.extras.append(drop)
                        drop.x = current_room.grey_left + current_room.square_size[0]*mean_slime.position[0] - 180
                        drop.y = current_room.grey_up + current_room.square_size[1]*mean_slime.position[1] - 130
                        loot[0] = "slime_chunk"
                        
                    if loot == ["" for nothing in range(6)] and drop in current_room.extras:
                        current_room.extras.remove(drop)
                        mean_slime.position = (-10,-10)
                        
                    
                    if keys.tab and not show_spellbook:
                        show_spellbook = True
                    
                    if keys.e:
                        if not cutscene3_played:
                            if is_interactable((46,20)):
                                current_room.extras.remove(book_item)
                                current_room.extras.remove(book_light)
                                cutscene_playing = True
                                cutscene_start_time = current_time
                                current = "cutscene3"
                        elif not cutscene4_played:
                            if is_interactable((104,25)):
                                cutscene_playing = True
                                cutscene_start_time = current_time
                                current = "cutscene4"
                        elif drop in current_room.extras:
                            if is_interactable(mean_slime.position):
                                display_loot_menu = True
                        elif "slime_chunk" in inventory and is_interactable((portal_x, portal_y)):
                            current_room.extras.append(slime_portal)
                            inventory.remove("slime_chunk")
                            slime_portal.x = placed_portal.x
                            slime_portal.y = placed_portal.y
                            
                    if slime_portal in rooms[2].extras and firebolt.position == (portal_x,portal_y) and firebolt.alive and not cutscene7_played:
                        firebolt.alive = False
                        cutscene_playing = True
                        cutscene_start_time = current_time
                        current = "cutscene7"                                                 
     
                    if keys.one or keys.numpad1:
                        firebolt.use(vincent[form])
                    
                    if keys.r and cutscene4_played and not slime_portal in rooms[2].extras:  # Creating a portal
                        if vincent[form].orientation == "left" and not (vincent[form].position[0]-1, vincent[form].position[1]) in (current_room.blocked + [(104,25)]) and not vincent[form].position[0]-1 < 0:
                            portal_x = vincent[form].position[0]-1
                            portal_y = vincent[form].position[1]                       
                            placed_portal.x = current_room.grey_left + current_room.square_size[0]*portal_x - 27
                            placed_portal.y = current_room.grey_up + current_room.square_size[1]*portal_y - 28
                        elif vincent[form].orientation == "up" and not (vincent[form].position[0], vincent[form].position[1]-1) in (current_room.blocked + [(104,25)]) and not vincent[form].position[1]-1 < 0:
                            portal_y = vincent[form].position[1]-1
                            portal_x = vincent[form].position[0]                       
                            placed_portal.x = current_room.grey_left + current_room.square_size[0]*portal_x - 27
                            placed_portal.y = current_room.grey_up + current_room.square_size[1]*portal_y - 28
                        elif vincent[form].orientation == "right" and not (vincent[form].position[0]+1, vincent[form].position[1]) in (current_room.blocked + [(104,25)]) and not vincent[form].position[0]+1 > current_room.max_coord[0]:
                            portal_x = vincent[form].position[0]+1
                            portal_y = vincent[form].position[1]                       
                            placed_portal.x = current_room.grey_left + current_room.square_size[0]*portal_x - 27
                            placed_portal.y = current_room.grey_up + current_room.square_size[1]*portal_y - 28
                        elif vincent[form].orientation == "down" and not (vincent[form].position[0], vincent[form].position[1]+1) in (current_room.blocked + [(104,25)]) and not vincent[form].position[1]+1 > current_room.max_coord[1]:
                            portal_y = vincent[form].position[1]+1
                            portal_x = vincent[form].position[0]                       
                            placed_portal.x = current_room.grey_left + current_room.square_size[0]*portal_x - 27
                            placed_portal.y = current_room.grey_up + current_room.square_size[1]*portal_y - 28
                    
                
                   
            except Exception as error:
                log(error, "An error occurred in game")
            
        elif current == "exit":
            ongoing = False
    
    ## Displaying an error message if requested
    try:
        if error_time > 0:
            error_time -= 1
            screen.blit(load("error_message.png"), (1320*(screen_width/1920.0), 0))
    except:
        log(error, "Failed to display error message")

    ## Updating the screen
    try:
        frame += 1  # Incrementing the current frame
        pygame.display.flip()   # Updating the screen at the end of blitting
        clock.tick(fps)          # Setting fps limit
    except Exception as error:
        log(error, "Failed to update screen")

### ---------- PROGRAM DISPLAY - END ---------- ###

## Closing and saving the program
try:
    save_game(save_number)
except Exception as error:
    log(error, "Game was unable to autosave on exit")
