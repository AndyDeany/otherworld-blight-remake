# Defining a function to check if the mouse is in a certain area
def mousein(start_x, end_x, start_y, end_y):
    """Takes in coordinates as if it was a 1920x1080 screen"""
    global error
    try:
        if mouse_x > start_x*(screen_width/1920.0) and mouse_x < end_x*(screen_width/1920.0) and mouse_y > start_y*(screen_height/1080.0) and mouse_y < end_y*(screen_height/1080.0):
            return True
        else:
            return False
    except Exception as error:
        log("Unable to determine whether mouse coordinates meet the requirements: " + str(start_x) + " < x < " + str(end_x) + ", " + str(start_y) + " < " + str(end_y))

# Checking if the given arrow key has been held down the longest
def is_longest_held(direction_held_time):
    global error
    try:
        longest = max(leftarrow_held_time, rightarrow_held_time, uparrow_held_time, downarrow_held_time, a_held_time, d_held_time, w_held_time, s_held_time)
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
                    return character.x + (self.square_size[0]*character.movement_cooldown*character.movespeed)/(3*fps)
                elif character.orientation == "right":
                    return character.x - (self.square_size[0]*character.movement_cooldown*character.movespeed)/(3*fps)
                else:
                    return character.x
            elif axis == "y":
                if character.orientation == "up":
                    return character.y + (self.square_size[1]*character.movement_cooldown*character.movespeed)/(3*fps)
                elif character.orientation == "down":
                    return character.y - (self.square_size[1]*character.movement_cooldown*character.movespeed)/(3*fps)
                else:
                    return character.y
        elif file_type == "canvas":
            if axis == "x":
                if character.orientation == "left":
                    return self.x - (self.square_size[0]*character.movement_cooldown*character.movespeed)/(3*fps)
                elif character.orientation == "right":
                    return self.x + (self.square_size[0]*character.movement_cooldown*character.movespeed)/(3*fps)
                else:
                    return self.x
            elif axis == "y":
                if character.orientation == "up":
                    return self.y - (self.square_size[1]*character.movement_cooldown*character.movespeed)/(3*fps)
                elif character.orientation == "down":
                    return self.y + (self.square_size[1]*character.movement_cooldown*character.movespeed)/(3*fps)
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
        else:   # when form = "slime"
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
        or (vincent[form].position == (coordinates[0]-1,coordinates[1]) and vincent[form].orientation == "right")
        or (vincent[form].position == (coordinates[0],coordinates[1]-1) and vincent[form].orientation == "down")
        or (vincent[form].position == (coordinates[0]+1,coordinates[1]) and vincent[form].orientation == "left")
        or (vincent[form].position == (coordinates[0],coordinates[1]+1) and vincent[form].orientation == "up")):
        return True
    else:
        return False

# Defining functinos to show exp drops, damage values and healing values
def number_drop(number_type, character, value):
    """number_type = \"damage\", \"exp\", \"heal\""""
    global error
    try:
        global number_drops
        drop_x = character.x + character.width/2
        drop_y = character.y + character.height/2
        if number_type == "damage":
            colour = (255,0,0)
        elif number_type == "exp":
            colour = (255,215,0)
        elif number_type == "heal":
            colour = (43,255,0)
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
        screen.blit(dropfont.render(number_drop_item[3], True, number_drop_item[2]), (number_drop_item[0], number_drop_item[1]))
        return number_drop_item[1] - 3
    except Exception as error:
        log(error, "Failed to display number drop")


