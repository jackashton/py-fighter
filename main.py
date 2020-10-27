from tkinter import *
import random

__author__ = "Jack Ashton"
__version__ = "3.0"


class TitleScreen:  # contains attributes and methods for the title screen of the game
    def __init__(self, canvas, canvas_height, canvas_width):
        self.canvas = canvas
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        self.title_image = PhotoImage(file="images/title.gif")  # stores the title image for the game
        self.title = Label(self.canvas, image=self.title_image, borderwidth=0, anchor=NW)  # displays the title image
        self.button_frame = Frame(self.canvas, padx=2.5, pady=2.5)
        self.difficulty_scale = Scale(self.button_frame, from_=1, to_=4, orient=HORIZONTAL)  # used to choose difficulty
        self.instruction_button = Button(self.button_frame, text="INSTRUCTIONS", bg="black", fg="white", font=("", 10),
                                         command=self.display_instructions, takefocus=0)
        # instruction button is configured to hide instructions when they are displayed
        self.instruction_frame = Frame(self.canvas, height=self.canvas_height/2, width=self.canvas_width, padx=2.5, pady=2.5)
        # instruction frame contains all instruction widgets so only the frame needs to be displayed / hidden
        self._instructions = StringVar()  # private variable since instructions should not be modified
        self.instructions_label = Label(self.instruction_frame, justify=LEFT, textvariable=self._instructions,
                                        wraplength=self.canvas_width)
        self.start = False  # this is checked by 'game_process' in Main() to start the game when value is 'True'
        self.start_button = Button(self.button_frame, text="START", bg="black", fg="white", font=("", 10),
                                   command=self.start_game, takefocus=0)

    def display_title_screen(self):  # displays the widgets for the title screen
        self.title.place(x=0, y=0)
        self.button_frame.place(x=(self.canvas_width / 2), y=100, anchor=CENTER)
        self.difficulty_scale.grid(row=1, column=1, columnspan=2)
        self.instruction_button.grid(row=2, column=1)
        self.start_button.grid(row=2, column=2)

    def display_instructions(self):  # displays the instructions and sets the instruction text
        self.instruction_button.config(text="CLOSE INSTRUCTIONS", command=self.remove_instructions)
        # configures instruction button to close instructions if clicked again
        self._instructions.set("""CLICK 'CLOSE INSTRUCTIONS' TO EXIT
    Instructions:
    1: USE a,s,d KEYS TO MOVE PLAYER CHARACTER: a=LEFT MOVEMENT, s=DUCK/DODGE, d=RIGHT MOVEMENT
    2: USE space KEY TO ATTACK ENEMY PLAYERS
    3: ATTACK AND DUCKS WILL STOP MOVEMENT, BE TACTICAL AND BE QUICK OR YOU WILL GET OVERRUN
    4: YOUR OBJECTIVE IS TO DEFEAT ENEMIES AND MAXIMISE YOUR SCORE POINTS, POINTS WILL BE REWARDED FOR DEFEATING AN
    ENEMY, MORE DIFFICULT ENEMIES WILL YIELD MORE POINTS BUT PRESENT A GREATER CHALLENGE AS THEY TAKE MORE HITS TO
    DEFEAT
    5: YOU WILL SUSTAIN DAMAGE FROM ATTACKS AT YOUR PLAYER, WHEN YOU SUSTAIN TOO MUCH DAMAGE THE GAME WILL END, THIS IS
    INDICATED BY YOUR HEALTH BAR IN THE TOP LEFT CORNER OF THE GAME
    6: CLICK 'START' TO PLAY GAME, WHEN THE GAME ENDS YOU WILL BE PROMPTED TO RESTART THE GAME BY CLICKING THE RESTART
    BUTTON
    7: DIFFICULTY DETERMINES THE NUMBERS OF ENEMIES, ENEMY HEALTH, ENEMY ATTACK DAMAGE AND
    OF COURSE POINTS! CHALLENGE YOURSELF FOR THE POTENTIAL OF A GREATER HIGH SCORE
    8: YOU'RE NOT INVINCIBLE, NOBODY CAN LAST FOREVER! YOU WILL STILL SUSTAIN DAMAGE WHEN ATTACKING ENEMIES!""")
        self.instruction_frame.place(x=0, y=self.canvas_height, anchor=SW)
        self.instructions_label.place(x=1, y=1)

    def remove_instructions(self):  # removes instructions
        self.instruction_button.config(text="INSTRUCTIONS", command=self.display_instructions)
        # configures instruction button to default values to display instructions again
        self.instruction_frame.place_forget()  # frame can be placed again when instructions need to be displayed

    def remove_title_screen(self):  # removes the title screen widgets
        self.title.place_forget()
        self.instruction_frame.place_forget()  # removes instructions in case they are visible when user starts game
        self.button_frame.place_forget()   # removes button frame

    def start_game(self):
        self.start = True  # checked by 'game_process' method in Main() to start game when value is 'True'


