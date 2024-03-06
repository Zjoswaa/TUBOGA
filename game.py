import pygame as pg
import random

from player import Player
from questions import *


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
        self.max_log_size = 5

        self.clock = pg.time.Clock()
        self.fps = 60

        self.d1_text = self.font_200.render("0", False, "Black").convert()
        self.d2_text = self.font_200.render("0", False, "Black").convert()

        self.pause_icon = pg.image.load("res/icon.png").convert_alpha()

        self.p1 = Player()
        self.p2 = Player()

        self.p1_money_text = self.font_40.render(str(self.p1.money), False, self.p1_color).convert()
        self.p2_money_text = self.font_40.render(str(self.p2.money), False, self.p2_color).convert()

        self.dice_rolls = [0, 0]

        self.min_break_free_roll = 6  # minimum number you need to roll to break out of jail.

        self.round_stages = ["P1_ANNOUNCE_ROLL", "P1_WAIT_FOR_ROLL", "P1_MOVE", "P1_ACTION", "P2_ANNOUNCE_ROLL", "P2_WAIT_FOR_ROLL", "P2_MOVE", "P2_ACTION"]
        self.current_round_stage = 0

        self.chances = [(400, 600), (250, 350), (200, 300), (75, 125), (20, 60), (-1, 1), (-75, -25), (-100, -50), (-350, -300), (-450, -250)]

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
                self.screen.blit(legend_text[i], legend_text[i].get_rect(topleft=(600, (i * 50) + 175)))

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
                self.screen.blit(self.log[i], self.log[i].get_rect(topleft=(800, (i * 50) + 20)))

            if self.round_stages[self.current_round_stage] == "P1_ANNOUNCE_ROLL":
                if self.p1.jailed:
                    self.add_to_log("P1 is jailed, press space to break out", self.p1_color)
                else:
                    self.add_to_log("P1, press space to roll dice", self.p1_color)
                self.next_round_stage()
            elif self.round_stages[self.current_round_stage] == "P1_MOVE":
                if not self.p1.jailed:
                    self.p1.position = (self.p1.position + (self.dice_rolls[0] + self.dice_rolls[1])) % 36
                elif self.p1.position == 19:
                    self.p1.jailed = False
                self.next_round_stage()
            elif self.round_stages[self.current_round_stage] == "P1_ACTION":
                #self.add_to_log(f"P1 is on tile: {self.p1.position}", self.p1_color)
                if self.p1.position == 18:  # if p1 landed on jail tile
                    self.p1.jailed = True
                    self.add_to_log("P1 landed on jail", (0, 0, 0))
                elif self.p1.position == 16 or self.p1.position == 34:  # random item tile
                    item = random.choice(list(self.p1.components.keys()))
                    self.add_to_log(f"P1 got: {item}", self.color_brown)
                    self.p1.components[item] += 1
                    print(f"P1: {self.p1.components}")
                elif self.p1.position == 11 or self.p1.position == 29:  # chance tile
                    self.chance(1)
                    print(f"P1 money: {self.p1.money}")
                self.next_round_stage()
            elif self.round_stages[self.current_round_stage] == "P2_ANNOUNCE_ROLL":
                if self.p2.jailed:
                    self.add_to_log("P2 is jailed, press space to break out", self.p2_color)
                else:
                    self.add_to_log("P2, press space to roll dice", self.p2_color)
                self.next_round_stage()
            elif self.round_stages[self.current_round_stage] == "P2_MOVE":
                if not self.p2.jailed:
                    self.p2.position = (self.p2.position + (self.dice_rolls[0] + self.dice_rolls[1])) % 36
                elif self.p2.position == 19:
                    self.p2.jailed = False
                self.next_round_stage()
            elif self.round_stages[self.current_round_stage] == "P2_ACTION":
                #self.add_to_log(f"P2 is on tile: {self.p2.position}", self.p2_color)
                if self.p2.position == 18:  # if p2 landed on jail tile
                    self.p2.jailed = True
                    self.add_to_log("P2 landed on jail", (0, 0, 0))
                elif self.p2.position == 16 or self.p2.position == 34:  # random item tile
                    item = random.choice(list(self.p2.components.keys()))
                    self.add_to_log(f"P2 got: {item}", self.color_brown)
                    self.p2.components[item] += 1
                    print(f"P2: {self.p2.components}")
                elif self.p2.position == 11 or self.p2.position == 29:  # chance tile
                    self.chance(2)
                    print(f"P2 money: {self.p2.money}")
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
        if len(self.log) > self.max_log_size:
            del self.log[0]
        self.log.append(self.font_40.render(message, False, color).convert())

    def next_round_stage(self):
        self.current_round_stage = (self.current_round_stage + 1) % len(self.round_stages)

    def chance(self, player):
        if not self.rig_dices:
            item = random.randrange(0, len(self.chances))
        else:
            item = 7
        print(f"Rolled: {item}")
        gain = random.randint(self.chances[item][0], self.chances[item][1])
        relatives = ["mom", "dad", "grandma", "grandpa"]
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
                self.add_to_log(f"P1 went all in, -{abs(gain)}", self.color_purple)
            elif item == 9:
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
                    self.add_to_log(f"P2 is starving", self.color_purple)
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
                self.add_to_log(f"P2 went all in, -{abs(gain)}", self.color_purple)
            elif item == 9:
                self.add_to_log(f"P2's {random.choice(relatives)}, is in the hospital, -{abs(gain)}", self.color_purple)
        if player == 1:
            if item != 5:
                if self.p1.money + gain < 0:
                    self.p1.money = 0
                else:
                    self.p1.money += gain
                self.p1_money_text = self.font_40.render(str(self.p1.money), False, self.p1_color).convert()
        else:
            if item != 5:
                if self.p2.money + gain < 0:
                    self.p2.money = 0
                else:
                    self.p2.money += gain
                self.p2_money_text = self.font_40.render(str(self.p2.money), False, self.p2_color).convert()