# Defining a function to display current loot on the floor
def display_loot():
    """returns False when the loot menu is closed"""
    global error
    try:
        global loot, current_loot_slot

        if escape or backspace:
            return False

        screen.blit(loot_images["loot" + str(current_loot_slot)], (0,0))

        for index in range(len(loot)):
            if loot[index] != "":
                screen.blit(loot_images[loot[index]], (781, 225 + 89*index))

        screen.blit(loot_images["controls"], (0,0))

        if (uparrow or w) and current_loot_slot > 0:
            current_loot_slot -= 1
        if (downarrow or s) and current_loot_slot < 5:
            current_loot_slot += 1

        if enter and loot[current_loot_slot] != "":
            inventory.append(loot[current_loot_slot])
            loot[current_loot_slot] = ""
        if e:
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
            screen.blit(spellbook_images["spellbook_default"], (0,0))
        else:
            screen.blit(spellbook_images["firebolt1"], (0,0))
        screen.blit(spellbook_images["firebolt_uncharged"], (0,0))
        screen.blit(font.render(str(vincent[form].level), True, (199,189,189)), (610,20))
        screen.blit(font.render(str(vincent[form].skill_points), True, (199,189,189)), (1665,20))
        screen.blit(font.render(str(firebolt.level), True, (142,0,0)), (834,239))
        screen.blit(esc_exit, (0,0))
    except Exception as error:
        log(error, "Failed to display spellbook")

# Defining a function that displays the Heads-up Display (HUD)
def display_hud():
    global error
    try:
        screen.blit(hud_images["expback"], (0,0))
        screen.blit(hud_images["expbar"], (728,951), (0,0,(vincent[form].exp/100.0)*467,130))
        screen.blit(hud_images["hud"], (0,0))
        screen.blit(hud_images["health_orb"], (1025,994+(1-(vincent[form].current_life/float(vincent[form].max_life)))*87), (0,(1-(vincent[form].current_life/float(vincent[form].max_life)))*87,123,(vincent[form].current_life/float(vincent[form].max_life))*87))

        for index in range(len(spells)):
            if abilities[spells[index]].cooldown > 0:
                screen.blit(hud_images[spells[index] + "_cooldown"], (760 + 51*index, 1029))
            else:
                screen.blit(hud_images[spells[index]], (760 + 51*index, 1029))

        for index in range(len(inventory)):
            screen.blit(hud_images[inventory[index]], (964 + 51*index, 1029))
    except Exception as error:
        log(error, "Failed to display heads up display")

# Defining a function that displays dialogue boxes with the respective text
def display_dialogue(character, dialogue_number):
    global error
    try:
        screen.blit(dialogue[character + "box"], (0,0))
        screen.blit(dialogue[character + str(dialogue_number)], (765,895))
        if space or enter or numpadenter:
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
        pygame.mixer.music.set_volume(multiplier*master_volume*volumes[music_type])
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
        sound = pygame.mixer.Sound(file_directory + "Sound Files\\" + name + ".ogg")
        sounds.append(sound)
        sound.set_volume(multiplier*master_volume*volumes[sound_type])
        sound.play(loops)
    except Exception as error:
        log(error, "Failed to play music track: " + name + ".ogg")

# Defining a function to load a save file
def load_game(savefile):
    try:
        save = open(file_directory + "Save Files/" + savefile + ".txt", "r")
        if save.readline()[:-1] == "No save data":
            save.close()
            return
        else:
            save = open(file_directory + "Save Files/" + savefile + ".txt", "r")
            current = save.readline()[:-1]
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
            for setting_value in menus["options menu"].settings:    # Reading in the saved options settings
                setting_value = int(save.readline()[:-1])
            globals().update(locals()) # Making all variables loaded global
    except Exception as error:
        log(error, "Failed to load " + savefile + " correctly")
        raise

# Defining a function to save a save file
def save_game(savefile):
    try:
        save = open(file_directory + "Save Files/" + savefile + ".txt", "w")
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
        for setting_value in menus["options menu"].settings:    # Saving the players option settings
            save.write(str(setting_value) + "\n")
        save.close()
    except Exception as error:
        log(error, "Failed to save game to " + savefile + ".txt")


# Defining a function to delete save files
def deletesave(savefile):
    line_number = 0
    save = open(file_directory + "Save Files/" + savefile + ".txt", "r")
    while True:
        if save.readline() == "\n":
            number_of_lines = line_number
            break
        else:
            line_number += 1
    save.close()

    save = open(file_directory + "Save Files\save" + savefile + ".txt", "w")
    save.write("No save data\n")
    for line in range(number_of_lines - 1):
        save.write("\n")
    save.close()