class Game:  # contains methods and attributes for playing the game
    def __init__(self, canvas, canvas_height, canvas_width, background_animation_speed):
        self.canvas = canvas
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        self.background_animation_speed = background_animation_speed / 10  # converts from milliseconds to s/10
        self._background_iteration_period = self.background_animation_speed
        self.background_image_list = []  # stores frame images for background
        self.current_background_image = ""  # reassigned to currently displayed background image
        self.background_image = self.canvas.create_image(0, 0, image="", anchor=NW)
        self.sprite_list = []  # sprite instances that are active in game are appended here
        self.player_image_list_right = []  # contains images for the player (sprite_type = 1) right movement
        self.player_image_list_left = []  # contains images for the player (sprite_type = 1) left movement
        self.enemy_image_list_right = []  # contains images for enemy animations for right movement
        self.enemy_image_list_left = []  # contains images for enemy animations for left movement
        self.health_bar_left_margin = 10
        self._health_bar_default_width = (self.canvas_width / 2) - self.health_bar_left_margin  # remove 10 to account for left margin of 10
        self._health_bar_default_height = 30
        self.health_bar_rectangle_red = None  # will be reassigned a red rectangle object
        self.health_bar_rectangle_green = None  # will be reassigned a green rectangle object to indicate health
        self.score = 0

    def change_background_image(self):  # animates the background image
        current_image = str(self.current_background_image)
        for i in range(len(self.background_image_list)):  # length of animation
            if current_image == str(self.background_image_list[i]) and self._background_iteration_period == \
                    self.background_animation_speed:  # controls frame rate of image change over
                if (i + 1) == len(self.background_image_list):  # if image will be last in list reset animation
                    self.canvas.itemconfig(self.background_image, image=self.background_image_list[0])
                    self.current_background_image = self.background_image_list[0]
                else:
                    self.canvas.itemconfig(self.background_image, image=self.background_image_list[(i + 1)])
                    self.current_background_image = self.background_image_list[(i + 1)]
                self._background_iteration_period = 0   # reseting this value means next image change will be at the same frame rate as the last
            elif current_image == "" and self._background_iteration_period == self.background_animation_speed:
                # if current image is default value "" then start animation
                self.canvas.itemconfig(self.background_image, image=self.background_image_list[0])
                self.current_background_image = self.background_image_list[0]
                self._background_iteration_period = 0
        self._background_iteration_period += 1

    def create_player(self):  # creates the player sprite
        default_health = 100
        player = Player(self.canvas, self.canvas_width, self.canvas_height, default_health)
        player.health = (0, default_health)  # sets the health value
        player.attack_damage = 25  # sets the attack damage value
        player.set_images(self.player_image_list_right, self.player_image_list_left)
        self.sprite_list.append(player)
        return player

    def create_enemy(self, difficulty):
        if difficulty > 1:  # difficulty determines the types of enemies that the player will face
            sprite_type = random.randint(difficulty, 4)  # greater difficulty reduces range of difficult enemies
        else:
            sprite_type = 2  # sprite type cannot be 1 as a player is always sprite type 1
        enemy = Enemy(self.canvas, self.canvas_width, self.canvas_height, sprite_type)
        # set enemy specific images based off sprite_type
        enemy.set_images(self.enemy_image_list_right, self.enemy_image_list_left)
        self.sprite_list.append(enemy)

    def display_sprites(self, index):  # spawns sprites in the game at certain locations
        sprite = self.sprite_list[index]
        if sprite.visibility is False:  # determines if sprite is visible
            directions = ["right", "left"]  # directions can only be left or right
            if index != 0:  # if sprite is not player
                enemy_sprite_direction = random.choice(directions)
                if enemy_sprite_direction == directions[0]:
                    coordinates = 0  # spawns enemy at left side of screen
                else:
                    coordinates = self.canvas_width - sprite.image_width  # spawns enemy at right side of screen subtracted amount accounts for image width
                sprite.display_sprite(enemy_sprite_direction, image_index=0,
                                      x_coordinates=coordinates)
            else:  # spawns player sprite in center of canvas
                sprite.display_sprite(random.choice(directions), image_index=0,
                                      x_coordinates=self.canvas_width / 2)
            sprite.visibility = True  # stops sprites from being 'spawned' again

    def display_health_bar(self):  # displays the health bar
        # red indicates loss of health, green indicates health remaining
        coordinates_list = [10, 10, self._health_bar_default_width, 35]
        self.health_bar_rectangle_red = self.canvas.create_rectangle(*coordinates_list, fill="red")
        self.health_bar_rectangle_green = self.canvas.create_rectangle(*coordinates_list, fill="green")

    def update_health_bar(self, player):  # updates the player health bar by configuring the coords of the green bar
        health_bar_coords = self.canvas.coords(self.health_bar_rectangle_green)
        if player.health != player.default_health > 0:  # game is currently playing and damage has been taken
            new_health = int(self._health_bar_default_width - ((self._health_bar_default_width / 100) *
                                                               (player.default_health - player.health)))
            self.canvas.coords(self.health_bar_rectangle_green, health_bar_coords[0], health_bar_coords[1], new_health,
                               health_bar_coords[3])
        else:  # game has ended as health is 0 or less so position of health bar must be reset
            self.canvas.coords(self.health_bar_rectangle_green, self.health_bar_left_margin, health_bar_coords[1],
                               self._health_bar_default_width, health_bar_coords[3])

    def update_score(self, enemy_dead, enemy):  # adds the defeated enemies health value to the score
        if enemy_dead is True:
            self.score += enemy.sprite_type * 25  # same method for calculating enemy health

    def find_overlapping(self, player, enemy):  # checks if player is overlapping with enemies
        enemy_bbox = self.canvas.bbox(enemy.sprite_object_image)
        overlapping = self.canvas.find_overlapping(*enemy_bbox)
        return overlapping

    def enemy_attack(self, player, enemy):
        enemy.attack_action(None)  # parameter None passed in place of event parameter filled when player calls function with kepress event
        if enemy.current_image_index == enemy.final_attack_image_index and enemy.image_iteration_period == enemy.animation_speed:  # attack animation is finishing
            player.health = (1, enemy.attack_damage)

    def sprite_interaction(self, player, enemy, overlapping):
        # determines effects on player / enemy depending on sprite attributes when the objects are overlapping
        if player.sprite_object_image in overlapping:
            if player.duck is not True and player.attack is not True:  # enemy can attack and guarentee damage
                self.enemy_attack(player, enemy)
            elif player.attack is True:  # the enemy may decide to duck or attack back, includes randomness in gameplay
                random_action = random.randint(0, 1)  # can only be either attack or duck
                if random_action == 0:
                    enemy.duck_action(None)
                else:
                    self.enemy_attack(player, enemy)

            if player.attack is True and player.image_iteration_period == player.animation_speed and \
                    player.current_image_index == player.final_attack_image_index and enemy.previous_direction != player.previous_direction \
                    and enemy.duck is not True:  # checks attack animation has completed before damage
                enemy.health = (1, player.attack_damage)

    def remove_sprite(self, remove_sprite, sprite):  # removes instances of a sprite from the game
        if remove_sprite is True:
            self.canvas.delete(sprite.sprite_object_image)
            self.sprite_list.remove(sprite)
            del sprite  # deletes sprite instance

    def reset(self):  # resets some of the game attributes to defaults for replayability
        initial_length = len(self.sprite_list)
        # length of sprite_list will change as sprites are removed so initial length is stored
        for i in range(initial_length):  # initial length is used as sprite list length varies as sprites removed
            self.remove_sprite(True, self.sprite_list[0])
        self.canvas.delete(self.health_bar_rectangle_red, self.health_bar_rectangle_green)  # remove health bars


