import pygame as pg
import random


class Game(object):
    def __init__(self, width, height, title):
        # PyGame initialization
        pg.init()
        self.screen = pg.display.set_mode((width, height))
        pg.display.set_caption(title)
        pg.display.set_icon(pg.image.load("res/icon.png"))

        # Game logic variables
        self.window_width = width
        self.window_height = height
        self.state_stack = []

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

        self.clock = pg.time.Clock()
        self.fps = 60

        self.font_100 = pg.font.Font("res/fonts/pixeltype.ttf", 100)
        self.font_50 = pg.font.Font("res/fonts/pixeltype.ttf", 50)
        self.font_24 = pg.font.Font("res/fonts/pixeltype.ttf", 25)

        self.pause_icon = pg.image.load("res/icon.png").convert_alpha()

        self.p1_pos = 0  # The tile the player is on, 0 is Start, 35 is max
        self.p2_pos = 0

        self.d1_roll = 0
        self.d2_roll = 0

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
                        self.dice_roll()
                        print(f"{self.d1_roll} {self.d2_roll}")
                        break
                    elif event.key == pg.K_1:
                        self.p1_pos = (self.p1_pos + 1) % 36
                        break
                    elif event.key == pg.K_2:
                        self.p2_pos = (self.p2_pos + 1) % 36
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
            if self.p1_pos == self.p2_pos:  # if both players are on the same tile
                pg.draw.circle(self.screen, self.p1_color, (self.coords[self.p1_pos][0] + 15, self.coords[self.p1_pos][1] + 15), 10)
                pg.draw.circle(self.screen, (70, 70, 70), (self.coords[self.p1_pos][0] + 15, self.coords[self.p1_pos][1] + 15), 10, 2)
                pg.draw.circle(self.screen, self.p2_color,(self.coords[self.p2_pos][0] + 35, self.coords[self.p2_pos][1] + 35), 10)
                pg.draw.circle(self.screen, (70, 70, 70), (self.coords[self.p2_pos][0] + 35, self.coords[self.p2_pos][1] + 35), 10, 2)
            else:
                pg.draw.circle(self.screen, self.p1_color, (self.coords[self.p1_pos][0] + 25, self.coords[self.p1_pos][1] + 25), 10)
                pg.draw.circle(self.screen, (70, 70, 70), (self.coords[self.p1_pos][0] + 25, self.coords[self.p1_pos][1] + 25), 10, 2)
                pg.draw.circle(self.screen, self.p2_color,(self.coords[self.p2_pos][0] + 25, self.coords[self.p2_pos][1] + 25), 10)
                pg.draw.circle(self.screen, (70, 70, 70), (self.coords[self.p2_pos][0] + 25, self.coords[self.p2_pos][1] + 25), 10, 2)

            pg.display.update()
            self.clock.tick(self.fps)

    def dice_roll(self):
        self.d1_roll = random.randint(1, 6)
        self.d2_roll = random.randint(1, 6)
