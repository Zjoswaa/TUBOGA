import pygame as pg
import random

from player import Player
from questions import *
from famousperson import *


class Game:
    def __init__(self, width, height, title):
        self.rig_dices = False
        # PyGame initialization
        pg.init()
        self.screen = pg.display.set_mode((width, height))
        pg.display.set_caption(title)
        pg.display.set_icon(pg.image.load("res/icon.png"))

        # Game logic variables
        self.window_width = width
        self.window_height = height
        self.state_stack = []

        self.font_200 = pg.font.Font("res/fonts/pixeltype.ttf", 200)
        self.font_100 = pg.font.Font("res/fonts/pixeltype.ttf", 100)
        self.font_50 = pg.font.Font("res/fonts/pixeltype.ttf", 50)
        self.font_40 = pg.font.Font("res/fonts/pixeltype.ttf", 40)
        self.font_24 = pg.font.Font("res/fonts/pixeltype.ttf", 25)

        self.bg_color = (150, 150, 170)
        self.text_color = (0, 0, 0)
        self.color_red = (255, 0, 0)
        self.color_purple = (112, 48, 160)
        self.color_blue = (0, 176, 240)
        self.color_brown = (198, 89, 17)
        self.color_yellow = (255, 255, 0)
        self.color_green = (146, 208, 80)
        self.color_gray = (100, 100, 100)
        self.p1_color = (250, 117, 24)
        self.p2_color = (252, 15, 192)
        self.coords = [(500, 560), (450, 560), (400, 560), (350, 560), (300, 560), (250, 560), (200, 560), (150, 560), (100, 560), (50, 560), (50, 510),  # Bottom
                       (50, 460), (50, 410), (50, 360), (50, 310), (50, 260), (50, 210), (50, 160), (50, 110),  # Left
                       (100, 110), (150, 110), (200, 110), (250, 110), (300, 110), (350, 110), (400, 110), (450, 110), (500, 110),  # Top
                       (500, 160), (500, 210), (500, 260), (500, 310), (500, 360), (500, 410), (500, 460), (500, 510)]  # Right

        # This keeps track of the most recent events
        self.log = []
        self.max_log_size = 8

        self.clock = pg.time.Clock()
        self.fps = 60

        self.d1_text = self.font_200.render("0", False, "Black").convert()
        self.d2_text = self.font_200.render("0", False, "Black").convert()

        self.pause_icon = pg.image.load("res/icon.png").convert_alpha()

        self.p1 = Player()
        self.p2 = Player()

        self.p1_money_text = self.font_40.render(f"${self.p1.money}", False, self.p1_color).convert()
        self.p2_money_text = self.font_40.render(f"${self.p2.money}", False, self.p2_color).convert()
        self.left_to_buy_text = self.font_50.render("Left to buy this turn: ", False, "White").convert()
        self.nums_in_word_text = self.font_50.render("Number that are in the word: 0", False, "Black").convert()
        self.nums_correct_text = self.font_50.render("Numbers in the correct spot: 0", False, "Black").convert()
        self.guesses_left_text = self.font_50.render("Guesses left: ", False, "Black").convert()

        self.dice_rolls = [0, 0]

        self.min_break_free_roll = 6  # minimum number you need to roll to break out of jail.

        self.round_stages = ["P1_ANNOUNCE_ROLL", "P1_WAIT_FOR_ROLL", "P1_MOVE", "P1_ACTION", "P2_ANNOUNCE_ROLL", "P2_WAIT_FOR_ROLL", "P2_MOVE", "P2_ACTION"]
        self.current_round_stage = 0

        self.chances = [(400, 600), (250, 350), (200, 300), (75, 125), (20, 60), (-1, 1), (-75, -25), (-100, -50), (-350, -300), (-450, -250)]

        self.resell_percentage = 0.8

        self.query_reward = (100, 200)
        self.event_reward = (250, 750)
        self.famous_reward = (100, 250)

        self.computer_price = 1000

        self.back_at_start_reward = (50, 100)

        self.max_event_guesses = 9

        self.event_answer = ""

    # Shows the start menu
    def start(self):
        hint_clock = 0
        hint_blink_speed = 30
        hint_black = True
        hint_color = (0, 0, 0)
        play_button = pg.Rect((80, 500), (200, 100))
        play_text = self.font_100.render("Play", False, self.color_brown).convert()
        quit_button = pg.Rect((1000, 500), (200, 100))
        quit_text = self.font_100.render("Quit", False, self.color_purple).convert()
        hint_text = [self.font_50.render("Press any key to play", False, hint_color).convert(),
                     self.font_50.render("ESC to quit", False, self.text_color).convert()]

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit(0)
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if quit_button.collidepoint(pg.mouse.get_pos()):
                        pg.quit()
                        exit(0)
                    elif play_button.collidepoint(pg.mouse.get_pos()):
                        # Go to main game loop
                        self.state_stack.append("GAME")
                        self.game()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        exit(0)
                    else:  # Any key pressed except escape
                        # Go to main game loop
                        self.state_stack.append("GAME")
                        self.game()

            # Update

            hint_clock += 1
            if hint_clock == hint_blink_speed:
                hint_clock = 0
                hint_black = not hint_black

            # Render

            self.screen.fill(self.bg_color)
            # Play button and text
            pg.draw.rect(self.screen, self.color_green, play_button)
            if play_button.collidepoint(pg.mouse.get_pos()):
                play_text = self.font_100.render("Play", False, self.color_blue).convert()
            else:
                play_text = self.font_100.render("Play", False, self.color_brown).convert()
            self.screen.blit(play_text, play_text.get_rect(center=(play_button.centerx + 5, play_button.centery + 5)))
            # Quit button and text
            pg.draw.rect(self.screen, self.color_red, quit_button)
            if quit_button.collidepoint(pg.mouse.get_pos()):
                quit_text = self.font_100.render("Quit", False, self.color_yellow).convert()
            else:
                quit_text = self.font_100.render("Quit", False, self.color_purple).convert()
            self.screen.blit(quit_text, quit_text.get_rect(center=(quit_button.centerx + 5, quit_button.centery + 5)))
            # Game icon
            self.screen.blit(self.pause_icon, self.pause_icon.get_rect(center=(self.window_width / 2, self.window_height / 2)))
            # Button press hint text
            if hint_black:
                hint_color = (0, 0, 0)
            else:
                hint_color = (255, 255, 255)
            hint_text[0] = self.font_50.render("Press any key to play", False, hint_color).convert()
            self.screen.blit(hint_text[0], hint_text[0].get_rect(center=(self.window_width / 2, 200)))
            # ESC to quit text
            self.screen.blit(hint_text[1], hint_text[1].get_rect(center=(self.window_width / 2, 525)))
            # PyGame Render
            pg.display.update()
            self.clock.tick(self.fps)

    # Shows the pause menu
    def pause(self):
        paused_text = self.font_100.render("Paused", False, self.text_color).convert()
        return_button = pg.Rect((80, 500), (250, 100))
        return_text = self.font_100.render("Return", False, self.color_brown).convert()
        quit_button = pg.Rect((1000, 500), (200, 100))
        quit_text = self.font_100.render("Quit", False, self.color_purple).convert()

        while self.state_stack[-1] == "PAUSE":
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit(0)
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if quit_button.collidepoint(pg.mouse.get_pos()):
                        pg.quit()
                        exit(0)
                    elif return_button.collidepoint(pg.mouse.get_pos()):
                        # Go back to previous state
                        self.state_stack.pop()
                        break
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        # Go back to previous state
                        self.state_stack.pop()
                        break

            # Update

            # Render

            self.screen.fill(self.bg_color)
            # Paused text
            self.screen.blit(paused_text, paused_text.get_rect(center=(self.window_width / 2, 100)))
            # Return button
            pg.draw.rect(self.screen, self.color_green, return_button)
            if return_button.collidepoint(pg.mouse.get_pos()):
                return_text = self.font_100.render("Return", False, self.color_blue).convert()
            else:
                return_text = self.font_100.render("Return", False, self.color_brown).convert()
            self.screen.blit(return_text, return_text.get_rect(center=(return_button.centerx + 5, return_button.centery + 5)))
            # Quit button
            pg.draw.rect(self.screen, self.color_red, quit_button)
            if quit_button.collidepoint(pg.mouse.get_pos()):
                quit_text = self.font_100.render("Quit", False, self.color_yellow).convert()
            else:
                quit_text = self.font_100.render("Quit", False, self.color_purple).convert()
            self.screen.blit(quit_text, quit_text.get_rect(center=(quit_button.centerx + 5, quit_button.centery + 5)))
            # Game icon
            self.screen.blit(self.pause_icon, self.pause_icon.get_rect(center=(self.window_width / 2, self.window_height / 2)))
            # PyGame Render
            pg.display.update()
            self.clock.tick(self.fps)

    # Shows the game
    def game(self):
        tile_size = 50
        tiles = ["START", "NONE", "EVENT", "NONE", "NONE", "QUERY", "NONE", "FAMOUS", "NONE", "SHOP", "NONE", "CHANCE", "NONE", "NONE", "QUERY", "NONE", "RANDOM",
                 "NONE", "JAIL", "NONE", "EVENT", "NONE", "NONE", "QUERY", "NONE", "FAMOUS", "NONE", "SHOP", "NONE", "CHANCE", "NONE", "NONE", "QUERY", "NONE", "RANDOM", "NONE"]

        legend_text = [self.font_24.render("Start", False, self.color_yellow).convert(),
                       self.font_24.render("Shop", False, self.color_red).convert(),
                       self.font_24.render("Query", False, self.color_blue).convert(),
                       self.font_24.render("Chance", False, self.color_purple).convert(),
                       self.font_24.render("Event", False, self.color_green).convert(),
                       self.font_24.render("Jail", False, "Black").convert(),
                       self.font_24.render("Famous Person", False, self.color_gray).convert(),
                       self.font_24.render("Random Item", False, self.color_brown).convert()]

        while self.state_stack[-1] == "GAME":
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit(0)
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        # Show pause menu
                        self.state_stack.append("PAUSE")
                        self.pause()
                    elif event.key == pg.K_SPACE:
                        if self.round_stages[self.current_round_stage] == "P1_WAIT_FOR_ROLL":
                            self.p1.has_done_query_this_turn = False
                            self.p1.has_done_event_this_turn = False
                            self.p1.has_done_famous_this_turn = False
                            self.p1.has_sold_computer_this_turn = False
                            self.p1.items_bought_this_turn = 0
                            self.p1.guesses_done_this_turn = 0
                            if self.p1.jailed:
                                self.dice_roll()
                                if sum(self.dice_rolls) < 6:  # if jailed, roll a break-free dice, if less than 6 he does not break free
                                    self.add_to_log(f"P1 Roll: {self.dice_rolls[0] + self.dice_rolls[1]}, didn't break free", (0, 0, 0))
                                else:
                                    self.add_to_log(f"P1 Roll: {self.dice_rolls[0] + self.dice_rolls[1]}, broke free", (0, 0, 0))
                                    self.p1.position += 1
                            else:
                                self.dice_roll()
                                self.add_to_log(f"P1 Roll: {self.dice_rolls[0] + self.dice_rolls[1]}", self.p1_color)
                            self.next_round_stage()
                        elif self.round_stages[self.current_round_stage] == "P2_WAIT_FOR_ROLL":
                            self.p2.has_done_query_this_turn = False
                            self.p2.has_done_event_this_turn = False
                            self.p2.has_done_famous_this_turn = False
                            self.p2.has_sold_computer_this_turn = False
                            self.p2.items_bought_this_turn = 0
                            self.p2.guesses_done_this_turn = 0
                            if self.p2.jailed:
                                self.dice_roll()
                                if sum(self.dice_rolls) < self.min_break_free_roll:  # if jailed, roll a break-free dice, if less than 6 he does not break free
                                    self.add_to_log(f"P2 Roll: {self.dice_rolls[0] + self.dice_rolls[1]}, didn't break free", (0, 0, 0))
                                else:
                                    self.add_to_log(f"P2 Roll: {self.dice_rolls[0] + self.dice_rolls[1]}, broke free", (0, 0, 0))
                                    self.p2.position += 1
                            else:
                                self.dice_roll()
                                self.add_to_log(f"P2 Roll: {self.dice_rolls[0] + self.dice_rolls[1]}", self.p2_color)
                            self.next_round_stage()
                        break
                    elif event.key == pg.K_1:
                        self.p1.position = (self.p1.position + 1) % 36
                        break
                    elif event.key == pg.K_2:
                        self.p2.position = (self.p2.position + 1) % 36
                        break
                    elif event.key == pg.K_b:
                        if self.round_stages[self.current_round_stage] == "P1_WAIT_FOR_ROLL" and self.p1.position == 9 or self.p1.position == 27:
                            self.state_stack.append("SHOP")
                            self.shop(1)
                        elif self.round_stages[self.current_round_stage] == "P2_WAIT_FOR_ROLL" and self.p2.position == 9 or self.p2.position == 27:
                            self.state_stack.append("SHOP")
                            self.shop(2)
                    elif event.key == pg.K_q:
                        if self.round_stages[self.current_round_stage] == "P1_WAIT_FOR_ROLL" and self.p1.position in [5, 14, 23, 32] and not self.p1.has_done_query_this_turn:
                            self.state_stack.append("QUERY")
                            self.query(1)
                        elif self.round_stages[self.current_round_stage] == "P2_WAIT_FOR_ROLL" and self.p2.position in [5, 14, 23, 32] and not self.p2.has_done_query_this_turn:
                            self.state_stack.append("QUERY")
                            self.query(2)
                    elif event.key == pg.K_e:
                        if self.round_stages[self.current_round_stage] == "P1_WAIT_FOR_ROLL" and self.p1.position in [2, 20] and not self.p1.has_done_event_this_turn:
                            self.state_stack.append("EVENT")
                            self.event(1)
                        elif self.round_stages[self.current_round_stage] == "P2_WAIT_FOR_ROLL" and self.p2.position in [2, 20] and not self.p2.has_done_event_this_turn:
                            self.state_stack.append("EVENT")
                            self.event(2)
                    elif event.key == pg.K_f:
                        if self.round_stages[self.current_round_stage] == "P1_WAIT_FOR_ROLL" and self.p1.position in [7, 25] and not self.p1.has_done_famous_this_turn:
                            self.state_stack.append("FAMOUS")
                            self.famous(1)
                        elif self.round_stages[self.current_round_stage] == "P2_WAIT_FOR_ROLL" and self.p2.position in [7, 25] and not self.p2.has_done_famous_this_turn:
                            self.state_stack.append("FAMOUS")
                            self.famous(2)

            # Update

            # Render
            self.screen.fill(self.bg_color)
            # Render the board
            for i in range(len(tiles)):
                if tiles[i] == "NONE":
                    pg.draw.rect(self.screen, "White", pg.Rect(self.coords[i][0], self.coords[i][1], tile_size, tile_size))
                elif tiles[i] == "JAIL":
                    pg.draw.rect(self.screen, "Black", pg.Rect(self.coords[i][0], self.coords[i][1], tile_size, tile_size))
                elif tiles[i] == "START":
                    pg.draw.rect(self.screen, self.color_yellow, pg.Rect(self.coords[i][0], self.coords[i][1], tile_size, tile_size))
                elif tiles[i] == "SHOP":
                    pg.draw.rect(self.screen, self.color_red, pg.Rect(self.coords[i][0], self.coords[i][1], tile_size, tile_size))
                elif tiles[i] == "QUERY":
                    pg.draw.rect(self.screen, self.color_blue, pg.Rect(self.coords[i][0], self.coords[i][1], tile_size, tile_size))
                elif tiles[i] == "CHANCE":
                    pg.draw.rect(self.screen, self.color_purple, pg.Rect(self.coords[i][0], self.coords[i][1], tile_size, tile_size))
                elif tiles[i] == "EVENT":
                    pg.draw.rect(self.screen, self.color_green, pg.Rect(self.coords[i][0], self.coords[i][1], tile_size, tile_size))
                elif tiles[i] == "FAMOUS":
                    pg.draw.rect(self.screen, self.color_gray, pg.Rect(self.coords[i][0], self.coords[i][1], tile_size, tile_size))
                elif tiles[i] == "RANDOM":
                    pg.draw.rect(self.screen, self.color_brown, pg.Rect(self.coords[i][0], self.coords[i][1], tile_size, tile_size))

            # Render the legend
            for i in range(len(legend_text)):
                self.screen.blit(legend_text[i], legend_text[i].get_rect(topleft=(560, (i * 50) + 175)))

            # Render the players
            if self.p1.position == self.p2.position:  # if both players are on the same tile
                pg.draw.circle(self.screen, self.p1_color, (self.coords[self.p1.position][0] + 15, self.coords[self.p1.position][1] + 15), 10)
                pg.draw.circle(self.screen, (70, 70, 70), (self.coords[self.p1.position][0] + 15, self.coords[self.p1.position][1] + 15), 10, 2)
                pg.draw.circle(self.screen, self.p2_color, (self.coords[self.p2.position][0] + 35, self.coords[self.p2.position][1] + 35), 10)
                pg.draw.circle(self.screen, (70, 70, 70), (self.coords[self.p2.position][0] + 35, self.coords[self.p2.position][1] + 35), 10, 2)
            else:
                pg.draw.circle(self.screen, self.p1_color, (self.coords[self.p1.position][0] + 25, self.coords[self.p1.position][1] + 25), 10)
                pg.draw.circle(self.screen, (70, 70, 70), (self.coords[self.p1.position][0] + 25, self.coords[self.p1.position][1] + 25), 10, 2)
                pg.draw.circle(self.screen, self.p2_color, (self.coords[self.p2.position][0] + 25, self.coords[self.p2.position][1] + 25), 10)
                pg.draw.circle(self.screen, (70, 70, 70), (self.coords[self.p2.position][0] + 25, self.coords[self.p2.position][1] + 25), 10, 2)

            # Render the dice numbers
            self.screen.blit(self.d1_text, self.d1_text.get_rect(midleft=(188, 380)))
            self.screen.blit(self.d2_text, self.d2_text.get_rect(midleft=(350, 380)))

            # Render the player inventories
            self.screen.blit(self.p1_money_text, (10, 10))
            self.screen.blit(self.p2_money_text, (10, 40))

            # Render the message log
            for i in range(len(self.log)):
                self.screen.blit(self.log[i], self.log[i].get_rect(topleft=(700, (i * 50) + 20)))

            if self.round_stages[self.current_round_stage] == "P1_ANNOUNCE_ROLL":
                if self.p1.jailed:
                    self.add_to_log("P1 is jailed, press space to attempt breakout", self.p1_color)
                else:
                    if self.p1.position in [9, 27]:
                        self.add_to_log("P1, press space to roll dice, B to shop", self.p1_color)
                    elif self.p1.position in [5, 14, 23, 32]:
                        self.add_to_log("P1, press space to roll dice, Q for query", self.p1_color)
                    elif self.p1.position in [2, 20]:
                        self.add_to_log("P1, press space to roll dice, E for event", self.p1_color)
                    elif self.p1.position in [7, 25]:
                        self.add_to_log("P1, press space to roll dice, F for famous", self.p1_color)
                    else:
                        self.add_to_log("P1, press space to roll dice", self.p1_color)
                self.next_round_stage()
            elif self.round_stages[self.current_round_stage] == "P1_MOVE":
                if not self.p1.jailed:
                    # Move the player
                    self.p1.position = (self.p1.position + (self.dice_rolls[0] + self.dice_rolls[1])) % 36
                    # Increase player money by product of rolls
                    self.p1.money += (self.dice_rolls[0] * self.dice_rolls[1])
                    self.p1_money_text = self.font_40.render(f"${self.p1.money}", False, self.p1_color).convert()
                elif self.p1.position == 19:
                    self.p1.jailed = False
                self.next_round_stage()
            elif self.round_stages[self.current_round_stage] == "P1_ACTION":
                # self.add_to_log(f"P1 is on tile: {self.p1.position}", self.p1_color)
                if self.p1.position == 18:  # if p1 landed on jail tile
                    self.p1.jailed = True
                    self.add_to_log("P1 is in jail", (0, 0, 0))
                elif self.p1.position == 16 or self.p1.position == 34:  # random item tile
                    item = random.choice(list(self.p1.components.keys()))
                    self.add_to_log(f"P1 got: {item}", self.color_brown)
                    self.p1.components[item] += 1
                    print(f"P1: {self.p1.components}")
                elif self.p1.position == 11 or self.p1.position == 29:  # chance tile
                    self.chance(1)
                elif self.p1.position == 2 or self.p1.position == 20:  # Event tile
                    self.add_to_log(f"P1 is on tile: {self.p1.position}", self.color_green)
                elif self.p1.position == 7 or self.p1.position == 25:  # Famous person tile
                    self.add_to_log(f"P1 is on tile: {self.p1.position}", self.color_gray)
                elif self.p1.position == 5 or self.p1.position == 14 or self.p1.position == 23 or self.p1.position == 32:  # Query tile
                    self.add_to_log(f"P1 is on tile: {self.p1.position}", self.color_blue)
                elif self.p1.position == 9 or self.p1.position == 27:  # Shop tile
                    self.add_to_log(f"P1 is on tile: {self.p1.position}", self.color_red)
                elif self.p1.position == 0:  # Start tile
                    reward = random.randint(self.back_at_start_reward[0], self.back_at_start_reward[1])
                    self.add_to_log(f"P1 is back at start, +${reward}", self.color_yellow)
                    self.p1.money += reward
                    self.p1_money_text = self.font_40.render(f"${self.p1.money}", False, self.p1_color).convert()

                self.next_round_stage()
            elif self.round_stages[self.current_round_stage] == "P2_ANNOUNCE_ROLL":
                if self.p2.jailed:
                    self.add_to_log("P2 is jailed, press space to attempt breakout", self.p2_color)
                else:
                    if self.p2.position in [9, 27]:
                        self.add_to_log("P2, press space to roll dice, B to shop", self.p2_color)
                    elif self.p2.position in [5, 14, 23, 32]:
                        self.add_to_log("P2, press space to roll dice, Q for query", self.p2_color)
                    elif self.p2.position in [2, 20]:
                        self.add_to_log("P2, press space to roll dice, E for event", self.p2_color)
                    elif self.p2.position in [7, 25]:
                        self.add_to_log("P2, press space to roll dice, F for famous", self.p2_color)
                    else:
                        self.add_to_log("P2, press space to roll dice", self.p2_color)
                self.next_round_stage()
            elif self.round_stages[self.current_round_stage] == "P2_MOVE":
                if not self.p2.jailed:
                    # Move the player
                    self.p2.position = (self.p2.position + (self.dice_rolls[0] + self.dice_rolls[1])) % 36
                    # Increase player money by product of rolls
                    self.p2.money += (self.dice_rolls[0] * self.dice_rolls[1])
                    self.p2_money_text = self.font_40.render(f"${self.p2.money}", False, self.p2_color).convert()
                elif self.p2.position == 19:
                    self.p2.jailed = False
                self.next_round_stage()
            elif self.round_stages[self.current_round_stage] == "P2_ACTION":
                # self.add_to_log(f"P2 is on tile: {self.p2.position}", self.p2_color)
                if self.p2.position == 18:  # if p2 landed on jail tile
                    self.p2.jailed = True
                    self.add_to_log("P2 is in jail", (0, 0, 0))
                elif self.p2.position == 16 or self.p2.position == 34:  # random item tile
                    item = random.choice(list(self.p2.components.keys()))
                    self.add_to_log(f"P2 got: {item}", self.color_brown)
                    self.p2.components[item] += 1
                    print(f"P2: {self.p2.components}")
                elif self.p2.position == 11 or self.p2.position == 29:  # chance tile
                    self.chance(2)
                elif self.p2.position == 2 or self.p2.position == 20:  # Event tile
                    self.add_to_log(f"P2 is on tile: {self.p2.position}", self.color_green)
                elif self.p2.position == 7 or self.p2.position == 25:  # Famous person tile
                    self.add_to_log(f"P2 is on tile: {self.p2.position}", self.color_gray)
                elif self.p2.position == 5 or self.p2.position == 14 or self.p2.position == 23 or self.p2.position == 32:  # Query tile
                    self.add_to_log(f"P2 is on tile: {self.p2.position}", self.color_blue)
                elif self.p2.position == 9 or self.p2.position == 27:  # Shop tile
                    self.add_to_log(f"P2 is on tile: {self.p1.position}", self.color_red)
                elif self.p2.position == 0:  # Start tile
                    reward = random.randint(self.back_at_start_reward[0], self.back_at_start_reward[1])
                    self.add_to_log(f"P2 is back at start, +${reward}", self.color_yellow)
                    self.p2.money += reward
                    self.p2_money_text = self.font_40.render(f"${self.p2.money}", False, self.p2_color).convert()

                self.next_round_stage()

            pg.display.update()
            self.clock.tick(self.fps)

    def dice_roll(self):
        # Roll 2 random numbers
        if not self.rig_dices:
            self.dice_rolls[0] = random.randint(1, 6)
            self.dice_rolls[1] = random.randint(1, 6)
        else:
            self.dice_rolls[0] = 1
            self.dice_rolls[1] = 1

        # Update the display
        self.d1_text = self.font_200.render(str(self.dice_rolls[0]), False, "Black").convert()
        self.d2_text = self.font_200.render(str(self.dice_rolls[1]), False, "Black").convert()

    def add_to_log(self, message, color=(0, 0, 0)):
        if len(self.log) >= self.max_log_size:
            del self.log[0]
        self.log.append(self.font_40.render(message, False, color).convert())

    def next_round_stage(self):
        self.current_round_stage = (self.current_round_stage + 1) % len(self.round_stages)

    def chance(self, player):
        if not self.rig_dices:
            item = random.randrange(0, len(self.chances))
        else:
            item = 8
        gain = random.randint(self.chances[item][0], self.chances[item][1])
        relatives = ["mom's", "dad's", "grandma's", "grandpa's"]
        # injury = ["broken leg", "broken arm", "broken foot", "broken hand"]
        food = ["lunch", "breakfast", "dinner"]
        if player == 1:
            if item == 0:
                self.add_to_log(f"P1 won the lottery, +{gain}", self.color_purple)
            elif item == 1:
                self.add_to_log(f"P1 hit the jackpot, +{gain}", self.color_purple)
            elif item == 2:
                self.add_to_log(f"P1 found a chest, +{gain}", self.color_purple)
            elif item == 3:
                self.add_to_log(f"P1 got some money from {random.choice(relatives)}, +{gain}", self.color_purple)
            elif item == 4:
                self.add_to_log(f"P1 found some money on the floor, +{gain}", self.color_purple)
            elif item == 5:
                self.add_to_log(f"Nothing seems to happen", self.color_purple)
            elif item == 6:
                if self.p1.money == 0:
                    self.add_to_log(f"P1 is starving, but has no money", self.color_purple)
                else:
                    self.add_to_log(f"P1 is hungry, {random.choice(food)} costs {gain}", self.color_purple)
            elif item == 7:
                if self.p1.money == 0:
                    self.add_to_log(f"P1 can't pay the ticket, to jail!", self.color_purple)
                    self.p1.jailed = True
                    self.p1.position = 18
                else:
                    if abs(gain) > self.p1.money:
                        gain = -1 * self.p1.money
                    self.add_to_log(f"P1 got a ticket, -{abs(gain)}", self.color_purple)
            elif item == 8:
                if self.p1.money == 0:
                    self.add_to_log(f"P1 went all in with nothing", self.color_purple)
                else:
                    self.add_to_log(f"P1 went all in, -{abs(gain)}", self.color_purple)
            elif item == 9:
                if self.p1.money == 0:
                    self.add_to_log(f"P1 has no money for {random.choice(relatives)} bill", self.color_purple)
                else:
                    self.add_to_log(f"P1's {random.choice(relatives)}, is in the hospital, -{abs(gain)}", self.color_purple)
        else:
            if item == 0:
                self.add_to_log(f"P2 won the lottery, +{gain}", self.color_purple)
            elif item == 1:
                self.add_to_log(f"P2 hit the jackpot, +{gain}", self.color_purple)
            elif item == 2:
                self.add_to_log(f"P2 found a chest, +{gain}", self.color_purple)
            elif item == 3:
                self.add_to_log(f"P2 got some money from {random.choice(relatives)}, +{gain}", self.color_purple)
            elif item == 4:
                self.add_to_log(f"P2 found some money on the floor, +{gain}", self.color_purple)
            elif item == 5:
                self.add_to_log(f"Nothing seems to happen", self.color_purple)
            elif item == 6:
                if self.p2.money == 0:
                    self.add_to_log(f"P2 is starving, but has no money", self.color_purple)
                else:
                    self.add_to_log(f"P2 is hungry, {random.choice(food)} costs {gain}", self.color_purple)
            elif item == 7:
                if self.p2.money == 0:
                    self.add_to_log(f"P2 can't pay the ticket, to jail!", self.color_purple)
                    self.p2.jailed = True
                    self.p2.position = 18
                else:
                    if abs(gain) > self.p2.money:
                        gain = -1 * self.p2.money
                    self.add_to_log(f"P2 got a ticket, -{abs(gain)}", self.color_purple)
            elif item == 8:
                if self.p2.money == 0:
                    self.add_to_log(f"P2 went all in with nothing", self.color_purple)
                else:
                    self.add_to_log(f"P2 went all in, -{abs(gain)}", self.color_purple)
            elif item == 9:
                if self.p2.money == 0:
                    self.add_to_log(f"P2 has no money for {random.choice(relatives)} bill", self.color_purple)
                else:
                    self.add_to_log(f"P2's {random.choice(relatives)}, is in the hospital, -{abs(gain)}", self.color_purple)
        if player == 1:
            if item != 5:
                if self.p1.money + gain < 0:
                    self.p1.money = 0
                else:
                    self.p1.money += gain
                self.p1_money_text = self.font_40.render(f"${self.p1.money}", False, self.p1_color).convert()
        else:
            if item != 5:
                if self.p2.money + gain < 0:
                    self.p2.money = 0
                else:
                    self.p2.money += gain
                self.p2_money_text = self.font_40.render(f"${self.p2.money}", False, self.p2_color).convert()

    def shop(self, player):
        def check_can_sell_computer():
            if player == 1:
                self.p1.can_sell_computer = True
                _keys = list(self.p1.components.keys())
                for _item in _keys:
                    if self.p1.components[_item] == 0:
                        self.p1.can_sell_computer = False
                        break
            else:
                self.p2.can_sell_computer = True
                _keys = list(self.p2.components.keys())
                for _item in _keys:
                    if self.p2.components[_item] == 0:
                        self.p2.can_sell_computer = False
                        break

        check_can_sell_computer()
        shop_text = self.font_100.render("Shop", False, self.text_color).convert()
        return_button = pg.Rect((1000, 590), (250, 100))
        return_text = self.font_100.render("Return", False, self.color_brown).convert()

        buy_buttons = [pg.Rect((420, 140), (100, 50)), pg.Rect((420, 210), (100, 50)), pg.Rect((420, 280), (100, 50)), pg.Rect((420, 350), (100, 50)), pg.Rect((420, 420), (100, 50)), pg.Rect((420, 490), (100, 50)),
                       pg.Rect((420, 560), (100, 50)), pg.Rect((420, 630), (100, 50))]
        sell_buttons = [pg.Rect((550, 140), (100, 50)), pg.Rect((550, 210), (100, 50)), pg.Rect((550, 280), (100, 50)), pg.Rect((550, 350), (100, 50)), pg.Rect((550, 420), (100, 50)), pg.Rect((550, 490), (100, 50)),
                        pg.Rect((550, 560), (100, 50)), pg.Rect((550, 630), (100, 50))]
        items = {"Keyboard": 100, "Mouse": 100, "Monitor": 100, "Printer": 100, "CPU": 100, "GPU": 100, "Motherboard": 100, "Mini Tower": 100}
        keys = list(items.keys())
        values = list(items.values())

        sell_computer_button = pg.Rect((1000, 450), (250, 100))
        # sell_computer_text = self.font_50.render(f"Sell PC: ${self.computer_price}", False, self.color_purple).convert()

        if player == 1:
            self.left_to_buy_text = self.font_50.render(f"Left to buy this turn: {int((len(self.p1.components) / 2) - self.p1.items_bought_this_turn)}", False, "White").convert()
        else:
            self.left_to_buy_text = self.font_50.render(f"Left to buy this turn: {int((len(self.p2.components) / 2) - self.p2.items_bought_this_turn)}", False, "White").convert()

        def buy_item(index):
            if (player == 1 and self.p1.items_bought_this_turn < len(self.p1.components) / 2) or (player == 2 and self.p2.items_bought_this_turn < len(self.p2.components) / 2):
                if player == 1 and self.p1.money >= values[index]:
                    self.p1.items_bought_this_turn += 1
                    self.left_to_buy_text = self.font_50.render(f"Left to buy this turn: {int((len(self.p1.components) / 2) - self.p1.items_bought_this_turn)}", False, "White").convert()
                    self.p1.money -= values[index]
                    self.p1.components[keys[index]] += 1
                    self.p1_money_text = self.font_40.render(f"${self.p1.money}", False, self.p1_color).convert()
                elif player == 2 and self.p2.money > values[index]:
                    self.p2.items_bought_this_turn += 1
                    self.left_to_buy_text = self.font_50.render(f"Left to buy this turn: {int((len(self.p2.components) / 2) - self.p2.items_bought_this_turn)}", False, "White").convert()
                    self.p2.money -= values[index]
                    self.p2.components[keys[index]] += 1
                    self.p2_money_text = self.font_40.render(f"${self.p2.money}", False, self.p2_color).convert()
            check_can_sell_computer()

        def sell_item(index):
            if player == 1 and self.p1.components[keys[index]] > 0:
                self.p1.money += int(values[index] * self.resell_percentage)
                self.p1.components[keys[index]] -= 1
                self.p1_money_text = self.font_40.render(f"${self.p1.money}", False, self.p1_color).convert()
            elif player == 2 and self.p2.components[keys[index]] > 0:
                self.p2.money += int(values[index] * self.resell_percentage)
                self.p2.components[keys[index]] -= 1
                self.p2_money_text = self.font_40.render(f"${self.p2.money}", False, self.p2_color).convert()
            check_can_sell_computer()

        while self.state_stack[-1] == "SHOP":
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit(0)
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if return_button.collidepoint(pg.mouse.get_pos()):
                        # Go back to previous state
                        self.state_stack.pop()
                        break
                    elif buy_buttons[0].collidepoint(pg.mouse.get_pos()):  # player wants to buy item 1
                        buy_item(0)
                    elif sell_buttons[0].collidepoint(pg.mouse.get_pos()):  # player wants to sell item 1
                        sell_item(0)
                    elif buy_buttons[1].collidepoint(pg.mouse.get_pos()):  # player wants to buy item 2
                        buy_item(1)
                    elif sell_buttons[1].collidepoint(pg.mouse.get_pos()):  # player wants to sell item 2
                        sell_item(1)
                    elif buy_buttons[2].collidepoint(pg.mouse.get_pos()):  # player wants to buy item 3
                        buy_item(2)
                    elif sell_buttons[2].collidepoint(pg.mouse.get_pos()):  # player wants to sell item 3
                        sell_item(2)
                    elif buy_buttons[3].collidepoint(pg.mouse.get_pos()):  # player wants to buy item 4
                        buy_item(3)
                    elif sell_buttons[3].collidepoint(pg.mouse.get_pos()):  # player wants to sell item 4
                        sell_item(3)
                    elif buy_buttons[4].collidepoint(pg.mouse.get_pos()):  # player wants to buy item 5
                        buy_item(4)
                    elif sell_buttons[4].collidepoint(pg.mouse.get_pos()):  # player wants to sell item 5
                        sell_item(4)
                    elif buy_buttons[5].collidepoint(pg.mouse.get_pos()):  # player wants to buy item 6
                        buy_item(5)
                    elif sell_buttons[5].collidepoint(pg.mouse.get_pos()):  # player wants to sell item 6
                        sell_item(5)
                    elif buy_buttons[6].collidepoint(pg.mouse.get_pos()):  # player wants to buy item 7
                        buy_item(6)
                    elif sell_buttons[6].collidepoint(pg.mouse.get_pos()):  # player wants to sell item 7
                        sell_item(6)
                    elif buy_buttons[7].collidepoint(pg.mouse.get_pos()):  # player wants to buy item 8
                        buy_item(7)
                    elif sell_buttons[7].collidepoint(pg.mouse.get_pos()):  # player wants to sell item 8
                        sell_item(7)

                    elif sell_computer_button.collidepoint(pg.mouse.get_pos()):
                        if player == 1 and self.p1.can_sell_computer and not self.p1.has_sold_computer_this_turn:
                            for item in list(self.p1.components):
                                self.p1.components[item] -= 1
                            self.p1.money += self.computer_price
                            self.p1_money_text = self.font_40.render(f"${self.p1.money}", False, self.p1_color).convert()
                            self.screen.blit(self.p1_money_text, (10, 10))
                            self.p1.has_sold_computer_this_turn = True
                        elif player == 2 and self.p2.can_sell_computer and not self.p2.has_sold_computer_this_turn:
                            for item in list(self.p2.components):
                                self.p2.components[item] -= 1
                            self.p2.money += self.computer_price
                            self.p2_money_text = self.font_40.render(f"${self.p2.money}", False, self.p2_color).convert()
                            self.screen.blit(self.p2_money_text, (10, 10))
                            self.p2.has_sold_computer_this_turn = True
                        check_can_sell_computer()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        # Go back to previous state
                        self.state_stack.pop()
                        break

            # Update

            # Render

            self.screen.fill(self.bg_color)
            # Player money
            if player == 1:
                self.screen.blit(self.p1_money_text, (10, 10))
            else:
                self.screen.blit(self.p2_money_text, (10, 10))
            # Shop text
            self.screen.blit(shop_text, shop_text.get_rect(center=(self.window_width / 2, 50)))
            # Left to buy this turn text
            self.screen.blit(self.left_to_buy_text, self.left_to_buy_text.get_rect(midleft=(10, 60)))
            # Return button
            pg.draw.rect(self.screen, self.color_green, return_button)
            if return_button.collidepoint(pg.mouse.get_pos()):
                return_text = self.font_100.render("Return", False, self.color_blue).convert()
            else:
                return_text = self.font_100.render("Return", False, self.color_brown).convert()
            self.screen.blit(return_text, return_text.get_rect(center=(return_button.centerx + 5, return_button.centery + 5)))
            # Sell computer button
            if player == 1 and self.p1.can_sell_computer and not self.p1.has_sold_computer_this_turn:
                pg.draw.rect(self.screen, self.color_red, sell_computer_button)
                if sell_computer_button.collidepoint(pg.mouse.get_pos()):
                    sell_computer_text = self.font_50.render(f"Sell PC: ${self.computer_price}", False, self.color_yellow).convert()
                else:
                    sell_computer_text = self.font_50.render(f"Sell PC: ${self.computer_price}", False, self.color_purple).convert()
                self.screen.blit(sell_computer_text, sell_computer_text.get_rect(midleft=(1025, 505)))
            elif player == 2 and self.p2.can_sell_computer and not self.p2.has_sold_computer_this_turn:
                pg.draw.rect(self.screen, self.color_red, sell_computer_button)
                if sell_computer_button.collidepoint(pg.mouse.get_pos()):
                    sell_computer_text = self.font_50.render(f"Sell PC: ${self.computer_price}", False, self.color_yellow).convert()
                else:
                    sell_computer_text = self.font_50.render(f"Sell PC: ${self.computer_price}", False, self.color_purple).convert()
                self.screen.blit(sell_computer_text, sell_computer_text.get_rect(midleft=(1025, 505)))

            # Item names
            for i in range(len(items)):
                item = list(items.keys())[i]
                # Item text
                text = self.font_50.render(f"{item} (${items[item]}/{int(items[item] * self.resell_percentage)})", False, (0, 0, 0))
                self.screen.blit(text, (50, 150 + (i * 70)))
                # Player has
                if player == 1:
                    text = self.font_50.render(f"(You have: {self.p1.components[item]})", False, (0, 0, 0))
                else:
                    text = self.font_50.render(f"(You have: {self.p2.components[item]})", False, (0, 0, 0))
                self.screen.blit(text, (700, 150 + (i * 70)))

            # Buy buttons
            if (player == 1 and self.p1.items_bought_this_turn < len(self.p1.components) / 2) or (player == 2 and self.p2.items_bought_this_turn < len(self.p2.components) / 2):
                pg.draw.rect(self.screen, self.color_green, buy_buttons[0])
                if buy_buttons[0].collidepoint(pg.mouse.get_pos()):
                    buy_text = self.font_50.render("Buy", False, self.color_yellow).convert()
                else:
                    buy_text = self.font_50.render("Buy", False, self.color_purple).convert()
                self.screen.blit(buy_text, buy_text.get_rect(center=(buy_buttons[0].centerx + 5, buy_buttons[0].centery + 5)))

            if (player == 1 and self.p1.items_bought_this_turn < len(self.p1.components) / 2) or (player == 2 and self.p2.items_bought_this_turn < len(self.p2.components) / 2):
                pg.draw.rect(self.screen, self.color_green, buy_buttons[1])
                if buy_buttons[1].collidepoint(pg.mouse.get_pos()):
                    buy_text = self.font_50.render("Buy", False, self.color_yellow).convert()
                else:
                    buy_text = self.font_50.render("Buy", False, self.color_purple).convert()
                self.screen.blit(buy_text, buy_text.get_rect(center=(buy_buttons[1].centerx + 5, buy_buttons[1].centery + 5)))

            if (player == 1 and self.p1.items_bought_this_turn < len(self.p1.components) / 2) or (player == 2 and self.p2.items_bought_this_turn < len(self.p2.components) / 2):
                pg.draw.rect(self.screen, self.color_green, buy_buttons[2])
                if buy_buttons[2].collidepoint(pg.mouse.get_pos()):
                    buy_text = self.font_50.render("Buy", False, self.color_yellow).convert()
                else:
                    buy_text = self.font_50.render("Buy", False, self.color_purple).convert()
                self.screen.blit(buy_text, buy_text.get_rect(center=(buy_buttons[2].centerx + 5, buy_buttons[2].centery + 5)))

            if (player == 1 and self.p1.items_bought_this_turn < len(self.p1.components) / 2) or (player == 2 and self.p2.items_bought_this_turn < len(self.p2.components) / 2):
                pg.draw.rect(self.screen, self.color_green, buy_buttons[3])
                if buy_buttons[3].collidepoint(pg.mouse.get_pos()):
                    buy_text = self.font_50.render("Buy", False, self.color_yellow).convert()
                else:
                    buy_text = self.font_50.render("Buy", False, self.color_purple).convert()
                self.screen.blit(buy_text, buy_text.get_rect(center=(buy_buttons[3].centerx + 5, buy_buttons[3].centery + 5)))

            if (player == 1 and self.p1.items_bought_this_turn < len(self.p1.components) / 2) or (player == 2 and self.p2.items_bought_this_turn < len(self.p2.components) / 2):
                pg.draw.rect(self.screen, self.color_green, buy_buttons[4])
                if buy_buttons[4].collidepoint(pg.mouse.get_pos()):
                    buy_text = self.font_50.render("Buy", False, self.color_yellow).convert()
                else:
                    buy_text = self.font_50.render("Buy", False, self.color_purple).convert()
                self.screen.blit(buy_text, buy_text.get_rect(center=(buy_buttons[4].centerx + 5, buy_buttons[4].centery + 5)))

            if (player == 1 and self.p1.items_bought_this_turn < len(self.p1.components) / 2) or (player == 2 and self.p2.items_bought_this_turn < len(self.p2.components) / 2):
                pg.draw.rect(self.screen, self.color_green, buy_buttons[5])
                if buy_buttons[5].collidepoint(pg.mouse.get_pos()):
                    buy_text = self.font_50.render("Buy", False, self.color_yellow).convert()
                else:
                    buy_text = self.font_50.render("Buy", False, self.color_purple).convert()
                self.screen.blit(buy_text, buy_text.get_rect(center=(buy_buttons[5].centerx + 5, buy_buttons[5].centery + 5)))

            if (player == 1 and self.p1.items_bought_this_turn < len(self.p1.components) / 2) or (player == 2 and self.p2.items_bought_this_turn < len(self.p2.components) / 2):
                pg.draw.rect(self.screen, self.color_green, buy_buttons[6])
                if buy_buttons[6].collidepoint(pg.mouse.get_pos()):
                    buy_text = self.font_50.render("Buy", False, self.color_yellow).convert()
                else:
                    buy_text = self.font_50.render("Buy", False, self.color_purple).convert()
                self.screen.blit(buy_text, buy_text.get_rect(center=(buy_buttons[6].centerx + 5, buy_buttons[6].centery + 5)))

            if (player == 1 and self.p1.items_bought_this_turn < len(self.p1.components) / 2) or (player == 2 and self.p2.items_bought_this_turn < len(self.p2.components) / 2):
                pg.draw.rect(self.screen, self.color_green, buy_buttons[7])
                if buy_buttons[7].collidepoint(pg.mouse.get_pos()):
                    buy_text = self.font_50.render("Buy", False, self.color_yellow).convert()
                else:
                    buy_text = self.font_50.render("Buy", False, self.color_purple).convert()
                self.screen.blit(buy_text, buy_text.get_rect(center=(buy_buttons[7].centerx + 5, buy_buttons[7].centery + 5)))

            # Sell buttons
            pg.draw.rect(self.screen, self.color_red, sell_buttons[0])
            if sell_buttons[0].collidepoint(pg.mouse.get_pos()):
                sell_text = self.font_50.render("Sell", False, self.color_yellow).convert()
            else:
                sell_text = self.font_50.render("Sell", False, self.color_purple).convert()
            self.screen.blit(sell_text, sell_text.get_rect(center=(sell_buttons[0].centerx + 5, sell_buttons[0].centery + 5)))

            pg.draw.rect(self.screen, self.color_red, sell_buttons[1])
            if sell_buttons[1].collidepoint(pg.mouse.get_pos()):
                sell_text = self.font_50.render("Sell", False, self.color_yellow).convert()
            else:
                sell_text = self.font_50.render("Sell", False, self.color_purple).convert()
            self.screen.blit(sell_text, sell_text.get_rect(center=(sell_buttons[1].centerx + 5, sell_buttons[1].centery + 5)))

            pg.draw.rect(self.screen, self.color_red, sell_buttons[2])
            if sell_buttons[2].collidepoint(pg.mouse.get_pos()):
                sell_text = self.font_50.render("Sell", False, self.color_yellow).convert()
            else:
                sell_text = self.font_50.render("Sell", False, self.color_purple).convert()
            self.screen.blit(sell_text, sell_text.get_rect(center=(sell_buttons[2].centerx + 5, sell_buttons[2].centery + 5)))

            pg.draw.rect(self.screen, self.color_red, sell_buttons[3])
            if sell_buttons[3].collidepoint(pg.mouse.get_pos()):
                sell_text = self.font_50.render("Sell", False, self.color_yellow).convert()
            else:
                sell_text = self.font_50.render("Sell", False, self.color_purple).convert()
            self.screen.blit(sell_text, sell_text.get_rect(center=(sell_buttons[3].centerx + 5, sell_buttons[3].centery + 5)))

            pg.draw.rect(self.screen, self.color_red, sell_buttons[4])
            if sell_buttons[4].collidepoint(pg.mouse.get_pos()):
                sell_text = self.font_50.render("Sell", False, self.color_yellow).convert()
            else:
                sell_text = self.font_50.render("Sell", False, self.color_purple).convert()
            self.screen.blit(sell_text, sell_text.get_rect(center=(sell_buttons[4].centerx + 5, sell_buttons[4].centery + 5)))

            pg.draw.rect(self.screen, self.color_red, sell_buttons[5])
            if sell_buttons[5].collidepoint(pg.mouse.get_pos()):
                sell_text = self.font_50.render("Sell", False, self.color_yellow).convert()
            else:
                sell_text = self.font_50.render("Sell", False, self.color_purple).convert()
            self.screen.blit(sell_text, sell_text.get_rect(center=(sell_buttons[5].centerx + 5, sell_buttons[5].centery + 5)))

            pg.draw.rect(self.screen, self.color_red, sell_buttons[6])
            if sell_buttons[6].collidepoint(pg.mouse.get_pos()):
                sell_text = self.font_50.render("Sell", False, self.color_yellow).convert()
            else:
                sell_text = self.font_50.render("Sell", False, self.color_purple).convert()
            self.screen.blit(sell_text, sell_text.get_rect(center=(sell_buttons[6].centerx + 5, sell_buttons[6].centery + 5)))

            pg.draw.rect(self.screen, self.color_red, sell_buttons[7])
            if sell_buttons[7].collidepoint(pg.mouse.get_pos()):
                sell_text = self.font_50.render("Sell", False, self.color_yellow).convert()
            else:
                sell_text = self.font_50.render("Sell", False, self.color_purple).convert()
            self.screen.blit(sell_text, sell_text.get_rect(center=(sell_buttons[7].centerx + 5, sell_buttons[7].centery + 5)))

            # PyGame Render
            pg.display.update()
            self.clock.tick(self.fps)

    def query(self, player):
        return_button = pg.Rect((1000, 590), (250, 100))
        return_text = self.font_100.render("Return", False, self.color_brown).convert()

        random_num = random.randrange(len(questions))

        question = questions[random_num]
        question_text = self.font_40.render(question, False, "White").convert()

        question_choices = choices[random_num]
        choices_texts = []
        for choice in question_choices:
            choices_texts.append(self.font_40.render(choice, False, "Black").convert())

        correct_answer = answers[random_num]
        print(correct_answer)

        answer_buttons = [pg.Rect(((self.window_width / 4) - 50, 400), (100, 100)), pg.Rect(((self.window_width / 2) - 50, 400), (100, 100)), pg.Rect((((self.window_width / 4) * 3) - 50, 400), (100, 100))]
        answer_button_texts = [self.font_100.render("A", False, "Black").convert(), self.font_100.render("B", False, "Black").convert(), self.font_100.render("C", False, "Black").convert()]

        while self.state_stack[-1] == "QUERY":
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit(0)
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if return_button.collidepoint(pg.mouse.get_pos()):
                        # Go back to previous state
                        self.state_stack.pop()
                        break
                    else:
                        if answer_buttons[0].collidepoint(pg.mouse.get_pos()):  # Player chose A
                            if player == 1:
                                self.p1.has_done_query_this_turn = True
                                if correct_answer == 0:  # Correct answer chosen
                                    reward = random.randint(self.query_reward[0], self.query_reward[1])
                                    self.p1.money += reward
                                    self.add_to_log(f"P1 chose the correct answer, +${reward}", self.color_blue)
                                else:  # Wrong answer chosen
                                    self.add_to_log("P1 chose the wrong answer", self.color_blue)
                            else:
                                self.p2.has_done_query_this_turn = True
                                if correct_answer == 0:  # Correct answer chosen
                                    reward = random.randint(self.query_reward[0], self.query_reward[1])
                                    self.p2.money += reward
                                    self.add_to_log(f"P2 chose the correct answer, +${reward}", self.color_blue)
                                else:  # Wrong answer chosen
                                    self.add_to_log("P2 chose the wrong answer", self.color_blue)

                        if answer_buttons[1].collidepoint(pg.mouse.get_pos()):  # Player chose B
                            if player == 1:
                                self.p1.has_done_query_this_turn = True
                                if correct_answer == 1:  # Correct answer chosen
                                    reward = random.randint(self.query_reward[0], self.query_reward[1])
                                    self.p1.money += reward
                                    self.add_to_log(f"P1 chose the correct answer, +${reward}", self.color_blue)
                                else:  # Wrong answer chosen
                                    self.add_to_log("P1 chose the wrong answer", self.color_blue)
                            else:
                                self.p2.has_done_query_this_turn = True
                                if correct_answer == 1:  # Correct answer chosen
                                    reward = random.randint(self.query_reward[0], self.query_reward[1])
                                    self.p2.money += reward
                                    self.add_to_log(f"P2 chose the correct answer, +${reward}", self.color_blue)
                                else:  # Wrong answer chosen
                                    self.add_to_log("P2 chose the wrong answer", self.color_blue)

                        if answer_buttons[2].collidepoint(pg.mouse.get_pos()):  # Player chose C
                            if player == 1:
                                self.p1.has_done_query_this_turn = True
                                if correct_answer == 2:  # Correct answer chosen
                                    reward = random.randint(self.query_reward[0], self.query_reward[1])
                                    self.p1.money += reward
                                    self.add_to_log(f"P1 chose the correct answer, +${reward}", self.color_blue)
                                else:  # Wrong answer chosen
                                    self.add_to_log("P1 chose the wrong answer", self.color_blue)
                            else:
                                self.p2.has_done_query_this_turn = True
                                if correct_answer == 2:  # Correct answer chosen
                                    reward = random.randint(self.query_reward[0], self.query_reward[1])
                                    self.p2.money += reward
                                    self.add_to_log(f"P2 chose the correct answer, +${reward}", self.color_blue)
                                else:  # Wrong answer chosen
                                    self.add_to_log("P2 chose the wrong answer", self.color_blue)

                        self.p1_money_text = self.font_40.render(f"${self.p1.money}", False, self.p1_color).convert()
                        self.p2_money_text = self.font_40.render(f"${self.p2.money}", False, self.p2_color).convert()
                        self.state_stack.pop()
                        break

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        # Go back to previous state
                        self.state_stack.pop()
                        break

            # Update

            # Render

            self.screen.fill(self.color_blue)
            # Question text
            self.screen.blit(question_text, question_text.get_rect(center=(self.window_width / 2, 50)))
            # Choices text
            for i in range(len(choices_texts)):
                self.screen.blit(choices_texts[i], choices_texts[i].get_rect(midleft=(50, 150 + (i * 70))))
            # Answer buttons
            for button in answer_buttons:
                pg.draw.rect(self.screen, self.color_green, button)
            # Check button hover
            if answer_buttons[0].collidepoint(pg.mouse.get_pos()):
                answer_button_texts[0] = self.font_100.render("A", False, "White").convert()
            else:
                answer_button_texts[0] = self.font_100.render("A", False, "Black").convert()
            if answer_buttons[1].collidepoint(pg.mouse.get_pos()):
                answer_button_texts[1] = self.font_100.render("B", False, "White").convert()
            else:
                answer_button_texts[1] = self.font_100.render("B", False, "Black").convert()
            if answer_buttons[2].collidepoint(pg.mouse.get_pos()):
                answer_button_texts[2] = self.font_100.render("C", False, "White").convert()
            else:
                answer_button_texts[2] = self.font_100.render("C", False, "Black").convert()
            # Answer button text
            for i in range(len(answer_button_texts)):
                self.screen.blit(answer_button_texts[i], answer_button_texts[i].get_rect(center=((i * self.window_width / 4) + (self.window_width / 4) + 5, 455)))
            # Return button
            pg.draw.rect(self.screen, self.color_green, return_button)
            if return_button.collidepoint(pg.mouse.get_pos()):
                return_text = self.font_100.render("Return", False, self.color_blue).convert()
            else:
                return_text = self.font_100.render("Return", False, self.color_brown).convert()
            self.screen.blit(return_text, return_text.get_rect(center=(return_button.centerx + 5, return_button.centery + 5)))

            # PyGame Render
            pg.display.update()
            self.clock.tick(self.fps)

    def event(self, player):
        self.nums_in_word_text = self.font_50.render("Number that are in the word: 0", False, "Black").convert()
        self.nums_correct_text = self.font_50.render("Numbers in the correct spot: 0", False, "Black").convert()
        if player == 1:
            self.guesses_left_text = self.font_50.render(f"Guesses left: {self.max_event_guesses - self.p1.guesses_done_this_turn}", False, "Black").convert()
        else:
            self.guesses_left_text = self.font_50.render(f"Guesses left: {self.max_event_guesses - self.p2.guesses_done_this_turn}", False, "Black").convert()
        if (player == 1 and self.p1.guesses_done_this_turn == 0) or (player == 2 and self.p2.guesses_done_this_turn == 0):
            self.event_answer = ""
        while len(self.event_answer) < 4:
            char = str(random.randint(1, 6))
            while char in self.event_answer:
                char = str(random.randint(1, 6))
            self.event_answer += char
        print(f"Answer: {self.event_answer}")
        user_text = ""
        user_text_display = self.font_50.render(user_text, False, (50, 255, 0))

        user_text_container = pg.Rect(((self.window_width / 2) - 40, 100), (80, 30))

        return_button = pg.Rect((1000, 590), (250, 100))

        instruction_text = [self.font_40.render("Input 4 numbers between 1 and 6 and hit enter, the numbers that are in the correct spot and numbers", False, "Black").convert(),
                            self.font_40.render("that are in the answer but not in the correct spot are shown.", False, "Black").convert()]
        note_text = self.font_24.render("Note: the answer contains no duplicate numbers. (eg. 2112 does not occur)", False, self.color_red).convert()

        while self.state_stack[-1] == "EVENT":
            if player == 1 and self.p1.guesses_done_this_turn == self.max_event_guesses:
                self.add_to_log("P1 did not guess the number", self.color_green)
                self.p1.has_done_event_this_turn = True
                self.state_stack.pop()
                break
            elif player == 2 and self.p2.guesses_done_this_turn == self.max_event_guesses:
                self.add_to_log("P2 did not guess the number", self.color_green)
                self.p2.has_done_event_this_turn = True
                self.state_stack.pop()
                break

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit(0)
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if return_button.collidepoint(pg.mouse.get_pos()):
                        # Go back to previous state
                        self.state_stack.pop()
                        break
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        # Go back to previous state
                        self.state_stack.pop()
                        break
                    elif event.key == pg.K_BACKSPACE:
                        if len(user_text) > 0:
                            user_text = user_text[:-1]
                            user_text_display = self.font_50.render(user_text, False, (50, 255, 0))
                    elif event.key == pg.K_RETURN:
                        if user_text == self.event_answer:
                            reward = random.randint(self.event_reward[0], self.event_reward[1])
                            if player == 1:
                                self.add_to_log(f"P1 guessed the number, +${reward}", self.color_green)
                                self.p1.money += reward
                                self.p1_money_text = self.font_40.render(f"${self.p1.money}", False, self.p1_color).convert()
                                self.p1.has_done_event_this_turn = True
                            else:
                                self.add_to_log(f"P2 guessed the number +${reward}", self.color_green)
                                self.p2.money += reward
                                self.p2_money_text = self.font_40.render(f"${self.p2.money}", False, self.p2_color).convert()
                                self.p2.has_done_event_this_turn = True
                            self.state_stack.pop()
                            break
                        elif len(user_text) == 4:
                            if player == 1:
                                self.p1.guesses_done_this_turn += 1
                                self.guesses_left_text = self.font_50.render(f"Guesses left: {self.max_event_guesses - self.p1.guesses_done_this_turn}", False, "Black").convert()
                            else:
                                self.p2.guesses_done_this_turn += 1
                                self.guesses_left_text = self.font_50.render(f"Guesses left: {self.max_event_guesses - self.p2.guesses_done_this_turn}", False, "Black").convert()
                            correct = 0
                            in_word = 0
                            print(user_text)
                            for i in range(4):
                                if user_text[i] == self.event_answer[i]:
                                    correct += 1
                                elif user_text[i] in self.event_answer:
                                    in_word += 1
                            self.nums_in_word_text = self.font_50.render(f"Number that are in the word: {in_word}", False, "Black").convert()
                            self.nums_correct_text = self.font_50.render(f"Numbers in the correct spot: {correct}", False, "Black").convert()
                            user_text = ""
                            user_text_display = self.font_50.render(user_text, False, (50, 255, 0))

                elif event.type == pg.TEXTINPUT:
                    if event.text in ["1", "2", "3", "4", "5", "6"] and len(user_text) < 4:
                        user_text += event.text
                        user_text_display = self.font_50.render(user_text, False, (50, 255, 0))

            # Update

            # Render

            self.screen.fill(self.bg_color)
            # Return button
            pg.draw.rect(self.screen, self.color_green, return_button)
            if return_button.collidepoint(pg.mouse.get_pos()):
                return_text = self.font_100.render("Return", False, self.color_blue).convert()
            else:
                return_text = self.font_100.render("Return", False, self.color_brown).convert()
            self.screen.blit(return_text, return_text.get_rect(center=(return_button.centerx + 5, return_button.centery + 5)))

            # Instruction text
            for i in range(len(instruction_text)):
                self.screen.blit(instruction_text[i], instruction_text[i].get_rect(midtop=(self.window_width / 2, (i * 20) + 10)))

            # Note text
            self.screen.blit(note_text, note_text.get_rect(midtop=(self.window_width / 2, 50 + 10)))

            # User text container
            if player == 1:
                pg.draw.rect(self.screen, self.p1_color, user_text_container, 2)
            else:
                pg.draw.rect(self.screen, self.p2_color, user_text_container, 2)
            # User Text
            self.screen.blit(user_text_display, user_text_display.get_rect(topleft=((self.window_width / 2) - 36, 104)))

            # Guesses left text
            self.screen.blit(self.guesses_left_text, self.guesses_left_text.get_rect(topleft=(10, 400)))

            # Number information text
            self.screen.blit(self.nums_in_word_text, self.nums_in_word_text.get_rect(topleft=(10, 200)))
            self.screen.blit(self.nums_correct_text, self.nums_correct_text.get_rect(topleft=(10, 300)))

            # PyGame Render
            pg.display.update()
            self.clock.tick(self.fps)
            

    def famous(self, player):
        return_button = pg.Rect((1000, 590), (250, 100))
        return_text = self.font_100.render("Return", False, self.color_brown).convert()

        random_num = random.randrange(len(famous_questions))

        question = famous_questions[random_num]
        question_text = self.font_40.render(question, False, "Black").convert()

        question_choices = famous_choices[random_num]
        choices_texts = []
        for choice in question_choices:
            choices_texts.append(self.font_40.render(choice, False, "Black").convert())

        correct_answer = famous_answers[random_num]
        print(correct_answer)

        answer_buttons = [pg.Rect((280, 400), (100, 100)), pg.Rect((480, 400), (100, 100)), pg.Rect((680, 400), (100, 100)), pg.Rect(((880, 400), (100, 100)))]
        answer_button_texts = [self.font_100.render("A", False, "Black").convert(), self.font_100.render("B", False, "Black").convert(), self.font_100.render("C", False, "Black").convert(), self.font_100.render("B", False, "Black").convert()]

        while self.state_stack[-1] == "FAMOUS":
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit(0)
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if return_button.collidepoint(pg.mouse.get_pos()):
                        # Go back to previous state
                        self.state_stack.pop()
                        break
                    else:
                        if answer_buttons[0].collidepoint(pg.mouse.get_pos()):  # Player chose A
                            if player == 1:
                                self.p1.has_done_famous_this_turn = True
                                if correct_answer == 0:  # Correct answer chosen
                                    reward = random.randint(self.famous_reward[0], self.famous_reward[1])
                                    self.p1.money += reward
                                    self.add_to_log(f"P1 chose the correct answer, +${reward}", self.color_gray)
                                else:  # Wrong answer chosen
                                    self.add_to_log("P1 chose the wrong answer", self.color_gray)
                            else:
                                self.p2.has_done_famous_this_turn = True
                                if correct_answer == 0:  # Correct answer chosen
                                    reward = random.randint(self.famous_reward[0], self.famous_reward[1])
                                    self.p2.money += reward
                                    self.add_to_log(f"P2 chose the correct answer, +${reward}", self.color_gray)
                                else:  # Wrong answer chosen
                                    self.add_to_log("P2 chose the wrong answer", self.color_gray)

                        if answer_buttons[1].collidepoint(pg.mouse.get_pos()):  # Player chose B
                            if player == 1:
                                self.p1.has_done_famous_this_turn = True
                                if correct_answer == 1:  # Correct answer chosen
                                    reward = random.randint(self.famous_reward[0], self.famous_reward[1])
                                    self.p1.money += reward
                                    self.add_to_log(f"P1 chose the correct answer, +${reward}", self.color_gray)
                                else:  # Wrong answer chosen
                                    self.add_to_log("P1 chose the wrong answer", self.color_gray)
                            else:
                                self.p2.has_done_famous_this_turn = True
                                if correct_answer == 1:  # Correct answer chosen
                                    reward = random.randint(self.famous_reward[0], self.famous_reward[1])
                                    self.p2.money += reward
                                    self.add_to_log(f"P2 chose the correct answer, +${reward}", self.color_gray)
                                else:  # Wrong answer chosen
                                    self.add_to_log("P2 chose the wrong answer", self.color_gray)

                        if answer_buttons[2].collidepoint(pg.mouse.get_pos()):  # Player chose C
                            if player == 1:
                                self.p1.has_done_famous_this_turn = True
                                if correct_answer == 2:  # Correct answer chosen
                                    reward = random.randint(self.famous_reward[0], self.famous_reward[1])
                                    self.p1.money += reward
                                    self.add_to_log(f"P1 chose the correct answer, +${reward}", self.color_gray)
                                else:  # Wrong answer chosen
                                    self.add_to_log("P1 chose the wrong answer", self.color_gray)
                            else:
                                self.p2.has_done_famous_this_turn = True
                                if correct_answer == 2:  # Correct answer chosen
                                    reward = random.randint(self.famous_reward[0], self.famous_reward[1])
                                    self.p2.money += reward
                                    self.add_to_log(f"P2 chose the correct answer, +${reward}", self.color_gray)
                                else:  # Wrong answer chosen
                                    self.add_to_log("P2 chose the wrong answer", self.color_gray)
                                    
                        if answer_buttons[2].collidepoint(pg.mouse.get_pos()):  # Player chose D
                            if player == 1:
                                self.p1.has_done_famous_this_turn = True
                                if correct_answer == 3:  # Correct answer chosen
                                    reward = random.randint(self.famous_reward[0], self.famous_reward[1])
                                    self.p1.money += reward
                                    self.add_to_log(f"P1 chose the correct answer, +${reward}", self.color_gray)
                                else:  # Wrong answer chosen
                                    self.add_to_log("P1 chose the wrong answer", self.color_gray)
                            else:
                                self.p2.has_done_famous_this_turn = True
                                if correct_answer == 3:  # Correct answer chosen
                                    reward = random.randint(self.famous_reward[0], self.famous_reward[1])
                                    self.p2.money += reward
                                    self.add_to_log(f"P2 chose the correct answer, +${reward}", self.color_gray)
                                else:  # Wrong answer chosen
                                    self.add_to_log("P2 chose the wrong answer", self.color_gray)


                        self.p1_money_text = self.font_40.render(f"${self.p1.money}", False, self.p1_color).convert()
                        self.p2_money_text = self.font_40.render(f"${self.p2.money}", False, self.p2_color).convert()
                        self.state_stack.pop()
                        break

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        # Go back to previous state
                        self.state_stack.pop()
                        break

            # Update

            # Render

            self.screen.fill(self.color_gray)
            # Question text
            self.screen.blit(question_text, question_text.get_rect(center=(self.window_width / 2, 50)))
            # Choices text
            for i in range(len(choices_texts)):
                self.screen.blit(choices_texts[i], choices_texts[i].get_rect(midleft=(50, 150 + (i * 70))))
            # Answer buttons
            for button in answer_buttons:
                pg.draw.rect(self.screen, self.color_green, button)
            # Check button hover
            if answer_buttons[0].collidepoint(pg.mouse.get_pos()):
                answer_button_texts[0] = self.font_100.render("A", False, "White").convert()
            else:
                answer_button_texts[0] = self.font_100.render("A", False, "Black").convert()
            if answer_buttons[1].collidepoint(pg.mouse.get_pos()):
                answer_button_texts[1] = self.font_100.render("B", False, "White").convert()
            else:
                answer_button_texts[1] = self.font_100.render("B", False, "Black").convert()
            if answer_buttons[2].collidepoint(pg.mouse.get_pos()):
                answer_button_texts[2] = self.font_100.render("C", False, "White").convert()
            else:
                answer_button_texts[2] = self.font_100.render("C", False, "Black").convert()
            if answer_buttons[3].collidepoint(pg.mouse.get_pos()):
                answer_button_texts[3] = self.font_100.render("D", False, "White").convert()
            else:
                answer_button_texts[3] = self.font_100.render("D", False, "Black").convert()
            # Answer button text
            for i in range(len(answer_button_texts)):
                self.screen.blit(answer_button_texts[i], answer_button_texts[i].get_rect(center=((i * 200) + 335, 455)))
            # Return button
            pg.draw.rect(self.screen, self.color_green, return_button)
            if return_button.collidepoint(pg.mouse.get_pos()):
                return_text = self.font_100.render("Return", False, self.color_blue).convert()
            else:
                return_text = self.font_100.render("Return", False, self.color_brown).convert()
            self.screen.blit(return_text, return_text.get_rect(center=(return_button.centerx + 5, return_button.centery + 5)))

            # PyGame Render
            pg.display.update()
            self.clock.tick(self.fps)