class Sprite:  # contains attributes and methods for a sprite
    def __init__(self, sprite_type):
        self.sprite_type = sprite_type  # determines some sprite attributes
        self.var_health = 0
        self.var_attack_damage = 0
        self.velocity = [0]  # velocity of a sprite stored as y, x. x values are stacked in this list
        self.previous_direction = "right"  # stores the previous direction of movement for determining actions
        self.event = False  # controls whether an attack or duck action can occur
        self.attack = None
        self.duck = None
        self.duck_delay = 0  # is incremented and reassigned to create a delay when a duck action is prompted
        self.ducking_period = 3  # default amount duck_delay must reach when ducking
        self.current_image = None  # stores the current image
        self.default_image_index = 0
        self.current_image_index = self.default_image_index  # stores the current image index for determining next frame of animation
        self.final_walk_image_index = 5
        self.first_duck_image_index = 6
        self.final_duck_image_index = 7
        self.first_attack_image_index = 8
        self.final_attack_image_index = 11
        self.image_list_right = []  # stores images for right movement
        self.image_list_left = []  # stores images for left movement
        self.image_width = 100  # image width by default should be 100
        self.sprite_object_image = None  # stores the canvas image that will be moved in the game
        self.animation_speed = 10  # animation speed of a sprite is constant
        self.image_iteration_period = self.animation_speed
        self.visibility = False  # when True the sprite has been spawned

    def set_images(self, images_right, images_left):  # reassigns the image lists of the parent class
        self.image_list_right = images_right
        self.image_list_left = images_left

    def display_sprite(self, direction, image_index, x_coordinates):  # spawns and displays the sprite pn canvas
        if direction == "right":  # direction determines image direction displayed
            for i in range(len(self.image_list_right)):
                if image_index == i:  # gets the current desired image index for display
                    self.current_image = self.image_list_right[i]
                    self.current_image_index = i
        elif direction == "left":  # direction determines image direction displayed
            for i in range(len(self.image_list_left)):
                if image_index == i:  # gets the current desired image index for display
                    self.current_image = self.image_list_left[i]
                    self.current_image_index = i
        # reassigns variable to value of canvas image created here, this is the object that will be animated and moved
        self.sprite_object_image = self.canvas.create_image(x_coordinates, self.canvas_height, image=self.current_image,
                                                            anchor=SW)

    @property
    def health(self):
        return self.var_health

    @health.setter
    def health(self, health):  # health passed as (operation type, amount)
        if health[0] == 0:  # set health
            self.var_health = health[1]
        else:  # remove health
            self.var_health -= health[1]

    @property
    def attack_damage(self):
        return self.var_attack_damage

    @attack_damage.setter
    def attack_damage(self, attack_damage):
        self.var_attack_damage = attack_damage

    def move(self):  # controls movement and prompts animation changes dependant on the sprites movement
        if abs(self.velocity[-1]) >= 0 and self.canvas_width - self.image_width >= self.canvas.coords(self.sprite_object_image)[0]\
                + self.velocity[-1] >= 0:
            if self.velocity[-1] == self.x_velocity_constant and self.attack is not True and self.duck is not True:
                self.previous_direction = "right"
                self.canvas.move(self.sprite_object_image, self.velocity[-1], self.velocity[0])
                self.sprite_image = self.current_image_index
            elif self.velocity[-1] == -self.x_velocity_constant and self.attack is not True and self.duck is not True:
                self.previous_direction = "left"
                self.canvas.move(self.sprite_object_image, self.velocity[-1], self.velocity[0])
                self.sprite_image = self.current_image_index
            elif self.attack is True:  # stops movement and animates the attack action
                self.sprite_image = self.current_image_index
            elif self.duck is True:  # stops movement and animates the ducking action
                self.sprite_image = self.current_image_index

    def attack_action(self, event):  # called with keypress of space if sprite is player hence event parameter
        if self.event is False:  # if ducking action is not occurring
            self.attack = True
            self.duck = False
            self.event = True  # prevent ducking action from occurring
            self.current_image_index = self.first_attack_image_index

    def duck_action(self, event):  # called with keypress of s if sprite is player hence event parameter
        if self.event is False:  # if attacking action is not occurring
            self.attack = False
            self.duck = True
            self.event = True  # prevent attacking action from occurring
            self.current_image_index = self.first_duck_image_index

    @property
    def sprite_image(self):
        return self.current_image

    @sprite_image.setter
    def sprite_image(self, index):  # animates sprite by changing the current image of the sprite canvas image object
        if self.image_iteration_period == self.animation_speed:
            if index < self.final_walk_image_index:  # if sprite is walking
                self.current_image_index = index + 1
            elif index == self.final_walk_image_index:  # if end of walking animation is reached
                self.current_image_index = self.default_image_index  # resets walking animation
            elif self.first_duck_image_index <= index < self.final_duck_image_index:  # animate ducking action
                self.current_image_index = index + 1
            elif index == self.final_duck_image_index and self.duck_delay == self.ducking_period:  # end ducking action if delay has passed
                self.current_image_index = self.default_image_index  # resets animation to walking
                self.event = False  # cancels the action so attack or duck can occur again
                self.duck = False
                self.duck_delay = self.default_image_index  # resets delay for next ducking action
            elif index == self.final_duck_image_index and self.duck_delay < self.ducking_period:  # create delay for ducking to dodge attacks
                self.duck_delay += 1
            elif self.first_attack_image_index <= index < self.final_attack_image_index:  # animate attacking action
                self.current_image_index = index + 1
            elif index == self.final_attack_image_index:  # attack animation ended
                self.current_image_index = self.default_image_index
                self.event = False  # cancels the action so attack or duck can occur again
                self.attack = False

            # determines which direction of movement to animate
            if self.previous_direction == "left":
                self.current_image = self.image_list_left[self.current_image_index]
                self.canvas.itemconfig(self.sprite_object_image, image=self.current_image)
            elif self.previous_direction == "right":
                self.current_image = self.image_list_right[self.current_image_index]
                self.canvas.itemconfig(self.sprite_object_image, image=self.current_image)
            self.image_iteration_period = 0
        self.image_iteration_period += 1


