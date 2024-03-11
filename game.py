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
        self.max_log_size = 12

        self.clock = pg.time.Clock()
        self.fps = 60

        self.d1_text = self.font_200.render("0", False, "Black").convert()
        self.d2_text = self.font_200.render("0", False, "Black").convert()

        self.pause_icon = pg.image.load("res/icon.png").convert_alpha()
        self.board_image = pg.image.load("res/board.png").convert_alpha()

        self.component_icons = [pg.image.load("res/keyboard.png"), pg.image.load("res/mouse.png"), pg.image.load("res/monitor.png"), pg.image.load("res/printer.png"), pg.image.load("res/cpu.png"), pg.image.load("res/gpu.png"), pg.image.load("res/motherboard.png"), pg.image.load("res/mini-tower.png"), pg.image.load("res/harddrive.png")]
        self.component_icons_small = [pg.image.load("res/keyboard_small.png"), pg.image.load("res/mouse_small.png"), pg.image.load("res/monitor_small.png"), pg.image.load("res/printer_small.png"), pg.image.load("res/cpu_small.png"), pg.image.load("res/gpu_small.png"), pg.image.load("res/motherboard_small.png"), pg.image.load("res/mini-tower_small.png"), pg.image.load("res/harddrive_small.png")]

        self.p1 = Player()
        self.p2 = Player()
        # uncomment and rig dices to 2 to make p2 initialize trade
        # comment and rig dices to 2 to make p1 initialize trade
        # self.p2.position = 2

        self.p1_money_text = self.font_40.render(f"${self.p1.money}", False, self.p1_color).convert()
        self.p2_money_text = self.font_40.render(f"${self.p2.money}", False, self.p2_color).convert()
        self.left_to_buy_text = self.font_50.render("Left to buy this turn: ", False, "White").convert()
        self.nums_in_word_text = self.font_50.render("Number that are in the word: 0", False, "Black").convert()
        self.nums_correct_text = self.font_50.render("Numbers in the correct spot: 0", False, "Black").convert()
        self.guesses_left_text = self.font_50.render("Guesses left: ", False, "Black").convert()

        self.dice_rolls = [0, 0]

        self.min_break_free_roll = 6  # minimum number you need to roll to break out of jail.
        self.max_buy_per_round = 4 # maximum of items a player can buy each round in the shop

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

        self.win_condition = 5000
        self.winner = 0  # 0: No winner yet, 1: P1 wins, 2: P2 wins
        self.logged_win_message = False  # so the win message is only logged once

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
        quit_button = pg.Rect((1000, 500), (200, 100))
        restart_button = pg.Rect((515, 550), (250, 100))

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
                    elif restart_button.collidepoint(pg.mouse.get_pos()):
                        self.restart()
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
            # Restart button
            pg.draw.rect(self.screen, self.color_green, restart_button)
            if restart_button.collidepoint(pg.mouse.get_pos()):
                restart_text = self.font_100.render("Restart", False, self.color_yellow).convert()
            else:
                restart_text = self.font_100.render("Restart", False, self.color_purple).convert()
            self.screen.blit(restart_text, restart_text.get_rect(center=(restart_button.centerx + 5, restart_button.centery + 5)))
            # Game icon
            self.screen.blit(self.pause_icon, self.pause_icon.get_rect(center=(self.window_width / 2, self.window_height / 2)))
            # PyGame Render
            pg.display.update()
            self.clock.tick(self.fps)

    # Shows the game
    def game(self):
        self.add_to_log(f"Welcome to TUBOGA. First player to ${self.win_condition} wins!", "White")
        self.add_to_log(f"This is the log, the most recent {self.max_log_size} events are shown here.", "White")
        while self.state_stack[-1] == "GAME":
            self.check_for_winner()
            if self.winner == 1 and not self.logged_win_message:
                self.add_to_log(f"P1 has earned ${self.win_condition} and wins!", self.p1_color)
                self.add_to_log("Thanks for playing :)", "White")
                self.logged_win_message = True
            elif self.winner == 2 and not self.logged_win_message:
                self.add_to_log(f"P2 has earned ${self.win_condition} and wins!", self.p2_color)
                self.add_to_log("Thanks for playing :)", "White")
                self.logged_win_message = True
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit(0)
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        # Show pause menu
                        self.state_stack.append("PAUSE")
                        self.pause()
                    elif event.key == pg.K_SPACE and not self.winner:
                        if self.round_stages[self.current_round_stage] == "P1_WAIT_FOR_ROLL":
                            self.p1.has_done_query_this_turn = False
                            self.p1.has_done_event_this_turn = False
                            self.p1.has_done_famous_this_turn = False
                            self.p1.has_sold_computer_this_turn = False
                            self.p1.has_traded_this_turn = False
                            self.p1.items_bought_this_turn = 0
                            self.p1.guesses_done_this_turn = 0
                            self.reset_components_trade(1)
                            if self.p1.jailed:
                                self.dice_roll()
                                if sum(self.dice_rolls) < self.min_break_free_roll:  # if jailed, roll a break-free dice, if less than 6 he does not break free
                                    self.add_to_log(f"P1 Roll: {self.dice_rolls[0] + self.dice_rolls[1]}, didn't break free", (0, 0, 0))
                                else:
                                    self.add_to_log(f"P1 Roll: {self.dice_rolls[0] + self.dice_rolls[1]}, broke free", (0, 0, 0))
                                    self.p1.position += 1
                            else:
                                self.dice_roll()
                                # self.add_to_log(f"P1 Roll: {self.dice_rolls[0] + self.dice_rolls[1]}", self.p1_color)
                            self.next_round_stage()
                        elif self.round_stages[self.current_round_stage] == "P2_WAIT_FOR_ROLL":
                            self.p2.has_done_query_this_turn = False
                            self.p2.has_done_event_this_turn = False
                            self.p2.has_done_famous_this_turn = False
                            self.p2.has_sold_computer_this_turn = False
                            self.p2.has_traded_this_turn = False
                            self.p2.items_bought_this_turn = 0
                            self.p2.guesses_done_this_turn = 0
                            self.reset_components_trade(2)
                            if self.p2.jailed:
                                self.dice_roll()
                                if sum(self.dice_rolls) < self.min_break_free_roll:  # if jailed, roll a break-free dice, if less than 6 he does not break free
                                    self.add_to_log(f"P2 Roll: {self.dice_rolls[0] + self.dice_rolls[1]}, didn't break free", (0, 0, 0))
                                else:
                                    self.add_to_log(f"P2 Roll: {self.dice_rolls[0] + self.dice_rolls[1]}, broke free", (0, 0, 0))
                                    self.p2.position += 1
                            else:
                                self.dice_roll()
                                # self.add_to_log(f"P2 Roll: {self.dice_rolls[0] + self.dice_rolls[1]}", self.p2_color)
                            self.next_round_stage()
                        break
                    elif event.key == pg.K_s and not self.winner:
                        if self.round_stages[self.current_round_stage] == "P1_WAIT_FOR_ROLL" and self.p1.position in [9, 27]:
                            self.state_stack.append("SHOP")
                            self.shop(1)
                        elif self.round_stages[self.current_round_stage] == "P2_WAIT_FOR_ROLL" and self.p2.position in [9, 27]:
                            self.state_stack.append("SHOP")
                            self.shop(2)
                    elif event.key == pg.K_q and not self.winner:
                        if self.round_stages[self.current_round_stage] == "P1_WAIT_FOR_ROLL" and self.p1.position in [5, 14, 23, 32] and not self.p1.has_done_query_this_turn:
                            self.state_stack.append("QUERY")
                            self.query(1)
                        elif self.round_stages[self.current_round_stage] == "P2_WAIT_FOR_ROLL" and self.p2.position in [5, 14, 23, 32] and not self.p2.has_done_query_this_turn:
                            self.state_stack.append("QUERY")
                            self.query(2)
                    elif event.key == pg.K_e and not self.winner:
                        if self.round_stages[self.current_round_stage] == "P1_WAIT_FOR_ROLL" and self.p1.position in [2, 20] and not self.p1.has_done_event_this_turn:
                            self.state_stack.append("EVENT")
                            self.event(1)
                        elif self.round_stages[self.current_round_stage] == "P2_WAIT_FOR_ROLL" and self.p2.position in [2, 20] and not self.p2.has_done_event_this_turn:
                            self.state_stack.append("EVENT")
                            self.event(2)
                    elif event.key == pg.K_f and not self.winner:
                        if self.round_stages[self.current_round_stage] == "P1_WAIT_FOR_ROLL" and self.p1.position in [7, 25] and not self.p1.has_done_famous_this_turn:
                            self.state_stack.append("FAMOUS")
                            self.famous(1)
                        elif self.round_stages[self.current_round_stage] == "P2_WAIT_FOR_ROLL" and self.p2.position in [7, 25] and not self.p2.has_done_famous_this_turn:
                            self.state_stack.append("FAMOUS")
                            self.famous(2)
                    elif event.key == pg.K_t and not self.winner:
                        if self.round_stages[self.current_round_stage] == "P1_WAIT_FOR_ROLL" and self.p1.position == self.p2.position and not self.p1.has_traded_this_turn:
                            self.state_stack.append("TRADE")
                            self.trade(1)
                        elif self.round_stages[self.current_round_stage] == "P2_WAIT_FOR_ROLL" and self.p2.position == self.p1.position and not self.p2.has_traded_this_turn:
                            self.state_stack.append("TRADE")
                            self.trade(2)
                    # TODO: Remove
                    elif event.key == pg.K_p:
                        print(f"P1: {self.p1.components}\nP1 (trade): {self.p1.components_trade}\nP2: {self.p2.components}\nP2 (trade): {self.p2.components_trade}")

            # Update

            # Render
            self.screen.fill(self.bg_color)
            # Render the board
            self.screen.blit(self.board_image, self.board_image.get_rect(topleft=(49, 109)))

            # # Render the legend
            # for i in range(len(legend_text)):
            #     self.screen.blit(legend_text[i], legend_text[i].get_rect(topleft=(560, (i * 50) + 175)))

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
                self.screen.blit(self.log[i], self.log[i].get_rect(topleft=(575, (i * 50) + 75)))

            if self.round_stages[self.current_round_stage] == "P1_ANNOUNCE_ROLL" and not self.winner:
                if self.p1.jailed:
                    self.add_to_log("P1 is jailed, press space to attempt breakout", self.p1_color)
                else:
                    if self.p1.position in [9, 27]:
                        if self.p1.position == self.p2.position and not self.p1.has_traded_this_turn:
                            self.add_to_log("P1, press space to roll dice, S to Shop, T to Trade", self.p1_color)
                        else:
                            self.add_to_log("P1, press space to roll dice, S to Shop", self.p1_color)
                    elif self.p1.position in [5, 14, 23, 32]:
                        if self.p1.position == self.p2.position and not self.p1.has_traded_this_turn:
                            self.add_to_log("P1, press space to roll dice, Q for Query, T to Trade", self.p1_color)
                        else:
                            self.add_to_log("P1, press space to roll dice, Q for Query", self.p1_color)
                    elif self.p1.position in [2, 20]:
                        if self.p1.position == self.p2.position and not self.p1.has_traded_this_turn:
                            self.add_to_log("P1, press space to roll dice, E for Event, T to Trade", self.p1_color)
                        else:
                            self.add_to_log("P1, press space to roll dice, E for Event", self.p1_color)
                    elif self.p1.position in [7, 25]:
                        if self.p1.position == self.p2.position and not self.p1.has_traded_this_turn:
                            self.add_to_log("P1, press space to roll dice, F for Famous, T to Trade", self.p1_color)
                        else:
                            self.add_to_log("P1, press space to roll dice, F for Famous", self.p1_color)
                    elif self.p1.position == self.p2.position and not self.p1.has_traded_this_turn:
                        self.add_to_log("P1, press space to roll dice, T to Trade", self.p1_color)
                    else:
                        self.add_to_log("P1, press space to roll dice", self.p1_color)
                self.next_round_stage()
            elif self.round_stages[self.current_round_stage] == "P1_MOVE" and not self.winner:
                if not self.p1.jailed:
                    # Move the player
                    self.p1.position = (self.p1.position + (self.dice_rolls[0] + self.dice_rolls[1])) % 36
                    # Increase player money by product of rolls
                    self.p1.money += (self.dice_rolls[0] * self.dice_rolls[1])
                    self.p1_money_text = self.font_40.render(f"${self.p1.money}", False, self.p1_color).convert()
                elif self.p1.position == 19:
                    self.p1.jailed = False
                self.next_round_stage()
            elif self.round_stages[self.current_round_stage] == "P1_ACTION" and not self.winner:
                # self.add_to_log(f"P1 is on tile: {self.p1.position}", self.p1_color)
                if self.p1.position == 18:  # if p1 landed on jail tile
                    self.p1.jailed = True
                    self.add_to_log("P1 is in jail", (0, 0, 0))
                elif self.p1.position == 16 or self.p1.position == 34:  # random item tile
                    item = random.choice(list(self.p1.components.keys()))
                    self.add_to_log(f"P1 got: {item}", self.color_brown)
                    self.p1.components[item] += 1
                    # prints out the component list, maybe needed for debugging
                    # print(f"P1: {self.p1.components}")
                elif self.p1.position in [11, 29]:  # chance tile
                    self.chance(1)
                elif self.p1.position in [2, 20]:  # Event tile
                    self.add_to_log(f"P1 landed on an Event tile", self.color_green)
                elif self.p1.position in [7, 25]:  # Famous person tile
                    self.add_to_log(f"P1 landed on a Famous Person tile", self.color_gray)
                elif self.p1.position in [5, 14, 23, 32]:  # Query tile
                    self.add_to_log(f"P1 landed on a Query tile", self.color_blue)
                elif self.p1.position in [9, 27]:  # Shop tile
                    self.add_to_log(f"P1 landed on a Shop tile", self.color_red)
                elif self.p1.position == 0:  # Start tile
                    reward = random.randint(self.back_at_start_reward[0], self.back_at_start_reward[1])
                    self.add_to_log(f"P1 is back at Start, +${reward}", self.color_yellow)
                    self.p1.money += reward
                    self.p1_money_text = self.font_40.render(f"${self.p1.money}", False, self.p1_color).convert()

                self.next_round_stage()
            elif self.round_stages[self.current_round_stage] == "P2_ANNOUNCE_ROLL" and not self.winner:
                if self.p2.jailed:
                    self.add_to_log("P2 is jailed, press space to attempt breakout", self.p2_color)
                else:
                    if self.p2.position in [9, 27]:
                        if self.p2.position == self.p1.position and not self.p2.has_traded_this_turn:
                            self.add_to_log("P2, press space to roll dice, S to Shop, T to Trade", self.p2_color)
                        else:
                            self.add_to_log("P2, press space to roll dice, S to Shop", self.p2_color)
                    elif self.p2.position in [5, 14, 23, 32]:
                        if self.p2.position == self.p1.position and not self.p2.has_traded_this_turn:
                            self.add_to_log("P2, press space to roll dice, Q for Query, T to Trade", self.p2_color)
                        else:
                            self.add_to_log("P2, press space to roll dice, Q for Query", self.p2_color)
                    elif self.p2.position in [2, 20]:
                        if self.p2.position == self.p1.position and not self.p2.has_traded_this_turn:
                            self.add_to_log("P2, press space to roll dice, E for Event, T to Trade", self.p2_color)
                        else:
                            self.add_to_log("P2, press space to roll dice, E for Event", self.p2_color)
                    elif self.p2.position in [7, 25]:
                        if self.p2.position == self.p1.position and not self.p2.has_traded_this_turn:
                            self.add_to_log("P2, press space to roll dice, F for Famous, T to Trade", self.p2_color)
                        else:
                            self.add_to_log("P2, press space to roll dice, F for Famous", self.p2_color)
                    elif self.p2.position == self.p1.position and not self.p2.has_traded_this_turn:
                        self.add_to_log("P2, press space to roll dice, T to Trade", self.p2_color)
                    else:
                        self.add_to_log("P2, press space to roll dice", self.p2_color)
                self.next_round_stage()
            elif self.round_stages[self.current_round_stage] == "P2_MOVE" and not self.winner:
                if not self.p2.jailed:
                    # Move the player
                    self.p2.position = (self.p2.position + (self.dice_rolls[0] + self.dice_rolls[1])) % 36
                    # Increase player money by product of rolls
                    self.p2.money += (self.dice_rolls[0] * self.dice_rolls[1])
                    self.p2_money_text = self.font_40.render(f"${self.p2.money}", False, self.p2_color).convert()
                elif self.p2.position == 19:
                    self.p2.jailed = False
                self.next_round_stage()
            elif self.round_stages[self.current_round_stage] == "P2_ACTION" and not self.winner:
                # self.add_to_log(f"P2 is on tile: {self.p2.position}", self.p2_color)
                if self.p2.position == 18:  # if p2 landed on jail tile
                    self.p2.jailed = True
                    self.add_to_log("P2 is in jail", (0, 0, 0))
                elif self.p2.position == 16 or self.p2.position == 34:  # random item tile
                    item = random.choice(list(self.p2.components.keys()))
                    self.add_to_log(f"P2 got: {item}", self.color_brown)
                    self.p2.components[item] += 1
                    # prints out component list, maybe needed for debugging
                    # print(f"P2: {self.p2.components}")
                elif self.p2.position in [11, 29]:  # chance tile
                    self.chance(2)
                elif self.p2.position in [2, 20]:  # Event tile
                    self.add_to_log(f"P2 landed on an Event tile", self.color_green)
                elif self.p2.position in [7, 25]:  # Famous person tile
                    self.add_to_log(f"P2 landed on a Famous Person tile", self.color_gray)
                elif self.p2.position in [5, 14, 23, 32]:  # Query tile
                    self.add_to_log(f"P2 landed on a Query tile", self.color_blue)
                elif self.p2.position in [9, 27]:  # Shop tile
                    self.add_to_log(f"P2 landed on a Shop tile", self.color_red)
                elif self.p2.position == 0:  # Start tile
                    reward = random.randint(self.back_at_start_reward[0], self.back_at_start_reward[1])
                    self.add_to_log(f"P2 is back at Start, +${reward}", self.color_yellow)
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
                if self.p1.money == 0:
                    self.add_to_log(f"P1 is starving, but has no money", self.color_purple)
                else:
                    if abs(gain) > self.p1.money:
                        gain = -1 * self.p1.money
                    self.add_to_log(f"P1 is hungry, {random.choice(food)} costs {abs(gain)}", self.color_purple)
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
                    if abs(gain) > self.p1.money:
                        gain = -1 * self.p1.money
                    self.add_to_log(f"P1 went all in, -{abs(gain)}", self.color_purple)
            elif item == 9:
                if self.p1.money == 0:
                    self.add_to_log(f"P1 has no money for {random.choice(relatives)}'s hospital bill", self.color_purple)
                else:
                    if abs(gain) > self.p1.money:
                        gain = -1 * self.p1.money
                    self.add_to_log(f"P1's {random.choice(relatives)} is in the hospital, -{abs(gain)}", self.color_purple)
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
                    if abs(gain) > self.p2.money:
                        gain = -1 * self.p2.money
                    self.add_to_log(f"P2 is hungry, {random.choice(food)} costs {abs(gain)}", self.color_purple)
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
                    if abs(gain) > self.p2.money:
                        gain = -1 * self.p2.money
                    self.add_to_log(f"P2 went all in, -{abs(gain)}", self.color_purple)
            elif item == 9:
                if self.p2.money == 0:
                    self.add_to_log(f"P2 has no money for {random.choice(relatives)}'s hospital bill", self.color_purple)
                else:
                    if abs(gain) > self.p2.money:
                        gain = -1 * self.p2.money
                    self.add_to_log(f"P2's {random.choice(relatives)} is in the hospital, -{abs(gain)}", self.color_purple)
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

        buy_buttons = [pg.Rect((420, 90), (100, 50)), pg.Rect((420, 160), (100, 50)), pg.Rect((420, 230), (100, 50)), pg.Rect((420, 300), (100, 50)), pg.Rect((420, 370), (100, 50)), pg.Rect((420, 440), (100, 50)),
                       pg.Rect((420, 510), (100, 50)), pg.Rect((420, 580), (100, 50)), pg.Rect((420, 650), (100, 50))]
        sell_buttons = [pg.Rect((550, 90), (100, 50)), pg.Rect((550, 160), (100, 50)), pg.Rect((550, 230), (100, 50)), pg.Rect((550, 300), (100, 50)), pg.Rect((550, 370), (100, 50)), pg.Rect((550, 440), (100, 50)),
                        pg.Rect((550, 510), (100, 50)), pg.Rect((550, 580), (100, 50)), pg.Rect((550, 650), (100, 50))]
        items = {"Keyboard": 100, "Mouse": 100, "Monitor": 100, "Printer": 100, "CPU": 100, "GPU": 100, "Motherboard": 100, "Mini Tower": 100, "Harddrive": 100}
        keys = list(items.keys())
        values = list(items.values())

        sell_computer_button = pg.Rect((1000, 450), (250, 100))
        # sell_computer_text = self.font_50.render(f"Sell PC: ${self.computer_price}", False, self.color_purple).convert()

        if player == 1:
            self.left_to_buy_text = self.font_50.render(f"Left to buy this turn: {int((len(self.p1.components) / 2) - self.p1.items_bought_this_turn)}", False, "White").convert()
        else:
            self.left_to_buy_text = self.font_50.render(f"Left to buy this turn: {int((len(self.p2.components) / 2) - self.p2.items_bought_this_turn)}", False, "White").convert()

        def buy_item(index):
            if (player == 1 and self.p1.items_bought_this_turn < self.max_buy_per_round) or (player == 2 and self.p2.items_bought_this_turn < self.max_buy_per_round):
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
                    elif buy_buttons[8].collidepoint(pg.mouse.get_pos()):  # player wants to buy item 9
                        buy_item(8)
                    elif sell_buttons[8].collidepoint(pg.mouse.get_pos()):  # player wants to sell item 9
                        sell_item(8)

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
                # Item icon
                self.screen.blit(self.component_icons[i], self.component_icons[i].get_rect(midleft=(50, 115 + (i * 70))))
                # Price text
                text = self.font_50.render(f"(${items[item]}/{int(items[item] * self.resell_percentage)})", False, (0, 0, 0))
                self.screen.blit(text, (150, 105 + (i * 70)))
                # Player has
                if player == 1:
                    text = self.font_50.render(f"(You have: {self.p1.components[item]})", False, (0, 0, 0))
                else:
                    text = self.font_50.render(f"(You have: {self.p2.components[item]})", False, (0, 0, 0))
                self.screen.blit(text, (700, 105 + (i * 70)))

            # Buy buttons
            if (player == 1 and self.p1.items_bought_this_turn < self.max_buy_per_round) or (player == 2 and self.p2.items_bought_this_turn < self.max_buy_per_round):
                pg.draw.rect(self.screen, self.color_green, buy_buttons[0])
                if buy_buttons[0].collidepoint(pg.mouse.get_pos()):
                    buy_text = self.font_50.render("Buy", False, self.color_yellow).convert()
                else:
                    buy_text = self.font_50.render("Buy", False, self.color_purple).convert()
                self.screen.blit(buy_text, buy_text.get_rect(center=(buy_buttons[0].centerx, buy_buttons[0].centery + 5)))

            if (player == 1 and self.p1.items_bought_this_turn < self.max_buy_per_round) or (player == 2 and self.p2.items_bought_this_turn < self.max_buy_per_round):
                pg.draw.rect(self.screen, self.color_green, buy_buttons[1])
                if buy_buttons[1].collidepoint(pg.mouse.get_pos()):
                    buy_text = self.font_50.render("Buy", False, self.color_yellow).convert()
                else:
                    buy_text = self.font_50.render("Buy", False, self.color_purple).convert()
                self.screen.blit(buy_text, buy_text.get_rect(center=(buy_buttons[1].centerx, buy_buttons[1].centery + 5)))

            if (player == 1 and self.p1.items_bought_this_turn < self.max_buy_per_round) or (player == 2 and self.p2.items_bought_this_turn < self.max_buy_per_round):
                pg.draw.rect(self.screen, self.color_green, buy_buttons[2])
                if buy_buttons[2].collidepoint(pg.mouse.get_pos()):
                    buy_text = self.font_50.render("Buy", False, self.color_yellow).convert()
                else:
                    buy_text = self.font_50.render("Buy", False, self.color_purple).convert()
                self.screen.blit(buy_text, buy_text.get_rect(center=(buy_buttons[2].centerx, buy_buttons[2].centery + 5)))

            if (player == 1 and self.p1.items_bought_this_turn < self.max_buy_per_round) or (player == 2 and self.p2.items_bought_this_turn < self.max_buy_per_round):
                pg.draw.rect(self.screen, self.color_green, buy_buttons[3])
                if buy_buttons[3].collidepoint(pg.mouse.get_pos()):
                    buy_text = self.font_50.render("Buy", False, self.color_yellow).convert()
                else:
                    buy_text = self.font_50.render("Buy", False, self.color_purple).convert()
                self.screen.blit(buy_text, buy_text.get_rect(center=(buy_buttons[3].centerx, buy_buttons[3].centery + 5)))

            if (player == 1 and self.p1.items_bought_this_turn < self.max_buy_per_round) or (player == 2 and self.p2.items_bought_this_turn < self.max_buy_per_round):
                pg.draw.rect(self.screen, self.color_green, buy_buttons[4])
                if buy_buttons[4].collidepoint(pg.mouse.get_pos()):
                    buy_text = self.font_50.render("Buy", False, self.color_yellow).convert()
                else:
                    buy_text = self.font_50.render("Buy", False, self.color_purple).convert()
                self.screen.blit(buy_text, buy_text.get_rect(center=(buy_buttons[4].centerx, buy_buttons[4].centery + 5)))

            if (player == 1 and self.p1.items_bought_this_turn < self.max_buy_per_round) or (player == 2 and self.p2.items_bought_this_turn < self.max_buy_per_round):
                pg.draw.rect(self.screen, self.color_green, buy_buttons[5])
                if buy_buttons[5].collidepoint(pg.mouse.get_pos()):
                    buy_text = self.font_50.render("Buy", False, self.color_yellow).convert()
                else:
                    buy_text = self.font_50.render("Buy", False, self.color_purple).convert()
                self.screen.blit(buy_text, buy_text.get_rect(center=(buy_buttons[5].centerx, buy_buttons[5].centery + 5)))

            if (player == 1 and self.p1.items_bought_this_turn < self.max_buy_per_round) or (player == 2 and self.p2.items_bought_this_turn < self.max_buy_per_round):
                pg.draw.rect(self.screen, self.color_green, buy_buttons[6])
                if buy_buttons[6].collidepoint(pg.mouse.get_pos()):
                    buy_text = self.font_50.render("Buy", False, self.color_yellow).convert()
                else:
                    buy_text = self.font_50.render("Buy", False, self.color_purple).convert()
                self.screen.blit(buy_text, buy_text.get_rect(center=(buy_buttons[6].centerx, buy_buttons[6].centery + 5)))

            if (player == 1 and self.p1.items_bought_this_turn < self.max_buy_per_round) or (player == 2 and self.p2.items_bought_this_turn < self.max_buy_per_round):
                pg.draw.rect(self.screen, self.color_green, buy_buttons[7])
                if buy_buttons[7].collidepoint(pg.mouse.get_pos()):
                    buy_text = self.font_50.render("Buy", False, self.color_yellow).convert()
                else:
                    buy_text = self.font_50.render("Buy", False, self.color_purple).convert()
                self.screen.blit(buy_text, buy_text.get_rect(center=(buy_buttons[7].centerx, buy_buttons[7].centery + 5)))

            if (player == 1 and self.p1.items_bought_this_turn < self.max_buy_per_round) or (player == 2 and self.p2.items_bought_this_turn < self.max_buy_per_round):
                pg.draw.rect(self.screen, self.color_green, buy_buttons[8])
                if buy_buttons[8].collidepoint(pg.mouse.get_pos()):
                    buy_text = self.font_50.render("Buy", False, self.color_yellow).convert()
                else:
                    buy_text = self.font_50.render("Buy", False, self.color_purple).convert()
                self.screen.blit(buy_text, buy_text.get_rect(center=(buy_buttons[8].centerx, buy_buttons[8].centery + 5)))

            # Sell buttons
            pg.draw.rect(self.screen, self.color_red, sell_buttons[0])
            if sell_buttons[0].collidepoint(pg.mouse.get_pos()):
                sell_text = self.font_50.render("Sell", False, self.color_yellow).convert()
            else:
                sell_text = self.font_50.render("Sell", False, self.color_purple).convert()
            self.screen.blit(sell_text, sell_text.get_rect(center=(sell_buttons[0].centerx, sell_buttons[0].centery + 5)))

            pg.draw.rect(self.screen, self.color_red, sell_buttons[1])
            if sell_buttons[1].collidepoint(pg.mouse.get_pos()):
                sell_text = self.font_50.render("Sell", False, self.color_yellow).convert()
            else:
                sell_text = self.font_50.render("Sell", False, self.color_purple).convert()
            self.screen.blit(sell_text, sell_text.get_rect(center=(sell_buttons[1].centerx, sell_buttons[1].centery + 5)))

            pg.draw.rect(self.screen, self.color_red, sell_buttons[2])
            if sell_buttons[2].collidepoint(pg.mouse.get_pos()):
                sell_text = self.font_50.render("Sell", False, self.color_yellow).convert()
            else:
                sell_text = self.font_50.render("Sell", False, self.color_purple).convert()
            self.screen.blit(sell_text, sell_text.get_rect(center=(sell_buttons[2].centerx, sell_buttons[2].centery + 5)))

            pg.draw.rect(self.screen, self.color_red, sell_buttons[3])
            if sell_buttons[3].collidepoint(pg.mouse.get_pos()):
                sell_text = self.font_50.render("Sell", False, self.color_yellow).convert()
            else:
                sell_text = self.font_50.render("Sell", False, self.color_purple).convert()
            self.screen.blit(sell_text, sell_text.get_rect(center=(sell_buttons[3].centerx, sell_buttons[3].centery + 5)))

            pg.draw.rect(self.screen, self.color_red, sell_buttons[4])
            if sell_buttons[4].collidepoint(pg.mouse.get_pos()):
                sell_text = self.font_50.render("Sell", False, self.color_yellow).convert()
            else:
                sell_text = self.font_50.render("Sell", False, self.color_purple).convert()
            self.screen.blit(sell_text, sell_text.get_rect(center=(sell_buttons[4].centerx, sell_buttons[4].centery + 5)))

            pg.draw.rect(self.screen, self.color_red, sell_buttons[5])
            if sell_buttons[5].collidepoint(pg.mouse.get_pos()):
                sell_text = self.font_50.render("Sell", False, self.color_yellow).convert()
            else:
                sell_text = self.font_50.render("Sell", False, self.color_purple).convert()
            self.screen.blit(sell_text, sell_text.get_rect(center=(sell_buttons[5].centerx, sell_buttons[5].centery + 5)))

            pg.draw.rect(self.screen, self.color_red, sell_buttons[6])
            if sell_buttons[6].collidepoint(pg.mouse.get_pos()):
                sell_text = self.font_50.render("Sell", False, self.color_yellow).convert()
            else:
                sell_text = self.font_50.render("Sell", False, self.color_purple).convert()
            self.screen.blit(sell_text, sell_text.get_rect(center=(sell_buttons[6].centerx, sell_buttons[6].centery + 5)))

            pg.draw.rect(self.screen, self.color_red, sell_buttons[7])
            if sell_buttons[7].collidepoint(pg.mouse.get_pos()):
                sell_text = self.font_50.render("Sell", False, self.color_yellow).convert()
            else:
                sell_text = self.font_50.render("Sell", False, self.color_purple).convert()
            self.screen.blit(sell_text, sell_text.get_rect(center=(sell_buttons[7].centerx, sell_buttons[7].centery + 5)))

            pg.draw.rect(self.screen, self.color_red, sell_buttons[8])
            if sell_buttons[8].collidepoint(pg.mouse.get_pos()):
                sell_text = self.font_50.render("Sell", False, self.color_yellow).convert()
            else:
                sell_text = self.font_50.render("Sell", False, self.color_purple).convert()
            self.screen.blit(sell_text, sell_text.get_rect(center=(sell_buttons[8].centerx, sell_buttons[8].centery + 5)))

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
        # for debugging, if the answers don't match up
        # print(correct_answer)

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
        # for debuggen if something goes wrong with the answers, this gives the answer
        # print(f"Answer: {self.event_answer}")
        user_text = ""
        user_text_display = self.font_50.render(user_text, False, (50, 255, 0))

        user_text_container = pg.Rect(((self.window_width / 2) - 40, 100), (80, 30))

        return_button = pg.Rect((1000, 590), (250, 100))

        instruction_text = [self.font_40.render("Input 4 numbers between 1 and 6 and hit enter, the numbers that are in the correct spot and numbers", False, "Black").convert(),
                            self.font_40.render("that are in the answer are shown.", False, "Black").convert()]
        note_text = self.font_24.render("Note: the answer contains no duplicate numbers. (eg. 2112 does not occur)", False, self.color_red).convert()

        while self.state_stack[-1] == "EVENT":
            if player == 1 and self.p1.guesses_done_this_turn == self.max_event_guesses:
                self.add_to_log(f"P1 did not guess the number, the number was: {self.event_answer}", self.color_green)
                self.p1.has_done_event_this_turn = True
                self.state_stack.pop()
                break
            elif player == 2 and self.p2.guesses_done_this_turn == self.max_event_guesses:
                self.add_to_log(f"P2 did not guess the number, the number was: {self.event_answer}", self.color_green)
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
                                self.add_to_log(f"P1 guessed the number, it was: {self.event_answer} +${reward}", self.color_green)
                                self.p1.money += reward
                                self.p1_money_text = self.font_40.render(f"${self.p1.money}", False, self.p1_color).convert()
                                self.p1.has_done_event_this_turn = True
                            else:
                                self.add_to_log(f"P2 guessed the number, it was: {self.event_answer} +${reward}", self.color_green)
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
                            # prints out the user input
                            # print(user_text)
                            for i in range(4):
                                if user_text[i] == self.event_answer[i]:
                                    correct += 1
                                if user_text[i] in self.event_answer:
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
        # prints out the correct answer, if needed for debugging
        # print(correct_answer)

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

                        if answer_buttons[3].collidepoint(pg.mouse.get_pos()):  # Player chose D
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

    def trade(self, player):
        return_button = pg.Rect((1000, 590), (250, 100))
        trade_button = pg.Rect((515, 590), (250, 100))

        add_buttons = [pg.Rect((70, 35), (70, 35)), pg.Rect((70, 95), (70, 35)), pg.Rect((70, 155), (70, 35)), pg.Rect((70, 215), (70, 35)), pg.Rect((70, 275), (70, 35)), pg.Rect((70, 335), (70, 35)), pg.Rect((70, 395), (70, 35)), pg.Rect((70, 455), (70, 35)), pg.Rect((70, 515), (70, 35)), pg.Rect((710, 35), (70, 35)), pg.Rect((710, 95), (70, 35)), pg.Rect((710, 155), (70, 35)), pg.Rect((710, 215), (70, 35)), pg.Rect((710, 275), (70, 35)), pg.Rect((710, 335), (70, 35)), pg.Rect((710, 395), (70, 35)), pg.Rect((710, 455), (70, 35)), pg.Rect((710, 515), (70, 35))]
        remove_buttons = [pg.Rect((150, 35), (120, 35)), pg.Rect((150, 95), (120, 35)), pg.Rect((150, 155), (120, 35)), pg.Rect((150, 215), (120, 35)), pg.Rect((150, 275), (120, 35)), pg.Rect((150, 335), (120, 35)), pg.Rect((150, 395), (120, 35)), pg.Rect((150, 455), (120, 35)), pg.Rect((150, 515), (120, 35)), pg.Rect((790, 35), (120, 35)), pg.Rect((790, 95), (120, 35)), pg.Rect((790, 155), (120, 35)), pg.Rect((790, 215), (120, 35)), pg.Rect((790, 275), (120, 35)), pg.Rect((790, 335), (120, 35)), pg.Rect((790, 395), (120, 35)), pg.Rect((790, 455), (120, 35)), pg.Rect((790, 515), (120, 35))]
        items = ["Keyboard", "Mouse", "Monitor", "Printer", "CPU", "GPU", "Motherboard", "Mini Tower", "Harddrive"]

        def add_item(index):
            if self.p1.components[items[index]] > 0 and (add_buttons[0].collidepoint(pg.mouse.get_pos()) or add_buttons[1].collidepoint(pg.mouse.get_pos()) or add_buttons[2].collidepoint(pg.mouse.get_pos()) or add_buttons[3].collidepoint(pg.mouse.get_pos()) or add_buttons[4].collidepoint(pg.mouse.get_pos()) or add_buttons[5].collidepoint(pg.mouse.get_pos()) or add_buttons[6].collidepoint(pg.mouse.get_pos()) or add_buttons[7].collidepoint(pg.mouse.get_pos()) or add_buttons[8].collidepoint(pg.mouse.get_pos())):
                self.p1.components_trade[items[index]] += 1
                self.p1.components[items[index]] -= 1
            elif self.p2.components[items[index]] > 0 and (add_buttons[9].collidepoint(pg.mouse.get_pos()) or add_buttons[10].collidepoint(pg.mouse.get_pos()) or add_buttons[11].collidepoint(pg.mouse.get_pos()) or add_buttons[12].collidepoint(pg.mouse.get_pos()) or add_buttons[13].collidepoint(pg.mouse.get_pos()) or add_buttons[14].collidepoint(pg.mouse.get_pos()) or add_buttons[15].collidepoint(pg.mouse.get_pos()) or add_buttons[16].collidepoint(pg.mouse.get_pos()) or add_buttons[17].collidepoint(pg.mouse.get_pos())):
                self.p2.components_trade[items[index]] += 1
                self.p2.components[items[index]] -= 1

        def remove_item(index):
            if self.p1.components_trade[items[index]] > 0 and (remove_buttons[0].collidepoint(pg.mouse.get_pos()) or remove_buttons[1].collidepoint(pg.mouse.get_pos()) or remove_buttons[2].collidepoint(pg.mouse.get_pos()) or remove_buttons[3].collidepoint(pg.mouse.get_pos()) or remove_buttons[4].collidepoint(pg.mouse.get_pos()) or remove_buttons[5].collidepoint(pg.mouse.get_pos()) or remove_buttons[6].collidepoint(pg.mouse.get_pos()) or remove_buttons[7].collidepoint(pg.mouse.get_pos()) or remove_buttons[8].collidepoint(pg.mouse.get_pos())):
                self.p1.components_trade[items[index]] -= 1
                self.p1.components[items[index]] += 1
            elif self.p2.components_trade[items[index]] > 0 and (remove_buttons[9].collidepoint(pg.mouse.get_pos()) or remove_buttons[10].collidepoint(pg.mouse.get_pos()) or remove_buttons[11].collidepoint(pg.mouse.get_pos()) or remove_buttons[12].collidepoint(pg.mouse.get_pos()) or remove_buttons[13].collidepoint(pg.mouse.get_pos()) or remove_buttons[14].collidepoint(pg.mouse.get_pos()) or remove_buttons[15].collidepoint(pg.mouse.get_pos()) or remove_buttons[16].collidepoint(pg.mouse.get_pos()) or remove_buttons[17].collidepoint(pg.mouse.get_pos())):
                self.p2.components_trade[items[index]] -= 1
                self.p2.components[items[index]] += 1

        while self.state_stack[-1] == "TRADE":
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit(0)
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if return_button.collidepoint(pg.mouse.get_pos()):
                        self.state_stack.pop()
                        break
                    elif add_buttons[0].collidepoint(pg.mouse.get_pos()):  # player wants to buy item 1
                        add_item(0)
                    elif remove_buttons[0].collidepoint(pg.mouse.get_pos()):  # player wants to sell item 1
                        remove_item(0)
                    elif add_buttons[1].collidepoint(pg.mouse.get_pos()):  # player wants to buy item 2
                        add_item(1)
                    elif remove_buttons[1].collidepoint(pg.mouse.get_pos()):  # player wants to sell item 2
                        remove_item(1)
                    elif add_buttons[2].collidepoint(pg.mouse.get_pos()):  # player wants to buy item 3
                        add_item(2)
                    elif remove_buttons[2].collidepoint(pg.mouse.get_pos()):  # player wants to sell item 3
                        remove_item(2)
                    elif add_buttons[3].collidepoint(pg.mouse.get_pos()):  # player wants to buy item 4
                        add_item(3)
                    elif remove_buttons[3].collidepoint(pg.mouse.get_pos()):  # player wants to sell item 4
                        remove_item(3)
                    elif add_buttons[4].collidepoint(pg.mouse.get_pos()):  # player wants to buy item 5
                        add_item(4)
                    elif remove_buttons[4].collidepoint(pg.mouse.get_pos()):  # player wants to sell item 5
                        remove_item(4)
                    elif add_buttons[5].collidepoint(pg.mouse.get_pos()):  # player wants to buy item 6
                        add_item(5)
                    elif remove_buttons[5].collidepoint(pg.mouse.get_pos()):  # player wants to sell item 6
                        remove_item(5)
                    elif add_buttons[6].collidepoint(pg.mouse.get_pos()):  # player wants to buy item 7
                        add_item(6)
                    elif remove_buttons[6].collidepoint(pg.mouse.get_pos()):  # player wants to sell item 7
                        remove_item(6)
                    elif add_buttons[7].collidepoint(pg.mouse.get_pos()):  # player wants to buy item 8
                        add_item(7)
                    elif remove_buttons[7].collidepoint(pg.mouse.get_pos()):  # player wants to sell item 8
                        remove_item(7)
                    elif add_buttons[8].collidepoint(pg.mouse.get_pos()):  # player wants to buy item 9
                        add_item(8)
                    elif remove_buttons[8].collidepoint(pg.mouse.get_pos()):  # player wants to sell item 9
                        remove_item(8)

                    # P2 buttons
                    elif add_buttons[9].collidepoint(pg.mouse.get_pos()):  # player wants to buy item 1
                        add_item(0)
                    elif remove_buttons[9].collidepoint(pg.mouse.get_pos()):  # player wants to sell item 1
                        remove_item(0)
                    elif add_buttons[10].collidepoint(pg.mouse.get_pos()):  # player wants to buy item 2
                        add_item(1)
                    elif remove_buttons[10].collidepoint(pg.mouse.get_pos()):  # player wants to sell item 2
                        remove_item(1)
                    elif add_buttons[11].collidepoint(pg.mouse.get_pos()):  # player wants to buy item 3
                        add_item(2)
                    elif remove_buttons[11].collidepoint(pg.mouse.get_pos()):  # player wants to sell item 3
                        remove_item(2)
                    elif add_buttons[12].collidepoint(pg.mouse.get_pos()):  # player wants to buy item 4
                        add_item(3)
                    elif remove_buttons[12].collidepoint(pg.mouse.get_pos()):  # player wants to sell item 4
                        remove_item(3)
                    elif add_buttons[13].collidepoint(pg.mouse.get_pos()):  # player wants to buy item 5
                        add_item(4)
                    elif remove_buttons[13].collidepoint(pg.mouse.get_pos()):  # player wants to sell item 5
                        remove_item(4)
                    elif add_buttons[14].collidepoint(pg.mouse.get_pos()):  # player wants to buy item 6
                        add_item(5)
                    elif remove_buttons[14].collidepoint(pg.mouse.get_pos()):  # player wants to sell item 6
                        remove_item(5)
                    elif add_buttons[15].collidepoint(pg.mouse.get_pos()):  # player wants to buy item 7
                        add_item(6)
                    elif remove_buttons[15].collidepoint(pg.mouse.get_pos()):  # player wants to sell item 7
                        remove_item(6)
                    elif add_buttons[16].collidepoint(pg.mouse.get_pos()):  # player wants to buy item 8
                        add_item(7)
                    elif remove_buttons[16].collidepoint(pg.mouse.get_pos()):  # player wants to sell item 8
                        remove_item(7)
                    elif add_buttons[17].collidepoint(pg.mouse.get_pos()):  # player wants to buy item 9
                        add_item(8)
                    elif remove_buttons[17].collidepoint(pg.mouse.get_pos()):  # player wants to sell item 9
                        remove_item(8)

                    elif trade_button.collidepoint(pg.mouse.get_pos()):
                        # Add traded items from P1 to items P2
                        for item in list(self.p1.components_trade.keys()):
                            self.p2.components[item] += self.p1.components_trade[item]
                        # Complete trade for P1 if at least 1 item was traded from any of the players
                        if player == 1:
                            if sum(self.p1.components_trade.values()) > 0 or sum(self.p2.components_trade.values()) > 0:
                                self.add_to_log("P1 has completed a trade.", self.p1_color)
                                self.reset_components_trade(1)
                                self.p1.has_traded_this_turn = True
                        # Add traded items from P2 to items P1
                        for item in list(self.p2.components_trade.keys()):
                            self.p1.components[item] += self.p2.components_trade[item]
                        # Complete trade for P2 if at least 1 item was traded from any of the players
                        if player == 2:
                            if sum(self.p2.components_trade.values()) > 0 or sum(self.p1.components_trade.values()) > 0:
                                self.add_to_log("P2 has completed a trade", self.p2_color)
                                self.reset_components_trade(2)
                                self.p2.has_traded_this_turn = True
                        self.state_stack.pop()
                        break

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.state_stack.pop()
                        break

            # Update

            # Render

            self.screen.fill(self.bg_color)
            # Player money
            self.screen.blit(self.p1_money_text, (10, 10))
            self.screen.blit(self.p2_money_text, (1180, 10))
            # Return button
            pg.draw.rect(self.screen, self.color_green, return_button)
            if return_button.collidepoint(pg.mouse.get_pos()):
                return_text = self.font_100.render("Return", False, self.color_blue).convert()
            else:
                return_text = self.font_100.render("Return", False, self.color_brown).convert()
            self.screen.blit(return_text, return_text.get_rect(center=(return_button.centerx + 5, return_button.centery + 5)))

            # Trade button
            pg.draw.rect(self.screen, self.color_green, trade_button)
            if trade_button.collidepoint(pg.mouse.get_pos()):
                trade_text = self.font_100.render("Trade", False, self.color_blue).convert()
            else:
                trade_text = self.font_100.render("Trade", False, self.color_brown).convert()
            self.screen.blit(trade_text, trade_text.get_rect(center=(trade_button.centerx + 5, trade_button.centery + 5)))

            # Item placing 
            for i in range(len(items)):
                item = items[i]
                # Item icon
                self.screen.blit(self.component_icons_small[i], self.component_icons_small[i].get_rect(midleft=(20, 50 + (i * 60))))
                self.screen.blit(self.component_icons_small[i], self.component_icons_small[i].get_rect(midleft=(660, 50 + (i * 60))))
                # Player has
                text_componentp1 = self.font_40.render(f"(P1 has: {self.p1.components[item]})", False, (0, 0, 0))
                text_componentp2 = self.font_40.render(f"(P2 has: {self.p2.components[item]})", False, (0, 0, 0))
                self.screen.blit(text_componentp1, (280, 45 + (i * 60)))
                self.screen.blit(text_componentp2, (920, 45 + (i * 60)))
                # Player amount trade
                text_tradep1 = self.font_40.render(f"(P1 trade: {self.p1.components_trade[item]})", False, (0, 0, 0))
                text_tradep2 = self.font_40.render(f"(P2 trade: {self.p2.components_trade[item]})", False, (0, 0, 0))
                self.screen.blit(text_tradep1, (415, 45 + (i * 60)))
                self.screen.blit(text_tradep2, (1055, 45 + (i * 60)))

            # Buy buttons 
            pg.draw.rect(self.screen, self.color_green, add_buttons[0])
            if add_buttons[0].collidepoint(pg.mouse.get_pos()):
                buy_text = self.font_40.render("Add", False, self.color_yellow).convert()
            else:
                buy_text = self.font_40.render("Add", False, self.color_purple).convert()
            self.screen.blit(buy_text, buy_text.get_rect(center=(add_buttons[0].centerx, add_buttons[0].centery + 5)))

            pg.draw.rect(self.screen, self.color_green, add_buttons[1])
            if add_buttons[1].collidepoint(pg.mouse.get_pos()):
                buy_text = self.font_40.render("Add", False, self.color_yellow).convert()
            else:
                buy_text = self.font_40.render("Add", False, self.color_purple).convert()
            self.screen.blit(buy_text, buy_text.get_rect(center=(add_buttons[1].centerx, add_buttons[1].centery + 5)))

            pg.draw.rect(self.screen, self.color_green, add_buttons[2])
            if add_buttons[2].collidepoint(pg.mouse.get_pos()):
                buy_text = self.font_40.render("Add", False, self.color_yellow).convert()
            else:
                buy_text = self.font_40.render("Add", False, self.color_purple).convert()
            self.screen.blit(buy_text, buy_text.get_rect(center=(add_buttons[2].centerx, add_buttons[2].centery + 5)))

            pg.draw.rect(self.screen, self.color_green, add_buttons[3])
            if add_buttons[3].collidepoint(pg.mouse.get_pos()):
                buy_text = self.font_40.render("Add", False, self.color_yellow).convert()
            else:
                buy_text = self.font_40.render("Add", False, self.color_purple).convert()
            self.screen.blit(buy_text, buy_text.get_rect(center=(add_buttons[3].centerx, add_buttons[3].centery + 5)))

            pg.draw.rect(self.screen, self.color_green, add_buttons[4])
            if add_buttons[4].collidepoint(pg.mouse.get_pos()):
                buy_text = self.font_40.render("Add", False, self.color_yellow).convert()
            else:
                buy_text = self.font_40.render("Add", False, self.color_purple).convert()
            self.screen.blit(buy_text, buy_text.get_rect(center=(add_buttons[4].centerx, add_buttons[4].centery + 5)))

            pg.draw.rect(self.screen, self.color_green, add_buttons[5])
            if add_buttons[5].collidepoint(pg.mouse.get_pos()):
                buy_text = self.font_40.render("Add", False, self.color_yellow).convert()
            else:
                buy_text = self.font_40.render("Add", False, self.color_purple).convert()
            self.screen.blit(buy_text, buy_text.get_rect(center=(add_buttons[5].centerx, add_buttons[5].centery + 5)))

            pg.draw.rect(self.screen, self.color_green, add_buttons[6])
            if add_buttons[6].collidepoint(pg.mouse.get_pos()):
                buy_text = self.font_40.render("Add", False, self.color_yellow).convert()
            else:
                buy_text = self.font_40.render("Add", False, self.color_purple).convert()
            self.screen.blit(buy_text, buy_text.get_rect(center=(add_buttons[6].centerx, add_buttons[6].centery + 5)))

            pg.draw.rect(self.screen, self.color_green, add_buttons[7])
            if add_buttons[7].collidepoint(pg.mouse.get_pos()):
                buy_text = self.font_40.render("Add", False, self.color_yellow).convert()
            else:
                buy_text = self.font_40.render("Add", False, self.color_purple).convert()
            self.screen.blit(buy_text, buy_text.get_rect(center=(add_buttons[7].centerx, add_buttons[7].centery + 5)))

            pg.draw.rect(self.screen, self.color_green, add_buttons[8])
            if add_buttons[8].collidepoint(pg.mouse.get_pos()):
                buy_text = self.font_40.render("Add", False, self.color_yellow).convert()
            else:
                buy_text = self.font_40.render("Add", False, self.color_purple).convert()
            self.screen.blit(buy_text, buy_text.get_rect(center=(add_buttons[8].centerx, add_buttons[8].centery + 5)))

            # Sell buttons
            pg.draw.rect(self.screen, self.color_red, remove_buttons[0])
            if remove_buttons[0].collidepoint(pg.mouse.get_pos()):
                sell_text = self.font_40.render("Remove", False, self.color_yellow).convert()
            else:
                sell_text = self.font_40.render("Remove", False, self.color_purple).convert()
            self.screen.blit(sell_text, sell_text.get_rect(center=(remove_buttons[0].centerx, remove_buttons[0].centery + 5)))

            pg.draw.rect(self.screen, self.color_red, remove_buttons[1])
            if remove_buttons[1].collidepoint(pg.mouse.get_pos()):
                sell_text = self.font_40.render("Remove", False, self.color_yellow).convert()
            else:
                sell_text = self.font_40.render("Remove", False, self.color_purple).convert()
            self.screen.blit(sell_text, sell_text.get_rect(center=(remove_buttons[1].centerx, remove_buttons[1].centery + 5)))

            pg.draw.rect(self.screen, self.color_red, remove_buttons[2])
            if remove_buttons[2].collidepoint(pg.mouse.get_pos()):
                sell_text = self.font_40.render("Remove", False, self.color_yellow).convert()
            else:
                sell_text = self.font_40.render("Remove", False, self.color_purple).convert()
            self.screen.blit(sell_text, sell_text.get_rect(center=(remove_buttons[2].centerx, remove_buttons[2].centery + 5)))

            pg.draw.rect(self.screen, self.color_red, remove_buttons[3])
            if remove_buttons[3].collidepoint(pg.mouse.get_pos()):
                sell_text = self.font_40.render("Remove", False, self.color_yellow).convert()
            else:
                sell_text = self.font_40.render("Remove", False, self.color_purple).convert()
            self.screen.blit(sell_text, sell_text.get_rect(center=(remove_buttons[3].centerx, remove_buttons[3].centery + 5)))

            pg.draw.rect(self.screen, self.color_red, remove_buttons[4])
            if remove_buttons[4].collidepoint(pg.mouse.get_pos()):
                sell_text = self.font_40.render("Remove", False, self.color_yellow).convert()
            else:
                sell_text = self.font_40.render("Remove", False, self.color_purple).convert()
            self.screen.blit(sell_text, sell_text.get_rect(center=(remove_buttons[4].centerx, remove_buttons[4].centery + 5)))

            pg.draw.rect(self.screen, self.color_red, remove_buttons[5])
            if remove_buttons[5].collidepoint(pg.mouse.get_pos()):
                sell_text = self.font_40.render("Remove", False, self.color_yellow).convert()
            else:
                sell_text = self.font_40.render("Remove", False, self.color_purple).convert()
            self.screen.blit(sell_text, sell_text.get_rect(center=(remove_buttons[5].centerx, remove_buttons[5].centery + 5)))

            pg.draw.rect(self.screen, self.color_red, remove_buttons[6])
            if remove_buttons[6].collidepoint(pg.mouse.get_pos()):
                sell_text = self.font_40.render("Remove", False, self.color_yellow).convert()
            else:
                sell_text = self.font_40.render("Remove", False, self.color_purple).convert()
            self.screen.blit(sell_text, sell_text.get_rect(center=(remove_buttons[6].centerx, remove_buttons[6].centery + 5)))

            pg.draw.rect(self.screen, self.color_red, remove_buttons[7])
            if remove_buttons[7].collidepoint(pg.mouse.get_pos()):
                sell_text = self.font_40.render("Remove", False, self.color_yellow).convert()
            else:
                sell_text = self.font_40.render("Remove", False, self.color_purple).convert()
            self.screen.blit(sell_text, sell_text.get_rect(center=(remove_buttons[7].centerx, remove_buttons[7].centery + 5)))

            pg.draw.rect(self.screen, self.color_red, remove_buttons[8])
            if remove_buttons[8].collidepoint(pg.mouse.get_pos()):
                sell_text = self.font_40.render("Remove", False, self.color_yellow).convert()
            else:
                sell_text = self.font_40.render("Remove", False, self.color_purple).convert()
            self.screen.blit(sell_text, sell_text.get_rect(center=(remove_buttons[8].centerx, remove_buttons[8].centery + 5)))

            # Buy buttons voor p2
            pg.draw.rect(self.screen, self.color_green, add_buttons[9])
            if add_buttons[9].collidepoint(pg.mouse.get_pos()):
                buy_text = self.font_40.render("Add", False, self.color_yellow).convert()
            else:
                buy_text = self.font_40.render("Add", False, self.color_purple).convert()
            self.screen.blit(buy_text, buy_text.get_rect(center=(add_buttons[9].centerx, add_buttons[9].centery + 5)))

            pg.draw.rect(self.screen, self.color_green, add_buttons[10])
            if add_buttons[10].collidepoint(pg.mouse.get_pos()):
                buy_text = self.font_40.render("Add", False, self.color_yellow).convert()
            else:
                buy_text = self.font_40.render("Add", False, self.color_purple).convert()
            self.screen.blit(buy_text, buy_text.get_rect(center=(add_buttons[10].centerx, add_buttons[10].centery + 5)))

            pg.draw.rect(self.screen, self.color_green, add_buttons[11])
            if add_buttons[11].collidepoint(pg.mouse.get_pos()):
                buy_text = self.font_40.render("Add", False, self.color_yellow).convert()
            else:
                buy_text = self.font_40.render("Add", False, self.color_purple).convert()
            self.screen.blit(buy_text, buy_text.get_rect(center=(add_buttons[11].centerx, add_buttons[11].centery + 5)))

            pg.draw.rect(self.screen, self.color_green, add_buttons[12])
            if add_buttons[12].collidepoint(pg.mouse.get_pos()):
                buy_text = self.font_40.render("Add", False, self.color_yellow).convert()
            else:
                buy_text = self.font_40.render("Add", False, self.color_purple).convert()
            self.screen.blit(buy_text, buy_text.get_rect(center=(add_buttons[12].centerx, add_buttons[12].centery + 5)))

            pg.draw.rect(self.screen, self.color_green, add_buttons[13])
            if add_buttons[13].collidepoint(pg.mouse.get_pos()):
                buy_text = self.font_40.render("Add", False, self.color_yellow).convert()
            else:
                buy_text = self.font_40.render("Add", False, self.color_purple).convert()
            self.screen.blit(buy_text, buy_text.get_rect(center=(add_buttons[13].centerx, add_buttons[13].centery + 5)))

            pg.draw.rect(self.screen, self.color_green, add_buttons[14])
            if add_buttons[14].collidepoint(pg.mouse.get_pos()):
                buy_text = self.font_40.render("Add", False, self.color_yellow).convert()
            else:
                buy_text = self.font_40.render("Add", False, self.color_purple).convert()
            self.screen.blit(buy_text, buy_text.get_rect(center=(add_buttons[14].centerx, add_buttons[14].centery + 5)))

            pg.draw.rect(self.screen, self.color_green, add_buttons[15])
            if add_buttons[15].collidepoint(pg.mouse.get_pos()):
                buy_text = self.font_40.render("Add", False, self.color_yellow).convert()
            else:
                buy_text = self.font_40.render("Add", False, self.color_purple).convert()
            self.screen.blit(buy_text, buy_text.get_rect(center=(add_buttons[15].centerx, add_buttons[15].centery + 5)))

            pg.draw.rect(self.screen, self.color_green, add_buttons[16])
            if add_buttons[16].collidepoint(pg.mouse.get_pos()):
                buy_text = self.font_40.render("Add", False, self.color_yellow).convert()
            else:
                buy_text = self.font_40.render("Add", False, self.color_purple).convert()
            self.screen.blit(buy_text, buy_text.get_rect(center=(add_buttons[16].centerx, add_buttons[16].centery + 5)))

            pg.draw.rect(self.screen, self.color_green, add_buttons[17])
            if add_buttons[17].collidepoint(pg.mouse.get_pos()):
                buy_text = self.font_40.render("Add", False, self.color_yellow).convert()
            else:
                buy_text = self.font_40.render("Add", False, self.color_purple).convert()
            self.screen.blit(buy_text, buy_text.get_rect(center=(add_buttons[17].centerx, add_buttons[17].centery + 5)))

            # Sell buttons
            pg.draw.rect(self.screen, self.color_red, remove_buttons[9])
            if remove_buttons[9].collidepoint(pg.mouse.get_pos()):
                sell_text = self.font_40.render("Remove", False, self.color_yellow).convert()
            else:
                sell_text = self.font_40.render("Remove", False, self.color_purple).convert()
            self.screen.blit(sell_text, sell_text.get_rect(center=(remove_buttons[9].centerx, remove_buttons[9].centery + 5)))

            pg.draw.rect(self.screen, self.color_red, remove_buttons[10])
            if remove_buttons[10].collidepoint(pg.mouse.get_pos()):
                sell_text = self.font_40.render("Remove", False, self.color_yellow).convert()
            else:
                sell_text = self.font_40.render("Remove", False, self.color_purple).convert()
            self.screen.blit(sell_text, sell_text.get_rect(center=(remove_buttons[10].centerx, remove_buttons[10].centery + 5)))

            pg.draw.rect(self.screen, self.color_red, remove_buttons[11])
            if remove_buttons[11].collidepoint(pg.mouse.get_pos()):
                sell_text = self.font_40.render("Remove", False, self.color_yellow).convert()
            else:
                sell_text = self.font_40.render("Remove", False, self.color_purple).convert()
            self.screen.blit(sell_text, sell_text.get_rect(center=(remove_buttons[11].centerx, remove_buttons[11].centery + 5)))

            pg.draw.rect(self.screen, self.color_red, remove_buttons[12])
            if remove_buttons[12].collidepoint(pg.mouse.get_pos()):
                sell_text = self.font_40.render("Remove", False, self.color_yellow).convert()
            else:
                sell_text = self.font_40.render("Remove", False, self.color_purple).convert()
            self.screen.blit(sell_text, sell_text.get_rect(center=(remove_buttons[12].centerx, remove_buttons[12].centery + 5)))

            pg.draw.rect(self.screen, self.color_red, remove_buttons[13])
            if remove_buttons[13].collidepoint(pg.mouse.get_pos()):
                sell_text = self.font_40.render("Remove", False, self.color_yellow).convert()
            else:
                sell_text = self.font_40.render("Remove", False, self.color_purple).convert()
            self.screen.blit(sell_text, sell_text.get_rect(center=(remove_buttons[13].centerx, remove_buttons[13].centery + 5)))

            pg.draw.rect(self.screen, self.color_red, remove_buttons[14])
            if remove_buttons[14].collidepoint(pg.mouse.get_pos()):
                sell_text = self.font_40.render("Remove", False, self.color_yellow).convert()
            else:
                sell_text = self.font_40.render("Remove", False, self.color_purple).convert()
            self.screen.blit(sell_text, sell_text.get_rect(center=(remove_buttons[14].centerx, remove_buttons[14].centery + 5)))

            pg.draw.rect(self.screen, self.color_red, remove_buttons[15])
            if remove_buttons[15].collidepoint(pg.mouse.get_pos()):
                sell_text = self.font_40.render("Remove", False, self.color_yellow).convert()
            else:
                sell_text = self.font_40.render("Remove", False, self.color_purple).convert()
            self.screen.blit(sell_text, sell_text.get_rect(center=(remove_buttons[15].centerx, remove_buttons[15].centery + 5)))

            pg.draw.rect(self.screen, self.color_red, remove_buttons[16])
            if remove_buttons[16].collidepoint(pg.mouse.get_pos()):
                sell_text = self.font_40.render("Remove", False, self.color_yellow).convert()
            else:
                sell_text = self.font_40.render("Remove", False, self.color_purple).convert()
            self.screen.blit(sell_text, sell_text.get_rect(center=(remove_buttons[16].centerx, remove_buttons[16].centery + 5)))

            pg.draw.rect(self.screen, self.color_red, remove_buttons[17])
            if remove_buttons[17].collidepoint(pg.mouse.get_pos()):
                sell_text = self.font_40.render("Remove", False, self.color_yellow).convert()
            else:
                sell_text = self.font_40.render("Remove", False, self.color_purple).convert()
            self.screen.blit(sell_text, sell_text.get_rect(center=(remove_buttons[17].centerx, remove_buttons[17].centery + 5)))

            # PyGame Render
            pg.display.update()
            self.clock.tick(self.fps)

    def check_for_winner(self):
        if self.p1.money > self.win_condition:
            self.winner = 1
        elif self.p2.money > self.win_condition:
            self.winner = 2
        # else winner stays 0

    def reset_components_trade(self, player):
        if player == 1:
            for item in list(self.p1.components_trade.keys()):
                self.p1.components_trade[item] = 0
        else:
            for item in list(self.p2.components_trade.keys()):
                self.p2.components_trade[item] = 0

    def restart(self):
        self.winner = 0
        self.current_round_stage = 0
        self.log = []
        self.add_to_log(f"Welcome to TUBOGA. First player to ${self.win_condition} wins!", "White")
        self.add_to_log(f"This is the log, the most recent {self.max_log_size} events are shown here.", "White")
        self.p1.position = 0
        self.p2.position = 0
        self.dice_rolls[0] = 0
        self.dice_rolls[1] = 0
        self.d1_text = self.font_200.render(str(self.dice_rolls[0]), False, "Black").convert()
        self.d2_text = self.font_200.render(str(self.dice_rolls[1]), False, "Black").convert()
        self.p1.money = 500
        self.p2.money = 500
        self.p1_money_text = self.font_40.render(f"${self.p1.money}", False, self.p1_color).convert()
        self.p2_money_text = self.font_40.render(f"${self.p2.money}", False, self.p2_color).convert()
        self.p1.jailed = False
        self.p2.jailed = False
        components = list(self.p1.components.keys())
        for component in components:
            self.p1.components[component] = 0
            self.p2.components[component] = 0
            self.p1.components_trade[component] = 0
            self.p1.components_trade[component] = 0
        self.p1.has_done_query_this_turn = False
        self.p2.has_done_query_this_turn = False
        self.p1.has_done_event_this_turn = False
        self.p2.has_done_event_this_turn = False
        self.p1.has_done_famous_this_turn = False
        self.p2.has_done_famous_this_turn = False
        self.p1.has_sold_computer_this_turn = False
        self.p2.has_sold_computer_this_turn = False
        self.p1.has_traded_this_turn = False
        self.p2.has_traded_this_turn = False
        self.p1.items_bought_this_turn = 0
        self.p2.items_bought_this_turn = 0
        self.p1.guesses_done_this_turn = 0
        self.p2.guesses_done_this_turn = 0
        self.p1.can_sell_computer = False
        self.p2.can_sell_computer = False