class Player(Sprite):  # contains player specific attributes and methods for a sprite, inherits from Sprite()
    def __init__(self, canvas, canvas_width, canvas_height, default_health):
        self.canvas = canvas
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.x_velocity_constant = 2.5
        self.default_health = default_health
        Sprite.__init__(self, 1)  # '1' will always be player sprite type

    def on_keypress(self, event):
        print("press", event.keysym, "x velocity", self.velocity)
        if event.keysym == "d" and self.x_velocity_constant not in self.velocity:
            self.velocity.append(self.x_velocity_constant)
        elif event.keysym == "a" and -self.x_velocity_constant not in self.velocity:
            self.velocity.append(-self.x_velocity_constant)

    def on_keyrelease(self, event):
        print("release", event.keysym, "x velocity", self.velocity)
        if event.keysym == "a" and -self.x_velocity_constant in self.velocity:
            self.velocity.remove(-self.x_velocity_constant)
        elif event.keysym == "d" and self.x_velocity_constant in self.velocity:
            self.velocity.remove(self.x_velocity_constant)
        print("finish release", event.keysym, "x velocity", self.velocity)


class Enemy(Sprite):  # contains enemy specific attributes and methods for a sprite, inherits from Sprite()
    def __init__(self, canvas, canvas_width, canvas_height, sprite_type):
        self.canvas = canvas
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.x_velocity_constant = 1.5
        Sprite.__init__(self, sprite_type)
        self.sprite_properties()

    def sprite_properties(self):  # sets enemy sprite health and attack damage based on sprite type
        self.health = (0, self.sprite_type * 25)
        self.attack_damage = self.sprite_type

    def calculate_movement(self, player):  # calculates which direction to move in next towards player
        enemy = self.sprite_object_image
        player_coordinates = self.canvas.coords(player.sprite_object_image)
        enemy_coordinates = self.canvas.coords(enemy)
        distance = enemy_coordinates[0] - player_coordinates[0]  # difference between coordinates
        distance_with_velocity = distance + self.velocity[-1]   # difference between coordinates with enemy velocity to see if enemy gets closer or further away from player with next movement
        if abs(distance_with_velocity) > abs(distance):
            return True
        else:
            return False

    def change_movement(self, swap_movement):  # if the enemy has moved away the movement will be swapped to move them closer
        enemy = self.sprite_object_image
        if self.velocity[-1] == self.x_velocity_constant and swap_movement is True:
            self.velocity.remove(self.x_velocity_constant)
            self.velocity.append(-self.x_velocity_constant)
        elif self.velocity[-1] == -self.x_velocity_constant and swap_movement is True:
            self.velocity.remove(-self.x_velocity_constant)
            self.velocity.append(self.x_velocity_constant)
        else:
            if self.previous_direction == "right" and self.x_velocity_constant not in self.velocity:
                self.velocity.append(self.x_velocity_constant)
            elif self.previous_direction == "left" and -self.x_velocity_constant not in self.velocity:
                self.velocity.append(-self.x_velocity_constant)


class Scoreboard:  # contains methods and attributes of the scoreboard to be displayed at end game
    def __init__(self, canvas, canvas_height, canvas_width):
        self.canvas = canvas
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        self.restart = False  # this is checked by game_process in Main() to restart game
        self.button_frame = Frame(self.canvas, padx=2.5, pady=2.5, bg="red")
        self.score_label = Label(self.button_frame, text="", bg="black", fg="white")  # text will be configured when displayed
        self.difficulty_label = Label(self.button_frame, text="", bg="black", fg="white")   # text will be configured when displayed
        self.restart_button = Button(self.button_frame, text="START", bg="black", fg="white", font=("", 10),
                                     command=self.restart_game, takefocus=0)

    def display_scoreboard(self, player_score, difficulty):  # displays the scoreboard
        difficulty_list = ["SUPER EASY", "MEH, NOT EVEN CHALLENGING", "I COULD STILL DO BETTER THAN THAT",
                           "HARD FOR YOU? EASY FOR ME."]  # gives choices of message to player based on difficulty
        self.button_frame.place(x=(self.canvas_width / 2), y=(self.canvas_height / 2), anchor=CENTER)
        self.score_label.config(text="PLAYER SCORE: {}".format(player_score))
        self.score_label.grid(row=1, column=1)
        self.difficulty_label.config(text="DIFFICULTY: {}".format(difficulty_list[(difficulty-1)]))  # displayes message relevant to difficulty
        self.difficulty_label.grid(row=2, column=1)
        self.restart_button.grid(row=3, column=1)

    def remove_scoreboard(self):  # removes scorebord from screen
        self.button_frame.place_forget()

    def restart_game(self):  # this is checked by game_process in Main() to restart game
        self.restart = True


class Main:
    def __init__(self, tk_window):
        self.window = tk_window
        self.window.title("BEAT 'EM UP")
        self.event_counter = 0
        self.canvas_width = 1024
        self.canvas_height = 490
        self.canvas = Canvas(self.window, width=self.canvas_width, height=self.canvas_height,
                             highlightthickness=0)
        self.title_screen = TitleScreen(self.canvas, self.canvas_height, self.canvas_width)
        self.game = Game(self.canvas, self.canvas_height, self.canvas_width, 100)
        self.scoreboard = Scoreboard(self.canvas, self.canvas_height, self.canvas_width)
        self.asset_list = ["giphy-6", "player", "player-left-move", "enemy", "enemy-left-move"]
        self.game_difficulty = None  # difficulty is set here to be used in the game after chosen by user in title screen
        self.player = None  # this will be assigned to the player instance when game is set up

    def bind_keys(self):
        # first item in sprite_list is always the player sprite
        self.window.bind('<KeyPress-a>', self.player.on_keypress)
        self.window.bind('<KeyRelease-a>', self.player.on_keyrelease)
        self.window.bind('<KeyPress-d>', self.player.on_keypress)
        self.window.bind('<KeyRelease-d>', self.player.on_keyrelease)
        self.window.bind('<KeyPress-space>', self.player.attack_action)
        self.window.bind('<KeyPress-s>', self.player.duck_action)
        self.window.bind('Alt-s', lambda: None)  # prevents tkinter menu from popping up when alt is pressed

    def load_assets(self):  # loads and stores images, can load any length gif.
        # allow this function to load images from multiple files / directories and store in different vars
        frames = []
        frame_counter = 0
        print("LOADING ASSETS")
        for item in self.asset_list:
            while True:
                try:
                    frames.append(PhotoImage(file="images/{}.gif".format(item), format="gif -index {}"
                                             .format(frame_counter)))
                    frame_counter += 1
                except TclError:
                    break

            if item == self.asset_list[0]:
                self.game.background_image_list = frames
            # all image assets for sprites must be stored as follows
            # 0, 5 walking & 6, 7 ducking & 8, 11 attacking
            elif item == self.asset_list[1]:
                self.game.player_image_list_right = frames
            elif item == self.asset_list[2]:
                self.game.player_image_list_left = frames
            elif item == self.asset_list[3]:
                self.game.enemy_image_list_right = frames
                print(len(frames))
            elif item == self.asset_list[4]:
                self.game.enemy_image_list_left = frames
                print(len(frames))
            # resets variables to be able to load more images and store them in game
            frames = []
            frame_counter = 0

    def create_enemies(self):  # creates enemies based on difficulty
        number_of_enemies = self.game_difficulty  # difficulty determines number in game
        while len(self.game.sprite_list) < number_of_enemies + 1:  # add one for player already in sprite_list
            self.game.create_enemy(self.game_difficulty)

    def game_process(self):  # controls game events and flow across different game states
        if self.event_counter == 0:  # this function only runs once to set up game initally
            print("Title Screen displayed")
            self.canvas.pack()
            self.load_assets()  # loads asset images for use in game
            self.event_counter += 1

        elif self.event_counter == 1:  # displays menu
            self.title_screen.display_title_screen()
            self.event_counter += 1

        elif self.title_screen.start is True and self.event_counter == 2:  # removes title screen when game starts
            print("Title Screen removed")
            self.title_screen.remove_title_screen()
            self.game_difficulty = self.title_screen.difficulty_scale.get()
            print("GAME DIFFICULTY: {}".format(self.game_difficulty))
            self.event_counter += 1

        elif self.event_counter == 3:  # set up the game
            print("Running Game setup")
            self.game.display_health_bar()
            self.player = self.game.create_player()  # player is always created before enemy sprites
            self.create_enemies()
            self.bind_keys()  # binds keys for player movement
            self.event_counter += 1

        elif self.event_counter == 4 and self.player.health > 0:  # while game is not over
            self.game.change_background_image()  # animate background image
            sprite_list = len(self.game.sprite_list)
            for i in range(len(self.game.sprite_list)):
                self.game.display_sprites(i)
                if self.game.sprite_list[i] != self.player:  # controls actions of enemies in game
                    enemy = self.game.sprite_list[i]  # stores enemy
                    enemy_velocity_change = enemy.calculate_movement(self.player)
                    enemy.change_movement(enemy_velocity_change)
                    enemy.move()  # moves enemy based on calculated dynamic movement in response to player actions
                    overlapping = self.game.find_overlapping(self.player, enemy)
                    self.game.sprite_interaction(self.player, enemy, overlapping)  # determines interactions between player and enemy depending on if they are overlapping
                    if enemy.health <= 0:
                        enemy_dead = True
                    else:
                        enemy_dead = False
                    self.game.update_score(enemy_dead, enemy)  # updates score if enemy is defeated
                    self.game.remove_sprite(enemy_dead, enemy)  # removes enemy if it is defeated
                    if len(self.game.sprite_list) < sprite_list:  # if an enemy has been defeated and removed
                        self.game.create_enemy(self.game_difficulty)  # replace dead enemy
                        break  # breaks loop when enemy is removed from game
                else:
                    self.player.move()
                self.game.update_health_bar(self.player)  # updates the health bar

        elif self.event_counter == 4 and self.player.health <= 0:  # checks game has finished
            print("Reset game all game values to default")
            self.game.update_health_bar(self.player)  # resets health bar
            self.game.reset()  # resets the game values
            self.title_screen.start = False  # resets game menu
            self.event_counter += 1

        elif self.event_counter == 5:  # displays the scoreboard
            self.scoreboard.display_scoreboard(self.game.score, self.game_difficulty)
            self.event_counter += 1

        elif self.scoreboard.restart is True and self.event_counter == 6:
            self.scoreboard.restart = False
            self.scoreboard.remove_scoreboard()
            self.game.score = 0
            self.event_counter = 1  # restarts game

        self.window.after(10, self.game_process)


window = Tk()
MAIN = Main(window)
MAIN.game_process()
window.mainloop()
